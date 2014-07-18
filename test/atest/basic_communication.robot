*** Settings ***
Resource          resource.robot
Suite Setup       Start And Import Remote Library    basics.py
Suite Teardown    Stop Remote Library

*** Variables ***
${COUNT}          100

*** Test Cases ***
Passing
    Passing

Failing
    [Documentation]    FAIL This is the error we get
    Run Keyword And Expect Error    Expected error message    Expected Fail

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
    : FOR    ${i}    IN RANGE    ${COUNT}
    \    Passing
    \    Logging    Round ${i + 1}

Private methods should be ignored
    Comment    FAIL No keyword with name 'Private Method' found.
    Run Keyword And Expect Error    No keyword*    Keyword Should Exist    Private Method

Attributes should be ignored
    Comment    FAIL No keyword with name 'attribute' found.
    Run Keyword And Expect Error    No keyword*    Keyword Should Exist    attribute


*** Keywords ***
Expected Fail
    Failing    Expected error message
    Fail    This should not be executed

