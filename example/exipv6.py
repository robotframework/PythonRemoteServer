#!/usr/bin/env python
# example of how to get RobotRemtoteServer working with IPv6: set up socketserver.TTCPServer.addresse_family
# class variable before importing RobotRemoteServer. Then use IPv6 notation, rather than IPv4

import sys

import socketserver
import socket

socketserver.TCPServer.address_family = socket.AF_INET6
    
from robotremoteserver import RobotRemoteServer

from examplelibrary import ExampleLibrary

if __name__ == '__main__':
    # listen on any IPv6 address, including all IPv4 addresses on the host
    #RobotRemoteServer(ExampleLibrary(), host="::", *sys.argv[1:])
    # listen on local loopback interface
    #RobotRemoteServer(ExampleLibrary(), host="::1", *sys.argv[1:])
    # example encoding of IPv4 RFC1918 address as IPv6 address
    #RobotRemoteServer(ExampleLibrary(), host="::ffff:192.168.194.81", *sys.argv[1:])
    # IPv4 notation will fail
    #RobotRemoteServer(ExampleLibrary(), host="192.168.194.81", *sys.argv[1:])
    # listen on any IPv4 address
    RobotRemoteServer(ExampleLibrary(), host="::ffff:0.0.0.0", *sys.argv[1:])
