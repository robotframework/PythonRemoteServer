*** Settings ***
Resource          resource.txt
Suite Setup       Start And Import Remote Library    arguments.py
Suite Teardown    Stop Remote Library

*** Test Cases ***
Using arguments when no accepted
    [Documentation]  FAIL Keyword 'Remote.No Arguments' expected 0 arguments, got 1.
    No Arguments  not allowed

Too few arguments when using only required arguments
    [Documentation]  FAIL Keyword 'Remote.One Argument' expected 1 argument, got 0.
    One Argument

Too many arguments when using only required arguments
    [Documentation]  FAIL Keyword 'Remote.Two Arguments' expected 2 arguments, got 3.
    Two Arguments    too    many    arguments

Too few arguments when using default values
    [Documentation]  FAIL Keyword 'Remote.Arguments With Default Values' expected 1 to 3 arguments, got 0.
    Arguments With Default Values

Too many arguments when using default values
    [Documentation]  FAIL Keyword 'Remote.Arguments With Default Values' expected 1 to 3 arguments, got 5.
    Arguments With Default Values    this    is    way    too    much

Too few arguments when using varargs
    [Documentation]  FAIL Keyword 'Remote.Required Defaults And Varargs' expected at least 1 argument, got 0.
    Required Defaults And Varargs

Using arguments when only kwargs accepted
    [Documentation]  FAIL Keyword 'Remote.Kwargs' expected 0 non-keyword arguments, got 4.
    Kwargs    normal    args    are    no-no

Too few arguments when kwargs accepted
    [Documentation]  FAIL Keyword 'Remote.Args And Kwargs' expected 1 to 2 non-keyword arguments, got 0.
    Args and kwargs

Too many arguments when kwargs accepted
    [Documentation]  FAIL Keyword 'Remote.Args And Kwargs' expected 1 to 2 non-keyword arguments, got 7.
    Args and kwargs    we    do    not    accept    this    many    args

Missing argument when using kwargs
    [Documentation]  FAIL Keyword 'Remote.Args And Kwargs' missing value for argument 'arg1'.
    Args and kwargs    arg2=2    foo=bar
