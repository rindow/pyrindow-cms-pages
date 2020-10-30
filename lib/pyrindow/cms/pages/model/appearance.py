import os,yaml

class RepositoryConfig(object):
    def __init__(self, repository=None,path=None,value=None,debug_path=None):
        pass

class YamlConfig(object):
    def __init__(self,filename=None,path=None,value=None,debug_path=None):
        if debug_path:
            self.debug_path = debug_path
        else:
            self.debug_path = ''
        if filename:
            stream = open(filename,'r',encoding='utf-8')
            self.yaml = yaml.safe_load(stream)
            stream.close()
            if path:
                self.path = path
            else:
                self.path = os.path.dirname(filename)
        elif path:
            self.path = path
            filename = self._filename(path)
            if filename:
                stream = open(filename,'r',encoding='utf-8')
                self.yaml = yaml.safe_load(stream)
                stream.close()
            elif os.path.isdir(self.path):
                self.yaml = {}
            else:
                raise Exception('path is not found:"%s"' % path)
        else:
            if not isinstance(value,dict):
                raise Exception('value must be dict type')
            self.path = None
            self.yaml = value
    def __getattr__(self, name):
        if self.yaml.has_key(name):
            value = self.yaml.get(name)
            if isinstance(value,dict):
                value = YamlConfig(value=value,debug_path=self.debug_path+name)
                self.yaml[name] = value
        else:
            if not self.path:
                raise AttributeError('proparty %s is not exist in dict on "%s"' % (name,self.debug_path))
            path = self.path + '/' + name
            filename = self._filename(path)
            if not os.path.isdir(path) and not filename:
                raise AttributeError('proparty %s is not exist on path "%s".' % (name,path))
            value = YamlConfig(path=path,debug_path=self.debug_path+name)
            self.yaml[name] = value
        return value
    def _filename(self,path):
        filename = path + '.yml'
        if not os.path.isfile(filename):
            filename = path + '.yaml'
            if not os.path.isfile(filename):
                filename = None
        return filename

class YamlLoader(object):
    def __init__(self,target=None,cache=None,timeout=300):
        self.target = target
        self.cache = cache
        self.timeout = timeout
        self.cache_key_prefix=self.__module__ + type(self).__name__

    def load(self,target=None):
        if target==None:
            target = self.target
        if self.cache:
            key = self.cache_key_prefix + target
            value = self.cache.get(key)
            if value is not None:
                return value
        value = self._loadfiles(target)
        if self.cache:
            self.cache.add(key, value, self.timeout)
        return value

    def file2dict(self,filename):
        stream = open( filename,'r',encoding='utf-8')
        config = yaml.safe_load(stream)
        stream.close()
        return config

    def _loadfiles(self,target):
        config = {}
        passfile = None
        if os.path.isfile(target):
            config = self.file2dict(target)
            passfile = os.path.basename(target)
            target = os.path.dirname(target)
        for filename in os.listdir(target):
            if filename == passfile:
                continue
            fullpath = os.path.join(target, filename)
            if os.path.isfile(fullpath):
                name,ext = os.path.splitext(filename)
                if ext == '.yml' or ext == '.yaml':
                    config[name] = self.file2dict(fullpath)
            elif os.path.isdir(fullpath):
                config[filename] = self._loadfiles(fullpath)
        return config

class CollectionProxy(object):
    def __init__(self,entity):
        self._entity = entity
    def __getattr__(self,name):
        if name=='name':
            return self._entity['name']
        return self._entity['config'].get(name)
    def dumpConfig(self):
        return DictToYaml(self._entity.config)
    def clear(self):
        self._entity = None
    #if isinstance(config,unicode):
    #   raise Exception('unicode')
    #if isinstance(config,str):
    #       raise Exception('str')

class DocumentProxy(object):
    def __init__(self,entity,documentManager,routeManager):
        self._entity = entity
        self._collection = 'unsolved'
        self._documentManager = documentManager
        self._routeManager = routeManager
        self.url = None
    def __getattr__(self,name):
        if name=='name':
            return self._entity['name']
        elif name=='content':
            return self._entity['content']
        elif name=='date':
            return self._entity['date']

        return self._entity['headers'].get(name)
    def dumpHeaders(self):
        return DictToYaml(self._entity.headers)
    @property
    def collection(self):
        """Get collection entity"""
        if self._collection == 'unsolved':
            self._collection = CollectionProxy(self._entity['collection'])
        return self._collection
    def findDocument(self,name):
        if name:
            document = self._documentManager.findOne(self.collection.name,name)
            if document:
                return DocumentProxy(document,self._documentManager,self._routeManager)
        return None
    def clear(self):
        self._entity = None
        if isinstance(self._collection,CollectionProxy):
            self._collection.clear()
        self._collection = None
    def getDocumentUrl(self,collection=None,name=None):
        if collection==None:
            collection = self.collection.name
        if name==None:
            name = self.name
        return self._routeManager.getDocumentUrl(collection,name)

def YamlToDict(textValue):
    return yaml.safe_load(textValue)

def DictToYaml(dictValue):
    return yaml.safe_dump(
            dictValue,
            default_flow_style=False,
            allow_unicode=True
        )
