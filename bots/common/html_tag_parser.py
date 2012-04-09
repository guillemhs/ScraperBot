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

    def parse_all_href(self, output):
        global all_href_parsed
        all_href_parsed = []
        for tag in output.findAll('a', href=True):
            all_href_parsed.append(tag['href'])
        return all_href_parsed