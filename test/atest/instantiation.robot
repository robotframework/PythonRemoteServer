*** Settings ***
Documentation     Testing the feature where instantiation of both a
...               single library or a list of libraries must be
...               possible.
Resource          resource.robot

*** Test Cases ***
A single library can be loaded
    [Setup]       Start And Import Remote Library    Basics.py    Remote1
    [Teardown]    Remote1.Stop Remote Server
    Passing

Multiple libraries can be loaded
    [Setup]       Start And Import Remote Library    MultiLib.py    Remote3
    [Teardown]    Remote3.Stop Remote Server
    Keyword from first library
    Keyword from second library
    Keyword from third library

Libraries can be bulk-loaded
    [Setup]       Start And Import Remote Library    Loading.py    Bulk    BulkMode
    [Teardown]    Bulk.Stop Remote Server
    Bulk.Basic
    Bulk.Complex    positional    named=Monty    free=Python

Libraries can be loaded per keyword
    [Setup]       Start And Import Remote Library    Loading.py    Single    SingleMode
    [Teardown]    Single.Stop Remote Server
    Single.Basic
    Single.Complex    positional    named=Monty    free=Python
