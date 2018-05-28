"一些插件，方法"
from functools import wraps

def sington(cls):
    "单例模式"
    if "_instance" not in cls.__dict__:
        cls._instance = None
    @wraps(cls)
    def wrapper(*args, **kwargs):
        if cls._instance is None:
            cls._instance = cls(*args, **kwargs)       
        return cls._instance
    return wrapper

def main():
    @sington
    class Dog:
        pass
    a = Dog()
    b = Dog()
    print(a is b)

if __name__ == '__main__':
    main()
