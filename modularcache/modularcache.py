#!/usr/bin/env python

import functools
from decorator import decorator

from cachedict import CacheDict

#@decorator
def cache(selector):
    """
    Decorator for cache.

    >>> from  modularcacheconfig import ModularCacheConfig
    

    >>> mc = ModularCacheConfig('test/ram.ini')
    >>> @cache('ram')
    ... def foo(a , b):
    ...     return a + b
    >>> foo(1,2)
    3
    >>> class A(object):
    ...     @cache('ram')
    ...     def b(self, c, d):
    ...         return c*d
    >>> a = A()
    >>> a.b(2,3)
    6
    >>> mc = ModularCacheConfig('test/fscache.ini')
    >>> @cache('fscache')
    ... def bar(a , b):
    ...     return a / b
    >>> bar(18,2)
    9
    >>> bar(18,2)
    9
    >>> class B(object):
    ...     @cache('fscache')
    ...     def b(self, c, d):
    ...         return c**d
    >>> b = B()
    >>> b.b(2,3)
    8
    >>> b.b(2,3)
    8
    >>> class D(object):
    ...     pass
    >>> import datetime
    >>> class C(object):
    ...     @cache('fscache')
    ...     def c(self, a):
    ...         return datetime.datetime.now()
    >>> c = C()
    >>> dt1 = c.c(1)
    >>> dt2 = c.c(1)
    >>> dt1 == dt2
    True
    >>>	dt1 is dt1
    True
    >>> #from cachedict import CacheDict
    >>> #cd = CacheDict.getInstance()
    >>> #cd['fscache'].stop()
    """
    
    def _cache(fctn):
        """
        Sub decorator.
        """
        @functools.wraps(fctn)
        def __cache(*args, **kwargs):
            """
            Sub sub decorator.
            """
            tmpArgs =[]

            cd = CacheDict.getInstance()

            if selector in cd:
                c = cd[selector]
                if c.isCached(fctn.__name__, *args, **kwargs):
                    return c.cached(fctn.__name__, *args, **kwargs)
                else:
                    return c.putInCache(fctn.__name__, fctn(*args, **kwargs), *args, **kwargs)
            else :
                return fctn(*args, **kwargs)
        return __cache

    return _cache

if __name__ == "__main__":
    import doctest
    doctest.testmod()
