#!/usr/bin/env path

from abstractcache import AbstractCache

from exceptionconfig import *

class DummyCache(AbstractCache):
    """
    Fake Cache.
    """
    
    def __init__(self):
        """
        Fake Cache.

        >>> DummyCache() #doctest: +ELLIPSIS
        <__main__.DummyCache object at 0x...>
        """
        AbstractCache.__init__(self)
    
    @staticmethod
    def checkConf(config):
        """
        Check configuration for fake Cache.

        >>> DummyCache.checkConf({})
        Traceback (most recent call last):
        ...
        IncoherentSectionConfig: not module DummyCache
        >>> DummyCache.checkConf({'module' : 'false'})
        Traceback (most recent call last):
        ...
        IncoherentSectionConfig: not module DummyCache
        >>> DummyCache.checkConf({'module' : 'DummyCache'})
        Traceback (most recent call last):
        ...
        MissingConfigException: missing param1 for DummyCache
        >>> DummyCache.checkConf({'module' : 'DummyCache', 'param1' : 'value1'})
        """
        try:
            if config['module'] == 'DummyCache':
                if 'param1' not in config:
                    raise MissingConfigException("missing param1 for DummyCache")
            else:
                raise IncoherentSectionConfig('not module DummyCache')
        except KeyError:
            raise IncoherentSectionConfig('not module DummyCache')
        

if __name__ == "__main__":
    import doctest
    doctest.testmod()
