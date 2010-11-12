#!/usr/bin/env path


class CacheDict(object):
    """
    Singleton class.
    """

    _instance = None

    def __init__(self):
        """
        Dict 
        >>> CacheDict() #doctest: +ELLIPSIS
        <__main__.CacheDict object at 0x...>
        """

        self._caches = {}

        CacheDict._instance = self
        

    @staticmethod
    def getInstance():
        """
        Return Singleton Instance.

        >>> CacheDict._instance = None
        >>> CacheDict.getInstance()
        >>> a = CacheDict() 
        >>> a #doctest: +ELLIPSIS
        <__main__.CacheDict object at 0x...>
        >>> b = CacheDict.getInstance()
        >>> a == b
        True
        """
        return CacheDict._instance

    def __setitem__(self, key, value):
        """
        Add item.

        >>> c = CacheDict()
        >>> c._caches
        {}
        >>> c['a'] = 1
        >>> c._caches
        {'a': 1}
        """
        self._caches[key] = value

    def __getitem__(self, key):
        """
        Get Item.

        >>> c = CacheDict()
        >>> c._caches['a'] = 1
        >>> c['a']
        1
        """

        return self._caches[key]

    def __delitem__(self, key):
        """
        Del item.

        >>> c = CacheDict()
        >>> c._caches['a'] = 1
        >>> c._caches
        {'a': 1}
        >>> del(c['a'])
        >>> c._caches
        {}
        """

        del(self._caches[key])

    def __contains__(self, key):
        """
        Contains key.
        >>> c = CacheDict()
        >>> c._caches['a'] = 1
        >>> 'a' in c
        True
        >>> 'b' in c
        False
        """
        return key in self._caches
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()
