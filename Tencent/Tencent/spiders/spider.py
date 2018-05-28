# -*- coding: utf-8 -*-  
import scrapy  
from Tencent.items import TencentItem  
 
class TencentpositionSpider(scrapy.Spider):  
    name = 'tencent'  
    allowed_domains = ['tencent.com']  
    #start_urls = ['http://tencent.com/']  
    url = "https://hr.tencent.com/position.php?&start="  
    offset = 0  
    start_urls = [url+str(offset)]  
    def parse(self, response):  
        for each in response.xpath("//tr[@class='even'] | //tr[@class='odd']"):  
            #初始化模型对象  
            item = TencentItem()  
  
            #职位名  
            item['positionname'] = each.xpath("./td[1]/a/text()").extract()[0]  
            #详情链接  
            item['positionlink'] = each.xpath("./td[1]/a/@href").extract()[0]  
            #职位类别  
            try:  
                item['positionType'] = each.xpath("./td[2]/text()").extract()[0]  
            except IndexError:  
                pass  
            #招聘人数  
            item['peopleNum'] = each.xpath("./td[3]/text()").extract()[0]  
            #工作地点  
            item['workLocation'] = each.xpath("./td[4]/text()").extract()[0]  
            #发布时间  
            item['publishTime'] = each.xpath("./td[5]/text()").extract()[0]  
            #将数据交给pipeline  
            yield item  
  
        if self.offset < 200:  
            self.offset += 10  
  
        #每次处理完一页的数据之后，重新发送下一页页面请求  
        #self.offset自增10,同时拼接为新的url，并调用回调函数self.parse处理Response  
        yield scrapy.Request(self.url+str(self.offset),callback = self.parse)
