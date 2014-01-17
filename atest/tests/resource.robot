*** Settings ***
Library           OperatingSystem
Library           Process
Library           Collections

*** Variables ***
${INTERPRETER}    python

*** Keywords ***
Start And Import Remote Library
    [Arguments]    ${library}
    Set Pythonpath
    ${port} =    Start Remote Library    ${library}
    Import Library    Remote    http://127.0.0.1:${port}
    Set Suite Variable    ${ACTIVE PORT}    ${port}
    Set Log Level    DEBUG

Start Remote Library
    [Arguments]    ${library}    ${port}=0
    ${library} =    Normalize Path    ${CURDIR}/../libs/${library}
    ${port file} =    Normalize Path    ${CURDIR}/../results/server_port.txt
    ${output} =    Normalize Path    ${CURDIR}/../results/server_output.txt
    Start Process    ${INTERPRETER}    ${library}    ${port}    ${port file}
    ...    alias=${library}    stdout=${output}    stderr=STDOUT
    Run Keyword And Return    Read Port File    ${port file}

Read Port File
    [Arguments]    ${path}
    Wait Until Created    ${path}    timeout=30s
    Run Keyword And Return   Get File    ${path}
    [Teardown]    Remove File    ${path}

Set Pythonpath
    ${src} =    Normalize Path    ${CURDIR}/../../src
    Set Environment Variable    PYTHONPATH    ${src}
    Set Environment Variable    JYTHONPATH    ${src}
    Set Environment Variable    IRONPYTHONPATH    ${src}

Stop Remote Library
    Stop Remote Server
    Server Should Be Stopped And Correct Messages Logged

Server Should Be Stopped And Correct Messages Logged
    ${result} =    Wait For Process    timeout=10s    on_timeout=terminate
    ${expected} =    Catenate    SEPARATOR=\n
    ...    Robot Framework remote server at 127.0.0.1:${ACTIVE PORT} starting.
    ...    Robot Framework remote server at 127.0.0.1:${ACTIVE PORT} stopping.
    Should Be Equal    ${result.stdout}    ${expected}
