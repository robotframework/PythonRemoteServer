#!/usr/bin/env python

import sys

import socketserver
import socket

socketserver.TCPServer.address_family = socket.AF_INET6
    
from robotremoteserver import RobotRemoteServer

from examplelibrary import ExampleLibrary

if __name__ == '__main__':
    #RobotRemoteServer(ExampleLibrary(), host="::", *sys.argv[1:])
    #RobotRemoteServer(ExampleLibrary(), host="::ffff:192.168.194.81", *sys.argv[1:])
    #RobotRemoteServer(ExampleLibrary(), host="192.168.194.81", *sys.argv[1:])
    RobotRemoteServer(ExampleLibrary(), host="::ffff:0.0.0.0", *sys.argv[1:])
