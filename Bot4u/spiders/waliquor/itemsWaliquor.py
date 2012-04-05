from scrapy.item import Item, Field

class BrandCategoryItem(Item):
    brandCategoryId = Field()
    brandCategoryName = Field()

class BrandItem(Item):
    brandId = Field()
    brandCategoryId = Field()
    brandName = Field()
    totalPrice = Field()
    specialNote = Field()
    size = Field()
    proof = Field()
    
class StockItem(Item):
    brandId = Field()
    stateStoreNumber = Field()
    amountInStock = Field()

