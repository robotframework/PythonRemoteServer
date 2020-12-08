*** Settings ***
Documentation     Testing basic communication using a class based library.
...               `module.robot` contains same tests using a library
...               implemented as a module.
Resource          resource.robot
Suite Setup       Start And Import Remote Library    Basics.py
Suite Teardown    Stop Remote Library

*** Variables ***
${COUNT}          100

*** Test Cases ***
Passing
    Passing

Failing
    [Documentation]    FAIL This is the error we get
    Failing    This is the error we get
    Fail    This should not be executed

Logging
    [Documentation]    LOG 1 INFO Hello, world! LOG 2 WARN Warning, warning!!
    Logging    Hello, world!
    Logging    Warning, warning!!    WARN

Returning
    ${ret} =    Returning    return this
    Should Be Equal    ${ret}    return this

Use multiple times
    [Documentation]
    ...    LOG 1.1.2 Round 1
    ...    LOG 1.2.2 Round 2
    ...    LOG 1.${COUNT}.2 Round ${COUNT}
    FOR    ${i}    IN RANGE    ${COUNT}
        Passing
        Logging    Round ${i + 1}
    END

Private methods should ne ignored
    [Documentation]    FAIL No keyword with name 'Private Method' found.
    Private Method

Attributes should be ignored
    [Documentation]    FAIL No keyword with name 'attribute' found.
    attribute
