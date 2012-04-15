import sys
import os
from wordpress_xmlrpc.methods.posts import NewPost
from wordpress_xmlrpc.base import Client
from wordpress_xmlrpc.wordpress import WordPressPost

class PostCreator():

    def __init__(self):
        homeDirectory = os.getenv("HOME")
        sys.path.append(r"" + homeDirectory + "/ScraperBot" + "")

    def enter_WP_user(self):
        user = raw_input ("WP user >> ")
        return user

    def enter_WP_password(self):
        password = raw_input ("WP password >> ")
        return password

    def createPost(self, title, thumbnail, iframe, videoduration, categories, tags):
        #user_from_keyboard = enter_WP_user()
        #password_from_keyboard = enter_WP_password()
        print "WP creating post ..."
        wp = Client('http://www.hottestporn4u.com/xmlrpc.php', 'pornmaster', 'pornmasterpiece')
        post0 = WordPressPost()
        post0.title = title
        print "WP title: " + post0.title
        post0.description = iframe + "<br><img src=" + thumbnail + " alt=" + title + "><br>Duration " + videoduration
        print "WP description: " + post0.description
        post0.tags = tags
        print "WP categories: " + post0.tags
        post0.categories = categories
        print "WP tags: " + post0.categories
        post0.date_created = '20120415T12:11:59'
        print "WP Date: " + post0.date_created
        wp.call(NewPost(post0, True))