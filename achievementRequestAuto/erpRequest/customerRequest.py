# -*- coding:utf8 -*-
"""
2018年4月10日17:42:22
__auto__ == zhonglinglong
爱上租ERP客户管理模块接口
"""

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from common.interface import *
import time


@log
def add_customer(name,phone):
	"""
	新增租客
	:param name:租客姓名
	:param phone: 租客电话
	:return:obj
	"""
	rent_date = str(time.strftime('%Y-%m-%d',time.localtime(time.time())))
	url = "http://isz.ishangzu.com/isz_customer/CustomerController/saveCustomer.action"
	data = {
	"customer_name": name,
	"phone": phone,
	"customer_status": "EFFECTIVE",
	"email": "zhonglinglong@ishangzu.com",
	"belong_did": get_conf("loginUser", "dep_id"),
	"belong_uid": get_conf("loginUser", "user_id"),
	"customer_from": "GANJICOM",
	"rent_class": "NOCLASS",
	"rent_type": "GATHERHOUSE",
	"rent_use": "RESIDENCE",
	"rent_fitment": "FITMENT_SIMPLE",
	"city_code": "330100",
	"rent_area_code": "330102",
	"rent_business_circle_ids": "35",
	"rent_rooms": "1",
	"rent_livings": "1",
	"rent_bathrooms": "1",
	"rent_from_price": "0.00",
	"rent_to_price": "6000.00",
	"rent_date": rent_date,
	"rent_people": "1",
	"area": "40",
	"gender": "MALE",
	"marriage": "UNMARRIED",
	"submit_channels": "ERP"}
	result = myRequest(url,str(data),Value=True)
	if result["code"] == 0:
		return "新增手机：" + str(phone) +"。租客成功！"
	else:
		return "新增手机：" + str(phone) +"。租客失败！错误返回：" + result["obj"]


