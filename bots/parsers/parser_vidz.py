from BeautifulSoup import BeautifulSoup

class VidZParser():
    "A vid Z simple parser class."

    def __init__(self, output):
        soup = BeautifulSoup(output)
        self.soup = soup
