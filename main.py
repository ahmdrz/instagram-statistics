# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 00:21:45 2016

@author: aiden
"""

import sys
from insta import Instagram
import os
import json
import pystache
import io

if len(sys.argv) < 3 :
    print "Incorrect input args, use insta.py <username> <password>"    

username = sys.argv[1]
password = sys.argv[2]

insta = Instagram(username,password)
insta.login()
followers = insta.getTotalFollowers(insta.username_id)
followings = insta.getTotalFollowings(insta.username_id)

fans = []
for fr in followers :
    flag = True
    for fg in followings:
        if fg["pk"] == fr["pk"]:
            flag = False
            break
    if flag:
        fans.append(fr)
        
notfollowedback = []
for fr in  followings:
    flag = True
    for fg in followers:
        if fg["pk"] == fr["pk"]:
            flag = False
            break
    if flag:
        notfollowedback.append(fr)

newfollowers = []
if os.path.exists('followers.json'):
    with open('followers.json') as data_file:    
        oldfollowers = json.load(data_file)            
        for fr in  followers:
            flag = True
            for fg in oldfollowers:
                if fg["pk"] == fr["pk"]:
                    flag = False
                    break
            if flag:
                newfollowers.append(fr)   

newfollowings = []
if os.path.exists('followings.json'):
    with open('followings.json') as data_file:    
        oldfollowings = json.load(data_file)    
        for fr in followings:
            flag = True
            for fg in oldfollowings:
                if fg["pk"] == fr["pk"]:
                    flag = False
                    break
            if flag:
                newfollowings.append(fr)  
 
        
with open('followers.json', 'w') as outfile:
    json.dump(followers, outfile)

with open('followings.json', 'w') as outfile:
    json.dump(followings, outfile)

file = open('template.tpl', 'r')
html = file.readlines()
tpl = ''
for line in html :
    tpl = tpl + " " + line

data = {
    "followers":followers[0:5],
    "followings":followings[0:5],
    "username":insta.username,
    "fans":fans[0:5],
    "notback":notfollowedback[0:5],
    "newfollowers":newfollowers,
    "newfollowings":newfollowings
}

output = pystache.render(tpl,data)
with io.open('output.html','w',encoding='utf8') as f:
    f.write(output) 