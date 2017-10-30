#! /usr/bin/python

from socket import *
import time
import struct
import os,multiprocessing

video_fmt = '>I32s2I'
HOST = '192.168.1.180'  
client = '192.168.1.91'
PORT = 6000
BUFSIZE = 40960
ADDR = (HOST, PORT)  

def test_6000_main(ip,port,index):
    print "create main fork %d" % index
    tcpClientSock = socket(AF_INET, SOCK_STREAM)  
    tcpClientSock.connect(ADDR)  
    nego = struct.pack(video_fmt,0,ip,port,0)
    tcpClientSock.send(nego)
    while True:  
        data = tcpClientSock.recv(BUFSIZE)  
        if not data:  
            break  
    tcpClientSock.close()  

def test_6000_sub(ip,port,index):
    print "create sub fork %d" % index
    tcpClientSock = socket(AF_INET, SOCK_STREAM)  
    tcpClientSock.connect(ADDR)  
    nego = struct.pack(video_fmt,0,ip,port,1)
    tcpClientSock.send(nego)
    while True:  
        data = tcpClientSock.recv(BUFSIZE)  
        if not data:  
            break  
    tcpClientSock.close()  

if __name__ == '__main__':
    num_job = range(20)
    jobs = []
    while True:
        for i in num_job:
            #time.sleep(0.5)
            p_main = multiprocessing.Process(target=test_6000_main,args=(client,PORT,i))
            jobs.append(p_main)
            p_main.start()
            p_sub = multiprocessing.Process(target=test_6000_sub,args=(client,PORT,i))
            jobs.append(p_sub)
            p_sub.start()
        for i in num_job:
            print "running",jobs[i].is_alive()

        time.sleep(600)

        for i in num_job:
            jobs[i].terminate()
            jobs[i].join()
            print "dead",jobs[i].is_alive()
        print "wait 5 seconds"
        time.sleep(10)
