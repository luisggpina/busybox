#!/usr/bin/python2

import argparse

import os
import os.path

from os import listdir
from os.path import isfile, join, abspath
from sys import argv
from shutil import move

from subprocess import call

busyboxesDir = abspath(join(os.pardir,'compilers'))
busyboxes    = [f for f in listdir(busyboxesDir) if isfile(join(busyboxesDir, f, 'busybox'))]

parser = argparse.ArgumentParser(description='Run BusyBox tests')

parser.add_argument('-vx',
        action='store_true',
        help='Run with Varan')

parser.add_argument('bbs',
        choices=busyboxes,
        nargs='+',
        help='BusyBoxes to use')

argLines = ' '.join(argv[1:]).split('--')

args = parser.parse_args(argLines[0].split())

if args.vx:
    logFileName = 'vx_' + '_'.join(args.bbs) + '.log'
else:
    logFileName = args.bbs[0] + '.log'


if isfile(logFileName):
    move(logFileName, logFileName + '.old')

logFile = open(logFileName, 'w')

command = './runtest'
if len(argLines) > 1:
    command = command + argLines[1]

env = os.environ.copy()
bbs = map((lambda bb: join(busyboxesDir, bb,'busybox')), args.bbs)

if args.vx:
    env['VX']  = '1'
    env['BBS'] = ' '.join(bbs)
else:
    env['VX']  = '0'
    env['BBS'] = bbs[0]

env['BB']  = bbs[0]

call(command,
        stdout=logFile,
        stderr=logFile,
        env=env,
        shell=True)
