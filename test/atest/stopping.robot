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
    Start And Import Remote Library    Basics.py    ${TEST NAME}
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
   [Documentation]  Send signal to server, not to possible wrapper (e.g. jython) running it.
   ${pid}=   Run Keyword    ${TEST NAME}.Get PID
   Evaluate   os.kill(${pid}, signal.${signal})   os,signal
