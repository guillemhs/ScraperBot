import csv
import itemsWaliquor

class WaliquorPipeline(object):
    
    def __init__(self):
        self.brandCategoryCsv = csv.writer(open('brandCategoryTable.csv', 'wb'))
        self.brandCategoryCsv.writerow(['brandCategoryId', 'brandCategoryName'])
        
        self.brandsCsv = csv.writer(open('brandsTable.csv', 'wb'))
        self.brandsCsv.writerow(['brandCategoryId', 'brandId', 'brandName', 'totalPrice', 'specialNote', 'size', 'proof'])
        
        self.storeStockTable = csv.writer(open('storeStockTable.csv', 'wb'))
        self.storeStockTable.writerow(['brandId', 'stateStoreNumber', 'amountInStock'])

    def process_item(self, item, spider):
                
        if isinstance(item, itemsWaliquor.BrandCategoryItem):
            self.brandCategoryCsv.writerow([item['brandCategoryId'], item['brandCategoryName'].title()])
            return item
    
        if isinstance(item, itemsWaliquor.BrandItem):
        
        # Double check that itemsWaliquor in the pipeline exist
        # Otherwise, an item with a an empty list would 
        # be completely skipped over by Scrapy
        
            try:
                item['brandId'][0]
            except:
                item['brandId'].append("")
                
            try:
                item['brandCategoryId']
            except:
                item['brandCategoryId'] = "9999"
                
            try:
                item['brandName'][0]
            except:
                item['brandName'].append("")
                
            try:
                item['totalPrice'][0]
            except:
                item['totalPrice'].append("")
                
            try:
                item['specialNote'][0]
            except:
                item['specialNote'].append("")
                
            try:
                item['size'][0]
            except:
                item['size'].append("")
                
            try:
                item['proof'][0]
            except:
                item['proof'].append("")

            self.brandsCsv.writerow([item['brandCategoryId'], item['brandId'][0], item['brandName'][0].title(), item['totalPrice'][0], item['specialNote'][0].title(), item['size'][0], item['proof'][0]])
            
            return item
            
        
        if isinstance(item, itemsWaliquor.StockItem):
            self.storeStockTable.writerow([item['brandId'][0], item['stateStoreNumber'][1], item['amountInStock'][0]])
            return item
