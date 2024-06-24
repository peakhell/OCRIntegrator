import time
from typing import Dict, List, Union
import tensorrt as trt
import pycuda.driver as cuda
import numpy as np
from collections import OrderedDict

TRT_LOGGER = trt.Logger(trt.Logger.WARNING)


def load_engine(path):
    print("Start loading engine")
    with open(path, "rb") as f, trt.Runtime(TRT_LOGGER) as runtime:
        engine = runtime.deserialize_cuda_engine(f.read())
    print('Completed loading engine')
    return engine


class OutputAllocator(trt.IOutputAllocator):
    def __init__(self):
        print("[MyOutputAllocator::__init__]")
        super().__init__()
        self.buffers = {}
        self.shapes = {}

    def reallocate_output(self, tensor_name: str, memory: int, size: int, alignment: int) -> int:
        print("[MyOutputAllocator::reallocate_output] TensorName=%s, Memory=%s, Size=%d, Alignment=%d" % (tensor_name, memory, size, alignment))
        if tensor_name in self.buffers:
            del self.buffers[tensor_name]

        address = cuda.mem_alloc(size)
        self.buffers[tensor_name] = address
        return int(address)

    def notify_shape(self, tensor_name: str, shape: trt.Dims):
        print("[MyOutputAllocator::notify_shape] TensorName=%s, Shape=%s" % (tensor_name, shape))
        self.shapes[tensor_name] = tuple(shape)


class TrtModelEngine:
    """
       trt模型管理，加载trt模型，分配内存，并提供推理接口
    """
    def __init__(self, engine: trt.ICudaEngine, cuda_ctx=None):
        # # 选择第一个可用的 GPU 设备
        # device = cuda.Device(0)
        # # 将所选设备设置为当前活动的上下文
        # self.cuda_context = device.make_context()
        # self.cuda_context.push()
        self.cuda_ctx = cuda_ctx
        if self.cuda_ctx:
            self.cuda_ctx.push()
        self.engine = engine
        self.output_allocator = OutputAllocator()
        # create execution context
        # get input and output tensor names
        self.input_tensor_names = self.get_input_tensor_names(engine)
        self.output_tensor_names = self.get_output_tensor_names(engine)

        # create stream
        self.stream = cuda.Stream()
        # Create a CUDA events
        self.start_event = cuda.Event()
        self.end_event = cuda.Event()
        try:
            self.context = self.engine.create_execution_context()
        except Exception as e:
            raise RuntimeError('fail to allocate CUDA resources') from e
        finally:
            if self.cuda_ctx:
                self.cuda_ctx.pop()
    # def __del__(self):
    #     self.cuda_context.pop()

    def __del__(self):
        """Free CUDA memories."""
        del self.stream
    def get_last_inference_time(self):
        return self.start_event.time_till(self.end_event)

    @staticmethod
    def get_input_tensor_names(engine: trt.ICudaEngine) -> list[str]:
        """
        :param engine: trt engine object
        :return: input tensor names
        """
        input_tensor_names = []
        for binding in engine:
            if engine.get_tensor_mode(binding) == trt.TensorIOMode.INPUT:
                input_tensor_names.append(binding)
        return input_tensor_names

    @staticmethod
    def get_output_tensor_names(engine: trt.ICudaEngine) -> list[str]:
        output_tensor_names = []
        for binding in engine:
            if engine.get_tensor_mode(binding) == trt.TensorIOMode.OUTPUT:
                output_tensor_names.append(binding)
        return output_tensor_names

    def infer(self, inputs: Union[Dict[str, np.ndarray], List[np.ndarray], np.ndarray]) -> OrderedDict[str, np.ndarray]:
        """
        inference process:
        1. create execution context
        2. set input shapes
        3. allocate memory
        4. copy input data to device
        5. run inference on device
        6. copy output data to host and reshape
        """
        # set input shapes, the output shapes are inferred automatically
        if isinstance(inputs, np.ndarray):
            inputs = [inputs]
        if isinstance(inputs, dict):
            inputs = [inp if name in self.input_tensor_names else None for (name, inp) in inputs.items()]
        if isinstance(inputs, list):
            for name, arr in zip(self.input_tensor_names, inputs):
                self.context.set_input_shape(name, arr.shape)
        buffers_host = []
        buffers_device = []
        # copy input data to device
        for name, arr in zip(self.input_tensor_names, inputs):
            host = cuda.pagelocked_empty(arr.shape, dtype=trt.nptype(self.engine.get_tensor_dtype(name)))
            device = cuda.mem_alloc(arr.nbytes)

            host[:] = arr
            cuda.memcpy_htod_async(device, host, self.stream)
            buffers_host.append(host)
            buffers_device.append(device)
        # set input tensor address
        for name, buffer in zip(self.input_tensor_names, buffers_device):
            self.context.set_tensor_address(name, int(buffer))
        # set output tensor allocator
        for name in self.output_tensor_names:
            self.context.set_tensor_address(name, 0)  # set nullptr
            self.context.set_output_allocator(name, self.output_allocator)
        # The do_inference function will return a list of outputs

        # Record the start event
        self.start_event.record(self.stream)
        # Run inference.
        self.context.execute_async_v3(stream_handle=self.stream.handle)
        # Record the end event
        self.end_event.record(self.stream)

        # self.memory.copy_to_host()

        output_buffers = []
        for name in self.output_tensor_names:
            arr = cuda.pagelocked_empty(self.output_allocator.shapes[name],
                                        dtype=trt.nptype(self.engine.get_tensor_dtype(name)))
            cuda.memcpy_dtoh_async(arr, self.output_allocator.buffers[name], stream=self.stream)
            output_buffers.append(arr)

        # Synchronize the stream
        self.stream.synchronize()

        return output_buffers

    def run(self, type, inputs):
        if self.cuda_ctx:
            self.cuda_ctx.push()
        trt_outputs = self.infer(inputs)
        if self.cuda_ctx:
            self.cuda_ctx.pop()
        return trt_outputs
