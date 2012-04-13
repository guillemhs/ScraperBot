from BeautifulSoup import BeautifulSoup

class FreePornParser():
    "A Free Porn simple parser class."

    def __init__(self, output):
        soup = BeautifulSoup(output)
        self.soup = soup
