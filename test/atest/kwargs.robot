*** Settings ***
Documentation     Cannot combine with other argument test suites because kwargs
...               cannot be passed to template user keywords they use. This can
...               be fixed if/when user keywords support kwargs in RF 2.9.
Resource          resource.robot
Suite Setup       Start And Import Remote Library    Arguments.py
Suite Teardown    Stop Remote Library

*** Test Cases ***
No kwargs
    ${result} =    Kwargs
    Should Be Equal    ${result}    ${EMPTY}

One kwarg
    ${result} =    Kwargs    foo=bar
    Should Be Equal    ${result}    foo:bar

Multiple kwargs
    ${result} =    Kwargs    a=1    c=3    d=4    b=2
    Should Be Equal    ${result}    a:1, b:2, c:3, d:4

Args and kwargs
    ${result} =    Args and kwargs    arg
    Should Be Equal    ${result}    arg, default
    ${result} =    Args and kwargs    arg    foo=bar
    Should Be Equal    ${result}    arg, default, foo:bar
    ${result} =    Args and kwargs    a    arg2=b    c=3    d=4
    Should Be Equal    ${result}    a, b, c:3, d:4

Varargs and kwargs
    ${result} =    Varargs and kwargs
    Should Be Equal    ${result}    ${EMPTY}
    ${result} =    Varargs and kwargs    foo=bar
    Should Be Equal    ${result}    foo:bar
    ${result} =    Varargs and kwargs    arg    foo=bar
    Should Be Equal    ${result}    arg, foo:bar
    ${result} =    Varargs and kwargs    a    b    c    d=4    e=5    f=6
    Should Be Equal    ${result}    a, b, c, d:4, e:5, f:6

Args, varargs and kwargs
    ${result} =    Args varargs and kwargs    arg
    Should Be Equal    ${result}    arg, default2
    ${result} =    Args varargs and kwargs    arg    foo=bar
    Should Be Equal    ${result}    arg, default2, foo:bar
    ${result} =    Args varargs and kwargs    arg2=foo    foo=bar
    Should Be Equal    ${result}    default1, foo, foo:bar
    ${result} =    Args varargs and kwargs    a    arg2=b    c=3
    Should Be Equal    ${result}    a, b, c:3
    ${result} =    Args varargs and kwargs    a    b    c    d    e=5    f=6
    Should Be Equal    ${result}    a, b, c, d, e:5, f:6

Non-ASCII kwargs
    ${result} =    Kwargs    a=hyvää    b=päivää    c=\u2603
    Should Be Equal    ${result}    a:hyvää, b:päivää, c:\u2603

Non-string kwargs
    ${list} =    Create List    1    ${2}
    ${result} =    Kwargs    a=${1}    b=${True}    c=${list}
    Should Be Equal    ${result}    a:1 (int), b:True (bool), c:['1', 2] (list)

Binary kwargs
    ${tuple} =    Evaluate    ('\x02',)
    ${result} =    Kwargs    a=\x00    b=\x01    c=${tuple}
    Log    ${result}    formatter=repr
    IF    ${PY2}
        Should be equal    ${result}    ${{b"a:\x00, b:\x01, c:['\\x02'] (list)"}}
    ELSE
        Should be equal    ${result}    ${{b"a:\x00, b:\x01, c:[b'\\x02'] (list)"}}
    END
