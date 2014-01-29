*** Settings ***
Resource          resource.robot
Test Setup        Start Server
Test Teardown     Server Should Be Stopped

*** Test Cases ***
Stop Remote Server
    Stop Remote Server

SIGINT
    Send Signal To Process    SIGINT

SIGHUP
    Send Signal To Process    SIGHUP

SIGTERM
    Send Signal To Process    SIGTERM

*** Keywords ***
Start Server
    Start And Import Remote Library    basics.py    ${TEST NAME}
    Server Should Be Started

Server Should Be Started
    Run Keyword    ${TEST NAME}.Passing

Server Should Be Stopped
    Server Should Be Stopped And Correct Messages Logged
    Run Keyword And Expect Error    Connection to remote server broken: *
    ...    Server Should Be Started
    [Teardown]    Run Keyword And Ignore Error    ${TEST NAME}.Stop Remote Server
