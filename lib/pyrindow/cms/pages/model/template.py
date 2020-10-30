from jinja2 import nodes,FileSystemLoader
from jinja2.ext import Extension
import markdown
#from markdown.extensions.wikilinks import WikiLinkExtension
from time import gmtime,strftime

def FileSystemLoaderFactory(serviceLocator,**kwargs):
    newKwargs = {}
    for kw,arg in kwargs.items():
        if kw=='searchpath':
            arg = serviceLocator.getConfigValue(arg['config'])
            searchpath = []
            for namespace,path in arg.items():
                if path:
                    if isinstance(path,tuple):
                        mode,alias = path
                        if mode=='alias':
                            tpath = serviceLocator.getConfigValue('mvc:view:template_path_aliases:'+alias)
                            searchpath.append(tpath)
                        else:
                            raise Exception('Invalid template path mode in "'+namespace+'": '+mode)
                    else:
                        searchpath.append(path)
            newKwargs[kw] = searchpath
        else:
            newKwargs[kw] = arg
    return FileSystemLoader(**newKwargs)

class MarkdownifyExtension(Extension):
    def __init__(self, environment):
        super(MarkdownifyExtension, self).__init__(environment)
        environment.filters.update({'markdownify':self.markdownify})
        self._markdown = markdown.Markdown(
            extensions=[
                #'attr_list',
                #'def_list',
                #'fenced_code',
                #'tables',
                'extra',
                #WikiLinkExtension(base_url='',end_url='')
            ]
        )

    def markdownify(self,text):
        if text:
            return self._markdown.convert(text)
        else:
            return ''

class DatetimeExtension(Extension):
    def __init__(self, environment):
        super(DatetimeExtension, self).__init__(environment)
        environment.globals.update({'gmtime':gmtime})
        environment.filters.update({'date':self.date})

    def date(self,timestamp,format):
        return strftime(format,timestamp)

class FragmentCacheExtension(Extension):
    # a set of names that trigger the extension.
    tags = {"cache"}

    def __init__(self, environment):
        super(FragmentCacheExtension, self).__init__(environment)

        # add the defaults to the environment
        environment.extend(
            fragment_cache_prefix=self.__module__ + type(self).__name__,
            fragment_cache=None)

    def parse(self, parser):
        # the first token is the token that started the tag.  In our case
        # we only listen to ``'cache'`` so this will be a name token with
        # `cache` as value.  We get the line number so that we can give
        # that line number to the nodes we create by hand.
        lineno = next(parser.stream).lineno

        # now we parse a single expression that is used as cache key.
        args = [parser.parse_expression()]

        # if there is a comma, the user provided a timeout.  If not use
        # None as second parameter.
        if parser.stream.skip_if("comma"):
            args.append(parser.parse_expression())
        else:
            args.append(nodes.Const(None))

        # now we parse the body of the cache block up to `endcache` and
        # drop the needle (which would always be `endcache` in that case)
        body = parser.parse_statements(["name:endcache"], drop_needle=True)

        # now return a `CallBlock` node that calls our _cache_support
        # helper method on this extension.
        return nodes.CallBlock(
            self.call_method("_cache_support", args), [], [], body
        ).set_lineno(lineno)

    def _cache_support(self, timeout, name, caller):
        """Helper callback."""
        key = self.environment.fragment_cache_prefix + name

        # try to load the block from the cache
        # if there is no fragment in the cache, render it and store
        # it in the cache.
        if self.environment.fragment_cache:
            rv = self.environment.fragment_cache.get(key)
            if rv is not None:
                return rv
        rv = caller()
        if self.environment.fragment_cache:
            self.environment.fragment_cache.add(key, rv, timeout)
        return rv
