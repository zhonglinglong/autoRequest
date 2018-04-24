# -*- coding:utf8 -*-
"""
2018年4月11日17:51:28
新增开发自营房源接口
"""

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from common.interface import *


@log
def add_house_delelop(residential_name,room_number=1):
	"""
	新增审核房源
	:param residential_name: 楼盘名称
	:param room_number: 新增开发房源数量,默认1
	:return:
	"""
	null = None

	try:
		sql = """SELECT
		count(*)
		FROM
		residential_building_house_no
		WHERE
		floor_id IN (
			SELECT
				floor_id
			FROM
				residential_building_floor
			WHERE
				unit_id IN (
					SELECT
						unit_id
					FROM
						residential_building_unit
					WHERE
						building_id IN (
							SELECT
								building_id
							FROM
								residential_building
							WHERE
								residential_id IN (
									SELECT
										residential_id
									FROM
										residential
									WHERE
										residential_name = "%s"
								)
						)
				)
		);""" % residential_name

		house_no_len = int(searchSQL(sql)[0][0])

		sql = """SELECT
			house_no_id
		FROM
			residential_building_house_no
		WHERE
			floor_id IN (
				SELECT
					floor_id
				FROM
					residential_building_floor
				WHERE
					unit_id IN (
						SELECT
							unit_id
						FROM
							residential_building_unit
						WHERE
							building_id IN (
								SELECT
									building_id
								FROM
									residential_building
								WHERE
									residential_id IN (
										SELECT
											residential_id
										FROM
											residential
										WHERE
											residential_name = "%s"
									)
							)
					)
			);""" % residential_name
		house_no_id = searchSQL(sql)

		sql = 'SELECT count(*) from house_develop where residential_name like "%s"' % (residential_name+"%")
		old_house_no_len= int(searchSQL(sql)[0][0])

		sql = 'SELECT house_no_id from house_develop where residential_name like "%s"' % (residential_name + "%")
		old_house_no_id = searchSQL(sql)

		sql = "select residential_id from residential where residential_name = '%s' and deleted = 0" % residential_name
		residential_id = searchSQL(sql)[0][0]
	except Exception as e:
		return "查询各种sql报错~~~错误信息：" + str(e)

	if house_no_len == old_house_no_len:
		return u"该楼盘下所有的房间都新增过至少一次，请新增房间号，或者换个楼盘！"
	number = house_no_len - old_house_no_len

	house_no_id_list = []
	for i in range(len(house_no_id)):
		if house_no_id[i] not in old_house_no_id:
			house_no_id_list.append(house_no_id[i][0])

	#查询楼盘信息
	url = "http://isz.ishangzu.com/isz_house/ResidentialController/selectResidentialDetail.action"
	data = {"residential_id":residential_id}
	residential = myRequest(url,str(data),Value=True)["obj"]
	area_code = residential["area_code"]
	area_name = residential["area_name"]
	city_code = residential["city_code"]
	city_name = residential["city_name"]
	residential_id = residential["residential_id"]
	byname = residential["byname"]
	business_circle_name = residential["taBusinessCircleList"][0]["business_circle_name"]
	business_circle_id = residential["taBusinessCircleList"][0]["business_circle_id"]
	address = residential["address"]


	if int(room_number) <= len(house_no_id_list):
		pass
	else:
		room_number = len(house_no_id_list)

	for i in range(int(room_number)):
		url = "http://isz.ishangzu.com/isz_house/HouseController/saveHouseDevelop.action"
		sql = "select building_id,unit_id,floor_id,house_no,rooms,livings,kitchens,bathrooms,balconys from residential_building_house_no where house_no_id = '%s'" % house_no_id_list[i]
		data_list = searchSQL(sql)[0]
		sql = "select building_name from residential_building where building_id = '%s'" % data_list[0]
		building_name = searchSQL(sql)[0][0]
		sql = "select unit_name from residential_building_unit where unit_id = '%s'" % data_list[1]
		unit_name = searchSQL(sql)[0][0]
		sql = "select floor_name from residential_building_floor where floor_id = '%s'" % data_list[2]
		floor_name = searchSQL(sql)[0][0]
		data ={
	"residential_name_search": residential_id,
	"building_name_search": data_list[0],
	"unit_search": data_list[1],
	"house_no_search": house_no_id_list[i],
	"residential_name": residential_name+"（"+byname+"）",
	"building_name": building_name,
	"unit": unit_name,
	"floor": floor_name,
	"house_no": data_list[3],
	"residential_address":city_name + " "+ area_name + " " +  business_circle_name + " " + address,
	"city_code":city_code,
	"area_code": area_code,
	"business_circle_id": business_circle_id,
	"contact": "联系人",
	"did": get_conf("loginUser", "dep_id"),
	"uid":  get_conf("loginUser", "user_id"),
	"house_status": "WAITING_RENT",
	"category": "NOLIMIT",
	"source": "INTRODUCE",
	"rental_price": "5000.00",
	"rooms": data_list[4],
	"livings": data_list[5],
	"kitchens": data_list[6],
	"bathrooms": data_list[7],
	"balconys": data_list[8],
	"build_area": "100",
	"orientation": "NORTH",
	"property_type": "HIGH_LIFE",
	"property_use": "HOUSE",
	"fitment_type": "FITMENT_ROUGH",
	"remark": "备注",
	"look_type": "DIRECTION",
	"residential_id": residential_id,
	"building_id": data_list[0],
	"unit_id": data_list[1],
	"floor_id": data_list[2],
	"house_no_id": house_no_id_list[i],
	"business_circle_name": business_circle_name,
	"contact_tel": get_conf("loginUser", "user")}
		myRequest(url,str(data),Value=True)

		url = "http://erp.ishangzu.com/isz_house/HouseController/selectHouseDevelopDetail.action"
		sql = "select house_develop_id from house_develop where residential_name like '%s' ORDER BY create_time desc limit 1" % (residential_name+"%")
		house_develop_id = searchSQL(sql)
		data = {"house_develop_id":house_develop_id[0][0]}
		house_develop = myRequest(url,str(data),Value=True)["obj"]

		balconys = house_develop["balconys"]
		bathrooms = house_develop["bathrooms"]
		build_area = house_develop["build_area"]
		building_id = house_develop["building_id"]
		building_name = house_develop["building_name"]
		floor_id = house_develop["floor_id"]
		floor = house_develop["floor"]
		house_no = house_develop["house_no"]
		house_no_id = house_develop["house_no_id"]
		kitchens = house_develop["kitchens"]
		livings = house_develop["livings"]
		residential_dep_id = house_develop["residential_dep_id"]
		residential_id = house_develop["residential_id"]
		residential_names = house_develop["residential_name"]
		unit = house_develop["unit"]
		unit_id = house_develop["unit_id"]
		update_time = house_develop["update_time"]

		url = "http://erp.ishangzu.com/isz_house/HouseController/auditHouseDevelop.action"
		data = {
	"area_code": area_code,
	"audit_content": "Agree",
	"audit_status": "PASS",
	"balconys": balconys,
	"bathrooms": bathrooms,
	"build_area": build_area,
	"building_id": building_id,
	"building_name": building_name ,
	"building_name_search": building_id,
	"category": "NOLIMIT",
	"city_code": city_code,
	"fitment_type": "FITMENT_ROUGH",
	"floor": floor,
	"floor_id": floor_id,
	"houseRent": {
		"category": "NOLIMIT",
		"house_status": "WAITING_RENT",
		"look_date": null,
		"look_type": "DIRECTION",
		"rental_price": 5000,
		"source": "INTRODUCE"
	},
	"house_develop_id": house_develop_id[0][0],
	"house_no": house_no,
	"house_no_id": house_no_id,
	"house_no_search": house_no_id,
	"house_no_suffix": null,
	"house_status": "WAITING_RENT",
	"kitchens": kitchens,
	"livings": livings,
	"look_date": null,
	"look_type": "DIRECTION",
	"orientation": "NORTH",
	"property_use": "HOUSE",
	"property_type": "HIGH_LIFE",
	"rental_price": 5000,
	"residential_address": city_name + " "+ area_name + " " +  business_circle_name + " " + address,
	"residential_department_did": residential_dep_id,
	"residential_id": residential_id,
	"residential_name": residential_names,
	"residential_name_search": residential_id,
	"remark": "test",
	"rooms": 1,
	"source": "INTRODUCE",
	"unit": unit,
	"unit_id": unit_id,
	"unit_search":unit_id,
	"update_time": update_time}
		myRequest(url,str(data),Value=True)

	if number >= int(room_number):
		return u"新增" + str(room_number)+"间房源成功"
	else:
		return u"新增" + str(number)+"间房源成功，PS：总共才剩余"+ str(number)+"间房可以新增"




