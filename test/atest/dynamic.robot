*** Settings ***
Resource          resource.robot
Suite Setup       Start And Import Remote Library    Dynamic.py
Suite Teardown    Stop Remote Library

*** Test Cases ***
Passing
    Passing
    Passing    one arg accepted

Failing
    [Documentation]    FAIL The message
    Failing    The message

Logging
    [Documentation]    LOG 1 INFO Hello, world!    LOG 2 DEBUG Hi!
    Logging    Hello, world!
    Logging    Hi!    DEBUG

Returning
    ${result} =    Returning
    Should Be Equal    ${result}    Hello, world!

Named arguments
    [Documentation]    FAIL Bye!!    LOG 2 INFO Hi, again!    LOG 3 FAIL Bye!!
    Passing    arg=ignored
    Logging    level=INFO    message=Hi, again!
    Failing    message=Bye!!

Kwargs
    [Template]    Kwargs
    ${EMPTY}
    a: 1    a=1
    c=3    a=1    expected=a: 1, b: 2, c: 3    b=2

Called with invalid arguments when arguments are known
    [Documentation]    FAIL Keyword 'Remote.Passing' expected 0 to 1 arguments, got 6.
    Passing    more    than    one    arg    not    accepted

Called with invalid arguments when arguments are not known
    [Documentation]    FAIL GLOB: TypeError: *returning* *3*
    Returning    too    many    arguments
