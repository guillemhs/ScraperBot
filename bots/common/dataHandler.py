import os
import shlex

class DataHandler():

    def read_categories(self):
        homeDirectory = os.getenv("HOME")
        folder = homeDirectory + "/ScraperBot"
        categories = []
        for line in open(str(folder) + "/data/categories.txt"):
            line = line.strip()
            categories.append(line)
        return categories

    def is_this_item_on_the_list(self, item, categorylist):
        for element in categorylist:
            if str(element) == str(item):
                return True
            else:
                return False

    def prepare_categories_for_post(self, title, categorylist):
        categories_to_post = []
        categories_to_post.append('latest updates')
        for item in title:
            for element in categorylist:
                if element == item:
                    categories_to_post.append(item)
        return categories_to_post

    def prepare_tags_for_post(self, title):
        auxString = shlex.split(title)
        categories = []
        for i in auxString:
            categories.append(str(i.lower()))
        return categories