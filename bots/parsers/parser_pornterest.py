from BeautifulSoup import BeautifulSoup

class EmpFlixParser():
    "A Pornterest simple parser class."

    def __init__(self, output):
        soup = BeautifulSoup(output)
        self.soup = soup
