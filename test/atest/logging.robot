*** Settings ***
Resource          resource.robot
Suite Setup       Start And Import Remote Library    Logging.py
Suite Teardown    Stop Remote Library

*** Test Cases ***
Simple message
    [Documentation]    LOG 1 INFO Hello, world!
    Logging    Hello, world!

Multiline message
    [Documentation]    LOG 1 INFO Can\n\haz\nmultiple\n\lines?\n\n\nYezzz!!!\n
    Logging    Can\n\haz\nmultiple\n\lines?\n\n\nYezzz!!!\n

Non-ASCII message
    [Documentation]    LOG 1 INFO Hyvä \u2603
    Logging    Hyvä \u2603

Non-ASCII bytes
    [Documentation]    Different message logged in (py2|py3|ipy).
    ...    LOG 1 INFO REGEXP: (Hyv\\\\xe4|b'Hyv\\\\xe4'|Hyvä)
    Logging    b'Hyv\\xe4'    evaluate=yes

Binary Unicode
    [Documentation]    LOG 1 INFO ++
    Logging    '\\x00+\\x01+\\x02'    evaluate=yes

Log levels
    [Documentation]
    ...    LOG 1 DEBUG Debug message
    ...    LOG 2 INFO Information message
    ...    LOG 3 WARN Warning message
    Logging    Debug message    DEBUG
    Logging    Information message    INFO
    Logging    Warning message    WARN

Multiple messages with different levels
    [Documentation]
    ...    LOG 1:1 INFO Info message
    ...    LOG 1:2 DEBUG Debug message
    ...    LOG 1:3 INFO Second info\n this time with two lines
    ...    LOG 1:4 INFO Third info
    ...    LOG 1:5 WARN Warning
    Multiple Messages With Different Levels

Logging and failing
    [Documentation]  FAIL Too slow
    ...    LOG 1:1 INFO This keyword will fail!
    ...    LOG 1:2 WARN Run for your lives!!
    ...    LOG 1:3 FAIL Too slow
    ...    LOG 1:4 DEBUG REGEXP: Traceback.*
    Logging And Failing

Logging and returning
    [Documentation]
    ...    LOG 1:1 INFO This is logged
    ...    LOG 1:2 INFO \${ret} = This is returned
    ...    LOG 3:1 INFO This keyword returns nothing
    ...    LOG 3:2 INFO \${ret} =
    ${ret} =    Logging and returning    This is logged    This is returned
    Should Be Equal    ${ret}    This is returned
    ${ret} =    Logging    This keyword returns nothing
    Should Be Equal    ${ret}    ${EMPTY}

Logging through stderr
    [Documentation]
    ...    LOG 1 INFO Hello, stderr!
    ...    LOG 2 DEBUG Hyvä \u2603
    ...    LOG 3 INFO 0\n1
    Logging    Hello, stderr!    stderr=yes
    Logging    Hyvä \u2603    level=DEBUG    stderr=yes
    Logging    '0\\x00\\n1\\x01'    evaluate=yes    stderr=yes

Logging both through stdout and stderr
    [Documentation]
    ...    LOG 1:1 INFO stdout
    ...    LOG 1:2 INFO stderr
    ...    LOG 2:1 DEBUG stdout-continue
    ...    LOG 2:2 INFO stderr
    ...    LOG 3:1 INFO o\no2
    ...    LOG 3:2 DEBUG e
    ...    LOG 3:3 INFO e2
    Logging both to stdout and stderr    stdout    stderr
    Logging both to stdout and stderr    *DEBUG* stdout    stderr    -continue
    Logging both to stdout and stderr    o\n    *DEBUG* e\n    o2    *INFO* e2
