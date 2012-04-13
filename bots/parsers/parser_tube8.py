from BeautifulSoup import BeautifulSoup

class Tube8Parser():
    "A Tube 8 simple parser class."

    def __init__(self, output):
        soup = BeautifulSoup(output)
        self.soup = soup
