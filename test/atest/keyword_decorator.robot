*** Settings ***
Resource          resource.robot
Suite Setup       Start And Import Remote Library    KeywordDecorator.py
Suite Teardown    Stop Remote Library

*** Test Cases ***
Custom name
    [Documentation]    FAIL Keyword 'Remote.Custom Name' expected 1 argument, got 3.
    Custom name    arg
    Custom name    too    many    args

Embedded arguments
    Result of 1 + 2 should be 3
    Result of (1+2) * 3 should be 9

No custom name
    Just marker

Tags
    Tags
    Tags with doc (and custom name)
