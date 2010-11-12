#!/usr/bin/env path

class AbstractCache(object):
    """
    TODO
    """

    def __init__(self):
        pass

    def isCached(self, func, *args, **kwargs):
        pass

    def cached(self, func, *args, **kwargs):
        pass

    def putInCache(self, func, result, *args, **kwargs):
        pass
    
    @staticmethod
    def checkConf(config):
        pass
    
