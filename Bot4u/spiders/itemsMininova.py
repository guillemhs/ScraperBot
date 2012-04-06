from scrapy.item import Item, Field

class TorrentItem(Item):
    urlsite = Field()
    name = Field()
    description = Field()
    size = Field()