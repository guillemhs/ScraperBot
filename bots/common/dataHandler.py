import os

class DataHandler():

    def read_categories(self):
        homeDirectory = os.getenv("HOME")
        folder = homeDirectory + "/ScraperBot"
        categories = []
        for line in open(str(folder) + "/data/categories.txt"):
            line = line.strip()
            categories.append(str(line))
        return categories

    def is_this_item_on_the_list(self, item, categorylist):
        for element in categorylist:
            if str(element) == str(item):
                return True
            else:
                return False

    def prepare_categories_for_post(self, title, categorylist, wp):
        categories_to_post = []
        latest = 'latest updates'
        for item in title:
            for element in categorylist:
                if element == item:
                    categories_to_post.append(str(item))
        categories_to_post.append(latest)
        return categories_to_post

    def prepare_tags_for_post(self, title):
        aux = title.split(" ")
        tags_to_post = []
        tags_to_post.append('porn')
        for item in aux:
            tags_to_post.append(str(item.strip()))
        return tags_to_post