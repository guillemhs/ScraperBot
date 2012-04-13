from BeautifulSoup import BeautifulSoup

class xHamsterParser():
    "A xHamster simple parser class."

    def __init__(self, output):
        soup = BeautifulSoup(output)
        self.soup = soup
