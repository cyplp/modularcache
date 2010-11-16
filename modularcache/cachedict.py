#!/usr/bin/env python


class CacheDict(dict, object):
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
	>>> a is b
	True
        """
        return CacheDict._instance

 
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()
