*** Settings ***
Library       Remote    http://${ADDRESS}:${PORT}

*** Variables ***
# localhost may be a suitable alias for the local IP stack loopback address
${ADDRESS}    localhost
# alternatively, use a protocol specific loopback address
# IPv6 loopback address
#${ADDRESS}    ::1
# IPv4 loopback address
#${ADDRESS}    127.0.0.1
${PORT}       8270

*** Test Cases ***
Count Items in Directory
    ${items1} =    Count Items In Directory    ${CURDIR}
    ${items2} =    Count Items In Directory    ${TEMPDIR}
    Log    ${items1} items in '${CURDIR}' and ${items2} items in '${TEMPDIR}'

Failing Example
    Strings Should Be Equal    Hello    Hello
    Strings Should Be Equal    not      equal
