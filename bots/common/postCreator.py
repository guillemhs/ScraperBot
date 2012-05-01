import sys
import os
from wordpress_xmlrpc.methods.posts import NewPost
from wordpress_xmlrpc.base import Client
from wordpress_xmlrpc.wordpress import WordPressPost, WordPressMedia
from wordpress_xmlrpc.methods.media import UploadFile

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
        wp = Client('http://localhost/wordpress/xmlrpc.php', 'pornmaster', 'pornmasterpiece')
        media = WordPressMedia()
        # set to the path to your file
        filename = '/home/guillem/Escriptori/test.jpg'

        # prepare metadata
        data = {
                'name': 'picture.jpg',
                'type': 'image/jpg', # mimetype
        }

        # read the binary file and let the XMLRPC library encode it into base64
        with open(filename, 'rb') as img:
                data['bits'] = wp.Binary(img.read())

        response = wp.call(media.UploadFile(data))
        # response == {
        #       'id': 6,
        #       'file': 'picture.jpg'
        #       'url': 'http://www.example.com/wp-content/uploads/2012/04/16/picture.jpg',
        #       'type': 'image/jpg',
        # }
        attachment_id = response['id']

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
        post0.post_thumbnail = attachment_id
        wp.call(NewPost(post0, True))