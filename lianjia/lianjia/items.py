# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field



class BasicInfoItem(Item):
    basic_id = Field()
    city_id = Field()
    city_name = Field()
    district_name = Field()
    district_id = Field()
    bizcircle_name = Field()
    process_status = Field()
    resblock_frame_area = Field()
    longitude = Field()
    latitude = Field()
    title = Field()
    resblock_name = Field()
    address = Field()
    avg_unit_price = Field()
    average_price = Field()
    address_remark = Field()
    project_name = Field()
    special_tags = Field()
    min_frame_area = Field()
    max_frame_area = Field()
    count = Field()
    room = Field()
    tags = Field()
    description = Field()
    house_type = Field()
    sale_status = Field()
    has_evaluate = Field()
    has_vr_aerial = Field()
    has_vr_house = Field()
    has_video = Field()
    has_virtual_view = Field()
    lowest_total_price = Field()
    show_price = Field()
    show_price_unit = Field()
    show_price_desc = Field()
    status = Field()
    evaluate_status = Field()
    total_price_start = Field()
    total_price_start_unit = Field()
    avg_price_start = Field()
    avg_price_start_unit = Field()
    insert_time=Field()

class DetailInfoItem(Item):
    fid=Field()  # 关联键
    insert_time=Field()  # 入库时间
    frames_id=Field()
    project_name=Field()
    resblock_id=Field()
    resblock_name=Field()
    frame_name=Field()
    bedroom_count=Field()
    parlor_count=Field()
    cookroom_count=Field()
    total_count=Field()
    toilet_count=Field()
    build_area=Field()
    inside_area=Field()
    frame_structure=Field()
    orientation=Field()
    # is_top=Field()
    # is_show=Field()
    is_main_frame=Field()
    status=Field()
    sell_status=Field()
    sell_status_txt=Field()
    # sell_status_color=Field()
    price=Field()
    total_price_min=Field()
    total_price_max=Field()
    total_price=Field()
    show_price=Field()
    show_price_unit=Field()
    show_price_desc=Field()
    show_price_confirm_time=Field()
    # 房型描述
    tags=Field()
    # 建筑面积
    frames_build_area=Field()
    # share_url=Field()
    # is_followed=Field()
    # virtual_view_url=Field()
    detail_url=Field()
    # 关联项目
    # relation_projects=Field()
    # house_info=Field()
    # evaluate=Field()
    # is_direct_train=Field()


class ResblockInfoItem(Item):
    rid=Field()  # 关联键
    insert_time=Field()  # 入库时间
    resblock_id=Field()
    city_id=Field()
    status=Field()
    average_price=Field()
    resblock_name=Field()
    resblock_alias=Field()
    sale_status=Field()
    process_status=Field()
    house_type=Field()
    house_type_value=Field()
    tags=Field()
    description=Field()
    project_name=Field()
    address_remark=Field()
    administrative_address=Field()
    open_date=Field()
    open_date_more=Field()
    special_tags=Field()
    developer_company=Field()
    # 交房时间
    hand_over_time=Field()
    properright=Field()
    longitude=Field()
    latitude=Field()
    district_id=Field()
    district_name=Field()
    bizcircle_id=Field()
    bizcircle_name=Field()
    store_addr=Field()
    build_type=Field()
    cubage_rate=Field()
    virescence_rate=Field()
    house_amount=Field()
    overground_car_num=Field()
    underground_car_num=Field()
    property_company=Field()
    property_price=Field()
    heating_type=Field()
    powersuply_kind=Field()
    watersuply_kind=Field()
    is_open_date_predict=Field()
    is_hand_over_predict=Field()
    # room=Field()
    # count=Field()
    lowest_total_price=Field()
    price_confirm_time=Field()
    show_price_confirm_time=Field()
    permit_number=Field()
    permit_time=Field()
    building_list=Field()
    show_permit=Field()
    show_price=Field()
    show_price_unit=Field()
    show_price_desc=Field()
    resblock_frame_area=Field()
    show_open_date=Field()
    show_hand_over_time=Field()
    total_area=Field()
    site_area=Field()
    # share_url=Field()
    pid=Field()
    # has_virtual_view=Field()
    # consult_discount_info=Field()

class BuildingInfoItem(Item):
    house_id=Field()  # 关联键
    project_name=Field()
    insert_time=Field()  # 入库时间
    bid=Field()
    resblock_id=Field()
    building_code=Field()
    part_num=Field()
    building_type=Field()
    total_unit_count=Field()
    total_house_count=Field()
    floor_height=Field()
    sell_count=Field()
    open_time=Field()
    hand_over_time=Field()
    sale_status=Field()


class UnitInfoItem(Item):
    ulid=Field()  # 关联键
    project_name=Field()
    insert_time=Field()  # 插入时间
    uid=Field()
    unit_name=Field()
    sorted=Field()
    overground_floors=Field()
    underground_floors=Field()
    floor_height=Field()
    elevator_count=Field()
    floor_house_count=Field()

class CommentInfoItem(Item):
    #总体的
    around=Field()
    traffic=Field()
    green=Field()
    composite_score=Field()
    composite_score_info=Field()
    total=Field()

    #单个用户的
    comment_id=Field()
    project_name=Field()  # 项目名(标识)
    user_name=Field()  # 评论的用户名
    user_around=Field()  # 该用户对该楼盘周边的评价
    user_traffic=Field()  # 该用户对该楼盘交通的评价
    user_green=Field()  # 该用户对该楼盘绿化的评价
    user_avg=Field()  # 该用户对该楼盘的平均评价
    content=Field()  # 该用户的评价
    ctime=Field()  # 评价时间
    pc_ctime=Field()  # 评价时间
    image=Field() # 评价里的图片
    phone=Field()  # 用户手机
    # is_real=Field()
    # ucid=Field()
    # picId=Field()
    like_num=Field()  # 该评论的点赞数
    is_interest=Field()  # 转发?
    show_status =Field() # 显式状态
    # frames=Field()
    official_reply=Field()  # 官方回复
    is_anonymity=Field()  # 是否匿名
    is_like=Field()  # 是否喜欢
    uc_avatar=Field()  # 头像
    # favicon=Field()
    used_time=Field()  # 浏览次数?
    insert_time=Field() #入库时间


class DynamicInfoItem(Item):
    project_name=Field()  # 项目标识
    total=Field() #动态消息总数
    dynamic_id=Field()
    title=Field()
    time=Field()
    content=Field()
    type=Field()
    insert_time=Field()