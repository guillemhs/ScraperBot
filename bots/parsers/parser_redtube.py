from BeautifulSoup import BeautifulSoup

class RedTubeParser():
    "A Redtube simple parser class."

    def __init__(self, output):
        soup = BeautifulSoup(output)
        self.soup = soup
