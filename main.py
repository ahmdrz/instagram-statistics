#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from instagram import instagram, utils
import os
import json
import jinja2
import tempfile
import time
import io
import webbrowser
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-u", "--username", required=True,
                help="Instagram username")
ap.add_argument("-p", "--password", required=True,
                help="Instagram password")
ap.add_argument("-t", "--template", default="basic",
                help="Template name, name of file in templates directory")
args = vars(ap.parse_args())

dir_path = os.path.dirname(os.path.realpath(__file__))
template_dir = os.path.join(dir_path, "templates")
template = os.path.join(template_dir, args["template"] + ".tpl")

if not os.path.exists(template):
    print " - There is no template file named " + args["template"]
    sys.exit(1)

data_storage = {"likers": {}, "followers": {}, "followings": {}}
last_data_storage = data_storage
exist_last_data_storage = False
file_name = args["username"] + ".json"

if os.path.exists(file_name):
    print " - Opening last result of application ({})...".format(file_name)
    exist_last_data_storage = True
    with open(file_name, 'r') as handler:
        last_data_storage = json.load(handler)
    print " - Done !"

print " ~ Connecting to Instagram"
connection = instagram.Instagram(args["username"], args["password"])
if not connection.login():
    print "Login failed"
    sys.exit(2)
print " ~ Connected."

print " ~ Sending request to Instagram , fetching your feeds"
next_max_id = ''
result = connection.user_feed(connection.username_id)
feeds = []
feeds.extend(result["items"])
while result["more_available"]:
    next_max_id = result["next_max_id"]
    result = connection.user_feed(connection.username_id, max_id=next_max_id)
    feeds.extend(result["items"])
print " ~ {} items fetched from Instagram.".format(len(feeds))

for feed in []:
    print " - Scanning media {} ...".format(feed["id"])
    likers = connection.media_likers(feed["id"])
    for user in likers["users"]:
        username = user["username"]
        if username not in data_storage["likers"]:
            data = {"count": 1, "name": user["full_name"], "username": username}
            data_storage["likers"][username] = data
        else:
            data_storage["likers"][username]["count"] += 1
    time.sleep(1)  # wait one second for instagram rate limiter !
    print " - Media scanned, number of user scanned is {}.".format(len(likers["users"]))

    data_storage["likers"] = sorted(data_storage["likers"].values(), key=lambda x: x["count"], reverse=True)

print " ~ Sending request to Instagram , fetching followers"
next_max_id = ''
result = connection.followers(connection.username_id)
utils.list_to_dict(data_storage["followers"], result["users"], "username")
while result["big_list"]:
    next_max_id = result["next_max_id"]
    result = connection.followers(connection.username_id, max_id=next_max_id)
    time.sleep(1)  # wait one second for instagram rate limiter !
    utils.list_to_dict(data_storage["followers"], result["users"], "username")
print " ~ {} items fetched from Instagram.".format(len(data_storage["followers"]))

print " ~ Sending request to Instagram , fetching followings"
next_max_id = ''
result = connection.followings(connection.username_id)
utils.list_to_dict(data_storage["followings"], result["users"], "username")
while result["big_list"]:
    next_max_id = result["next_max_id"]
    result = connection.followers(connection.username_id, max_id=next_max_id)
    time.sleep(1)  # wait one second for instagram rate limiter !
    utils.list_to_dict(data_storage["followings"], result["users"], "username")
print " ~ {} items fetched from Instagram.".format(len(data_storage["followings"]))

with open(file_name, 'w') as outfile:
    print " - Saving result of application ({}) ...".format(file_name)
    json.dump(data_storage, outfile)
    print " - Data in {} is about your privacy ! Please note.".format(file_name)

never_liked = []
fans = {}
for follower in data_storage["followers"]:
    if follower not in data_storage["followings"]:
        fans[follower] = data_storage["followers"][follower]

    if follower not in data_storage["likers"]:
        never_liked.append(follower)

not_followed_back = {}
for following in data_storage["followings"]:
    if following not in data_storage["followers"]:
        not_followed_back[following] = data_storage["followings"][following]

new_followers = []
new_followings = []
if exist_last_data_storage:
    new_followers = list(set(data_storage["followers"]).difference(last_data_storage["followers"]))
    new_followings = list(set(data_storage["followings"]).difference(last_data_storage["followings"]))

temporary_directory = tempfile.mktemp()
os.mkdir(temporary_directory)

with open(template, 'r') as template_reader:
    tpl = jinja2.Template(template_reader.read())
    output = tpl.render(user_info=connection.logged_in_user,
                        followings=data_storage["followings"],
                        followers=data_storage["followers"],
                        new_followers=new_followers,
                        new_followings=new_followings,
                        likers=data_storage["likers"],
                        never_liked=never_liked)

    print " ~ Creating HTML file"
    temporary_file = os.path.join(temporary_directory, 'output.html')
    with io.open(temporary_file, 'w', encoding='utf8') as f:
        f.write(output)

    webbrowser.open_new_tab(temporary_file)

print " ~ Logging out ..."
connection.logout()
