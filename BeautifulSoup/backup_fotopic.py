#! /usr/bin/env python

import urllib, string

from bs4 import BeautifulSoup

collections_soup = BeautifulSoup()

# Replace the example URL below with the address of the pictures you want to backup
base_url = 'http://www.mitorestaurant.com'

f = urllib.urlopen(base_url)
result = f.read()
f.close()

for collection in collections_soup('a'):
    print '>>>' + base_url + collection['href']
    f = urllib.urlopen(base_url + collection['href'])
    result = f.read()
    f.close()
    collection_soup = BeautifulSoup()
    collection_soup.feed(result)
    for thumb in collection_soup('td', {'class' : 'thumbs'}):
        for image in thumb('a'):
            if string.find(image['href'], 'javascript') == -1 and string.find(image['href'], 'title') == -1:
                f = urllib.urlopen(base_url + image['href'])
                result = f.read()
                f.close()
                image_soup = BeautifulSoup()
                image_soup.feed(result)
                title = image_soup.first('title').contents[0]
                filename = string.split(title.string, '.JPG')[0]
                print filename
                for photo_div in image_soup('div', {'class' : 'photo-image'}):
                    for img in photo_div('img'):
                        print img
                        print filename
                        f = urllib.urlopen(img['src'])
                        result = f.read()
                        f.close()

			# Replace /tmp/ below with the path to a folder on your hard drive
                        img = open('/tmp/' + filename + '.JPG', 'wb+')
                        img.write(result)
                        img.close()
