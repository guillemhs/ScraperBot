from scrapy.spider import BaseSpider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from itemsWaliquor import BrandCategoryItem
from itemsWaliquor import BrandItem
from itemsWaliquor import StockItem


class WaliquorSpider(BaseSpider):
    name = "liq.wa.gov"
    allowed_domains = ["liq.wa.gov"]
    
SPIDER = WaliquorSpider()
#
# Setup the initial request to begin the spidering process
#
def start_requests(self):
    brandCategoriesRequest = Request("http://liq.wa.gov/homepageServices/brandsearch.asp",
                              callback=self.parseBrandCategories)
    
    return  [brandCategoriesRequest]
    #
# Scrape, parse all the brand categories into a list
# Create a request for every brand category
#
def parseBrandCategories(self, response):
    hxs = HtmlXPathSelector(response)
    
    # Gather all brand categories into list
    brandCategoryList = hxs.select('//form/div/center/table/tr/td/select/option[position()>1]/text()').extract()
    
    for i in range(len(brandCategoryList)):
        
        # Generate new request for each brand category's page
        yield FormRequest("http://liq.wa.gov/homepageServices/brandpicklist.asp",
                    method='POST',
                    formdata={'BrandName':'', 'CatBrand':brandCategoryList[i], 'submit1':'Find+Product'},
                    callback=self.parseBrandPage,
                    meta={'brandCategoryId':i, 'brandCategoryName':brandCategoryList[i]})
        
        # Create items for the brand category pipeline
        item = BrandCategoryItem()
        item['brandCategoryId'] = str(i)
        item['brandCategoryName'] = brandCategoryList[i]
        yield item
        
        #
# Parse each individual brandCategory page
# brandCode (unique key), brandCategoryId, brandName, brandCode, totalPrice, specialNote, size, proof
#
def parseBrandPage(self, response):
    
    hxs = HtmlXPathSelector(response)
    brandRows = hxs.select('//table[@class=\'tbl\']/tr[position()>1]')
    
    for brandRow in brandRows:
    
        brandId = brandRow.select('td[position()=2]/strong/text()').extract()
    
        # Generate new request for this brand category's page
        yield FormRequest("http://liq.wa.gov/homepageServices/find_store.asp",
            method='POST', formdata={'brandCode':brandId, 'CityName':'', 'CountyName':'', 'StoreNo':''},
            callback=self.parseBrandInStockPage,
            meta={'brandId':brandId})

        item = BrandItem()
        item['brandId'] = brandId
        item['brandCategoryId'] = response.request.meta['brandCategoryId']
        item['brandName'] = brandRow.select('td[position()=1]/strong/text()').extract()
        
        item['totalPrice'] = brandRow.select('td[position()=5]/strong/text()').extract()
        item['totalPrice'][0] = item['totalPrice'][0].replace('$', '')
        item['totalPrice'][0] = item['totalPrice'][0].replace(',', '')
        
        item['specialNote'] = brandRow.select('td[position()=7]/text()').extract()
        item['size'] = brandRow.select('td[position()=8]/text()').extract()
        item['proof'] = brandRow.select('td[position()=10]/text()').extract()
        
        yield item
        
        #
# Parse each individual brand's store availability page
# brandId ("Brand Code" provided), stateStoreNumber(id), amountInStock
#
def parseBrandInStockPage(self, response):
    
    hxs = HtmlXPathSelector(response)   
    storeRows = hxs.select('//table[@class=\'tbl\']/tr[position()>1]')
    
    items = []
    
    for storeRow in storeRows:
        item = StockItem()
        item['brandId'] = response.request.meta['brandId']
        item['stateStoreNumber'] = storeRow.select('td[position()=1]/text()').extract()
        item['amountInStock'] = storeRow.select('td[position()=5]/font/text()').extract()
        items.append(item)  
        
    return items
