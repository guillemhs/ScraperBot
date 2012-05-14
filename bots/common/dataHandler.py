import os

class DataHandler():

    def read_categories(self):
        homeDirectory = os.getenv("HOME")
        folder = homeDirectory + "/ScraperBot"
        categories = []
        for line in open(str(folder) + "/data/categories.txt"):
            line = line.strip()
            categories.append(line)
        return categories

    def is_this_item_on_the_list(self, item, list):
        for element in list:
            if str(element) == str(item):
                return True
            else:
                return False

    def prepare_categories_for_post(self, title, list):
        categories_to_post = []
        categories_to_post.append('latest updates')
        splitted = title.split(" ")
        print splitted
        for item in splitted:
            for element in list:
                if element == item:
                    categories_to_post.append(item)
        return categories_to_post