import shlex
from BeautifulSoup import BeautifulSoup

class HtmlTagParser():
    def __init__(self, output):
        soup = BeautifulSoup(output)
        self.soup = soup

    def get_title (self):
        return self.soup.findAll('title')

    def get_metadata(self):
        return self.soup.findAll('meta')

    def get_description(self):
        return self.soup.findAll(attrs={"name":"description"})

    def get_keywords(self):
        return self.soup.findAll(attrs={"name":"keywords"})

    def parse_href(self, output):
        global href_parsed
        href_parsed = []
        for tag in output.findAll('a', href=True):
            href_parsed = tag['href']
        return href_parsed

    def parse_src_from_video_iframe(self, content):
        print "parse_src_from_video_iframe " + content
        mosoup = BeautifulSoup(content)
        #tags = mosoup.findAll('iframe')
        #print "\n".join(set(tag['src'] for tag in tags))
        for tag in mosoup.findAll('iframe'):
            src_url = tag['src']
        return src_url

    def parse_all_href(self, output):
        global all_href_parsed
        all_href_parsed = []
        for tag in output.findAll('a', href=True):
            all_href_parsed.append(tag['href'])
        return all_href_parsed

    def convert_title_to_categories(self, output):
        auxString = shlex.split(output)
        categories = []
        for i in auxString:
            categories.append(str(i.lower()))
        return categories

    def convert_hypen_into_space(self, output):
        return output.replace('-', ' ').lower()

    def convert_underscore_into_space(self, output):
        return output.replace('_', ' ').lower()

    def convert_string_into_categories(self, output):
        return output.split(" ")

    def uppercase_first_letter_from_string(self, output):
        return  output.capitalize()