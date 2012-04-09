from BeautifulSoup import BeautifulSoup

class HtmlTagParser():

    def get_title (self, output):
        soup = BeautifulSoup(output)
        return soup.findAll('title')


    def get_metadata(self, output):
        soup = BeautifulSoup(output)
        return soup.findAll('meta')

    def get_description(self, output):
        soup = BeautifulSoup(output)
        return soup.findAll(attrs={"name":"description"})

    def get_keywords(self, output):
        soup = BeautifulSoup(output)
        return soup.findAll(attrs={"name":"keywords"})

    def parse_href(self, output):
        results = []
        soup = BeautifulSoup(output)
        for tag in soup.findAll('a', href=True):
            results.append(tag['href'])
        return results