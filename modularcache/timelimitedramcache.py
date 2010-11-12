#!/usr/bin/env path

import datetime

from ramcache import RamCache


from exceptionconfig import *

class TimeLimitedRamCache(RamCache):
    """
    Ram Cache.
    """
    
    def __init__(self, config):
        """
        Ram Cache.

        >>> r = TimeLimitedRamCache({'duration' : 2}) 
        >>> r #doctest: +ELLIPSIS
        <__main__.TimeLimitedRamCache object at 0x...>
        >>> r._cache
        {}
        >>> r._dateHit
        {}
        >>> r._timedelta
        datetime.timedelta(0, 2)
        """
        RamCache.__init__(self)

        self._timedelta = datetime.timedelta(seconds=config['duration'])
        self._dateHit = {}
        
    
    @staticmethod
    def checkConf(config):
        """
        Check configuration for fake Cache.

        >>> TimeLimitedRamCache.checkConf({})
        Traceback (most recent call last):
        ...
        IncoherentSectionConfig: not module TimeLimitedRamCache
        >>> TimeLimitedRamCache.checkConf({'module' : 'false'})
        Traceback (most recent call last):
        ...
        IncoherentSectionConfig: not module TimeLimitedRamCache
        >>> TimeLimitedRamCache.checkConf({'module' : 'TimeLimitedRamCache'})
        Traceback (most recent call last):
        ...
        MissingConfigException: no duration in config
        >>> TimeLimitedRamCache.checkConf({'module': 'TimeLimitedRamCache', 'duration': '2'})
        
        """
        try:
            if config['module'] == 'TimeLimitedRamCache':
                if 'duration' in config:
                    pass
                else:
                    raise MissingConfigException('no duration in config')
            else:
                raise IncoherentSectionConfig('not module TimeLimitedRamCache')
        except KeyError:
            raise IncoherentSectionConfig('not module TimeLimitedRamCache')



    def isCached(self, func, *args, **kwargs):
        """
        >>> r = TimeLimitedRamCache({'duration' : 2})
        >>> r._cache
        {}
        >>> r.isCached('a',[1, 2], {})
        False
        >>> r._cache =  {'a': {'([1, 2], {})': {'{}': 3}}}
        >>> r.isCached('a',[1, 2], {})
        False
        >>> import datetime
        >>> now = datetime.datetime.now()
        >>> r._dateHit = {'a': {'([1, 2], {})': {'{}': now}}}
        >>> r.isCached('a',[1, 2], {})
        True
        """
        return func in self._cache and str(args) in self._cache[func] and str(kwargs) in self._cache[func][str(args)] and  \
               func in self._dateHit and str(args) in self._dateHit[func] and str(kwargs) in self._dateHit[func][str(args)] and \
                self._dateHit[func][str(args)][str(kwargs)] - datetime.datetime.now() < self._timedelta

    def cached(self, func, *args, **kwargs):
        """
        >>> r = TimeLimitedRamCache({'duration' : 2})
        >>> r._cache =  {'a': {'([1, 2], {})': {'{}': 3}}}
        >>> r.cached('a',[1, 2], {})
        3
        """
        return  self._cache[func][str(args)][str(kwargs)]

    def putInCache(self, func, result, *args, **kwargs):
        """
        >>> r = TimeLimitedRamCache({'duration' : 2})
        >>> r.putInCache('a', 3, [1, 2], {})
        3
        >>> r._cache
        {'a': {'([1, 2], {})': {'{}': 3}}}
        """
        if func not in self._cache:
            self._cache[func] = {}
            self._dateHit[func] = {}

        if str(args) not in self._cache[func]:
            self._cache[func][str(args)] = {}
            self._dateHit[func][str(args)] = {}
            

        self._cache[func][str(args)][str(kwargs)] = result
        self._dateHit[func][str(args)][str(kwargs)] = datetime.datetime.now()
        return result
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()
