import os

config = {
    'container': {
        'components': {
            'pyrindow.cms.pages.template.FileSystemLoader': {
                'class': 'jinja2.FileSystemLoader',
                'factory':'pyrindow.cms.pages.model.template.FileSystemLoaderFactory',
                'factory_args': {
                    'searchpath': { 'config': 'mvc:view:template_paths'}
                }
            },
            'pyrindow.cms.pages.template': {
                'class': 'jinja2.Environment',
                'construct_args': {
                    'loader': { 'ref': 'pyrindow.cms.pages.template.FileSystemLoader' },
                    'bytecode_cache':{ 'ref': 'pyrindow.cms.pages.template.MemcachedBytecodeCache' },
                    'extensions': { 'value': [
                        'jinja2.ext.autoescape',
                        'jinja2.ext.loopcontrols',
                        'pyrindow.cms.pages.model.template.MarkdownifyExtension',
                        'pyrindow.cms.pages.model.template.DatetimeExtension',
                        'pyrindow.cms.pages.model.template.FragmentCacheExtension',
                    ] },
                    'autoescape': { 'value': True }
                },
                'properties':{
                    'fragment_cache': {'value': None }
                }
            },
            'pyrindow.cms.pages.template.FileSystemBytecodeCache': {
                'class': 'jinja2.FileSystemBytecodeCache',
                #'construct_args': {
                #    'directory': { 'value': os.path.dirname(__file__) + '/../cache'}
                #},
            },
            'pyrindow.cms.pages.template.MemcachedBytecodeCache': {
                'class': 'jinja2.MemcachedBytecodeCache',
                'construct_args': {
                    'client': {'value': None }
                },
            },
            'pyrindow.cms.pages.ConfigLoader': {
                'class': 'pyrindow.cms.pages.model.appearance.YamlLoader',
                'construct_args': {
                    'target': { 'config': 'theme:config'},
                    'cache': {'value': None },
                    'timeout': {'value': 300 }
                }
            }
        }
    },
    'mvc': {
        'view': {
            'template_paths':{
                'pyrindow.cms.pages.template.views':
                    ('alias','pyrindow.cms.pages.template.bootstrap3'),
            },
            'template_path_aliases':{
                'pyrindow.cms.pages.template.bootstrap3': os.path.dirname(__file__) + '/../views/bootstrap3',
                'pyrindow.cms.pages.template.amp': os.path.dirname(__file__) + '/../views/amp',
            }
        }
    },
    'flask': {
        'jinja_options': {
            'loader': 'pyrindow.cms.pages.template.FileSystemLoader',
            'extensions': {
                'jinja2.ext.autoescape':True,
                'jinja2.ext.loopcontrols':True,
                'pyrindow.cms.pages.model.template.MarkdownifyExtension':True,
                'pyrindow.cms.pages.model.template.DatetimeExtension':True,
                #'pyrindow.cms.pages.model.template.FragmentCacheExtension':True,
            },
        },
    },
    'theme': {
        'config': 'your_configuration/wiki/_config.yml',
    }
}
