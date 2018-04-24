# -*- coding:UTF-8 -*-

"""
author = crazyzhong
2018年4月11日10:02:10
爱上租ERP工程管理接口
"""

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from common.interface import *


@log
def add_delivered_house(contract_num,room_number=3,Value=True,number=-60):
	"""
	交房
	:param contract_num: 委托合同号
	:param room_number: 分割数量
	:param Value:True需要交房，Fasle,不交房
	:param number:完成流程的日期 0 是今天
	:return:
	"""
	now_times = now_time(number)
	null = None
	true = True
	#下单
	url = "http://decorate.ishangzu.com/isz_decoration/NewDecorationProjectController/changeProgress/placeOrder"
	place_order_date = now_times + " 10:09:54"
	predict_survey_date = now_times + " 11:00"
	try:
		sql = 'SELECT project_id from new_decoration_project where info_id = (SELECT info_id from decoration_house_info where contract_num = "%s")' % contract_num
		project_id = searchSQL(sql,db="decoration")[0][0]
	except Exception as e:
		return "查询委托工程信息sql报错，sql:" + sql + "错误返回：" + str(e)
	data = {
	"place_order_dep": "8A2152435E2E34E5015E30F811BB2653",
	"place_order_reason": "测试下单原因",
	"place_order_uid": "1444",
	"place_order_uname": "测试专用 勿改",
	"place_order_date": place_order_date,
	"predict_survey_date": predict_survey_date,
	"project_id": project_id}
	myRequest(url,str(data))

	#派单
	#装配专员
	url = "http://decorate.ishangzu.com/isz_decoration/AssembleAreaController/searchAssemblyPerson"
	data = {"city_code":"330100"}
	result = myRequest(url,str(data),Value=True)["obj"][0]
	construct_uname = result["user_name"]
	construct_uid = result["user_id"]
	#供应商
	url = "http://decorate.ishangzu.com/isz_decoration/DecorationProjectController/suppliers?city_code=330100&supplier_type=STUFF"
	result = myRequest(url,method="get",Value=True)["obj"][0]
	supplier_name = result["item_name"]
	supplier_id = result["item_id"]
	#工长
	url = "http://decorate.ishangzu.com/isz_decoration/DecorationProjectController/supplier/"+ supplier_id + "/persons?supplier_person_type=MANAGER&supplier_id=" + supplier_id
	result = myRequest(url, method="get",Value=True)["obj"][0]
	supplier_uname = result["item_name"]
	supplier_uid = result["item_id"]
	#派单
	url = "http://decorate.ishangzu.com/isz_decoration/NewDecorationProjectController/changeProgress/dispatchOrder"
	data = {
	"construct_uid": construct_uid,
	"construct_uname": construct_uname,
	"dispach_remark": "派单备注",
	"project_id": project_id,
	"supplier_id": supplier_id,
	"supplier_uid": supplier_uid,
	"predict_survey_date": "",
	"supplier_name": supplier_name,
	"supplier_uname": supplier_uname}
	myRequest(url,str(data))

	#接单
	url = "http://decorate.ishangzu.com/isz_decoration/NewDecorationProjectController/changeProgress/acceptOrder"
	data = {"project_id":project_id}
	myRequest(url,str(data))

	#量房
	url = "http://decorate.ishangzu.com/isz_decoration/NewDecorationProjectController/survey/score"
	picture = eval(json.dumps(eval(get_conf("picture", get_conf("testCondition", "test")))))
	data = {
	"grade": "3",
	"project_id": project_id,
	"reform_way_fact": "REFORM",
	"score_remark": "",
	"attachments": [{
		"attach_type": "TOILET",
		"imgs": []
	}, {
		"attach_type": "KITCHEN",
		"imgs": []
	}, {
		"attach_type": "LIVING_ROOM",
		"imgs": []
	}, {
		"attach_type": "ROOM",
		"imgs": []
	}, {
		"attach_type": "OTHER",
		"imgs": [{
			"url": picture[0]["url"],
			"img_id": picture[0]["img_id"],
			"create_name": "",
			"create_dept": "",
			"create_time": "",
			"sort": 0,
			"type": "OTHER"
		}]
	}]}
	myRequest(url,str(data))

	#勘测
	url = "http://decorate.ishangzu.com/isz_decoration/NewDecorationProjectController/survey/profee"
	data = {
	"air_switch": "",
	"door_card": "",
	"door_key": "",
	"electricity_card": "",
	"electricity_meter_num": "",
	"electricity_meter_remain": "",
	"gas_card": "",
	"gas_meter_num": "",
	"gas_meter_remain": "",
	"project_id": project_id,
	"water_card": "",
	"water_card_remain": "",
	"water_meter_num": "",
	"attachments": [{
		"attach_type": "PROPERTY_DELIVERY_ORDER",
		"imgs": [{
			"url": picture[0]["url"],
			"img_id": picture[0]["img_id"],
			"create_name": "",
			"create_dept": "",
			"create_time": "",
			"sort": 0,
			"type": ""
		}]
	}],
	"resource": "SURVEY"}
	myRequest(url,str(data))

	#闭水试验
	url = "http://decorate.ishangzu.com/isz_decoration/NewDecorationProjectController/survey/closed"
	data = {
	"remark": "闭水试验备注",
	"attachments": [{
		"attach_type": "SCENE",
		"imgs": [{
			"url": picture[0]["url"],
			"img_id": picture[0]["img_id"],
			"create_name": "",
			"create_dept": "",
			"create_time": "",
			"sort": 0,
			"type": ""
		}]
	}],
	"project_id": project_id,
	"closed_water_test_result": "Y"}
	myRequest(url,str(data))

	#项目方案
	#查询房间号及创建房间
	url = "http://decorate.ishangzu.com/isz_decoration/decoFunctionZoneController/getRoomNoByZoneType/ROOM"
	result = myRequest(url,method="get",Value=True)["obj"]
	zoneList = []
	for i in range(room_number):
		room = {
			"zone_type": "ROOM",
			"zone_type_name": "房间",
			"room_no": "METH",
			"room_no_name": "甲",
			"zone_orientation": "NORTH",
			"zone_orientation_name": "北",
			"have_toilet": "WITHOUT",
			"have_toilet_name": "-",
			"have_balcony": "WITHOUT",
			"have_balcony_name": "-",
			"have_window_name": "-",
			"zone_status_name": "已创建",
			"zone_status": "FOUND",
			"usearea": "33",
			"window_type": "WITHOUT",
			"zone_id": ""}
		room["room_no_name"] = result[i]["keyCn"]
		room["room_no"] = result[i]["keyEn"]
		zoneList.append(room)

	try:
		sql = "SELECT info_id from decoration_house_info where contract_num ='%s'" % contract_num
		info_id = searchSQL(sql,db="decoration")[0][0]
	except Exception as e:
		return "查询房屋信息sql报错,sql:" + sql + "错误返回：" + str(e)

	try:
		sql = "SELECT project_no from new_decoration_project where project_id ='%s'" % project_id
		project_no = searchSQL(sql,db="decoration")[0][0]
	except Exception as e:
		return "查询工程管理信息sql报错,sql:" + sql + "错误返回：" + str(e)
	url = "http://decorate.ishangzu.com/isz_decoration/decoHouseInfoController/saveOrUpdateApartment/updateApartment/projectOrder"
	data = {
	"build_area": "136.8",
	"reform_way_fact": "REFORM",
	"decoration_style": "DWELLING_MAX",
	"house_orientation": "SOURTH",
	"remould_rooms": room_number,
	"remould_livings": "0",
	"remould_kitchens": "0",
	"remould_bathrooms": "0",
	"remould_balconys": "0",
	"info_id": info_id ,
	"module_type": "projectOrder",
	"handle_type": "updateApartment",
	"project_id": project_id,
	"project_no": project_no,
	"entrust_type": "ENTIRE"}
	data["zoneList"] = zoneList
	myRequest(url,str(data))

	#配置清单
	#供应商
	url = "http://decorate.ishangzu.com/isz_decoration/SupplierProductController/querySupplierId"
	data = {"category_one_id":"8A2152435CF46E82015CF86E019E002C","city_code":"330100"}
	result = myRequest(url,str(data),Value=True)["obj"][0]
	supplier_name = result["item_name"]
	supplier_id = result["item_id"]

	#获取房间id
	url = 'http://decorate.ishangzu.com/isz_decoration/NewConfigurationController/queryZone/%s' % project_id
	result = myRequest(url, method='get',Value=True)

	zoneInfo = result['obj']
	for i in zoneInfo:
		if i['function_zone'] == u'甲':
			zone_id = i['zone_id']

	#新增配置清单
	url = "http://decorate.ishangzu.com/isz_decoration/NewDecorationConfigController/confirm"
	data = [{
		"acceptance_num": null,
		"acceptance_num_this": null,
		"acceptance_time": null,
		"brand_id": null,
		"brand_name": "爱上租定制",
		"category_flag": null,
		"category_one_id": null,
		"category_one_len": null,
		"category_one_nm": "家具",
		"category_two_id": null,
		"category_two_nm": "书桌",
		"config_list_id": null,
		"config_list_status": null,
		"config_list_status_name": null,
		"create_name": null,
		"create_time": null,
		"create_uid": null,
		"deleted": null,
		"flag": null,
		"function_zone": "甲",
		"function_zone_len": null,
		"new_replenish_id": null,
		"order_type": null,
		"predict_delivery_date": null,
		"project_id": project_id,
		"purchase_num": "1",
		"purchase_order_no": null,
		"real_delivery_time": null,
		"remark": null,
		"remark_accept": null,
		"remark_return": null,
		"replacement_order": null,
		"return_num": null,
		"return_num_this": null,
		"standard_id": null,
		"standard_name": "0.86M（3.0）",
		"submit_time": null,
		"supplier_id": supplier_id,
		"supplier_name": supplier_name,
		"total_account": null,
		"total_paid": 285,
		"unit_id": null,
		"unit_name": "张",
		"unit_price": 285,
		"update_time": null,
		"update_uid": null,
		"zone_id": zone_id,
		"index": 0,
		"disabled": true}]
	myRequest(url,str(data))
	#提交订单
	url = "http://decorate.ishangzu.com/isz_decoration/NewDecorationConfigController/submitOrder"
	data =[{
	"predict_delivery_date": now_times+" 12:00:00",
	"project_id": project_id,
	"supplier_id": supplier_id,
	"supplier_name": supplier_name}]
	myRequest(url, str(data))
	#验收订单
	url = 'http://decorate.ishangzu.com/isz_decoration/NewDecorationConfigController/supplierOrdersDetail'
	data = {"project_id": project_id, "supplier_id": supplier_id}
	result = myRequest(url, str(data),Value=True)["obj"]
	result[0]["real_delivery_time"] = now_times + " 13:37:03"
	url = "http://decorate.ishangzu.com/isz_decoration/NewDecorationConfigController/acceptance/confirm"
	myRequest(url, str(result))
	#不做硬装清单
	url = "http://decorate.ishangzu.com/isz_decoration/NewDecorationProjectController/changeProgress/judgeConfigList"
	data = {"has_configs":"Y","project_id":project_id}
	myRequest(url,str(data))

	#整体验收
	url = "http://decorate.ishangzu.com/isz_decoration/NewDecorationProjectController/proCheck/wholeCheck"
	data = {
	"air_switch": null,
	"attachments": null,
	"card_attachs": [{
		"attach_type": "CARDS",
		"imgs": []
	}],
	"closed_water_test_result": null,
	"curOneLevelNode": null,
	"curTwoLevelNode": null,
	"door_card": null,
	"door_key": null,
	"electricity_card": null,
	"electricity_meter_num": null,
	"electricity_meter_remain": null,
	"gas_card": null,
	"gas_meter_num": null,
	"gas_meter_remain": null,
	"grade": null,
	"landlordGoods": null,
	"newStuffList": null,
	"overall_check_date": now_times+ " 14:00:00",
	"project_id": project_id,
	"remark": "",
	"score_remark": null,
	"three_attachs": [{
		"attach_type": "THREE",
		"imgs": [{
			"url": picture[0]["url"],
			"img_id": picture[0]["img_id"],
			"create_name": "",
			"create_dept": "",
			"create_time": "",
			"sort": 0,
			"type": ""
		}]
	}],
	"water_card": null,
	"water_card_remain": null,
	"water_meter_num": null}
	myRequest(url, str(data))

	#项目验收
	url = "http://decorate.ishangzu.com/isz_decoration/NewDecorationProjectController/proCheck/profee"
	data = {
	"air_switch": "",
	"door_card": "",
	"door_key": "",
	"electricity_card": "",
	"electricity_meter_num": "",
	"electricity_meter_remain": "",
	"gas_card": "",
	"gas_meter_num": "",
	"gas_meter_remain": "",
	"project_id": project_id,
	"water_card": "",
	"water_card_remain": "",
	"water_meter_num": "",
	"attachments": [{
		"attach_type": "PROPERTY_DELIVERY_ORDER",
		"imgs": [{
			"url": picture[0]["url"],
			"img_id": picture[0]["img_id"],
			"create_name": "",
			"create_dept": "",
			"create_time": "",
			"sort": 0,
			"type": ""
		}]
	}],
	"resource": "PROJECT_CHECK"}
	myRequest(url, str(data))

	#房屋室内图
	#查看房间
	url = "http://decorate.ishangzu.com/isz_decoration/NewDecorationProjectController/searchAllZoneByInfoId/" + str(info_id)
	result = myRequest(url,method="get",Value=True)["obj"]
	house_attachs = []
	for i in range(len(result)):
		houses = {
		"attach_type": result[i]["room_no"],
		"imgs": [{
			"url": picture[0]["url"],
			"img_id": picture[0]["img_id"],
			"create_name": "",
			"create_dept": "",
			"create_time": "",
			"sort": i,
			"type": result[i]["room_no"]
		}]}
		house_attachs.append(houses)
	url = "http://decorate.ishangzu.com/isz_decoration/NewDecorationProjectController/proComp/indoor"
	data = {
	"curOneLevelNode": null,
	"curTwoLevelNode": null,
	"deliver_room_date": null,
	"layout_attachs": [{
		"attach_type": "LAYOUT",
		"imgs": [{
			"url": picture[0]["url"],
			"img_id":picture[0]["img_id"],
			"create_name": "",
			"create_dept": "",
			"create_time": "",
			"sort": 0,
			"type": ""
		}]
	}],
	"project_id": project_id,
	"remark": null}
	data["house_attachs"] = house_attachs
	myRequest(url,str(data))

	#交房
	url = "http://decorate.ishangzu.com/isz_decoration/NewDecorationProjectController/proComp/delivery"
	data = {"deliver_room_date":now_times+" 17:08:58","project_id":project_id,"remark":""}
	if Value:
		result = myRequest(url,str(data),Value=True)
		if result["code"] == 0:
			return "委托合同:" + contract_num + "完成工程订单所有流程！"
		else:
			return "委托合同:" + contract_num + "完成工程订单流程异常！接口返回：" + result["obj"]
	elif Value == False:
		return  u"委托合同在工程订单中处于待交房状态"






