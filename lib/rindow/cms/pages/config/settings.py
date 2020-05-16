import os

config = {
    'container': {
        'components': {
            'rindow.cms.pages.template': {
                'class': 'jinja2.Environment',
                'construct_args': {
                    'loader': { 'ref': 'rindow.cms.pages.template.FileSystemLoader' },
                    'bytecode_cache':{ 'ref': 'rindow.cms.pages.template.MemcachedBytecodeCache' },
                    'extensions': { 'value': [
                        'jinja2.ext.autoescape',
                        'jinja2.ext.loopcontrols',
                        'rindow.cms.pages.model.template.MarkdownifyExtension',
                        'rindow.cms.pages.model.template.DatetimeExtension',
                        'rindow.cms.pages.model.template.FragmentCacheExtension',
                    ] },
                    'autoescape': { 'value': True }
                },
                'properties':{
                    'fragment_cache': {'value': None }
                }
            },
            'rindow.cms.pages.template.FileSystemLoader': {
                'class': 'jinja2.FileSystemLoader',
                'construct_args': {
                    'searchpath': { 'config': 'mvc:view:template_paths'}
                }
            },
            'rindow.cms.pages.template.FileSystemBytecodeCache': {
                'class': 'jinja2.FileSystemBytecodeCache',
                'construct_args': {
                    'directory': { 'value': os.path.dirname(__file__) + '/../cache'}
                }
            },
            'rindow.cms.pages.template.MemcachedBytecodeCache': {
                'class': 'jinja2.MemcachedBytecodeCache',
                'construct_args': {
                    'client': {'value': None }
                }
            },
            'rindow.cms.pages.ConfigLoader': {
                'class': 'rindow.cms.pages.model.appearance.YamlLoader',
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
            'template_paths':[
                os.path.dirname(__file__) + '/../views'
            ]
        }
    },
    'theme': {
        'config': 'your_configuration/wiki/_config.yml',
    }
}
