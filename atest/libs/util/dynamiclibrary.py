import inspect


class DynamicApi:
    """A wrapper to make static API libraries use the dynamic API."""
    def __init__(self, library, kwdoc=True, argsdoc=True):
        self._library = library
        if kwdoc:
            self.get_keyword_documentation = self._get_keyword_documentation
        if argsdoc:
            self.get_keyword_arguments = self._get_keyword_arguments

    def get_keyword_names(self):
        return [attr for attr in dir(self._library) if attr[0] != '_'
                     and inspect.isroutine(getattr(self._library, attr))]

    def run_keyword(self, name, args):
        return self._get_keyword(name)(*args)

    def _get_keyword_documentation(self, name):
        if name == '__intro__':
            return inspect.getdoc(self._library) or ''
        if name == '__init__' and inspect.ismodule(self._library):
            return ''
        return inspect.getdoc(self._get_keyword(name)) or ''

    def _get_keyword_arguments(self, name):
        kw = self._get_keyword(name)
        if not kw:
            return []
        return self._arguments_from_kw(kw)

    def _get_keyword(self, name):
        kw = getattr(self._library, name, None)
        if inspect.isroutine(kw):
            return kw
        return None

    def _arguments_from_kw(self, kw):
        args, varargs, _, defaults = inspect.getargspec(kw)
        if inspect.ismethod(kw):
            args = args[1:]  # drop 'self'
        if defaults:
            args, names = args[:-len(defaults)], args[-len(defaults):]
            args += ['%s=%s' % (n, d) for n, d in zip(names, defaults)]
        if varargs:
            args.append('*%s' % varargs)
        return args
