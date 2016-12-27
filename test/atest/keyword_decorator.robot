*** Settings ***
Resource          resource.robot
Suite Setup       Start And Import Remote Library    keyword_decorator.py
Suite Teardown    Stop Remote Library

*** Test Cases ***
Keyword with 2 arguments
    Add 7 Copies Of Coffee To Cart

When embedded name is empty keyword is still callable
    Embedded name empty

Tags added with keyword decorator
    login  admin
