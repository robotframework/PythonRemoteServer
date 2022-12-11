*** Settings ***
Library              OperatingSystem
Library              Process
Library              Collections

*** Variables ***
${INTERPRETER}       python
${SERVER TIMEOUT}    30 seconds

*** Keywords ***
Start And Import Remote Library
    [Arguments]    ${library}    ${name}=Remote    @{args}
    Set Pythonpath
    ${port} =    Start Remote Library    ${library}    args=${args}
    Import Library    Remote    http://127.0.0.1:${port}    WITH NAME    ${name}
    Set Suite Variable    ${ACTIVE PORT}    ${port}
    Set Log Level    DEBUG

Start Remote Library
    [Arguments]    ${library}    ${port}=0    ${args}=@{EMPTY}
    @{interpreter} =    Split Command Line    ${INTERPRETER}
    ${library} =        Normalize Path        ${CURDIR}/../libs/${library}
    ${port file} =      Normalize Path        ${CURDIR}/../results/server_port.txt
    ${output} =         Normalize Path        ${CURDIR}/../results/server_output.txt
    Start Process    @{interpreter}    ${library}    ${port}    ${port file}
    ...    @{args}    alias=${library}    stdout=${output}    stderr=STDOUT
    TRY
        Wait Until Created    ${port file}    timeout=${SERVER TIMEOUT}
    EXCEPT
        ${result} =    Wait For Process    timeout=10s    on_timeout=terminate
        Fail    Starting remote server failed:\n${result.stdout}
    END
    ${port} =    Get File    ${port file}
    RETURN    ${port}

Set Pythonpath
    ${src} =    Normalize Path    ${CURDIR}/../../src
    Set Environment Variable    PYTHONPATH    ${src}
    Set Environment Variable    JYTHONPATH    ${src}
    Set Environment Variable    IRONPYTHONPATH    ${src}

Stop Remote Library
    [Arguments]    ${test logging}=True
    Stop Remote Server
    Server Should Be Stopped And Correct Messages Logged    ${test logging}

Server Should Be Stopped And Correct Messages Logged
    [Arguments]    ${test logging}=True
    ${result} =    Wait For Process    timeout=10s    on_timeout=terminate
    ${expected} =    Catenate    SEPARATOR=\n
    ...    Robot Framework remote server at 127.0.0.1:${ACTIVE PORT} started.
    ...    Robot Framework remote server at 127.0.0.1:${ACTIVE PORT} stopped.
    IF    ${test logging}
        Should Be Equal    ${result.stdout}    ${expected}
    END
    Should Be Equal    ${result.rc}    ${0}
