#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from insta import Instagram
import os
import json
import pystache
import io
import webbrowser

if len(sys.argv) < 3:
    print "Incorrect input args, use main.py <username> <password>"
    sys.exit(1)

username = sys.argv[1]
password = sys.argv[2]

print " ~ Connecting to Instagram"
insta = Instagram(username, password)
if insta.login() == False:
    print "Login failed"
    sys.exit(2)

print " ~ Sending request to Instagram , fetching your feeds"
temp = insta.getTotalUserFeed(insta.username_id)
likedUsers = {}
for item in temp:
    insta.getMediaLikers(item["id"])
    test = insta.LastJson["users"]
    for user in test:
        if user["username"] not in likedUsers:
            data = {}
            data["count"] = 1
            data["name"] = user["full_name"]
            data["image"] = user["profile_pic_url"]
            data["username"] = user["username"]
            likedUsers[user["username"]] = data
        else:
            likedUsers[user["username"]]["count"] += 1

print " ~ Sending request to Instagram , fetching followers"
followers = insta.getTotalFollowers(insta.username_id)
print " ~ Sending request to Instagram , fetching followings"
followings = insta.getTotalFollowings(insta.username_id)

print " ~ Processing..."
fans = []
for fr in followers:
    flag = True
    for fg in followings:
        if fg["pk"] == fr["pk"]:
            flag = False
            break
    if flag:
        fans.append(fr)

notfollowedback = []
for fr in followings:
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
        for fr in followers:
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

neverLiked = []
for follower in followers:
    if follower["username"] not in likedUsers:
        neverLiked.append(follower)

file = open('template.tpl', 'r')
html = file.readlines()
tpl = ''
for line in html:
    tpl = tpl + " " + line

likedUsers = sorted(likedUsers.values(),
                    key=lambda x: x["count"], reverse=True)

if len(followers) > 10:
    followers = followers[:10]
if len(followings) > 10:
    followings = followings[:10]
if len(fans) > 10:
    fans = fans[:10]
if len(notfollowedback) > 10:
    notfollowedback = notfollowedback[:10]

data = {
    "followers": followers,
    "followings": followings,
    "username": insta.username,
    "fans": fans,
    "notback": notfollowedback,
    "newfollowers": newfollowers,
    "newfollowings": newfollowings,
    "bestlikers": likedUsers[:10],
    "badlikers": likedUsers[len(likedUsers) - 10:],
    "neverliked": neverLiked[0:10]
}

print " ~ Creating output.html"
output = pystache.render(tpl, data)
with io.open('output.html', 'w', encoding='utf8') as f:
    f.write(output)
    
webbrowser.open_new_tab('output.html')
