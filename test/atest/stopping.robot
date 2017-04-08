*** Settings ***
Resource          resource.robot
Test Setup        Start Server
Test Teardown     Server Should Be Stopped

*** Test Cases ***
Stop Remote Server
    Stop Remote Server

Stop Remote Server Disabled
    [Documentation]    FAIL Not stopped!
    ...    LOG 2 WARN GLOB: Robot Framework remote server at 127.0.0.1:* does not allow stopping.
    [Setup]    Start Server    no_stop
    Stop Remote Server Disabled.Stop Remote Server
    Fail    Not stopped!
    [Teardown]    Terminate Process

SIGINT
    [Tags]    no-windows
    Send Signal To Process    SIGINT

SIGHUP
    [Tags]    no-windows
    Send Signal To Process    SIGHUP

SIGTERM
    [Tags]    no-windows
    Send Signal To Process    SIGTERM

*** Keywords ***
Start Server
    [Arguments]    @{args}
    Start And Import Remote Library    Basics.py    ${TEST NAME}    @{args}
    Server Should Be Started

Server Should Be Started
    Run Keyword    ${TEST NAME}.Passing

Server Should Be Stopped
    Server Should Be Stopped And Correct Messages Logged
    Run Keyword And Expect Error    Connection to remote server broken: *
    ...    Server Should Be Started
    [Teardown]    Run Keyword And Ignore Error    ${TEST NAME}.Stop Remote Server
