# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv
import pymysql
import datetime
from lenovo.__init__ import *


class LenovoPipeline:
    ## Connect to Mysql
    def __init__(self):
        self.item_list = []
        self.search_name = Search_name
        '''更改所选数据库
        '''
        if activate_mysql == True:
            self.connect = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', \
                                           db=database, charset='utf8')
            self.cursor = self.connect.cursor()
            drop_sql = """
            DROP TABLE IF EXISTS %s;
            """
            self.cursor.execute(drop_sql % (self.search_name))
            create_sql = """
                CREATE TABLE %s(id int primary key auto_increment,
                            item_id BIGINT not Null UNIQUE,
                            item_name varchar(200),
                            price float default 0,
                            shopname varchar(50),
                            counting smallint default 0,
                            comment_num varchar(20) default '0',
                            GoodRate float default 0,
                            GoodCountstr varchar(20) default '0',
                            DefaultGoodCountstr varchar(20) default '0',
                            PoorRate float default 0,
                            PoorCountstr varchar(20) default '0',
                            start_time datetime default NULL,
                            end_time datetime default NULL,
                            create_time  timestamp DEFAULT current_timestamp COMMENT '创建时间',
                            update_time  timestamp DEFAULT current_timestamp on update CURRENT_TIMESTAMP COMMENT '修改时间');
                """ % (self.search_name)
            self.cursor.execute(create_sql)
            self.connect.commit()

    def process_item(self, item, spider):
        this_item = []
        item['end_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        this_item.append(item['item_id'])
        this_item.append(item['price'])
        this_item.append(item['name'])
        this_item.append(item['shopname'])
        this_item.append(item['num_comment'])
        this_item.append(item['GoodRate'])
        this_item.append(item['GoodCount'])
        this_item.append(item['DefaultGoodCount'])
        this_item.append(item['PoorRate'])
        this_item.append(item['PoorCount'])
        this_item.append(item['start_time'])
        this_item.append(item['end_time'])
        self.item_list.append(this_item)
        # print(self.item_list)
        if activate_mysql == True:
            insert_sql = '''INSERT INTO %s(item_name, price,shopname,comment_num,item_id,start_time,end_time,
            GoodRate,GoodCountstr,DefaultGoodCountstr,PoorRate,PoorCountstr) VALUES('%s',%d,'%s','%s',%d,'%s','%s',%f,'%s','%s',%f,'%s')
            on duplicate key update counting=counting+1;'''
            print(insert_sql % (self.search_name,
                                item['name'], float(item['price']), item['shopname'], item['num_comment'],
                                int(item['item_id']),
                                item['start_time'], item['end_time'], item['GoodRate'], item['GoodCount'],
                                item['DefaultGoodCount'], item['PoorRate'], item['PoorCount']))
            self.cursor.execute(insert_sql % (self.search_name,
                                              item['name'], float(item['price']), item['shopname'], item['num_comment'],
                                              int(item['item_id']),
                                              item['start_time'], item['end_time'], item['GoodRate'], item['GoodCount'],
                                              item['DefaultGoodCount'], item['PoorRate'], item['PoorCount']))
            self.connect.commit()
        return item

    def close_spider(self, spider):
        cannot_save = []
        filename = self.search_name + '.csv'
        if activate_mysql == True:
            self.cursor.close()
            self.connect.close()
        with open(filename, 'w', newline='', encoding='gbk') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(
                ['item_id', 'Price', 'Name', 'Shopname', 'commentNum', 'GoodRate', 'GoodCount', 'DefaultGoodRate',
                 'PoorRate', 'PoorCount', 'start_time', 'end_time'])
            for i in range(len(self.item_list)):
                try:
                    csv_writer.writerow(self.item_list[i])
                except:
                    cannot_save.append(self.item_list[i])
                    continue
        if not connot_save == []:
            print('不能保存至CSV的商品有：')
            print(cannot_save)
