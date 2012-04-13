from BeautifulSoup import BeautifulSoup

class PornHubParser():
    "A PornHub simple parser class."

    def __init__(self, output):
        soup = BeautifulSoup(output)
        self.soup = soup
