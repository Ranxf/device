#!/usr/bin/env python

def tr(srcstr,dststr,string):
    if len(srcstr) != len(dststr):
        print("translate string length error!")
    trmap = {}
    for i in range(0,len(srcstr)):
        trmap[srcstr[i]] = dststr[i]
    trstr=''
    for i in range(0,len(string)):
        if string[i] in srcstr:
            trstr=trstr+trmap[srcstr[i]]
        else:
            trstr=trstr+string[i]
    string = trstr
    return string


print(tr('abc','def','abcdefg'))
