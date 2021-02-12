#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

def hi_file(name):
    f=open('/home/ubuntu/hi.txt','w')
    f.write('Hello '+name+'\n')
    f.close()

if len(sys.argv) > 1:
    name = sys.argv[1]
else:
    print('Usage: python test.py <name>')
    sys.exit(1)

hi_file(name)
