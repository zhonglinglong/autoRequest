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


@log
def apartment_contract_collecting_money(contract_num):
    """
    出租合同首付款全部收钱
    :param contract_num:
    :return:
    """
    try:
        sql = "select contract_id from apartment_contract where contract_num = '%s'" % contract_num
        contract_id = searchSQL(sql)[0][0]
    except Exception as e:
        return "查询出租合同sql报错，sql:" + sql + "错误返回" + str(e)

    try:
        sql = """SELECT
        receivable_id,receivable_money
        FROM
        apartment_contract_receivable
        WHERE
        money_type IN (
            "FRIST_RENT",
            "FIRST_MANAGE_SERVER_FEE",
            "DEPOSIT"
        )
        AND contract_id = '%s' and end_status = 'NOTGET'""" % contract_id
        receivable_id_tuple  = searchSQL(sql)
    except Exception as e:
        return "查询出租合同sql报错，sql:" + sql + "错误返回" + str(e)

    if receivable_id_tuple == ():
        return u"该出租合同首付款都是已收状态"
    url = "http://isz.ishangzu.com/isz_finance/ApartmentContractReceiptsController/saveOrUpdateNewReceipts.action"
    for i in range(len(receivable_id_tuple)):
        data = {
        "receipts_date": now_time(),
        "company": "ISZTECH",
        "bank_name": "ABC",
        "bank_card_last_four": "3714",
        "operation_total": int(receivable_id_tuple[i][1]),
        "remark": "出租合同实收",
        "receipts_money": int(receivable_id_tuple[i][1]),
        "receivable_id": receivable_id_tuple[i][0],
        "contract_id": contract_id,
        "receipts_type": "BANKTRANSFER"}
        myRequest(url,str(data),Value=True)
    return u"该出租合同下所有首付款已经完成收款"


@log
def pay_down_payment(apartment_code,phone,earnest_money="4000"):
    """
    下定
    :param apartment_code: 房源编号
    :param phone: 客户手机号
    :param earnest_money: 下定金额
    :return:
    """
    try:
        sql = "SELECT customer_id from customer where phone='%s';" % phone
        customer_id = searchSQL(sql)[0][0]
    except Exception as e:
        return "查询租客sql报错，sql:" + sql + "错误返回" + str(e)
    #预定房源信息
    url = "http://isz.ishangzu.com/isz_customer/CustomerController/initBookAvailability.action"
    data = {"customer_id":customer_id}
    result = myRequest(url,str(data),Value=True)["obj"]
    #查询房源信息
    if "-" in apartment_code:
        url = "http://isz.ishangzu.com/isz_customer/CustomerController/searchBookAvailabilityShareList.action"
        rent_type_search = "SHARE"
    else:
        url = "http://isz.ishangzu.com/isz_customer/CustomerController/searchBookAvailabilityEntireList.action"
        rent_type_search = "ENTIRE"
    data = {"residential_name_house_code_search":apartment_code,"pageNumber":1,"pageSize":50,"sort":"update_time","order":"DESC","rent_type_search":rent_type_search}
    house_list = myRequest(url,str(data),Value=True)["obj"]["rows"][0]

     #plan_sign_data,预计签约时间
    url = "http://isz.ishangzu.com/isz_contract/ApartmentContractController/getLastApartmentContractRealDueDate.action"
    datas = {
	"house_id": house_list["house_id"],
	"room_id": house_list["room_id"],
	"object_id": house_list["apartment_id"],
	"object_type": house_list["object_type"],
	"property_address": house_list["property_address"],
	"rent_type": house_list["rent_type"],
	"object_status": house_list["rent_status"],
	"rent_price": house_list["rent_price"]}
    plan_sign_data = myRequest(url,str(datas),Value=True)["obj"]['sign_date_last']

    #下定
    picture = eval(json.dumps(eval(get_conf("picture", get_conf("testCondition", "test")))))
    url = "http://isz.ishangzu.com/isz_contract/EarnestController/saveEarnest.action"
    data = {
	"earnest_money": earnest_money,
	"plan_sign_date": plan_sign_data,
	"remark": "下定备注",
	"customer_id": customer_id,
	"earnestImgList": [{
		"img_id": picture[0]["img_id"]
	}]}
    data.update(result)
    data.update(datas)
    result = myRequest(url,str(data),Value=True)
    if result["code"] ==0:
        return "房源编号：" + apartment_code + "下定成功！"
    else:
        return "房源编号：" + apartment_code + "下定失败！接口返回：" + result["obj"]


@log
def confirmation_down_payment(apartment_code,breach_money="2000"):
    """
    违约
    :param apartment_code: 房源编号
    :param breach_money: 违约金额
    :return:
    """
    #查询定金编号id
    url = "http://isz.ishangzu.com/isz_contract/EarnestController/searchEarnestList.action"
    data = {"residential_name_object_code_search":apartment_code,"pageNumber":1,"pageSize":50,"sort":"create_time","order":"DESC","current_dep_id":"00000000000000000000000000000000"}
    result = myRequest(url,str(data),Value=True)["obj"]["rows"][0]
    earnest_id = result["earnest_id"]

    #确认定金
    url = "http://isz.ishangzu.com/isz_contract/EarnestController/confirmEarnest.action"
    data = {
	"receipt_date": now_time(),
	"earnest_id": earnest_id,
	"earnest_money": result["earnest_money"],
	"payment_way": "BANKTRANSFER",
	"receipt_name": "收据姓名",
	"company": "ISZTECH"}
    myRequest(url,str(data))

    #违约
    url = "http://isz.ishangzu.com/isz_contract/EarnestController/saveEarnestBreach.action"
    data = {
	"breach_reason": "auto违约原因",
	"breach_money": breach_money,
	"earnest_id": earnest_id,
	"earnest_money": result["earnest_money"]}

    result = myRequest(url,str(data),Value=True)
    if result["code"] == 0:
        return "房源编号：" + apartment_code + "。确认违约成功！"
    else:
        return "房源编号：" + apartment_code + "。确认违约失败！错误返回：" + result["obj"]


