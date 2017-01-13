from robotremoteserver import Binary

try:
    basestring
except:
    basestring = str


class Arguments(object):

    def argument_should_be_correct(self, argument, expected):
        expected = eval(expected)
        if argument != expected:
            raise AssertionError('%r != %r' % (argument, expected))
        self.should_not_contain_binary(argument)

    def should_not_contain_binary(self, argument):
        if isinstance(argument, Binary):
            raise AssertionError('Binary with data %r found!' % argument.data)
        if isinstance(argument, dict):
            for key, value in argument.items():
                self.should_not_contain_binary(key)
                self.should_not_contain_binary(value)
        if isinstance(argument, list):
            for item in argument:
                self.should_not_contain_binary(item)

    def no_arguments(self):
        return self._format_args()

    def one_argument(self, arg):
        return self._format_args(arg)

    def two_arguments(self, arg1, arg2):
        return self._format_args(arg1, arg2)

    def six_arguments(self, arg1, arg2, arg3, arg4, arg5, arg6):
        return self._format_args(arg1, arg2, arg3, arg4, arg5, arg6)

    def arguments_with_default_values(self, arg1, arg2='2', arg3=3):
        return self._format_args(arg1, arg2, arg3)

    def variable_number_of_arguments(self, *args):
        return self._format_args(*args)

    def required_defaults_and_varargs(self, req, default='world', *varargs):
        return self._format_args(req, default, *varargs)

    def kwargs(self, **kwargs):
        self.should_not_contain_binary(kwargs)
        return self._format_args(**kwargs)

    def args_and_kwargs(self, arg1, arg2='default', **kwargs):
        return self._format_args(arg1, arg2, **kwargs)

    def varargs_and_kwargs(self, *varargs, **kwargs):
        return self._format_args(*varargs, **kwargs)

    def args_varargs_and_kwargs(self, arg1='default1', arg2='default2',
                                *varargs, **kwargs):
        return self._format_args(arg1, arg2, *varargs, **kwargs)

    def _format_args(self, *args, **kwargs):
        args += tuple('%s:%s' % (k, self._format_arg(v))
                      for k, v in sorted(kwargs.items()))
        return ', '.join(self._format_arg(a) for a in args)

    def _format_arg(self, arg):
        if isinstance(arg, basestring):
            return arg
        return '%s (%s)' % (arg, type(arg).__name__)


if __name__ == '__main__':
    import sys
    from robotremoteserver import RobotRemoteServer

    RobotRemoteServer(Arguments(), '127.0.0.1', *sys.argv[1:])
