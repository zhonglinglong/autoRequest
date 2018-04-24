# -*- coding:utf8 -*-

# Author : Zhong Ling Long
# Create on : 2018年3月28日13:45:46

"""
2018年4月11日17:51:35
erp楼盘接口
"""

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from common.interface import *
host_set("test")
get_cookie()


@log
def add_residential(residential_name):
	"""
	新增楼盘
	:param residential_name:楼盘名称
	:return:
	"""
	try:
		sql = "SELECT sd.parent_id from sys_department sd INNER JOIN sys_user sur on sur.dep_id = sd.dep_id INNER JOIN sys_position spt on spt.position_id = sur.position_id " \
			  "where sd.dep_district = '330100' and sd.dep_id <> '00000000000000000000000000000000' and (spt.position_name like '资产管家%' or spt.position_name like '综合管家%') " \
			  "ORDER BY RAND() LIMIT 1"
		parent_id = searchSQL(sql)[0][0]
	except Exception as e:
		return "查询责任部门sql报错，sql:" + sql + "错误返回：" + str(e)

	url = "http://isz.ishangzu.com/isz_house/ResidentialController/saveResidential.action"
	data = {
	"residential_name": residential_name,
	"residential_jianpin": "xqzxcslp",
	"city_code": "330100",
	"area_code": "330108",
	"taBusinessCircleString": "4",
	"address": "海创基地南楼",
	"gd_lng": "120.138631",
	"gd_lat": "30.186537",
	"property_type": "ordinary",
	"taDepartString": parent_id,
	"build_date": "1975",
	"totle_buildings": "50",
	"total_unit_count": "200",
	"total_house_count": "4000",
	"build_area": "5000.00",
	"property_company": "我是物业公司",
	"property_fee": "2",
	"plot_ratio": "20.00",
	"green_rate": "30.00",
	"parking_amount": "2500",
	"other_info": "我是楼盘亮点",
	"bus_stations": "我是公交站",
	"metro_stations": "我是地铁站",
	"byname": "cs"}
	result = myRequest(url,str(data),Value=True)
	if result["code"] == 0:
		return "新增楼盘名称为：" + residential_name + "。提交成功！"
	else:
		return "新增楼盘名称为：" + residential_name + "。提交失败！错误返回：" + result["obj"]

@log
def add_residential_number(residential_name,number,house_nos):
	#生成楼盘，不管有没有该楼盘
	add_residential(residential_name)

	#新增栋座
	try:
		sql = "select residential_id from residential WHERE residential_name='%s' and deleted=0" % residential_name
		residential_id = searchSQL(sql)[0][0]
	except Exception as e:
		return "查询楼盘sql报错,sql:" + sql + "错误返回：" + str(e)
	url = 'http://isz.ishangzu.com/isz_house/ResidentialBuildingController/saveResidentialBuildingNew.action'
	data = {"property_name": residential_name,
		"building_name": "1幢",
		"no_building": "无",
		"gd_lng": "120.152476",
		"gd_lat": "30.287232",
		"housing_type": "ordinary",
		"ground_floors": "20",
		"underground_floors": "2",
		"ladder_count": "10",
		"house_count": "200",
		"residential_id": residential_id,
		"have_elevator": "Y"}
	myRequest(url,str(data),Value=True)

	#新增单元
	try:
		sql = "SELECT building_id  from residential_building where residential_id ='%s'and deleted=0 " % residential_id
		building_id = searchSQL(sql)[0][0]
	except Exception as e:
		return "查询栋座sql报错,sql:" + sql + "错误返回：" + str(e)
	url = 'http://isz.ishangzu.com/isz_house/ResidentialBuildingController/saveResidentialBuildingUnit.action'
	data = {"property_name": residential_name+ '1幢',"unit_name": "A","no_unit": "无","building_id": building_id}
	myRequest(url,str(data),Value=True)

	#新增楼层
	try:
		sql = "SELECT unit_id from  residential_building_unit where  building_id='%s' " % building_id
		unit_id = searchSQL(sql)[0][0]
	except Exception as e:
		return "查询单元sql报错,sql:" + sql + "错误返回：" + str(e)
	url = 'http://isz.ishangzu.com/isz_house/ResidentialBuildingController/saveResidentialBuildingFloor.action'
	data = {"property_name":residential_name+ '1幢A',"floor_name":"1","building_id":building_id,"unit_id":unit_id }
	myRequest(url, str(data), Value=True)

	#新增房间号
	try:
		sql = "SELECT floor_id from residential_building_floor where unit_id='%s' " % unit_id
		floor_id = searchSQL(sql)[0][0]
		house_no = house_nos
		url = 'http://isz.ishangzu.com/isz_house/ResidentialBuildingController/saveResidentialBuildingHouseNo.action'
		for i in range(int(number)):
			house_no = house_no + 1
			data = {
	"property_name": residential_name+'1幢A1层',
	"house_no": house_no,
	"rooms": "1",
	"livings": "1",
	"bathrooms": "1",
	"kitchens": "1",
	"balconys": "1",
	"build_area": "100.00",
	"orientation": "NORTH",
	"building_id": building_id,
	"unit_id": unit_id,
	"floor_id": floor_id}
			myRequest(url,str(data),Value=True)
	except Exception as e:
		return "新增房间接口报错。错误返回：" + str(e)
		pass
	return "批量新增房间成功！"

