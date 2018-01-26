# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from items import BasicInfoItem,DetailInfoItem,ResblockInfoItem,BuildingInfoItem,UnitInfoItem,CommentInfoItem,DynamicInfoItem
from scrapy.utils.project import get_project_settings
import pymysql
from twisted.enterprise import adbapi
import logging
import time

logger=logging.getLogger("LianjiaPipeline")

'''scrapy的解析速度要远大于MySQL的入库速度，当有大量解析的时候，MySQL的入库就可能会阻塞。可以使用Twisted将MySQL的入库和解析变成异步操作'''

class LianjiaPipeline(object):
    def __init__(self,dbpool):
        self.dbpool=dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWD"],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("pymysql", **dbparms)

        return cls(dbpool)



    def process_item(self, item, spider):
        if isinstance(item, BasicInfoItem):
            # runInteraction可以将传入的函数变成异步的
            query = self.dbpool.runInteraction(self.insert_basic_info, item)
            # 处理异常
            query.addErrback(self.handle_error, item, spider)
            return item
        elif isinstance(item,DetailInfoItem):
            query = self.dbpool.runInteraction(self.insert_detail_info, item)
            query.addErrback(self.handle_error, item, spider)
            return item
        elif isinstance(item,ResblockInfoItem):
            query = self.dbpool.runInteraction(self.insert_resblock_info, item)
            query.addErrback(self.handle_error, item, spider)
            return item
        elif isinstance(item,BuildingInfoItem):
            query = self.dbpool.runInteraction(self.insert_build_info, item)
            query.addErrback(self.handle_error, item, spider)
            return item
        elif isinstance(item,UnitInfoItem):
            query = self.dbpool.runInteraction(self.insert_unit_info, item)
            query.addErrback(self.handle_error, item, spider)
            return item
        elif isinstance(item,CommentInfoItem):
            query = self.dbpool.runInteraction(self.insert_comment_info, item)
            query.addErrback(self.handle_error, item, spider)
            return item
        elif isinstance(item,DynamicInfoItem):
            query = self.dbpool.runInteraction(self.insert_dynamic_info, item)
            query.addErrback(self.handle_error, item, spider)
            return item
        else:
            pass

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        logger.error(failure)


    def insert_basic_info(self,cursor,item):
        sql="""insert into basic_info(basic_id,city_id,city_name,district_name,district_id,bizcircle_name,process_status,
            resblock_frame_area,longitude,latitude,title,resblock_name,address,avg_unit_price,average_price,
            address_remark,project_name,special_tags,min_frame_area,max_frame_area,count,room,tags,description,
            house_type,sale_status,has_evaluate,has_vr_aerial,has_vr_house,has_video,has_virtual_view,lowest_total_price,show_price,show_price_unit,
            show_price_desc,status,evaluate_status,total_price_start,total_price_start_unit,avg_price_start,avg_price_start_unit,
            insert_time) 
            values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(sql,(item["basic_id"],item["city_id"],item["city_name"],item["district_name"],item["district_id"],
                            item["bizcircle_name"],item["process_status"],item["resblock_frame_area"],item["longitude"],
                            item["latitude"],item["title"],item["resblock_name"],item["address"],item["avg_unit_price"],
                            item["average_price"],item["address_remark"],item["project_name"],item["special_tags"],item["min_frame_area"],
                            item["max_frame_area"],item["count"],item["room"],item["tags"],item["description"],item["house_type"],
                            item["sale_status"],item["has_evaluate"],item["has_vr_aerial"],item["has_vr_house"],item["has_video"],
                            item["has_virtual_view"],item["lowest_total_price"],item["show_price"],item["show_price_unit"],
                            item["show_price_desc"],item["status"],item["evaluate_status"],item["total_price_start"],
                            item["total_price_start_unit"],item["avg_price_start"],item["avg_price_start_unit"],item["insert_time"]))
    def insert_detail_info(self,cursor,item):
        sql="""insert detail_info (fid,frames_id,project_name,resblock_id,resblock_name,frame_name,bedroom_count,parlor_count,cookroom_count,total_count,toilet_count,build_area,inside_area,frame_structure,orientation,is_main_frame,status,sell_status
            ,sell_status_txt,price,total_price_min,total_price_max,total_price,show_price,show_price_unit,show_price_desc,show_price_confirm_time,tags,frames_build_area,detail_url
            ,insert_time) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(sql,(item['fid'],item['frames_id'],item['project_name'],item['resblock_id'],item['resblock_name'],item['frame_name'],
                            item['bedroom_count'],item['parlor_count'],item['cookroom_count'],item['total_count'],
                            item['toilet_count'],item['build_area'],item['inside_area'],item['frame_structure'],item['orientation'],
                            item['is_main_frame'],item['status'],item['sell_status'],
                            item['sell_status_txt'],item['price'],item['total_price_min'],
                            item['total_price_max'],item['total_price'],item['show_price'],item['show_price_unit'],
                            item['show_price_desc'],item['show_price_confirm_time'],item['tags'],item['frames_build_area'],
                            item['detail_url'],item['insert_time']))
    def insert_resblock_info(self,cursor,item):
        sql="""insert into resblock_info (rid,insert_time,resblock_id,city_id,status,average_price,resblock_name,resblock_alias,sale_status,
            process_status,house_type,house_type_value,tags,description,project_name,address_remark,administrative_address,open_date,
            open_date_more,special_tags,developer_company,hand_over_time,properright,longitude,latitude,district_id,district_name,
            bizcircle_id,bizcircle_name,store_addr,build_type,
            cubage_rate,
            virescence_rate,house_amount,overground_car_num,underground_car_num,property_company,property_price,heating_type,
            powersuply_kind,watersuply_kind,is_open_date_predict,is_hand_over_predict,lowest_total_price,
            price_confirm_time,permit_number,permit_time,building_list,show_permit,show_price,show_price_unit,
            show_price_desc,resblock_frame_area,show_open_date,show_hand_over_time,total_area,site_area,pid) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(sql,(item["rid"],item["insert_time"],item["resblock_id"],item["city_id"],item["status"],item["average_price"],
                            item["resblock_name"],item["resblock_alias"],item["sale_status"],item["process_status"],item["house_type"],
                            item["house_type_value"],item["tags"],item["description"],item["project_name"],item["address_remark"],
                            item["administrative_address"],item["open_date"],item["open_date_more"],item["special_tags"],item["developer_company"],
                            item["hand_over_time"],item["properright"],item["longitude"],item["latitude"],item["district_id"],item["district_name"],
                            item["bizcircle_id"],item["bizcircle_name"],item["store_addr"],item["build_type"],
                            item["cubage_rate"],item["virescence_rate"],item["house_amount"],item["overground_car_num"],item["underground_car_num"],
                            item["property_company"],item["property_price"],item["heating_type"],item["powersuply_kind"],
                            item["watersuply_kind"],item["is_open_date_predict"],item["is_hand_over_predict"],
                            item["lowest_total_price"],item["price_confirm_time"],item["permit_number"],
                            item["permit_time"],item["building_list"],item["show_permit"],item["show_price"],item["show_price_unit"],
                            item["show_price_desc"],item["resblock_frame_area"],item["show_open_date"],item["show_hand_over_time"],item["total_area"],
                            item["site_area"],item["pid"]))
    def insert_build_info(self,cursor,item):
        sql="""insert into build_info(house_id,project_name,insert_time,bid,resblock_id,building_code,part_num,building_type,
            total_unit_count,total_house_count,floor_height,sell_count,open_time,hand_over_time,sale_status
            ) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(sql,(item["house_id"],item["project_name"],item["insert_time"],item["bid"],item["resblock_id"],
                            item["building_code"],item["part_num"],item["building_type"],item["total_unit_count"],
                            item["total_house_count"],item["floor_height"],item["sell_count"],item["open_time"],
                            item["hand_over_time"],item["sale_status"]))
    def insert_unit_info(self,cursor,item):
        sql="""
            insert into unit_info(ulid,project_name,insert_time,uid,unit_name,sorted,overground_floors,
            underground_floors,floor_height,elevator_count,floor_house_count
            ) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        cursor.execute(sql,(item["ulid"],item["project_name"],item["insert_time"],item["uid"],item["unit_name"],item["sorted"],
                            item["overground_floors"],item["underground_floors"],item["floor_height"],item["elevator_count"],
                            item["floor_house_count"]))
    def insert_comment_info(self,cursor,item):
        sql="""insert into comment_info(around,traffic,green,composite_score,composite_score_info,total,comment_id,
        project_name,user_name,user_around,user_traffic,user_green,user_avg,content,
        ctime,pc_ctime,image,phone,like_num,is_interest,show_status,official_reply,
        is_anonymity,is_like,uc_avatar,used_time,insert_time
        ) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(sql,(item["around"],item["traffic"],item["green"],item["composite_score"],item["composite_score_info"],
                            item["total"],item["comment_id"],item["project_name"],item["user_name"],item["user_around"],
                            item["user_traffic"],item["user_green"],item["user_avg"],item["content"],item["ctime"],
                            item["pc_ctime"],item["image"],item["phone"],
                            item["like_num"],item["is_interest"],item["show_status"],item["official_reply"],
                            item["is_anonymity"],item["is_like"],item["uc_avatar"],item["used_time"],
                            item["insert_time"]))
    def insert_dynamic_info(self,cursor,item):
        sql="""insert into dynamic_info(project_name,total,dynamic_id,title,time,content,type,insert_time) 
        values (%s,%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(sql,(item["project_name"],item["total"],item["dynamic_id"],item["title"],item["time"],
                            item["content"],item["type"],item["insert_time"]))
