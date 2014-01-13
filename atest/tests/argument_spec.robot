*** Settings ***
Resource          resource.robot
Suite Setup       Start And Import Remote Library    arguments.py
Test Template     Arguments Should Be Accepted
Suite Teardown    Stop Remote Library

*** Test Cases ***
No arguments
    ${EMPTY}            No Arguments

Required arguments
    some argument       One Argument       some argument
    arg1, arg2          Two Arguments      arg1    arg2
    1, 2, 3, 4, 5, 6    Six Arguments    1    2    3    4    5    6

Arguments with default values
    one, two, three     Arguments With Default Values    one    two    three
    one, two, 3 (int)   Arguments With Default Values    one    two
    one, 2, 3 (int)     Arguments With Default Values    one

Variable number of arguments
    ${EMPTY}            Variable Number Of Arguments
    One argument        Variable Number Of Arguments    One argument
    3, args, now        Variable Number Of Arguments    3    args    now
    1, 2, 3 (int), 4    Variable Number Of Arguments    1    2    ${3}    4

Required arguments, default values and varargs
    Hello, world        Required Defaults And Varargs    Hello
    Hi, tellus          Required Defaults And Varargs    Hi    tellus
    Hei, taas, maa      Required Defaults And Varargs    Hei    taas    maa
    1, 2, 3 (int), 4    Required Defaults And Varargs    1    2    ${3}    4

*** Keywords ***
Arguments Should Be Accepted
    [Arguments]    ${expected}    ${keyword}    @{arguments}
    ${actual} =    Run Keyword    ${keyword}    @{arguments}
    Should Be Equal    ${actual}    ${expected}
