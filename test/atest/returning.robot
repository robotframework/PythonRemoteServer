*** Settings ***
Resource          resource.robot
Suite Setup       Start And Import Remote Library    returning.py
Suite Teardown    Stop Remote Library    test logging='ipy' not in '${INTERPRETER}'
Test Template     Return Value Should Be

*** Test Cases ***
Empty string
    u''
    ''

ASCII string
    u'Hello, world!'
    b'Hello, world!'

Non-ASCII String
    u'Hyv\\xe4'
    u'\\u2603'

Non-ASCII Bytes
    b'Hyv\\xe4'
    b'\\x80\\xff'

Binary
    b'\\x00\\x01\\x02'
    u'\\x00\\x01\\x02'    b'\\x00\\x01\\x02'
    b'\\x00\\xe4\\xff'

Unrepresentable binary
    [Documentation]    FAIL REGEXP: ValueError: Cannot represent (u'\\x00\\xe4\\xff'|'\x00дя') as binary.
    u'\\x00\\xe4\\xff'

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
    MyObject()    '<MyObject>'
    MyObject('xxx')    'xxx'

Custom object with non-ASCII representation
    MyObject(u'hyv\\xe4')    u'hyv\\xe4'

Custom object with binary representation
    MyObject('\\x00\\x01')    b'\\x00\\x01'

List
    \[]
    \['Hei', u'\\xe4iti', 63, True, '\\x00']    ['Hei', u'\\xe4iti', 63, True, b'\\x00']
    \[None, MyObject('xxx'), MyObject(u'\\xe4')]    ['', 'xxx', u'\\xe4']
    \[[0, [[]]], [1, 2], [[True], False], 'xxx']

List-like
    [Documentation]    Tuples etc. are converted to lists
    ()    []
    ('Hei', u'\\xe4iti', 63, (), None)    ['Hei', u'\\xe4iti', 63, [], '']
    set(['hello'])    ['hello']
    range(5)    [0, 1, 2, 3, 4]

Dictionary
    {}
    {'a': 1, u'b': 2, 'nested': {'k': 'v'}}
    {'x': None}    {'x': ''}

Dictionary with non-ASCII keys and values
    {u'\\xe4': u'\\xe4', u'\\u2603': u'\\u2603'}

Dictionary with non-ASCII byte keys is not supported
    [Documentation]  FAIL REGEXP: TypeError: unhashable .*
    {b'\\xe4': 'value'}

Dictionary with non-ASCII byte values
    {'key': b'\\xe4'}

Dictionary with binary keys is not supported
    [Documentation]  FAIL REGEXP: TypeError: unhashable .*
    {'\\x00': 'value'}

Dictionary with binary values
    {'0': b'\\x00', '1': b'\\x01'}

Dictionary with non-string keys and values
    [Documentation]    XML-RPC supports only strings as keys so must convert them
    {42: 42, True: False, None: None}    {'42': 42, 'True': False, '': ''}
    {MyObject('key'): MyObject('value')}    {'key': 'value'}
    {MyObject(u'\\xe4'): MyObject(u'\\xe4')}    {u'\\xe4': u'\\xe4'}

Mapping
    MyMapping()    {}
    MyMapping({'a': 1, 2: 'b', u'\\xe4': '\\x00'})    {'a': 1, '2': 'b', u'\\xe4': b'\\x00'}
    MyMapping({'x': MyMapping(), 'y': None})    {'x': {}, 'y': ''}

*** Keywords ***
Return Value Should Be
    [Arguments]    ${value}    ${expected}=
    ${actual} =    Return Evaluated    ${value}
    ${expected} =    Set Variable If    """${expected}"""
    ...    ${expected}    ${value}
    ${expected} =    Evaluate    ${expected}
    Should Be Equal    ${actual}    ${expected}
