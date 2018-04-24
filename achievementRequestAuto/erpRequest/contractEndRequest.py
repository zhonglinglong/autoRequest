# -*- coding:UTF-8 -*-

"""
author = crazyzhong
2018年4月14日14:10:35
爱上租ERP合同终止结算
"""

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from common.interface import *


@log
def apartment_contract_end(contract_num,rent_end_date,end_type,end_date=now_time()):
	"""
	出租合同终止结算
	:param contract_num:出租合同名称
	:param rent_end_date: 出租合同到期日
	:param end_type:终止类型
	:param end_date:终止日期
	:return:
	"""

	if end_type == "正退":
		#类型明细，终止原因
		end_type_detail = None
		end_reason = None
	elif end_type == "退租":
		end_type_detail = "CUSTOMER_BREAK_CONTRACT"
		end_reason = "CANT_DO_PROMISE"
	elif end_type == "转租" or end_type == u"换租" :
		end_type_detail = None
		end_reason = "CANT_DO_PROMISE"
	elif end_type == "收房":
		end_type_detail = None
		end_reason =  "ARREARAGE"

	picture = eval(json.dumps(eval(get_conf("picture", get_conf("testCondition", "test")))))
	end_type = get_conf("house_contract_type",end_type)

	try:
		sql = "select contract_id from apartment_contract where contract_num = '%s'" % contract_num
		contract_id = searchSQL(sql)[0][0]
	except Exception as e:
		return "查询出租合同sql报错。sql:" + sql + "错误返回：" + str(e)


	#查询出租终止合同款项结算
	url = "http://erp.ishangzu.com/isz_contract/ContractEndController/settlementOfContract"
	data = {"contract_id":contract_id,"end_date":end_date,"end_type":end_type}
	apartmentContractEndReceivableList = myRequest(url,str(data),Value=True)["obj"]

	if end_type == "COLLECTHOUSE":
		apartmentContractEndReceivableList[3]["balance_amount"] = -50000

	#查询出租终止合同基本信息
	url = "http://erp.ishangzu.com/isz_contract/ContractEndController/searchContractEndInfo"
	data = {"contract_id":contract_id,"is_old_data":"N"}
	result = myRequest(url,str(data),Value=True)["obj"]
	detailList = result["detailList"]
	endBasicInfo = result["endBasicInfo"]

	#获取liquidateOrTurnFee
	url = "http://erp.ishangzu.com/isz_contract/ContractEndController/calculateLiquidatedOrTurnFee"
	data = {"contract_id":contract_id,"end_type":end_type,"end_type_detail":end_type_detail}
	result = myRequest(url,str(data),Value=True)["obj"]
	liquidatedOrTurnFee = {}
	liquidatedOrTurnFee["liquidatedOrTurnFee"] = {
		"liquidated_receivable": result["liquidated_receivable"],
		"discount_liquidated_receivable": result["discount_liquidated_receivable"],
		"liquidated_discount_scale": "100.00%",
		"turn_receivable": result["turn_receivable"],
		"discount_turn_receivable": result["discount_turn_receivable"],
		"turn_discount_scale": 0,
		"liquidated_return": result["liquidated_return"],
		"fileList": [{
			"create_time": now_time() + " 14:15:04",
			"create_uid": get_conf("loginUser", "user_id"),
			"deleted": 0,
			"img_id": picture[0]["img_id"],
			"src": picture[0]["src"],
			"update_time": now_time() + " 14:15:04",
			"update_uid": get_conf("loginUser", "user_id"),
			"url": picture[0]["src"]
		}],
		"discount_img_id": None,
		"discountImgList": [{
			"img_id": picture[0]["img_id"],
			"src": picture[0]["src"]
		}],
		"discount_img_src": None
	}

	#提交终止结算
	url = "http://erp.ishangzu.com/isz_contract/ContractEndController/saveOrUpdateApartmentContractEnd"
	data = {"imgList": [{
		"attachment_type": None,
		"img_id":  picture[0]["img_id"],
		"src": picture[0]["src"]
	}],
		"loanFee": {
			"is_show": None
		},
		"receiverInfo": {
			"contractEndPayerAgintType": "PAYER",
			"receipt_name": "testauto",
			"pay_object": "PERSONAL",
			"receipt_bank_no": "622848156",
			"bank": "未知发卡银行",
			"receipt_bank_location": "测试"}
	}

	data["apartmentContractEndReceivableList"] = apartmentContractEndReceivableList
	data["detailList"] = detailList
	data["endBasicInfo"] = endBasicInfo
	data["liquidatedOrTurnFee"] = liquidatedOrTurnFee["liquidatedOrTurnFee"]
	data ["endBasicInfo"]["end_reason"] = end_reason
	data["endBasicInfo"]["receivable_date"] = now_time() + " 16:00:00"
	data["endBasicInfo"]['end_reason_remark'] = u"终止原因"
	data["endBasicInfo"]['contract_id'] = contract_id
	data["endBasicInfo"]['end_contract_num'] = u"终止协议" + random_name()[14:17]
	data["endBasicInfo"]['receivable_total'] = 33680
	data["endBasicInfo"]['end_date'] = end_date + " 00:00:00"
	data["endBasicInfo"]['remark'] = u"备注"
	data["endBasicInfo"]['is_old_data'] = "N"
	data["endBasicInfo"]['end_type'] = end_type
	data["endBasicInfo"]['payable_totle'] = 0
	data["endBasicInfo"]["end_type_detail"] = end_type_detail

	try:
		sql = 'SELECT contract_num from house_contract where house_id = (SELECT house_id from apartment_contract where contract_num= "%s")' % contract_num
		data["endBasicInfo"]['house_contract_num'] = searchSQL(sql)[0][0]
	except Exception as e:
		return "查询委托合同sql报错，sql:" + sql + "。返回错误：" + str(e)

	result = myRequest(url,str(data),Value=True)
	if result["code"] == 0:
		return  "出租合同名称："+ contract_num +"提交终止结算成功！"
	else:
		return "出租合同提交终止结算提交失败。错误返回：" + str(result)



@log
def house_contract_end(contract_num,end_type,payable_date):
	"""
	委托合同终止结算
	:param contract_num:委托合同号
	:param end_type:终止类似，正退，公司违约，业主违约
	:param payable_date:终止日期
	:return:
	"""
	null = None
	picture = eval(json.dumps(eval(get_conf("picture", get_conf("testCondition", "test")))))

	try:
		sql = "select contract_id from house_contract where contract_num = '%s'" % contract_num
		contract_id = searchSQL(sql)[0][0]
	except Exception as e:
		return "查询委托合同sql报错。sql:" + sql +"。错误返回：" + str(e)

	#委托合同终止基础数值
	url = "http://erp.ishangzu.com/isz_housecontract/houseContractEndController/searchHouseContractEndMsg/" + contract_id
	house_contract_list = myRequest(url,method="get",Value=True)["obj"]

    #提交委托合同终止结算
	url = "http://erp.ishangzu.com/isz_housecontract/houseContractEndController/saveHouseContractEnd"
	data = {
	"achieve_audit_status": null,
	"address": house_contract_list["address"],
	"apartment_type": null,
	"audit_status": null,
	"audit_time": null,
	"audit_uid": null,
	"bank": null,
	"building_name": house_contract_list["building_name"],
	"company_no": "还款公司",
	"complement_status": null,
	"complete_money": null,
	"complete_remark": null,
	"complete_time": null,
	"contractImgList": [{
		"src": picture[0]["src"],
		"url": picture[0]["src"],
		"type": "",
		"img_id": picture[0]["img_id"]
	}],
	"contract_id": house_contract_list["contract_id"],
	"contract_num": house_contract_list["contract_num"],
	"create_time": null,
	"create_uid": null,
	"delay_date": house_contract_list["delay_date"],
	"deleted": null,
	"delivery_code": null,
	"dids": null,
	"end_balance_type": null,
	"end_contract_num": "终止合同号"+random_name()[14:18],
	"end_dName": house_contract_list["end_dName"],
	"end_date": now_time()+" 00:00:00",
	"end_dep_name": null,
	"end_did": house_contract_list["end_did"],
	"end_id": null,
	"end_reason": null,
	"end_type": get_conf("house_contract_type",end_type),
	"end_uName": house_contract_list["end_uName"],
	"end_uid": house_contract_list["end_uid"],
	"end_user_name": null,
	"entrust_end_date": house_contract_list["entrust_end_date"],
	"entrust_start_date": house_contract_list["entrust_start_date"],
	"entrust_type": null,
	"financial_provide_money": null,
	"fitment_charge": house_contract_list["fitment_charge"],
	"fitment_charge_remark": "装修扣款备注",
	"floor": house_contract_list["floor"],
	"houseContractEndReturnList": [],
	"house_code": house_contract_list["house_code"],
	"house_id": house_contract_list["house_id"],
	"house_no": house_contract_list["house_no"],
	"landlord_name": house_contract_list["landlord_name"],
	"no_charge": house_contract_list["no_charge"],
	"no_charge_remark": "未扣款项备注",
	"other": house_contract_list["other"],
	"other_remark": "其他备注",
	"pay_bank": "测试",
	"pay_bank_no": "6228448151615",
	"pay_emp_bank_location": null,
	"pay_emp_bank_no": null,
	"pay_emp_name": null,
	"pay_name": "测试",
	"pay_object": "PERSONAL",
	"pay_owner": null,
	"pay_owner_bank_location": null,
	"pay_owner_bank_no": null,
	"pay_type": "OWNER",
	"payable_date": payable_date + " 00:00:00",
	"payable_totle": null,
	"payerType": null,
	"penalty": house_contract_list["penalty"],
	"penalty_remark": "违约金赔入备注",
	"real_due_date": null,
	"receipt_bank_location": null,
	"receipt_bank_no": null,
	"receipt_name": null,
	"receivable_date": payable_date + " 00:00:00",
	"receivable_total": null,
	"remark": "终止结算备注",
	"repair_charge": house_contract_list["repair_charge"],
	"repair_charge_remark": null,
	"residential_name": house_contract_list["residential_name"],
	"return_company": null,
	"return_emp_name": null,
	"return_rent": house_contract_list["return_rent"],
	"return_rent_remark": "返还房租备注",
	"server_manage_did": null,
	"server_manage_uid": null,
	"sign_body": house_contract_list["sign_body"],
	"sign_body_en": house_contract_list["sign_body_en"],
	"sign_dep_name": house_contract_list["sign_dep_name"],
	"sign_did": null,
	"sign_name": house_contract_list["sign_name"],
	"sign_uid": null,
	"submit_audit_time": null,
	"submit_audit_uid": null,
	"suffix": null,
	"uids": null,
	"unit": house_contract_list["unit"],
	"update_time": null,
	"update_uid": null,
	"user_name": null}

	result = myRequest(url,str(data),Value=True)
	if result["code"] == 0:
		return "委托合同号：" + contract_num + "提交终止结算成功！"
	else:
		return "委托合同提交终止结算失败。错误返回：" + result["obj"]


@log
def reviewed_apartment_contract_end(contract_num):
	"""
	审核出租终止结算
	:param contract_num:出租合同号
	:return:
	"""
	picture = eval(json.dumps(eval(get_conf("picture", get_conf("testCondition", "test")))))
	null = None

	try:
		sql = "select contract_id from apartment_contract where contract_num = '%s'" % contract_num
		contract_id = searchSQL(sql)[0][0]
	except Exception as e:
		return "查询出租合同sql报错。sql:" + sql +"; 错误返回：" + str(e)

	try:
		sql = "select end_id from apartment_contract_end where contract_id = '%s'" % contract_id
		end_id = searchSQL(sql)[0][0]
	except Exception as e:
		return "查询出租合同终止结算sql报错。sql:" + sql +"; 错误返回：" + str(e)

	#查询终止合同基本信息
	url = "http://erp.ishangzu.com/isz_contract/ContractEndController/searchContractEndInfo"
	data = {"contract_id":contract_id,"end_id":end_id,"is_old_data":"N"}
	result = myRequest(url,str(data),Value=True)["obj"]

	#初审
	url = "http://erp.ishangzu.com/isz_contract/ContractEndController/auditApartmrntContractEnd"
	data = {
	"endBasicInfo": {
		"audit_status": "PASS",
		"content": "同意！",
		"contract_id": contract_id,
		"end_contract_num": result["endBasicInfo"]["end_contract_num"],
		"end_date": result["endBasicInfo"]["end_date"],
		"update_time": result["endBasicInfo"]["update_time"],
		"end_id": end_id,
		"end_type": result["endBasicInfo"]["end_type"],
		"ins_result": "",
		"payment_type": result["endBasicInfo"]["payment_type"]
	},
	"liquidatedOrTurnFee": {
		"discount_liquidated_receivable": result["liquidatedOrTurnFee"]["discount_liquidated_receivable"],
		"liquidated_receivable": result["liquidatedOrTurnFee"]["liquidated_receivable"],
		"discountImgList": [{
			"img_id": picture[0]["img_id"],
			"src": picture[0]["src"]
		}],
		"discount_img_id": null
	},
	"receiverInfo": {
		"bank": result["receiverInfo"]["bank"],
		"contractEndPayerAgintType":  result["receiverInfo"]["contractEndPayerAgintType"],
		"pay_object":  result["receiverInfo"]["pay_object"],
		"receipt_bank_location":  result["receiverInfo"]["receipt_bank_location"],
		"receipt_bank_no":  result["receiverInfo"]["receipt_bank_no"],
		"receipt_name":  result["receiverInfo"]["receipt_name"]
	}}
	result = myRequest(url,str(data),Value=True)
	if result["code"] != 0:
		return "出租合同号：" + contract_num + "。出租终止结算初审失败。错误返回：" + str(result)

	# 查询终止合同基本信息
	url = "http://erp.ishangzu.com/isz_contract/ContractEndController/searchContractEndInfo"
	data = {"contract_id": contract_id, "end_id": end_id, "is_old_data": "N"}
	result = myRequest(url, str(data), Value=True)["obj"]
	# 复审
	url = "http://erp.ishangzu.com/isz_contract/ContractEndController/auditApartmrntContractEnd"
	data = {
		"endBasicInfo": {
			"audit_status": "REVIEW",
			"content": "同意！",
			"contract_id": contract_id,
			"end_contract_num": result["endBasicInfo"]["end_contract_num"],
			"end_date": result["endBasicInfo"]["end_date"],
			"update_time": result["endBasicInfo"]["update_time"],
			"end_id": end_id,
			"end_type": result["endBasicInfo"]["end_type"],
			"ins_result": "",
			"payment_type": result["endBasicInfo"]["payment_type"]
		},
		"liquidatedOrTurnFee": {
			"discount_liquidated_receivable": result["liquidatedOrTurnFee"][
				"discount_liquidated_receivable"],
			"liquidated_receivable": result["liquidatedOrTurnFee"]["liquidated_receivable"],
			"discountImgList": [{
				"img_id": picture[0]["img_id"],
				"src": picture[0]["src"]
			}],
			"discount_img_id": null
		},
		"receiverInfo": {
			"bank": result["receiverInfo"]["bank"],
			"contractEndPayerAgintType": result["receiverInfo"]["contractEndPayerAgintType"],
			"pay_object": result["receiverInfo"]["pay_object"],
			"receipt_bank_location": result["receiverInfo"]["receipt_bank_location"],
			"receipt_bank_no": result["receiverInfo"]["receipt_bank_no"],
			"receipt_name": result["receiverInfo"]["receipt_name"]
		}}
	result = myRequest(url, str(data), Value=True)
	if result["code"] == 0:
		return "出租合同号：" + contract_num + "。终止结算复审成功！"
	else:
		return "出租合同号：" + contract_num + "。终止结算复审异常。错误返回：" + str(result)


@log
def reviewed_house_contract_end(contract_num,Value = True):

	try:
		sql = "select end_id from house_contract_end where contract_id = (select contract_id from house_contract where contract_num = '%s')" % contract_num
		end_id = searchSQL(sql)[0][0]
	except Exception as e:
		return "查询委托合同终止结算ID异常,sql:" + sql + " 错误返回："+str(e)

	#初审
	url = "http://isz.ishangzu.com/isz_contract/endAgreementControl/houseContractEndAudit.action"
	data = {
	"achieveid": end_id,
	"activityId": "18",
	"content": "同意"}
	result  = myRequest(url,str(data),Value=True)

	if not Value:
		if result["code"] == 0:
			return "委托合同号：" + contract_num + " 终止结算初审成功！"
		else:
			return  "委托终止结算"+contract_num+"初审异常。错误返回：" + str(result["obj"])

	#复审
	url = "http://isz.ishangzu.com/isz_contract/endAgreementControl/houseContractEndAudit.action"
	data = {
	"achieveid": end_id,
	"activityId": "19",
	"content": "同意"}
	result = myRequest(url,str(data),Value=True)

	if result["code"] == 0:
		return "委托合同号：" + contract_num + " 终止结算复审成功！"
	else:
		return "委托终止结算" + contract_num + "复审异常。错误返回：" + str(result["obj"])


