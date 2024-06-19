import contextvars


class SingletonMeta(type):
    """
    元类实现单例模式, 解决模型文件一次加载多次调用的问题。
    """
    _instances = {}
    _lock = contextvars.ContextVar('lock')

    def __call__(cls, *args, **kwargs):
        if not hasattr(cls._lock, 'instance'):
            cls._lock.set(super().__call__(*args, **kwargs))
        return cls._lock.get()
