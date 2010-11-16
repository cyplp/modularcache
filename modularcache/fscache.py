#!/usr/bin/env python

import hashlib
import os
import threading
import glob
import datetime
import time
import cPickle

from abstractcache import AbstractCache
from exceptionconfig import *


class FsCache(threading.Thread, object):
    """
    Cache on filesytem.
    """

    def __init__(self, config):
       """
       Cache on filesytem.

       >>> f = FsCache({'dir' : 'test/cache', 'freq' :'2' ,'expirationdelay': '3'})
       >>> f #doctest: +ELLIPSIS
       <FsCache(Thread-1, ...)>
       >>> f._dir
       'test/cache'
       """ 
       threading.Thread.__init__(self)

       self.setDaemon(True)

       self._dir = config['dir']
       self._freq = int(config['freq'])
       self._expirationdelay = datetime.timedelta(seconds=int(config['expirationdelay']))
       self._go = True
	
      
    def stop(self):
        """
	Stop loop.
	>>> f = FsCache({'dir' : 'test/cache', 'freq' :'2' ,'expirationdelay': '3'})
	>>> f._go
	True
	>>> f.stop()
	>>> f._go
	False
	"""
	self._go = False
    def run(self):
        """
        Cleaning loop.
        """

        while(self._go):
            cacheFiles = glob.glob(os.path.join(self._dir,'*'))
            now = datetime.datetime.now()
            for i in cacheFiles:
                if self._isExpired(i, now):
                    self._cleanFile(i)
            time.sleep(self._freq)

    def _isExpired(self, cacheFile, timeRef):
        """
        the file is expired ?

        >>> f = FsCache({'dir' : 'test/cache', 'freq' :'2' ,'expirationdelay': '1'})
        >>> foo = open('test/expiredfile', 'wb')
        >>> foo.write('bar')
        >>> foo.close()
        >>> import datetime
        >>> f._isExpired('test/expiredfile', datetime.datetime.now())
        False
        >>> import time
        >>> time.sleep(2)
        >>> f._isExpired('test/expiredfile', datetime.datetime.now())
        True
        >>> os.remove('test/expiredfile')
        """

        accessTime = datetime.datetime.fromtimestamp(os.stat(cacheFile).st_atime)
        return accessTime + self._expirationdelay <= timeRef

    def _cleanFile(self, cacheFile):
        """
        Delete the file.

        >>> foo = open('test/cleanedfile', 'wb')
        >>> foo.write('bar')
        >>> foo.close()
        >>> os.path.isfile('test/cleanedfile')
        True
        >>> f = FsCache({'dir' : 'test/cache', 'freq' :'2' ,'expirationdelay': '2'})
        >>> f._cleanFile('test/cleanedfile')
        >>> os.path.isfile('test/cleanedfile')
        False
        """
        os.remove(cacheFile)

    
            
    def isCached(self, func, *args, **kwargs):
        """
        Is in Cache ?
        
        >>> f = FsCache({'dir' : 'test/cache', 'freq' :'2' ,'expirationdelay': '3'})
        >>> f.isCached('b',[1, 2], {})
        False
        >>> foo = open('test/cache/455bdde8de3f1b5ddbeac7ba0af07ba23f8b725c', 'wb')
        >>> foo.write('bar')
        >>> foo.close()
        >>> f.isCached('c',[1, 2], {})
        True
        """
        return os.path.isfile(os.path.join(self._dir,
                                           self._computeFilename(func, *args, **kwargs)))

    def cached(self, func, *args, **kwargs):
        """
        Return cache result.
        
        >>> f = FsCache({'dir' : 'test/cache', 'freq' :'2' ,'expirationdelay': '3'})
        >>> foo = open('test/cache/455bdde8de3f1b5ddbeac7ba0af07ba23f8b725c', 'wb')
        >>> import cPickle
        >>> cPickle.dump('bar', foo)
        >>> foo.close()
        >>> f.cached('c',[1, 2], {})
        'bar'
        """
        cachedFile = open(os.path.join(self._dir,
                                       self._computeFilename(func, *args, **kwargs)),'rb')
        tmp = cPickle.load(cachedFile)
        cachedFile.close()
        return tmp
    

    def putInCache(self, func, result, *args, **kwargs):
        """
        Put file in cache.

        >>> f = FsCache({'dir' : 'test/cache', 'freq' :'2' ,'expirationdelay': '3'})
        >>> f.putInCache('a', 3, [1, 2], {})
        3
        >>> os.path.isfile('test/cache/b546706c3d1155e7fbd95e03f25ae7695590d1d0')
        True
        """
        filename = self._computeFilename(func, *args, **kwargs)
        cacheFile = open(os.path.join(self._dir, filename), 'wb')
        cPickle.dump(result,cacheFile)
        cacheFile.close()
        return result

    def _computeFilename(self, func, *args, **kwargs):
        """
        Compute sha1 hash for filename.

        >>> f = FsCache({'dir' : 'test/cache', 'freq' :'2' ,'expirationdelay': '3'})
        >>> f._computeFilename('a',[1, 2], {})
        'b546706c3d1155e7fbd95e03f25ae7695590d1d0'
        """
        s = hashlib.sha1()
        s.update(str(func))
        s.update(str(args))
        s.update(str(kwargs))

        return s.hexdigest()
    
    @staticmethod
    def checkConf(config):
        """
        Check configuration for fake Cache.

        >>> FsCache.checkConf({})
        Traceback (most recent call last):
        ...
        IncoherentSectionConfig: not module FsCache
        >>> FsCache.checkConf({'module' : 'false'})
        Traceback (most recent call last):
        ...
        IncoherentSectionConfig: not module FsCache
        >>> FsCache.checkConf({'module' : 'FsCache'})
        Traceback (most recent call last):
        ...
        MissingConfigException: no dir in config
        >>> FsCache.checkConf({'module': 'FsCache', 'dir': 'test/noexist'})
        Traceback (most recent call last):
        ...
        MissingConfigException: no freq in config
        >>> FsCache.checkConf({'module': 'FsCache', 'dir': 'test/noexist', 'freq': False})
        Traceback (most recent call last):
        ...
        MissingConfigException: no expirationdelay in config
        >>> FsCache.checkConf({'module': 'FsCache', 'dir': 'test/noexist', 'freq': 'foo', 'expirationdelay': 'bar'})
        Traceback (most recent call last):
        ...
        CacheDirIncorrect: test/noexist isn't correct
        >>> FsCache.checkConf({'module': 'FsCache', 'dir': 'test/cache', 'freq': 'foo', 'expirationdelay': 'bar'})
        Traceback (most recent call last):
        ...
        NotInteger: freq must be an integer
        >>> FsCache.checkConf({'module': 'FsCache', 'dir': 'test/cache', 'freq': '2', 'expirationdelay': 'bar'})
        Traceback (most recent call last):
        ...
        NotInteger: expirationdelay must be an integer
        >>> FsCache.checkConf({'module': 'FsCache', 'dir': 'test/cache', 'freq': '2', 'expirationdelay': '3'})
        """
        try:
            
            
            if config['module'] != 'FsCache':
                raise IncoherentSectionConfig('not module FsCache')

            for option in ['dir', 'freq', 'expirationdelay'] :
                if not option in config:
                    raise MissingConfigException('no %s in config' % option)
                    

            if not os.path.isdir(config['dir']):
                raise CacheDirIncorrect(config['dir']+ " isn't correct")
                    
            for option in ['freq', 'expirationdelay']:
                try:
                    tmp = int(config[option])
                except ValueError:
                    raise NotInteger('%s must be an integer' % option)

        except KeyError:
            raise IncoherentSectionConfig('not module FsCache')

class CacheDirIncorrect(Exception):
    """
    >>> CacheDirIncorrect('foo')
    CacheDirIncorrect('foo',)
    """
    pass


class NotInteger(Exception):
    """
    >>> NotInteger('foo')
    NotInteger('foo',)
    """
    pass

if __name__ == "__main__":
    import doctest
    doctest.testmod()
