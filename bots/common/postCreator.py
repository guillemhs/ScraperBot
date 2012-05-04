import sys
import os
import urllib2
from wordpress_xmlrpc.base import Client
import xmlrpclib
import time
from wordpress_xmlrpc.wordpress import WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost



class PostCreator():

    def __init__(self):
        homeDirectory = os.getenv("HOME")
        sys.path.append(r"" + homeDirectory + "/ScraperBot" + "")

    def get_url_content(self, url):
        try:
            content = urllib2.urlopen(url)
            return content.read()
        except:
            print 'error! NOOOOOO!!!'

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
        wp = Client('http://localhost/wordpress/xmlrpc.php', 'pornmaster', 'pornmasterpiece')

        print "Client connected ..."
        # set to the path to your file
        file_url = thumbnail
        extension = file_url.split(".")
        leng = extension.__len__()
        extension = extension[leng - 1]
        if (extension == 'jpg'):
            xfileType = 'image/jpeg'
        elif(extension == 'png'):
            xfileType = 'image/png'
        elif(extension == 'bmp'):
            xfileType = 'image/bmp'

        file = self.get_url_content(file_url)
        file = xmlrpclib.Binary(file)
        server = xmlrpclib.Server('http://localhost/wordpress/xmlrpc.php')
        filename = str(time.strftime('%H:%M:%S'))
        mediarray = {'name':filename + '.' + extension,
                     'type':xfileType,
                     'bits':file,
                     'overwrite':'false'}
        xarr = ['1', 'pornmaster', 'pornmasterpiece', mediarray]
        result = server.wp.uploadFile(xarr)
        print result


        post0 = WordPressPost()
        post0.title = title
        print "WP title: " + post0.title
        post0.description = "<img src=" + thumbnail + " alt=" + title + "><br>" + iframe + "Duration " + videoduration
        print "WP description: " + post0.description
        post0.tags = tags
        print "WP categories: " + post0.tags
        post0.categories = categories
        print "WP tags: " + post0.categories
        post0.date_created = '20120503T12:11:59'
        print "WP Date: " + post0.date_created
        wp.call(NewPost(post0, True))