# Jd_Crawler

## 简介

利用Scrapy模块爬取京东商品信息

爬取京东的商品信息，**输入**为

| 名称           | 变量类型     | 描述                                              |
| -------------- | ------------ | ------------------------------------------------- |
| Search_name    | str          | 输入你想要搜索的东西，例如“苹果”、“iphone”等      |
| total_page     | int          | 输入想要爬取的页数                                |
| activate_mysql | `True/False` | 是否启用mysql进行存储，细节见`lenovo/__init__.py` |
| database       | str          | 输入使用的数据库名称                              |

**输出**为：

| 名称         | 描述                                                         |
| ------------ | ------------------------------------------------------------ |
| id           | 爬取的按照顺序存储的id(Auto_increment, int, primary key)     |
| item_id      | 京东商品的内部id，可直接利用https://item.jd.com/100011386554.html(左侧一串数目即为id)进行访问 |
| item_name    | 商品名称                                                     |
| price        | 商品价格                                                     |
| shopname     | 商铺名称                                                     |
| counting     | 计算在爬取过程中该商品重复了几次                             |
| comment_num  | 评论数量                                                     |
| start_time   | 开始爬取的时间                                               |
| end_time     | 存储的时间                                                   |
| create_time* | 该条目被创建的时间                                           |
| update_time* | 更新该条目的时间(例如再次碰到同样的商品时，就会更新该时间)   |

*仅mysql数据库有。

### 如何使用

若要更改爬取的信息，打开`lenovo/__init__.py`，更改里面对应的参数即可。一般利用pycharm直接打开，直接运行`lenovo\spiders\quotes_spider.py`也可以，只不过文件会保存在spiders文件夹下。



利用cmd或是anaconda(需安装scrapy和itemadapter等模块)，进入(cd)到 Jd 文件目录下，然后输入

```
scrapy crawl lenovo
```

由于一开始用lenovo试手，spiders的名字就叫lenovo了。



## 其余文件解释

一些csv文件为直接试爬取的结果。

顺带附上`__init__.py`文件：

```python
Search_name = '苹果' ## 输入你想要搜索的东西，之后的表格、csv文件等将会以这个名字命名
total_page = 2 ## 输入需要爬取的页数
'''
默认采取0.3秒的请求延迟，也就是每件物品需要0.3秒的延迟。15页物品大概需要5-6分钟。
经测试，若不给予延迟，可能会导致丢页。若需修改，请至settings.py中修改
DOWNLOAD_DELAY = .3
'''

'''
是否启用mysql数据库，默认采用本地数据库ip:127.0.0.1,port = 3306
若需更改连接ip请至pipelines.py中修改。并填写写入的数据库名称。必须已有该数据库。
'''
activate_mysql = True
database = 'lenovo'
'''
最后写入csv文件，有部分文字因格式问题，无法写入。最终会打印出来，请自行复制填写。mysql没有该问题。
'''

```

scrapy的具体教程见http://docs.scrapy.org/en/latest。



# 写在最后

这个爬虫就是写着玩玩练练手，运行不起来自己调试一下吧。反正我这里挺正常的。