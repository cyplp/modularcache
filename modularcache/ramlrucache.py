#!/usr/bin/env path

from ramcache import RamCache

from exceptionconfig import *

class RamLRUCache(RamCache):
    """
    Ram LRU Cache.
    """
    
    def __init__(self, config=None):
        """
        Ram Cache.

        >>> r = RamLRUCache({'size' : 5}) 
        >>> r #doctest: +ELLIPSIS
        <__main__.RamLRUCache object at 0x...>
        >>> r._cache
        {}
        >>> r._order
        []
        >>> r._size
        5
        """
        
        RamCache.__init__(self)

        self._order = []
        self._size = int(config['size'])

    @classmethod
    def checkConf(cls, config):
        """
        Check configuration for Ram LRU Cache.

        >>> RamLRUCache.checkConf({})
        Traceback (most recent call last):
        ...
        IncoherentSectionConfig: not module RamLRUCache
        >>> RamLRUCache.checkConf({'module' : 'false'})
        Traceback (most recent call last):
        ...
        IncoherentSectionConfig: not module RamLRUCache
        >>> RamLRUCache.checkConf({'module' : 'RamLRUCache', })
        Traceback (most recent call last):
        ...
        MissingConfigException: no size in config
        >>> RamLRUCache.checkConf({'module' : 'RamLRUCache', 'size': 'a'})
        Traceback (most recent call last):
        ...
        NotInteger: size must be an integer
        >>> RamLRUCache.checkConf({'module' : 'RamLRUCache', 'size': '3'})
        >>> RamLRUCache.checkConf({'module' : 'RamLRUCache', 'size': 3})
        """
        #RamCache.checkConf(config)

        # TODO factoriser
        try:
            if config['module'] == cls.__name__:
                pass
            else:
                raise IncoherentSectionConfig('not module %s' %  cls.__name__)
        except KeyError:
            raise IncoherentSectionConfig('not module %s' % cls.__name__)

        if 'size' in config:
            try:
                tmp = int(config['size'])
            except ValueError:
                raise NotInteger('size must be an integer')
        else:
            raise MissingConfigException('no size in config')



    def cached(self, func, *args, **kwargs):
        """
        >>> r = RamLRUCache({'size' : 5})
        >>> r._cache =  {'a': {'([1, 2], {})': {'{}': 3}}}
        >>> r.cached('a',[1, 2], {})
        3
        >>> r._order
        ['a||(([1, 2], {}), {})||{}']
        >>> r._cache = {'a': {'([1, 2], {})': {'{}': 3}}, 'c': {'([1, 3], {})': {'{}': 3.1400000000000001}}, 'b': {'([1, 3], {})': {'{}': 66}}}
        >>> r._order = ['a||(([1, 2], {}), {})||{}', 'b||(([1, 3], {}), {})||{}', 'c||(([1, 3], {}), {})||{}']
        >>> r._order
        ['a||(([1, 2], {}), {})||{}', 'b||(([1, 3], {}), {})||{}', 'c||(([1, 3], {}), {})||{}']
        >>> r.cached('a',[1, 2], {})
        3
        >>> r._order
        ['b||(([1, 3], {}), {})||{}', 'c||(([1, 3], {}), {})||{}', 'a||(([1, 2], {}), {})||{}']
        """
        
        key = self._computeKey(func, args, kwargs )

        if key in self._order:
            self._order.remove(key)
           
        self._order.append(key)
        
        return RamCache.cached(self, func, *args, **kwargs)
        

    def putInCache(self, func, result, *args, **kwargs):
        """
        >>> r = RamLRUCache({'size' : 5})
        >>> r.putInCache('a', 3, [1, 2], {})
        3
        >>> r._order
        ['a||(([1, 2], {}), {})||{}']
        >>> r.putInCache('b', 66, [1, 3], {})
        66
        >>> r.putInCache('c', 3.14, [1, 3], {})
        3.1400000000000001
        >>> r._order
        ['a||(([1, 2], {}), {})||{}', 'b||(([1, 3], {}), {})||{}', 'c||(([1, 3], {}), {})||{}']
        >>> r._cache
        {'a': {'([1, 2], {})': {'{}': 3}}, 'c': {'([1, 3], {})': {'{}': 3.1400000000000001}}, 'b': {'([1, 3], {})': {'{}': 66}}}
        """

        key = self._computeKey(func, args, kwargs )

        self._order.append(key)
        if len(self._order) >= self._size:
            tmp = self._order.pop(0).split('||')
            del(_cache[tmp[0]][tmp[1]][tmp[2]])

        return RamCache.putInCache(self, func, result, *args, **kwargs)
            

    def _computeKey(self, func, *args, **kwargs):
        """
        TODO improve compute
        >>> r = RamLRUCache({'size' : 5})
        >>> r._computeKey('func', ['args1', 'args2'], {'kwargs1': 'value1',})
        \"func||(['args1', 'args2'], {'kwargs1': 'value1'})||{}\"
        """
        return '||'.join([str(i) for i in  [func, args, kwargs]] )


    
class NotInteger(Exception):
    """
    >>> NotInteger('foo')
    NotInteger('foo',)
    """
    pass
           
            
            
                       
            

if __name__ == "__main__":
    import doctest
    doctest.testmod()

