*** Settings ***
Documentation     These tests actually test the Remote library more than the remote server.
Resource          resource.robot
Variables         arguments.py
Suite Setup       Start And Import Remote Library    arguments.py
Suite Teardown    Stop Remote Library
Test Template     Argument Should Be Correct

*** Test Cases ***
Empty string
    ''

ASCII string
    u'Hello, world!'
    'Hello, world!'

Non-ASCII string
    u'Hyv\\xe4'
    u'\\u2603'

Binary
    '\\x00\\x01'

Integer
    42
    -1
    0

Float
    3.14
    -0.1e10
    0.0

Boolean
    True
    False

None
    [Documentation]    None is converted to empty string because it is not supported by all XML-RPC versions.
    None    ''

Custom object
    [Documentation]    Arbitrary objects cannot be transferred over XML-RPC and thus only their string presentation is used
    MyObject()            '<MyObject>'
    MyObject('xxx')       'xxx'
    MyObject(u'\\xe4')    u'\\xe4'
    MyObject('\\x00')     '\\x00'

List
    \[]
    \['Hei', u'\\xe4iti', 63, True]
    \[None]    ['']
    \[[], [1, 2], [[True], False], 'xxx']

List-like
    [Documentation]    Tuples etc. are converted to lists
    ()    []
    ('Hei', u'\\xe4iti', 63, (), None)    ['Hei', u'\\xe4iti', 63, [], '']
    set(['hello'])    ['hello']
    xrange(5)    [0, 1, 2, 3, 4]

Dictionary
    {}
    {'a': 1, u'\\xe4': 2, 'nested': {'k': 'v'}}
    {'x': None}    {'x': ''}

Dictionary With Non-String Keys
    [Documentation]    XML-RPC supports only strings as keys so must convert them
    {42: 42, True: False, None: None}    {'42': 42, 'True': False, '': ''}

*** Keywords ***
Argument Should Be Correct
     [Arguments]    ${argument}    ${expected}=
     ${expected} =    Set Variable If    """${expected}"""
     ...    ${expected}    ${argument}
     ${ns} =    Create Dictionary    MyObject=${MyObject}
     ${argument} =    Evaluate    ${argument}    namespace=${ns}
     Remote.Argument Should Be Correct    ${argument}    ${expected}
