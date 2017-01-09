*** Settings ***
Resource          resource.robot
Suite Setup       Start And Import Remote Library    Failing.py
Suite Teardown    Stop Remote Library
Test Template     Correct failure should occur

*** Variables ***
${SOURCE}         File "[\\w: /\\\\]+Failing.py", line \\d+

*** Test Cases ***
Generic exceptions
    Exception    My message
    AssertionError    Another message
    RuntimeError    Yet another message

Non-generic exceptions
    NameError    My message    NameError: My message
    ZeroDivisionError    Another message    ZeroDivisionError: Another message

Custom exceptions
    MyException    The message    MyException: The message

Suppress name
    SuppressNameException    The message    The message

No message
    Exception    ${NONE}    Exception
    SuppressNameException    ${NONE}    SuppressNameException

Empty message
    Exception    ${EMPTY}    Exception
    SuppressNameException    ${EMPTY}    SuppressNameException

Multiline message
    Exception    Can\n\haz\nmultiple\n\lines?\n\n\nYezzz!!!\n

Non-ASCII message
    Exception    Hyvä \u2603!!

Non-ASCII bytes
    Exception    b'Hyv\\xe4'    *Hyv?*    evaluate=yes

Binary Unicode
    Exception    u'\\x00+\\x01+\\x02'    \x00+\x01+\x02    evaluate=yes

Non-string message
    Exception    42    evaluate=yes
    Exception    None
    Exception    ('Message', 42)    evaluate=yes
    Exception    ('-\\x01-', 42)    evaluate=yes

Failure deeper
    [Documentation]    FAIL Finally failing
    [Template]    NONE
    Failure Deeper

Traceback
    [Documentation]  FAIL MyException: My error message
    ...    LOG 1:1 FAIL MyException: My error message
    ...    LOG 1:2 DEBUG REGEXP: Traceback \\(most recent call last\\):
    ...    \\s+${SOURCE}, in failure
    ...    \\s+raise exception\\(message\\)
    [Template]    NONE
    Failure    MyException    My error message

Traceback with multiple entries
    [Documentation]  FAIL Finally failing
    ...    LOG 1:1 FAIL Finally failing
    ...    LOG 1:2 DEBUG REGEXP: Traceback \\(most recent call last\\):
    ...    \\s+${SOURCE}, in failure_deeper
    ...    \\s+self.failure_deeper\\(rounds-1\\)
    ...    \\s+${SOURCE}, in failure_deeper
    ...    \\s+self.failure_deeper\\(rounds-1\\)
    ...    \\s+${SOURCE}, in failure_deeper
    ...    \\s+raise RuntimeError\\('Finally failing'\\)
    [Template]    NONE
    Failure Deeper    rounds=3

*** Keywords ***
Correct failure should occur
    [Arguments]    ${exception}    ${message}    ${expected}=    ${evaluate}=
    ${expected} =    Set Variable If    $expected    ${expected}    ${message}
    Run Keyword And Expect Error    ${expected}
    ...    Failure    ${exception}    ${message}    ${evaluate}
