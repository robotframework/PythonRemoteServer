*** Settings ***
Resource          resource.robot
Test Setup        Start Server
Test Teardown     Server Should Be Stopped

*** Test Cases ***
Stop Remote Server
    Stop Remote Server

SIGINT
    Skip On Windows
    Send Signal To Remote Server    SIGINT

SIGHUP
    Skip On Windows
    Send Signal To Remote Server    SIGHUP

SIGTERM
    Skip On Windows
    Send Signal To Remote Server    SIGTERM

*** Keywords ***
Start Server
    Start And Import Remote Library    basics.py    ${TEST NAME}
    Server Should Be Started

Server Should Be Started
    Run Keyword    ${TEST NAME}.Passing

Server Should Be Stopped
    Return From Keyword If    "skip" in @{TEST TAGS}
    Server Should Be Stopped And Correct Messages Logged
    Run Keyword And Expect Error    Connection to remote server broken: *
    ...    Server Should Be Started
    [Teardown]    Run Keyword And Ignore Error    ${TEST NAME}.Stop Remote Server

Skip On Windows
    Run Keyword If    "${:}" == ";"    Fail    Skipped on Windows    skip

Send Signal To Remote Server
   [Arguments]     ${signal}
   ${process pid}=   Run Keyword    ${TEST NAME}.get_pid
   Evaluate   os.kill(${process pid}, signal.${signal})   os,signal