import hashlib
import functools
from threading import local

def class_method_cache(min_length=1024):
    def decorator(func):
        local_cache = local()
        local_cache.cached = {}
        @functools.wraps(func)
        def inner(self, *args, **kwargs):
            hash_content = unicode(func.__name__) + unicode(args) + unicode(kwargs)
            if len(hash_content) < min_length:
                return func(self, *args, **kwargs)
            
            hashed = hashlib.sha256(hash_content).hexdigest()
            
            if not local_cache.cached.has_key(hashed):
                local_cache.cached[hashed] = func(self, *args, **kwargs)
            
            return local_cache.cached[hashed]
            
        return inner
    return decorator
