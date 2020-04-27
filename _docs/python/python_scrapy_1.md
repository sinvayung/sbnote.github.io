# 爬虫分类总结——Scrapy总结与实战



![img](https://upload-images.jianshu.io/upload_images/9262853-710df2ed06b11066.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1000)

> 首先祭出中文[Scrapy文档](https://link.jianshu.com/?t=http%3A%2F%2Fscrapy-chs.readthedocs.io%2Fzh_CN%2Flatest%2Findex.html)，较枯燥，但是很有用。

Python开发的一个快速、高层次的屏幕抓取和web抓取框架，用于抓取web站点并从页面中提取结构化的数据。Scrapy用途广泛，可以用于数据挖掘、监测和自动化测试。

流程图如下：



![img](https://upload-images.jianshu.io/upload_images/9262853-925cc724ea020931.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/700)



① Scrapy Engine

> 引擎负责控制数据流在系统中所有组件中流动，并在相应动作发生时触发事件。 详细内容查看下面的数据流(Data Flow)部分

② 调度器(Scheduler)

> 调度器从引擎接受request并将他们入队，以便之后引擎请求他们时提供给引擎

③ 下载器(Downloader)

> 下载器负责获取页面数据并提供给引擎，而后提供给spider

④ Spiders

> Spider是Scrapy用户编写用于分析response并提取item(即获取到的item)或额外跟进的URL的类。 每 个spider负责处理一个特定(或一些)网站

⑤ Item Pipeline

> Item Pipeline负责处理被spider提取出来的item。典型的处理有清理、 验证及持久化(例如存取到数 据库中)

⑥ 下载器中间件(Downloader middlewares)

> 下载器中间件是在引擎及下载器之间的特定钩子(specific hook)，处理Downloader传递给引擎的 response。 其提供了一个简便的机制，通过插入自定义代码来扩展Scrapy功能

⑦ Spider中间件(Spider middlewares)

> Spider中间件是在引擎及Spider之间的特定钩子(specific hook)，处理spider的输入(response)和输出 (items及requests)。 其提供了一个简便的机制，通过插入自定义代码来扩展Scrapy功能

⑧ 数据流(Data flow)

> Scrapy中的数据流由执行引擎控制，其过程如下:

> 引擎打开一个网站(open a domain)，找到处理该网站的Spider并向该spider请求第一个要爬取的 URL(s)。
> 引擎从Spider中获取到第一个要爬取的URL并在调度器(Scheduler)以Request调度。
> 引擎向调度器请求下一个要爬取的URL。
> 调度器返回下一个要爬取的URL给引擎，引擎将URL通过下载中间件(请求(request)方向)转发给下载 器(Downloader)。
> 一旦页面下载完毕，下载器生成一个该页面的Response，并将其通过下载中间件(返回(response)方 向)发送给引擎。
> 引擎从下载器中接收到Response并通过Spider中间件(输入方向)发送给Spider处理。
> Spider处理Response并返回爬取到的Item及(跟进的)新的Request给引擎。
> 引擎将(Spider返回的)爬取到的Item给Item Pipeline，将(Spider返回的)Request给调度器。
> (从第二步)重复直到调度器中没有更多地request，引擎关闭该网站

流程归纳：

1.首先下载器下载request回执的html等的response
2.然后下载器传给爬虫解析
3.接着爬虫解析后交给调度器过滤，查重等等
4.最后交给管道，进行爬取数据的处理

**实战应用**

**第一步**：首先打开CMD，进入我们要保存项目的路径，**新建爬虫项目**。

```
scrapy startproject douban
```

文件夹PATH列表如下：



![img](https://upload-images.jianshu.io/upload_images/9262853-e66a9784aae39376.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/358)

- scrapy.cfg: 项目的配置文件
- douban/: 该项目的python模块。之后您将在此加入代码
- douban/items.py: 项目中的item文件
- douban/pipelines.py: 项目中的pipelines文件
- douban/settings.py: 项目的设置文件
- douban/spiders/:放置spider代码的目录

**第二步**：**编辑items.py文件（定义Item）**

> Items是**将要装载抓取的数据的容器**，它工作方式像 python 里面的字典，但它提供更多的保护，比如对未定义的字段填充以防止拼写错误。
>
> 通过创建scrapy.Item类, 并且定义类型为 **scrapy.Field 的类属性来声明一个Item**.
> 我们通过将需要的item模型化，来控制从 dmoz.org 获得的站点数据，比如我们要获得站点的**名字，url 和网站描述**，我们定义这三种属性的域。在 tutorial 目录下的 items.py 文件编辑

```
# -*- coding: utf-8 -*-  
  
# Define here the models for your scraped items  
#  
# See documentation in:  
# http://doc.scrapy.org/en/latest/topics/items.html  
  
from scrapy import Item, Field  
  
class DoubanItem(Item):  
    # define the fields for your item here like:  
    # name = scrapy.Field()  
    title = Field()  
    movieInfo = Field()  
    star = Field()  
    quote = Field()  
```

**第三步**：**编写spider（制作爬虫）**

> 先爬后取（获取整个网页内容，再取出有用部分）

第一招：**爬**

Spider 是用户编写的类, 用于从一个域（或域组）中抓取信息, 定义了用于下载的URL的初步列表, 如何跟踪链接，以及如何来解析这些网页的内容用于提取items。

要建立一个 Spider，继承 scrapy.Spider 基类，并确定三个主要的、强制的属性：

> **name**：爬虫的识别名，它必须是唯一的，在不同的爬虫中你必须定义不同的名字.

> **start_urls**：包含了Spider在启动时进行爬取的url列表。因此，第一个被获取到的页面将是其中之一。后续的URL则从初始的URL获取到的数据中提取。我们可以利用正则表达式定义和过滤需要进行跟进的链接。

> **parse()**：是spider的一个方法。被调用时，每个初始URL完成下载后生成的 Response 对象将会作为唯一的参数传递给该函数。该方法负责解析返回的数据(response data)，提取数据(生成item)以及生成需要进一步处理的URL的 Request 对象。
> 这个方法负责解析返回的数据、匹配抓取的数据(解析为 item )并跟踪更多的 URL。

创建doubnaspider.py，保存在douban\spiders目录下。

```
# -*- coding: utf-8 -*-  
from scrapy.spiders import CrawlSpider  
  
class Douban(CrawlSpider):  
    name = "douban"  
    start_urls = ['http://movie.douban.com/top250']  
  
    def parse(self,response):  
        print response.body  
```

在douban目录下按住shift右击，在此处打开命令窗口，输入：scrapy crawl douban

运行结果为：

```
2018-02-24 16:29:53 [scrapy.utils.log] INFO: Scrapy 1.3.3 started (bot: douban)
2018-02-24 16:29:53 [scrapy.utils.log] INFO: Overridden settings: {'NEWSPIDER_MODULE': 'douban.spiders', 'SPIDER_MODULES': ['douban.spiders'], 'ROBOTSTXT_OBEY': True, 'BOT_NAME': 'douban'}
2018-02-24 16:29:53 [scrapy.middleware] INFO: Enabled extensions:
['scrapy.extensions.logstats.LogStats',
 'scrapy.extensions.telnet.TelnetConsole',
 'scrapy.extensions.corestats.CoreStats']
2018-02-24 16:29:53 [scrapy.middleware] INFO: Enabled downloader middlewares:
['scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware',
 'scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware',
 'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware',
 'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware',
 'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware',
 'scrapy.downloadermiddlewares.retry.RetryMiddleware',
 'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware',
 'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware',
 'scrapy.downloadermiddlewares.redirect.RedirectMiddleware',
 'scrapy.downloadermiddlewares.cookies.CookiesMiddleware',
 'scrapy.downloadermiddlewares.stats.DownloaderStats']
2018-02-24 16:29:53 [scrapy.middleware] INFO: Enabled spider middlewares:
['scrapy.spidermiddlewares.httperror.HttpErrorMiddleware',
 'scrapy.spidermiddlewares.offsite.OffsiteMiddleware',
 'scrapy.spidermiddlewares.referer.RefererMiddleware',
 'scrapy.spidermiddlewares.urllength.UrlLengthMiddleware',
 'scrapy.spidermiddlewares.depth.DepthMiddleware']
2018-02-24 16:29:53 [scrapy.middleware] INFO: Enabled item pipelines:
[]
2018-02-24 16:29:53 [scrapy.core.engine] INFO: Spider opened
2018-02-24 16:29:53 [scrapy.extensions.logstats] INFO: Crawled 0 pages (at 0 pages/min), scraped 0 items (at 0 items/min)
2018-02-24 16:29:53 [scrapy.extensions.telnet] DEBUG: Telnet console listening on 127.0.0.1:6023
2018-02-24 16:29:54 [scrapy.core.engine] DEBUG: Crawled (403) <GET http://movie.douban.com/robots.txt> (referer: None)
2018-02-24 16:29:54 [scrapy.core.engine] DEBUG: Crawled (403) <GET http://movie.douban.com/top250> (referer: None)
2018-02-24 16:29:54 [scrapy.spidermiddlewares.httperror] INFO: Ignoring response <403 http://movie.douban.com/top250>: HTTP status code is not handled or not allowed
2018-02-24 16:29:54 [scrapy.core.engine] INFO: Closing spider (finished)
2018-02-24 16:29:54 [scrapy.statscollectors] INFO: Dumping Scrapy stats:
{'downloader/request_bytes': 444,
 'downloader/request_count': 2,
 'downloader/request_method_count/GET': 2,
 'downloader/response_bytes': 496,
 'downloader/response_count': 2,
 'downloader/response_status_count/403': 2,
 'finish_reason': 'finished',
 'finish_time': datetime.datetime(2018, 2, 24, 8, 29, 54, 184000),
 'log_count/DEBUG': 3,
 'log_count/INFO': 8,
 'response_received_count': 2,
 'scheduler/dequeued': 1,
 'scheduler/dequeued/memory': 1,
 'scheduler/enqueued': 1,
 'scheduler/enqueued/memory': 1,
 'start_time': datetime.datetime(2018, 2, 24, 8, 29, 53, 960000)}
2018-02-24 16:29:54 [scrapy.core.engine] INFO: Spider closed (finished)
```

最后一句INFO: Closing spider (finished)表明爬虫已经成功运行并且自行关闭了。

再看看此时的文件夹PATH列表



![img](https://upload-images.jianshu.io/upload_images/9262853-aae3ac57e2e9ecd1.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/453)

其实在douban目录下的main.py我们可以事先创建，并写入：

```
from scrapy import cmdline  
cmdline.execute("scrapy crawl douban".split())  
```

在pycharm里运行main.py,可以得到相同的结果。

------

若出现：

DEBUG: Ignoring response <403 [http://movie.douban.com/top250](https://link.jianshu.com/?t=http%3A%2F%2Fmovie.douban.com%2Ftop250)>: HTTP status code is not handled or not allowed

在settings.py写入：

```
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.54 Safari/536.5'
```

第二招：**取**

[http://movie.douban.com/top250](https://link.jianshu.com/?t=http%3A%2F%2Fmovie.douban.com%2Ftop250) 按F12：



![img](https://upload-images.jianshu.io/upload_images/9262853-1b2e326982d777d2.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/542)

每一部电影的信息都在一个**<**li**>**...**<**li**>**里（包括图片），我们需要的都在**<**div class=info**>**...**<**div**>**里面。利用Xpath来解析：

```
selector = Selector(response)  
Movies = selector.xpath('//div[@class="info"]')  
for eachMoive in Movies:  
     title = eachMoive.xpath('div[@class="hd"]/a/span/text()').extract()  
     movieInfo = eachMoive.xpath('div[@class="bd"]/p/text()').extract()  
     star = eachMoive.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').extract()[0]  
     quote = eachMoive.xpath('div[@class="bd"]/p[@class="quote"]/span/text()').extract()  
```

这里面有两个小问题，title包括两个，而quote有的电影没有，所以我们调整一下，完整代码如下：

```
# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from douban.items import DoubanItem

class Douban(CrawlSpider):
    name = "douban"
    start_urls = ['http://movie.douban.com/top250']

    def parse(self,response):
        #print response.body
        item = DoubanItem()
        selector = Selector(response)
        #print selector
        Movies = selector.xpath('//div[@class="info"]')
        #print Movies
        for eachMoive in Movies:
            title = eachMoive.xpath('div[@class="hd"]/a/span/text()').extract()
            # 把两个名称合起来
            fullTitle = ''
            for each in title:
                fullTitle += each
            movieInfo = eachMoive.xpath('div[@class="bd"]/p/text()').extract()
            star = eachMoive.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').extract()[0]
            quote = eachMoive.xpath('div[@class="bd"]/p[@class="quote"]/span/text()').extract()
            # quote可能为空，因此需要先进行判断
            if quote:
                quote = quote[0]
            else:
                quote = ''
            print fullTitle
            print movieInfo
            print star
            print quote
```

运行结果截取一部分（setting没有设置USER_AGENT可能出现403错误）：



![img](https://upload-images.jianshu.io/upload_images/9262853-fe9fa047558e8edc.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1000)

接下来就是处理自动处理自动抓取下一页的内容。看下图：



![img](https://upload-images.jianshu.io/upload_images/9262853-9dff1e62af05de7c.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/787)

里面关于rel="next"的介绍看这个链接：[SEO:分页使用rel=“next” 和 rel=“prev”](https://link.jianshu.com/?t=http%3A%2F%2Fwww.jdon.com%2Fidea%2Fjs%2Frel-prev-net.html)

我们把它抓出来补成完整的URL，就可以循环抓取了。

这里我们要引入Request。
from scrapy.http import Request

获取链接的代码如下：

```
nextLink = selector.xpath('//span[@class="next"]/link/@href').extract()  
# 第10页是最后一页，没有下一页的链接  
if nextLink:  
    nextLink = nextLink[0]  
    print nextLink  
    url = 'http://movie.douban.com/top250'  
    yield Request(self.url + nextLink, callback=self.parse)  
```

下面是完整代码：(http改为了https，不然出现301重定向错误)

```
# -*- coding: utf-8 -*-  
  
from scrapy.spiders import CrawlSpider  
from scrapy.selector import Selector  
from douban.items import DoubanItem  
from scrapy.http import Request  
  
class Douban(CrawlSpider):  
    name = "douban"  
    start_urls = ['https://movie.douban.com/top250']  
  
    url = 'https://movie.douban.com/top250'  
  
    def parse(self,response):  
        #print response.body  
        item = DoubanItem()  
        selector = Selector(response)  
        #print selector  
        Movies = selector.xpath('//div[@class="info"]')  
        #print Movies  
        for eachMoive in Movies:  
            title = eachMoive.xpath('div[@class="hd"]/a/span/text()').extract()  
            # 把两个名称合起来  
            fullTitle = ''  
            for each in title:  
                fullTitle += each  
            movieInfo = eachMoive.xpath('div[@class="bd"]/p/text()').extract()  
            star = eachMoive.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').extract()[0]  
            quote = eachMoive.xpath('div[@class="bd"]/p[@class="quote"]/span/text()').extract()  
            # quote可能为空，因此需要先进行判断  
            if quote:  
                quote = quote[0]  
            else:  
                quote = ''  
            #print fullTitle  
            #print movieInfo  
            #print star  
            #print quote  
            item['title'] = fullTitle  
            item['movieInfo'] = ';'.join(movieInfo)  
            item['star'] = star  
            item['quote'] = quote  
            yield item  
            nextLink = selector.xpath('//span[@class="next"]/link/@href').extract()  
            # 第10页是最后一页，没有下一页的链接  
            if nextLink:  
                nextLink = nextLink[0]  
                print nextLink  
                yield Request(self.url + nextLink, callback=self.parse)  
```

**第四步**：**存储内容（Pipline）**

要用到Scrapy自带的[Feed exports](https://link.jianshu.com/?t=http%3A%2F%2Fscrapy-chs.readthedocs.io%2Fzh_CN%2Flatest%2Ftopics%2Ffeed-exports.html)功能。

常用的就四种输出格式：JSON，JSON lines，CSV，XML。

我们导出为JSON格式：

```
scrapy crawl douban -o douban.json -t csv
```

导出为csv格式则为：

```
scrapy crawl douban -o douban.csv -t csv
```

其实我们可以直接在settings.py文件中设置输出的位置和文件类型:

```
FEED_URI = u'file:///C:/Users/Administrator/Desktop/dban/douban/douban.csv' 
FEED_FORMAT = 'CSV'
```

FEED_URL是必须的。然后file后面的三斜杠是标准文档规定的，最好这么写吧。



![img](https://upload-images.jianshu.io/upload_images/9262853-50ac46996fbb5930.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/361)

标准文档用的三斜杠

在pycharm中运行main.py，就可以看到所有的电影信息。

**补充：**

1.item的使用

Item对象是自定义的python字典,可以使用标准的字典语法来获取到其每个字段的值(字段即是我们之前用Field赋值的属性)

一般来说，Spider将会将**爬取到的数据以 Item 对象返回**, 最后修改爬虫类，**使用 Item 来保存数据**。

列一段示例代码：

```
from scrapy.spider import Spider
from scrapy.selector import Selector
from tutorial.items import DmozItem 

            
class DmozSpider(Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/",
    ]

    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//ul[@class="directory-url"]/li')
        items = []

        for site in sites:
            item = DmozItem()
            item['name'] = site.xpath('a/text()').extract()
            item['url'] = site.xpath('a/@href').extract()
            item['description'] = site.xpath('text()').re('-\s[^\n]*\\r')
            items.append(item)
        return items
```

2.Item Pipeline(条目管道)的使用

参考[标准文档](https://link.jianshu.com/?t=http%3A%2F%2Fscrapy-chs.readthedocs.io%2Fzh_CN%2Flatest%2Ftopics%2Fitem-pipeline.html)。

当Item在Spider中被收集之后，它将会被传递到Item Pipeline，一些组件会按照一定的顺序执行对Item的处理。
每个item pipeline组件(有时称之为ItemPipeline)是实现了简单方法的Python类。他们接收到Item并通过它执行一些行为，同时也决定此Item是否继续通过pipeline，或是被丢弃而不再进行处理。
以下是item pipeline的一些典型应用：

- 清理HTML数据
- 验证爬取的数据(检查item包含某些字段)
- 去重
- 将爬取结果保存，如保存到数据库、XML、JSON等文件中

编写你自己的item pipeline很简单，每个item pipeline组件是一个独立的Python类，同时必须实现以下方法:

```
process_item(item, spider)  #每个item pipeline组件都需要调用该方法，这个方法必须返回一个 Item (或任何继承类)对象，或是抛出 DropItem异常，被丢弃的item将不会被之后的pipeline组件所处理。
#参数:
item: 由 parse 方法返回的 Item 对象(Item对象)
spider: 抓取到这个 Item 对象对应的爬虫对象(Spider对象)

open_spider(spider)  #当spider被开启时，这个方法被调用。
#参数: 
spider : (Spider object) – 被开启的spider
　　
close_spider(spider)  #当spider被关闭时，这个方法被调用，可以再爬虫关闭后进行相应的数据处理。
#参数: 
spider : (Spider object) – 被关闭的spider
```

具体应用时参考标准文档即可。

------

参考文章链接：[Scrapy爬取豆瓣电影](https://www.jianshu.com/p/a6d3db78bbc9m)



https://www.jianshu.com/p/0f9671e583eb

