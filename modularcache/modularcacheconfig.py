#!/usr/bin/env python

from cachedict import CacheDict

import ConfigParser

import exceptionconfig

class ModularCacheConfig(object):
    """
    Singleton class.
    """
    _instance = None

    def __init__(self, fileconf):
        """
        Make a modular cache config.
        fileconf : path to a config file.
        
        >>> ModularCacheConfig('test/test.ini') #doctest: +ELLIPSIS
        <__main__.ModularCacheConfig object at 0x...>
        """
        self._config = ConfigParser.ConfigParser()
        self._config.read(fileconf)
        
        if self._checkConfig():
            pass
        
        ModularCacheConfig._instance = self 

    @staticmethod    
    def getInstance():
        """
        Return the previous instance.
        
        >>> ModularCacheConfig._instance = None
        >>> ModularCacheConfig.getInstance()
        >>> m0 = ModularCacheConfig('test/test.ini') #doctest: +ELLIPSIS
        >>> ModularCacheConfig.getInstance() #doctest: +ELLIPSIS
        <__main__.ModularCacheConfig object at 0x...>
        >>> m1 = ModularCacheConfig.getInstance()
        >>> m1 == m0
        True
        """
        return ModularCacheConfig._instance

    def _checkConfig(self):
        """
        Check if config file is ok.
        Return True or False

        >>> ModularCacheConfig('test/bad1.ini')
        Traceback (most recent call last):
        ...
        NoModularCacheSection

        
        >>> ModularCacheConfig('test/bad2.ini')
        Traceback (most recent call last):
        ...
        NoKeysOptions

        >>> ModularCacheConfig('test/bad3.ini')
        Traceback (most recent call last):
        ...
        CacheSectionNotDefined: No Cache_dummy1 section
        """

        try:
            mainSection = self._config._sections['ModularCache']
        except KeyError:
            raise exceptionconfig.NoModularCacheSection()

        try:
            options = [i.strip() for i in mainSection['keys'].split(',')]
        except KeyError:
            raise exceptionconfig.NoKeysOptions()

        for option in options:
            if 'Cache_'+option  not in self._config._sections :
                raise exceptionconfig.CacheSectionNotDefined('No Cache_'+option+' section')

        for option in options:

            self._checkSection(option)
            

        CacheDict()

        for option in options:
            self._addCache(option)

    def _checkSection(self, section):
        """
        Check a section.
        >>> m = ModularCacheConfig('test/bad4.ini')
        >>> m._checkSection('dummy1')
        """
        module = __import__(self._config._sections['Cache_'+str(section)]['module'].lower()).__dict__[self._config._sections['Cache_'+str(section)]['module']]
        return module.checkConf(self._config._sections['Cache_'+str(section)])

    def _addCache(self, section):
        """
        >>> m = ModularCacheConfig('test/bad4.ini')
        >>> m._addCache('dummy1')
        >>> cd = CacheDict.getInstance()
        >>> cd['dummy1'] #doctest: +ELLIPSIS
        <dummycache.DummyCache object at 0x...>
        """

        cd = CacheDict.getInstance()
        module = __import__(self._config._sections['Cache_'+str(section)]['module'].lower()).__dict__[self._config._sections['Cache_'+str(section)]['module']]( self._config._sections['Cache_'+str(section)])

        cd[section] = module

        
if __name__ == "__main__":
    import doctest
    doctest.testmod()
