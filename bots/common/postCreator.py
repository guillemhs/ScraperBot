import sys
import os
import urllib2
from wordpress_xmlrpc.base import Client
import xmlrpclib
import time
from wordpress_xmlrpc.wordpress import WordPressPost, WordPressCategory
from wordpress_xmlrpc.methods.posts import NewPost, GetRecentPosts
import datetime
from Crypto.Random.random import randrange
from wordpress_xmlrpc.methods.categories import NewCategory, SetPostCategories

class PostCreator():

    def __init__(self):
        homeDirectory = os.getenv("HOME")
        sys.path.append(r"" + homeDirectory + "/ScraperBot" + "")
        self.wp_site = "http://localhost/wordpress/xmlrpc.php"
        #self.wp_site = "http://www.hottestporn4u.com/xmlrpc.php"
        self.login = "pornmaster"
        self.password = "pornmasterpiece"

    def connect_the_client(self):
        wp = Client(self.wp_site, self.login, self.password)
        return wp

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

    def uploadFileToWp(self, thumbnail):
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
        server = xmlrpclib.Server(self.wp_site)
        filename = str(time.strftime('%H:%M:%S'))
        mediarray = {'name':filename + '.' + extension,
                     'type':xfileType,
                     'bits':file,
                     'overwrite':'false'}
        xarr = ['1', self.login, self.password, mediarray]
        result = server.wp.uploadFile(xarr)
        print result

    def createPost(self, title, thumbnail, iframe, videoduration, categories, tags):
        #user_from_keyboard = enter_WP_user()
        #password_from_keyboard = enter_WP_password()
        print "WP creating post ..."

        wp = self.connect_the_client()

        post0 = WordPressPost()
        post0.title = title
        print "WP title: " + post0.title
        post0.description = iframe + "Duration <img src=" + thumbnail + " alt=" + title + "><br>" + videoduration
        print "WP description: " + post0.description
        #Categories and tags correct
        #post0.categories = ['amateur', 'american', 'anal', 'blonde']
        #post0.tags = ['amateur', 'american', 'anal', 'blonde']
        print "WP categories: " + categories
        print "WP tags: " + tags
        post0.categories = categories
        post0.tags = tags
        dateFormat = self.prepare_post_date()
        post0.date_created = str(dateFormat)
        print dateFormat
        #post0.date_created = '20120507T12:11:59'
        print "WP Date: " + post0.date_created
        wp.call(NewPost(post0, True))

    def prepare_post_date(self):
        print "prepare post date"
        now = datetime.datetime.now()
        minute = randrange(now.minute, 59)
        if now.month < 10:
            month = "0" + str(now.month)
        else:
            month = str(now.month)

        if now.day < 10:
            day = "0" + str(now.day)
        else:
            day = str(now.day)

        if now.hour < 10:
            hour = "0" + str(now.hour)
        else:
            hour = str(now.hour)

        if now.minute < 10:
            minute = "0" + str(now.minute)
        else:
            minute = str(now.minute)

        if now.second < 10:
            second = "0" + str(now.second)
        else:
            second = str(now.second)

        date = str(now.year) + "" + month + "" + day + "T" + hour + ":" + minute + ":" + second
        return str(date)

    def get_posts(self, number_of_posts):
        wp = self.connect_the_client()
        post0 = WordPressPost()
        post0 = wp.call(GetRecentPosts(number_of_posts))
        return post0

    def is_this_item_on_the_list(self, item, list):
        for element in list:
            if str(element) == str(item):
                return True
            else:
                return False