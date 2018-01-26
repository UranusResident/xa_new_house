#-*- coding:utf-8 -*-

# Author:longjiang

from scrapy.spiders import CrawlSpider,Rule

import re
import requests
from scrapy_redis.spiders import RedisSpider
from scrapy.selector import Selector
from scrapy.http import Request
import logging
import time
from bs4 import BeautifulSoup
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from ..items import BasicInfoItem,DetailInfoItem,ResblockInfoItem,BuildingInfoItem,UnitInfoItem,CommentInfoItem,DynamicInfoItem



class Spider(CrawlSpider):

    name = "lianjia"

    start_urls = ["https://m.weibo.cn/api/container/getIndex?type=uid&value=1816289645"]


    def start_requests(self):

        query_string = {
            "city_id": "610100",
            "is_showing_banner": "0",
            "is_showing_topic": "0",
            "limit_count": "20",
            "limit_offset": "20",
            "position": "19",
            "request_ts": int(time.time())
        }
        url = "https://app.api.lianjia.com/newhouse/apisearch?city_id={}&is_showing_banner={}&is_showing_topic={}&limit_count={}&limit_offset={}&position={}&request_ts={}" \
            .format(query_string["city_id"], query_string["is_showing_banner"], query_string["is_showing_topic"],
                    query_string["limit_count"], query_string["limit_offset"], query_string["position"],
                    query_string["request_ts"])

        yield self.make_requests_from_url(url)


    def parse(self, response):

        list=json.loads(response.body)["data"]["resblock_list"]

        for item in list["list"]:
            data = BasicInfoItem()
            data["basic_id"] = item["id"]
            data["city_id"] = item["city_id"]
            data["city_name"] = item["city_name"]
            data["district_name"] = item["district_name"]

            # 区域id
            data["district_id"] = item["district_id"]

            data["bizcircle_name"] = item["bizcircle_name"]
            data["process_status"] = item["process_status"]
            # 建筑面积
            data["resblock_frame_area"] = item["resblock_frame_area"]
            # 坐标
            data["longitude"] = item["longitude"]
            data["latitude"] = item["latitude"]
            # 小区名称
            data["title"] = item["title"]
            data["resblock_name"] = item["resblock_name"]
            # 地址
            data["address"] = item["address"]
            # 平均单价
            data["avg_unit_price"] = item["avg_unit_price"]
            # 均价
            data["average_price"] = item["average_price"]
            # 地址
            data["address_remark"] = item["address_remark"]
            # 项目标识(sfsyaalqy)
            data["project_name"] = item["project_name"]
            # special_tags
            data["special_tags"] = ','.join(item["special_tags"])
            #
            data["min_frame_area"] = item["min_frame_area"]

            data["max_frame_area"] = item["max_frame_area"]

            if len(item["frame_rooms"]) > 0:
                for obj in item["frame_rooms"]:
                    data["count"] = obj["count"]

                    data["room"] = obj["room"]
            else:
                data["count"] = None
                data["room"] = None

            data["tags"] = ','.join(item["tags"])

            if len(item["project_tags"]) > 0:
                desc = []
                for ele in item["project_tags"]:
                    desc.append(ele["desc"])
                # 描述
                data["description"] = ','.join(desc)
            else:
                data["description"] = None
            # 住宅/公寓
            data["house_type"] = item["house_type"]
            # 是否在售
            data["sale_status"] = item["sale_status"]
            # 有评价?
            data["has_evaluate"] = item["has_evaluate"]

            data["has_vr_aerial"] = item["has_vr_aerial"]

            data["has_vr_house"] = item["has_vr_house"]

            data["has_video"] = item["has_video"]

            data["has_virtual_view"] = item["has_virtual_view"]
            # 最低总价
            data["lowest_total_price"] = item["lowest_total_price"]
            # 显示价格
            data["show_price"] = item["show_price"]
            # 显式价格单位(万/元)
            data["show_price_unit"] = item["show_price_unit"]
            # 显示价格描述
            data["show_price_desc"] = item["show_price_desc"]
            # 状态
            data["status"] = item["status"]

            data["evaluate_status"] = item["evaluate_status"]

            # 总价
            data["total_price_start"] = item["total_price_start"]
            # 总价单位
            data["total_price_start_unit"] = item["total_price_start_unit"]
            # 平均最低单价
            data["avg_price_start"] = item["avg_price_start"]
            # 平均最低单价单位
            data["avg_price_start_unit"] = item["avg_price_start_unit"]

            data["insert_time"]=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            yield data


            #详情
            detail_params = {
                "city_id": "610100",
                "project_name": item["project_name"],
                "request_ts": "1516673168"
            }
            detail_url="https://app.api.lianjia.com/newhouse/app/resblock/detail?city_id={}&project_name={}&request_ts={}".format(detail_params["city_id"],detail_params["project_name"],detail_params["request_ts"])

            yield Request(url=detail_url,callback=self.parse_detail,meta={"house_id":item["id"],"project_name":item["project_name"]})


            #评论
            comment_params = {
                "is_real": "",
                "limit": "20",
                "offset": "0",
                "project_name": item["project_name"],
                "request_ts": int(time.time())
            }

            comment_url = "https://app.api.lianjia.com/newhouse/commentlist?is_real={}&limit={}&offset={}&project_name={}&request_ts={}".format(
                comment_params["is_real"], comment_params["limit"],comment_params["offset"], comment_params["project_name"], comment_params["request_ts"])

            yield Request(url=comment_url,callback=self.parse_comment,meta={"project_name":item["project_name"]})


            #动态信息
            dynamic_params={
                "limit":"10",
                "offset":"0",
                "project_name":item["project_name"],
                "request_ts":int(time.time())
            }
            dynamic_url="https://app.api.lianjia.com/newhouse/dongtailist?limit={}&offset={}&project_name={}&request_ts={}".format(dynamic_params["limit"],dynamic_params["offset"],dynamic_params["project_name"],dynamic_params["request_ts"])

            yield Request(url=dynamic_url,callback=self.parse_dynamic,meta={"project_name":item["project_name"]})


        #获取更多
        offset = int(re.findall("limit_offset=(\d+)&?", response.url)[0])
        # 是否还有更多数据
        if list["has_more_data"] == "1":
            offset+=20
            query_string = {
                "city_id": "610100",
                "is_showing_banner": "0",
                "is_showing_topic": "0",
                "limit_count": "20",
                "limit_offset": offset,
                "position": "19",
                "request_ts": int(time.time())
            }
            url = "https://app.api.lianjia.com/newhouse/apisearch?city_id={}&is_showing_banner={}&is_showing_topic={}&limit_count={}&limit_offset={}&position={}&request_ts={}" \
                .format(query_string["city_id"], query_string["is_showing_banner"],
                        query_string["is_showing_topic"],
                        query_string["limit_count"], query_string["limit_offset"], query_string["position"],
                        query_string["request_ts"])
            yield Request(url=url,callback=self.parse)

    #详情
    def parse_detail(self,response):

        house_id=response.meta["house_id"]

        project_name=response.meta["project_name"]

        data = json.loads(response.body)["data"]

        # item={}

        # detail_info表(基本框架信息)
        for item_f in data["frames"]:
            detail_info = DetailInfoItem()
            # id
            detail_info["fid"] = house_id  # 关联键
            detail_info["insert_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 入库时间
            detail_info["frames_id"] = item_f["id"]
            detail_info["project_name"] = item_f["project_name"]
            detail_info["resblock_id"] = item_f["resblock_id"]
            detail_info["resblock_name"] = item_f["resblock_name"]
            detail_info["frame_name"] = item_f["frame_name"]
            detail_info["bedroom_count"] = item_f["bedroom_count"]
            detail_info["parlor_count"] = item_f["parlor_count"]
            detail_info["cookroom_count"] = item_f["cookroom_count"]
            detail_info["total_count"] = item_f["total_count"]
            detail_info["toilet_count"] = item_f["toilet_count"]
            detail_info["build_area"] = item_f["build_area"]
            detail_info["inside_area"] = item_f["inside_area"]
            detail_info["frame_structure"] = item_f["frame_structure"]
            detail_info["orientation"] = item_f["orientation"]
            detail_info["is_main_frame"] = item_f["is_main_frame"]
            detail_info["status"] = item_f["status"]
            detail_info["sell_status"] = item_f["sell_status"]
            detail_info["sell_status_txt"] = item_f["sell_status_txt"]
            detail_info["price"] = item_f["price"]
            detail_info["total_price_min"] = item_f["total_price_min"]
            detail_info["total_price_max"] = item_f["total_price_max"]
            detail_info["total_price"] = item_f["total_price"]
            detail_info["show_price"] = item_f["show_price"]
            detail_info["show_price_unit"] = item_f["show_price_unit"]
            detail_info["show_price_desc"] = item_f["show_price_desc"]
            detail_info["show_price_confirm_time"] = item_f["show_price_confirm_time"]
            # 房型描述
            detail_info["tags"] = ','.join(item_f["tags"])
            # 建筑面积
            detail_info["frames_build_area"] = item_f["frame_build_area"]
            detail_info["detail_url"] = item_f["detail_url"]


            yield detail_info


            # print detail_info

        # resblock表
        resblock_info = data["resblock_info"]

        resblock_info_item = ResblockInfoItem()
        resblock_info_item["rid"] = house_id  # 关联键
        resblock_info_item["insert_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 入库时间
        resblock_info_item["resblock_id"] = resblock_info["resblock_id"]
        resblock_info_item["city_id"] = resblock_info["city_id"]
        resblock_info_item["status"] = resblock_info["status"]
        resblock_info_item["average_price"] = resblock_info["average_price"]
        resblock_info_item["resblock_name"] = resblock_info["resblock_name"]
        resblock_info_item["resblock_alias"] = resblock_info["resblock_alias"]
        resblock_info_item["sale_status"] = resblock_info["sale_status"]
        resblock_info_item["process_status"] = resblock_info["process_status"]
        resblock_info_item["house_type"] = resblock_info["house_type"]
        resblock_info_item["house_type_value"] = resblock_info["house_type_value"]

        resblock_info_item["tags"] = ','.join(resblock_info["tags"])
        desc = []
        for t in resblock_info["project_tags"]:
            desc.append(t["desc"])

        resblock_info_item["description"] = ','.join(desc)

        resblock_info_item["project_name"] = resblock_info["project_name"]
        resblock_info_item["address_remark"] = resblock_info["address_remark"]
        resblock_info_item["administrative_address"] = resblock_info["administrative_address"]
        resblock_info_item["open_date"] = resblock_info["open_date"]
        resblock_info_item["open_date_more"] = resblock_info["open_date_more"]
        resblock_info_item["special_tags"] = ','.join(resblock_info["special_tags"])
        resblock_info_item["developer_company"] = ','.join(resblock_info["developer_company"])
        # 交房时间
        resblock_info_item["hand_over_time"] = resblock_info["hand_over_time"]
        resblock_info_item["properright"] = resblock_info["properright"]
        resblock_info_item["longitude"] = resblock_info["longitude"]
        resblock_info_item["latitude"] = resblock_info["latitude"]
        resblock_info_item["district_id"] = resblock_info["district_id"]
        resblock_info_item["district_name"] = resblock_info["district_name"]
        resblock_info_item["bizcircle_id"] = resblock_info["bizcircle_id"]
        resblock_info_item["bizcircle_name"] = resblock_info["bizcircle_name"]
        resblock_info_item["store_addr"] = resblock_info["store_addr"]
        resblock_info_item["build_type"] = resblock_info["build_type"]
        resblock_info_item["cubage_rate"] = resblock_info["cubage_rate"]
        resblock_info_item["virescence_rate"] = resblock_info["virescence_rate"]
        resblock_info_item["house_amount"] = resblock_info["house_amount"]
        resblock_info_item["overground_car_num"] = resblock_info["overground_car_num"]
        resblock_info_item["underground_car_num"] = resblock_info["underground_car_num"]

        resblock_info_item["property_company"] = ','.join(resblock_info["property_company"])

        resblock_info_item["property_price"] = resblock_info["property_price"]
        resblock_info_item["heating_type"] = resblock_info["heating_type"]
        resblock_info_item["powersuply_kind"] = resblock_info["powersuply_kind"]
        resblock_info_item["watersuply_kind"] = resblock_info["watersuply_kind"]
        resblock_info_item["is_open_date_predict"] = resblock_info["is_open_date_predict"]
        resblock_info_item["is_hand_over_predict"] = resblock_info["is_hand_over_predict"]


        resblock_info_item["lowest_total_price"] = resblock_info["lowest_total_price"]
        resblock_info_item["price_confirm_time"] = resblock_info["price_confirm_time"]

        if len(resblock_info["permit_list"]) > 0:
            for r in resblock_info["permit_list"]:
                resblock_info_item["permit_number"] = r["permit_number"]
                resblock_info_item["permit_time"] = r["permit_time"]
                resblock_info_item["building_list"] = r["building_list"]

        resblock_info_item["show_permit"] = resblock_info["show_permit"]
        resblock_info_item["show_price"] = resblock_info["show_price"]
        resblock_info_item["show_price_unit"] = resblock_info["show_price_unit"]
        resblock_info_item["show_price_desc"] = resblock_info["show_price_desc"]
        resblock_info_item["resblock_frame_area"] = resblock_info["resblock_frame_area"]
        resblock_info_item["show_open_date"] = resblock_info["show_open_date"]
        resblock_info_item["show_hand_over_time"] = resblock_info["show_hand_over_time"]
        resblock_info_item["total_area"] = resblock_info["total_area"]
        resblock_info_item["site_area"] = resblock_info["site_area"]
        resblock_info_item["pid"] = resblock_info["pid"]


        yield resblock_info_item

        # build_info表
        building_info = data["building_info"]

        if len(building_info["build_list"]) > 0:
            for item_b in building_info["build_list"]:
                building_info_item = BuildingInfoItem()
                building_info_item["house_id"] = house_id  # 关联键
                building_info_item["project_name"]=project_name
                building_info_item["insert_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 入库时间
                building_info_item["bid"] = item_b["id"]
                building_info_item["resblock_id"] = item_b["resblock_id"]
                building_info_item["building_code"] = item_b["building_code"]
                building_info_item["part_num"] = item_b["part_num"]
                building_info_item["building_type"] = item_b["building_type"]
                building_info_item["total_unit_count"] = item_b["total_unit_count"]
                building_info_item["total_house_count"] = item_b["total_house_count"]
                building_info_item["floor_height"] = item_b["floor_height"]
                building_info_item["sell_count"] = item_b["sell_count"]
                building_info_item["open_time"] = item_b["open_time"]
                building_info_item["hand_over_time"] = item_b["hand_over_time"]
                building_info_item["sale_status"] = item_b["sale_status"]

                yield building_info_item

                if len(item_b["unit_list"]) > 0:
                    for item_u in item_b["unit_list"]:
                        unit_list_item = UnitInfoItem()
                        unit_list_item["ulid"] = house_id  # 关联键
                        unit_list_item["project_name"]=project_name
                        unit_list_item["insert_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 插入时间
                        unit_list_item["uid"] = item_u["id"]
                        unit_list_item["unit_name"] = item_u["unit_name"]
                        unit_list_item["sorted"] = item_u["sorted"]
                        unit_list_item["overground_floors"] = item_u["overground_floors"]
                        unit_list_item["underground_floors"] = item_u["underground_floors"]
                        unit_list_item["floor_height"] = item_u["floor_height"]
                        unit_list_item["elevator_count"] = item_u["elevator_count"]
                        unit_list_item["floor_house_count"] = item_u["floor_house_count"]

                        yield unit_list_item

    #评论
    def parse_comment(self,response):

        project_name=response.meta["project_name"]

        data=json.loads(response.body)["data"]

        if int(data["total"])>0:
            #评论列表
            for comm in data["list"]:
                comment_info_item = CommentInfoItem()
                #项目标识
                comment_info_item["project_name"]=project_name
                # 周边评分
                comment_info_item["around"]=data["around"]
                # 交通评分
                comment_info_item["traffic"]=data["traffic"]
                # 绿化评分
                comment_info_item["green"] =data["green"]
                # 综合评分
                comment_info_item["composite_score"] =data["composite_score"]
                # 综合评价描述
                comment_info_item["composite_score_info"] =data["composite_score_info"]
                # 评论总数
                comment_info_item["total"] =data["total"]

                comment_info_item["comment_id"]=comm["id"] #评论id
                comment_info_item["project_name"] =comm["project_name"] #项目名
                comment_info_item["user_name"] =comm["user_name"] #评论的用户名
                comment_info_item["user_around"] =comm["around"] #该用户对该楼盘周边的评价
                comment_info_item["user_traffic"] =comm["traffic"]#该用户对该楼盘交通的评价
                comment_info_item["user_green"] =comm["green"]#该用户对该楼盘绿化的评价
                comment_info_item["user_avg"] =comm["avg"]#该用户对该楼盘的平均评价
                comment_info_item["content"] =comm["content"] #该用户的评价
                comment_info_item["ctime"] =comm["ctime"] #评价时间
                comment_info_item["pc_ctime"] =comm["pc_ctime"] #评价时间
                comment_info_item["image"]=','.join(comm["image"]) #评价里的图片
                comment_info_item["phone"] =comm["phone"] #用户手机
                comment_info_item["like_num"] =comm["like_num"] #该评论的点赞数
                comment_info_item["is_interest"] =comm["is_interest"] #转发?
                comment_info_item["show_status"] =comm["show_status"]#显式状态
                comment_info_item["official_reply"] =comm["official_reply"] #官方回复
                comment_info_item["is_anonymity"] =comm["is_anonymity"] #是否匿名
                comment_info_item["is_like"] =comm["is_like"] #是否喜欢
                comment_info_item["uc_avatar"] =comm["uc_avatar"] #头像
                comment_info_item["used_time"] =comm["used_time"] #浏览次数?
                comment_info_item["insert_time"]=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


                yield comment_info_item



        #是否还有更多
        offset = int(re.findall("offset=(\d+)&?", response.url)[0])
        if data["more"]=="1":
            offset += 20
            params = {
                "is_real": "",
                "limit": "20",
                "offset": offset,
                "project_name": project_name,
                "request_ts": int(time.time())
            }

            url = "https://app.api.lianjia.com/newhouse/commentlist?is_real={}&limit={}&offset={}&project_name={}&request_ts={}".format(
                params["is_real"], params["limit"], params["offset"], params["project_name"], params["request_ts"])

            print url

            yield Request(url=url,callback=self.parse_comment,meta={"project_name":project_name})

    #动态信息
    def parse_dynamic(self,response):

        project_name=response.meta["project_name"]

        data=json.loads(response.body)["data"]



        #动态列表
        if len(data["list"])>0:
            for item in data["list"]:
                dynamic_info_item=DynamicInfoItem()
                dynamic_info_item["project_name"]=project_name #项目标识
                dynamic_info_item["total"]=data["total"] # 动态信息总数
                dynamic_info_item["dynamic_id"]=item["id"] #动态信息id
                dynamic_info_item["title"]=item["title"] #信息标题
                dynamic_info_item["time"]=item["time"] #消息发布时间
                dynamic_info_item["content"]=item["content"] #消息内容
                dynamic_info_item["type"]=item["type"] #消息类型
                dynamic_info_item["insert_time"]=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

                yield dynamic_info_item

        #是否有更多
        offset = int(re.findall("offset=(\d+)&?", response.url)[0])
        if data["more"]=="1":
            offset+=10
            dynamic_params = {
                "limit": "10",
                "offset": offset,
                "project_name": project_name,
                "request_ts": int(time.time())
            }

            dynamic_url = "https://app.api.lianjia.com/newhouse/dongtailist?limit={}&offset={}&project_name={}&request_ts={}".format(
                dynamic_params["limit"], dynamic_params["offset"], dynamic_params["project_name"],dynamic_params["request_ts"])

            yield Request(url=dynamic_url, callback=self.parse_dynamic,meta={"project_name":project_name})









