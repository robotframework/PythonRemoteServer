*** Settings ***
Resource          resource.robot
Suite Setup       Start And Import Remote Library    failing.py
Suite Teardown    Stop Remote Library

*** Test Cases ***
Not special
    [Documentation]  FAIL message
    Not special    message
    Fail    This should not be executed

Continuable
    [Documentation]  FAIL Several failures occurred:\n\n
    ...    1) message\n\n
    ...    2) second message\n\n
    ...    3) third message
    Continuable    message
    Continuable    second message
    Continuable    third message

Fatal
    [Documentation]  FAIL Execution ends here
    Fatal    Execution ends here
    Fail    This should not be executed

Fails due to earlier fatal error
    [Documentation]  FAIL Test execution stopped due to a fatal error.
    Fail    This should not be executed
