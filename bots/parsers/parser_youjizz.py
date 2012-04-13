from BeautifulSoup import BeautifulSoup

class YouJizzParser():
    "A YouJizz simple parser class."

    def __init__(self, output):
        soup = BeautifulSoup(output)
        self.soup = soup
