#!/usr/bin/env path

from abstractcache import AbstractCache

from exceptionconfig import *

class RamCache(AbstractCache):
    """
    Ram Cache.
    """
    
    def __init__(self, config=None):
        """
        Ram Cache.

        >>> r = RamCache() 
        >>> r #doctest: +ELLIPSIS
        <__main__.RamCache object at 0x...>
        >>> r._cache
        {}
        """
        AbstractCache.__init__(self)

        self._cache = {}
        
    
    @staticmethod
    def checkConf(config):
        """
        Check configuration for fake Cache.

        >>> RamCache.checkConf({})
        Traceback (most recent call last):
        ...
        IncoherentSectionConfig: not module RamCache
        >>> RamCache.checkConf({'module' : 'false'})
        Traceback (most recent call last):
        ...
        IncoherentSectionConfig: not module RamCache
        >>> RamCache.checkConf({'module' : 'RamCache', 'param1' : 'value1'})
        """
        try:
            if config['module'] == 'RamCache':
                pass
            else:
                raise IncoherentSectionConfig('not module RamCache')
        except KeyError:
            raise IncoherentSectionConfig('not module RamCache')

    def __setitem__(self, key, value):
        """
        Set items.

        >>> r = RamCache()
        >>> r['a'] = 1
        >>> r._cache
        {'a': 1}
        """
        self._cache[key] = value

    def __getitem__(self, key):
        """
        Get Item.
        >>> r = RamCache()
        >>> r._cache['a'] = 1
        >>> r['a']
        1


        """

        return self._cache[key]

    def __delitem__(self, key):
        """
        del Item.
        
        >>> r = RamCache()
        >>> r._cache['a'] = 1
        >>> r._cache
        {'a': 1}
        >>> del(r['a'])
        >>> r._cache
        {}
        """
        
        del(self._cache[key])

    def has_key(self, key):
        """
        Has key in dict.
        >>> r = RamCache()
        >>> r._cache['a'] = 1
        >>> r.has_key('a')
        True
        """

        return self._cache.has_key(key)

    def __contains__(self, key):
        """
        Contains key.
        
        >>> r = RamCache()
        >>> r._cache['a'] = 1
        >>> r.__contains__('a')
        True
        >>> 'a' in r
        True
        >>> 'b' in r
        False
        """
        
        return key in self._cache


    def isCached(self, func, *args, **kwargs):
        """
        >>> r = RamCache()
        >>> r._cache
        {}
        >>> r.isCached('a',[1, 2], {})
        False
        >>> r._cache =  {'a': {'([1, 2], {})': {'{}': 3}}}
        >>> r.isCached('a',[1, 2], {})
        True
        """
        return func in self._cache and str(args) in self._cache[func] and str(kwargs) in self._cache[func][str(args)]

    def cached(self, func, *args, **kwargs):
        """
        >>> r = RamCache()
        >>> r._cache =  {'a': {'([1, 2], {})': {'{}': 3}}}
        >>> r.cached('a',[1, 2], {})
        3
        """
        return  self._cache[func][str(args)][str(kwargs)]

    def putInCache(self, func, result, *args, **kwargs):
        """
        >>> r = RamCache()
        >>> r.putInCache('a', 3, [1, 2], {})
        3
        >>> r._cache
        {'a': {'([1, 2], {})': {'{}': 3}}}
        """
        if func not in self._cache:
            self._cache[func] = {}

        if str(args) not in self._cache[func]:
            self._cache[func][str(args)] = {}


        self._cache[func][str(args)][str(kwargs)] = result
        return result
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()
