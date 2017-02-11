#!/usr/bin/env python
import urllib2
import re
import argparse
import sys
import os
import os.path
import subprocess
import shutil


URL_PATTERN="https://datatracker.ietf.org/iesg/agenda/telechat-%s-docs.tgz"

def debug(msg):
    global args
    if args.verbose:
        print msg

def err(msg):
    print "Error: %s"%msg
    
def download_package(date):
    u = urllib2.urlopen(URL_PATTERN%date)
    fn = "%s.tgz"%date
    f = open(fn, "w")
    f.write(u.read())
    f.close()
    # unpack
    subprocess.check_call(["tar", "xf", fn])
    os.remove(fn)

def swap_xtn(f, ext):
    return os.path.splitext(f)[0] + "." + ext
    
def pdfize_cwd():
    files = os.listdir(".")
    for f in files:
        m = re.match("(draft|charter)-[^\.]*.txt", f)
        if m is None:
            debug("Skipping %s"%f)
            continue
        else:
            debug("PDFizing %s"%f)
            subprocess.check_call(["enscript","--margins", "76::76:", "-B", "-q", "-p",
                                   swap_xtn(f, "ps"), f])
            os.remove(f)
            subprocess.check_call(["ps2pdf", swap_xtn(f, "ps"), swap_xtn(f, "pdf")])
            os.remove(swap_xtn(f, "ps"))

        
def do_date(date):
    #Safety check
    m = re.match("\d\d\d\d-\d\d-\d\d", date)
    if m is None:
        err("Invalid date format")
        sys.exit(1)

    shutil.rmtree(date)
    os.mkdir(date)
    os.chdir(date)
    download_package(date)
    pdfize_cwd()
    os.chdir("..")
    
parser = argparse.ArgumentParser(description='fetch telechat package')
parser.add_argument('--verbose', dest='verbose', action='store_true')
parser.add_argument('dates', nargs='+', help='date1 date2...')

args = parser.parse_args()
for d in args.dates:
    do_date(d)


    

    
