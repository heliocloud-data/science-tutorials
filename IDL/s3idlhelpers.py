#!/usr/bin/env python

""" Script to copy S3 file to a temporary local copye
 Given an s3:// location,
 converts to bucket and filename (key),
 copies it over as a temp file
 and returns the new temp file name.

 Also has a 'purge' command that deletes the temp file
 (can be called with the temp file name or original s3://)

 temp files are stored flat in the given tempdir
 (default for tempdir is './s3temp')
 
 Antunes, sandy.antunes@jhuapl.edu, Mar 2022
"""

import os
import sys
import re
import boto3

def s3tempdir(tempdir):
    # if not given one, look for env var S3TEMP, otherwise default is './s3temp'
    # makes tempdir if it can, if not defaults to current '.' directory
    if tempdir == None: tempdir=os.environ.get('S3TEMP')
    if tempdir == None: tempdir = "./s3temp"
    if not os.path.isdir(tempdir):
        try:
            os.mkdir(tempdir)
        except:
            print("Could not make tempdir ",tempdir,", using current directory")
            tempdir="."
    #print('debug, tempdir is ',tempdir)
    return(tempdir)

def s3parse(s3url):
    surl=re.sub('^s3://','',s3url)
    ele=surl.split('/')
    mybucket=ele[0]
    mykey='/'.join(ele[1:])
    myfile=os.path.basename(mykey)
    return(mybucket,mykey,myfile)
    
def s3tempsync(s3url,tempdir=None):
    tempdir=s3tempdir(tempdir)
    s3 = boto3.resource('s3')
    (mybucket,mykey,myfile)=s3parse(s3url)
    localfile = tempdir + '/' + myfile
    s3.Bucket(mybucket).download_file(mykey,localfile)
    print(localfile) # here to support IDL spawn
    return(localfile)

# note uses similar syntax as s3tempcopy
def s3temppurge(s3url,tempdir=None):
    tempdir=s3tempdir(tempdir)
    print("checking ",s3url)
    myfile=os.path.basename(s3url)
    localfile = tempdir + '/' + myfile
    if os.path.exists(localfile):
        print("Deleting temp file ",localfile)
        os.remove(localfile)
    else:
        print("File ",localfile, " does not exist, no deletion done.")

if __name__ == '__main__':
    try:
        action=sys.argv[1]
        s3url=sys.argv[2]
    except:
        print("Did not provide <action> <s3url_or_fname>")

    try:
        tempdir=sys.argv[3]
    except:
        tempdir=None # use default
    
    if action == 'del':
        s3temppurge(s3url,tempdir)
    elif action == 'sync':
        s3tempsync(s3url,tempdir)
