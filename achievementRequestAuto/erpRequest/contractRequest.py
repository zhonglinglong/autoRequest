# -*- coding:UTF-8 -*-

"""
author = crazyzhong
2018年4月10日17:20:22
爱上租ERP合同模块的接口
"""

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from common.interface import *
import datetime
from erpRequest import customerRequest


@log
def add_house_contract(residential_name,contract_num,entrust_start_date,apartment_type,entrust_type,reform_way,sign_body=u"杭州爱上租科技有限公司"):
    """
    新签委托合同
    :param residential_name: 楼盘名称
    :param contract_num: 委托合同号
    :param entrust_start_date: 委托开始日
    :param apartment_type: 公寓类型 品牌 服务
    :param entrust_type: 合同类型  整租 合租
    :param reform_way: 改造方式
    :param sign_body: 签约公司
    :return:
    """

    null = None
    second_pay_date = str(datetime.datetime.strptime(entrust_start_date, '%Y-%m-%d') + datetime.timedelta(days=30)).split(" ")[0]
    sql = """SELECT
	h.house_code
FROM
	house h
LEFT JOIN house_rent hr ON hr.house_id = h.house_id
LEFT JOIN residential re ON re.residential_id = h.residential_id
AND hr.house_status = 'WAITING_RENT'
AND hr.deleted = 0
WHERE
re.residential_name = "%s"
AND h.deleted = 0
AND NOT EXISTS (
	SELECT
		1
	FROM
		house_contract hc
	WHERE
		hc.house_id = h.house_id
	AND deleted = 0
) LIMIT 1 """ % residential_name
    try:
        searchSQL(sql)
        house_code = searchSQL(sql)[0][0]
    except BaseException as e:
        return "该楼盘所有开发自营房源至少签过一次，为了避免被老数据影响，请新增开发自营房源或者换个楼盘~!"

    try:
        sql = 'select property_name,house_code,building_id,house_id,city_code,area_code,residential_id from house where house_code = "%s"' % house_code
        house_contact_data = searchSQL(sql)
    except Exception as e:
        return "查询房间信息sql报错。sql:" + sql + "。错误返回：" + str(e)

    fitment_end_date = str(datetime.datetime.strptime(entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=1))
    fitment_start_date = str(datetime.datetime.strptime(entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=90))
    entrust_end_date = str(datetime.datetime.strptime(entrust_start_date, '%Y-%m-%d') + datetime.timedelta(days=730))

    entrust_start_date = entrust_start_date + " 00:00:00"
    sign_date = entrust_start_date
    area_code = house_contact_data[0][5]
    building_id = house_contact_data[0][2]
    city_code = house_contact_data[0][4]
    #delay_date = entrust_end_date
    entrust_type = get_conf("house_contract_type", entrust_type.encode('utf-8'))
    first_pay_date = entrust_start_date
    house_id = house_contact_data[0][3]
    owner_sign_date = entrust_start_date
    reform_way = get_conf("house_contract_type", reform_way.encode('utf-8'))
    residential_id = house_contact_data[0][6]
    sign_body = get_conf("house_contract_type", sign_body.encode('utf-8'))
    sign_dep_name = get_conf("loginUser", "sign_dep_name")
    sign_did = get_conf("loginUser", "dep_id")
    sign_uid = get_conf("loginUser", "user_id")
    sign_user_name = get_conf("loginUser", "user_name")
    payment_cycle = "SEASON"
    apartment_type = get_conf("house_contract_type", apartment_type.encode('utf-8'))
    address = house_contact_data[0][0]
    house_code = house_contact_data[0][1]
    picture = eval(json.dumps(eval(get_conf("picture", get_conf("testCondition", "test")))))

    HouseContractFrist = {}
    HouseContractFrist["houseContractFrist"] = {
        "address": address,
        "certificate_type": "",
        "certificate_type_id": "2",
        "commonLandlords": [],
        "common_case": "PRIVATE",
        "common_case_cn": "",
        "contract_id": "",
        "contract_type": "NEWSIGN",
        "contract_type_cn": "新签",
        "houseContractLandlord": {
            "card_type": "PASSPORT",
            "id_card": "66778899",
            "landlord_name": "产权人姓名",
            "property_owner_type": "PROPERTYOWNER",
            "property_card_id": "123456789",
            "idCardPhotos": picture ,
            "name": "产权人姓名"
        },
        "house_code": house_code,
        "inside_space": "136.8",
        "is_new_data": "",
        "mortgageeStatementOriginal": [],
        "pledge": "0",
        "productionVos": [{
            "attachments":  picture,
            "file_type": "主页（业主姓名/物业地址）",
            "file_type_id": 2,
            "is_active": "Y",
            "is_approved_need": "N",
            "is_audit_need": "Y",
            "is_save_need": "Y"
        }, {
            "attachments":  picture,
            "file_type": "带证号页(产权证编号)",
            "file_type_id": 1,
            "is_active": "Y",
            "is_approved_need": "N",
            "is_audit_need": "N",
            "is_save_need": "Y"
        }, {
            "attachments": picture,
            "file_type": "附记页",
            "file_type_id": 3,
            "is_active": "Y",
            "is_approved_need": "N",
            "is_audit_need": "N",
            "is_save_need": "Y"
        }],
        "production_address": "产权地址",
        "property_card_id": "",
        "property_use": "HOUSE",
        "property_use_cn": ""}

    HouseContractSecond = {}
    HouseContractSecond ["houseContractSecond"] = {
		"agreedRentOriginalStatements":  picture,
		"any_agent": "0",
		"assetsOfLessor": [{
			"landlord_name": "产权人姓名",
			"phone": "18279881085",
			"email": "zhonglinglong@qq.com",
			"mailing_address": "通讯地址"
		}],
		"contract_id": "",
		"houseContractSign": {
			"address": "",
			"agent_type": "",
			"attachments": [],
			"card_type": "",
			"email": "",
			"id_card": "",
			"phone": "",
			"sign_name": ""
		},
		"is_new_data": "",
		"originalAgentDataRelations": [],
		"originalLessorHasDied": []}

    HouseContractThird = {}
    HouseContractThird ["houseContractThird"] = {
		"account_bank": "支行",
		"account_name": "产权人姓名",
		"account_num": "18279881085",
		"bank": "支付宝",
		"contract_id": "",
		"is_new_data": "",
		"notPropertyOwnerGrantReceipts": [],
		"pay_object": "ALIPAY",
		"payeeIdPhotos":  picture,
		"payee_card_type": "PASSPORT",
		"payee_card_type_cn": "",
		"payee_emergency_name": "紧急联系人姓名",
		"payee_emergency_phone": "18244556677",
		"payee_id_card": "66778899",
		"payee_type": "PROPERTYOWNER",
		"payee_type_cn": "" }

    HouseContractFour = {}
    HouseContractFour ["houseContractFour"] = {
	"apartment_type": apartment_type,
	"apartment_type_cn": "",
	"area_code": area_code,
	"audit_status": null,
	"audit_time": null,
	"audit_uid": null,
	"building_id": building_id,
	"city_code": city_code,
	"contractAttachments": picture,
	"contract_id": null,
	"contract_num": contract_num,
	"contract_status": null,
	"contract_type": "NEWSIGN",
	"contract_type_cn": "新签",
	#"delay_date": delay_date,
	"electron_file_src": null,
	"energy_company": null,
	"energy_fee": null,
	"entrust_end_date": entrust_end_date,
	"entrust_start_date": entrust_start_date,
	"entrust_type": entrust_type,
	"entrust_type_cn": "",
	"entrust_year": "2",
	"entrust_year_cn": "",
	"first_pay_date": first_pay_date,
	"fitment_end_date": fitment_end_date,
	"fitment_start_date": fitment_start_date,
	"freeType": null,
	"freeType_cn": "",
	"free_days": 30,
	"free_end_date": null,
	"free_start_date": null,
	"have_parking": "N",
	"house_id": house_id,
	"housekeep_mange_dep": null,
	"housekeep_mange_dep_user": "-",
	"housekeep_mange_did": null,
	"housekeep_mange_uid": null,
	"housekeep_mange_user_name": null,
	"is_electron": null,
	"is_new_data": null,
	"owner_sign_date": owner_sign_date,
	"parent_id": null,
	"parking": "",
	"payment_cycle": payment_cycle,
	"payment_cycle_cn": "",
	"property": null,
	"property_company": null,
	"reform_way": reform_way,
	"reform_way_cn": "",
	"remark": "备注",
	"rentMoney": "6000",
	"rental_price": "6000",
	"reset_finance": "false",
	"residential_id": residential_id,
	"second_pay_date": second_pay_date,
	"server_manage_dep_user": "",
	"server_manage_did": null,
	"server_manage_did_name": null,
	"server_manage_uid": null,
	"server_manage_uid_name": null,
	"service_fee_factor": 0.01,
	"sign_body": sign_body,
	"sign_date": sign_date,
	"sign_dep_name": sign_dep_name,
	"sign_did": sign_did,
	"sign_uid": sign_uid,
	"sign_user_name": sign_user_name,
	"year_service_fee": null
}
    #生成租金策略
    url = "http://erp.ishangzu.com/isz_housecontract/houseContractController/getHouseRentStrategyVo"
    data = {
        "apartment_type": apartment_type,
        "contract_type": "NEWSIGN",
        "entrust_start_date": entrust_start_date,
        "entrust_end_date": entrust_end_date,
        "free_end_date": "",
        "free_start_date": "",
        "parking": "",
        "payment_cycle": payment_cycle,
        "rent_money": "5000",
        "sign_date": sign_date,
        "city_code": city_code,
        "entrust_year": "2",
        "free_days": 30,
        "version": "V_TWO"}

    HouseContractFour_02 = {}
    try:
        HouseContractFour_02 ["rentStrategys"] = myRequest(url,str(data),Value=True)["obj"]
        HouseContractFour["houseContractFour"]["rentStrategys"] = HouseContractFour_02["rentStrategys"]
    except Exception as e:
        return "新签委托合同生成租金策略失败。错误返回：" + str(e)

    #生成租金明细
    url = "http://erp.ishangzu.com/isz_finance/HouseContractPayableController/createContractPayable"
    data = {
        "contractId": "",
        "firstPayDate": first_pay_date,
        "secondPayDate": second_pay_date,
        "version": "V_TWO"}
    datas = {}
    datas["rentInfoList"] = HouseContractFour_02["rentStrategys"]
    data.update(datas)

    HouseContractFive = {}
    try:
        HouseContractFive["houseContractFive"] = myRequest(url, str(data), Value=True)["obj"]
    except Exception as e:
        return "新签委托合同生成租金明细异常。错误返回：" + str(e)

    houseContract = {}
    houseContract.update(HouseContractFrist)
    houseContract.update(HouseContractSecond)
    houseContract.update(HouseContractThird)
    houseContract.update(HouseContractFour)
    houseContract.update(HouseContractFive)

    #新签委托合同
    url = "http://erp.ishangzu.com/isz_housecontract/houseContractController/saveHouseContract"
    result = myRequest(url,str(houseContract),Value=True)
    if result["code"] == 0:
        return "新签委托合同号:" + contract_num + "。提交成功！"
    else:
        return "新签委托合同号:" + contract_num + "。提交失败！错误返回：" + str(result["obj"])


@log
def add_apartment_contract_entire(apartment_code,phone,contract_num,rent_start_date,rent_end_date,sign_body=u"杭州爱上租科技有限公司"):
    """
    新签出租类型是整租的出租合同
    :param apartment_code:  房源编号 or 物业地址
    :param phone: 租客手机号
    :param contract_num: 出租合同号
    :param rent_start_date: 承租开始日
    :param rent_end_date: 承租到期日
    :param sign_body: 签约公司
    :return:
    """

    id_card = add_phone_number()
    try:
        sql = "select customer_id,customer_num,customer_from,customer_name from customer where phone = '%s'" % phone
        customer = searchSQL(sql)[0]
    except Exception as e:
        return "查询租客sql报错。sql:" + sql + ";错误返回：" + str(e)

    # 获取自营房源数据
    try:
        sql = "SELECT apartment_id,service_uid,service_did,rent_type from apartment where apartment_code = '%s' " % apartment_code
        apartment_id = searchSQL(sql)[0]
    except Exception as e:
        return "查询公寓sql报错。sql:" + sql + ";错误返回：" + str(e)

    try:
        url = "http://isz.ishangzu.com/isz_contract/ApartmentContractController/searchApartmentContractDetail.action"
        data = {"apartment_id": apartment_id[0], "contract_type": apartment_id[3]}
        dic = myRequest(url, str(data), Value=True)["obj"]["apartmentContract"]
    except Exception as e:
        return "查询自营房源详情报错。错误返回：" + str(e)

    # print dics
    # #把字典空值去掉
    # dic = empty_dict_null(dics)
    cash_rent = int(dic['rent_price']) * 0.1
    apartment_contract = {"house_id": dic["house_id"],
              "residential_id": dic['residential_id'],
              "building_id": dic['building_id'],
              "city_code": dic['city_code'],
              "area_code": dic['area_code'],
              "entrust_type": dic['entrust_type'],
              "apartment_id": dic['apartment_id'],
              "server_flag": dic['server_flag'],
              "apartment_rent_price": dic['rent_price'],
              "contract_type": "NEWSIGN",
              "apartment_code": dic['apartment_code'],
              "property_address": dic['property_address'],
              "houseRoom": dic['houseRoom'],
              "apartment_type": dic['apartment_type'],
              "service_dep_name": dic['service_dep_name'],
              "service_user_name": dic['service_user_name'],
              "input_dep_name": dic['input_dep_name'],
              "input_user_name": dic['input_user_name'],
              "sign_did": dic['sign_did'],
              "sign_uid": dic['sign_uid'],
              "contract_num": contract_num,
              "sign_body": get_conf("house_contract_type", sign_body.encode('utf-8')),
              "sign_date": rent_start_date,
              "apartment_check_in_date": dic['apartment_check_in_date'],
              "rent_start_date": rent_start_date,
              "rent_end_date": rent_end_date,
              "payment_date": rent_start_date,
              "deposit_type": "ONE",
              "payment_type": "NORMAL",
              "payment_cycle": "SEASON",
              "cash_rent": cash_rent,
              "deposit": dic['rent_price'],
              "agency_fee": "0.00",
              "month_server_fee": cash_rent,
              "month_server_fee_discount": "100%",
              "load_interest": dic['load_interest'],
              "remark": "测试",
              "undefined": rent_end_date,
              "dispostIn": 1,
              "sign_name": customer[3],
              "sign_id_type": "PASSPORT",
              "sign_id_no": id_card,
              "sign_phone": phone,
              "sign_is_customer": "Y",
              "address": dic['address'],
              "model": "4"}
    # 获取"person"列表字段值
    apartment_contract["person"] = {
        "urgent_customer_name": "租客紧急联4",
        "urgent_phone": "13855667744",
        "customer_id": customer[0],
        "customer_num": customer[1],
        "customer_from": customer[2],
        "customer_type": "PERSONALITY",
        "customer_name": customer[3],
        "card_type": "PASSPORT",
        "id_card": id_card,
        "phone": phone,
        "gender": "MALE",
        "socialQualification": "on",
        "person_type": 2,
        "social_qualification": "N"}

    # 获取houseContractList
    # 出租合同内的委托合同时间
    url = "http://isz.ishangzu.com/isz_contract/ApartmentContractController/getHouseContractByHouseId.action"
    data = {
        "rent_start_date": rent_start_date,
        "rent_end_date": rent_end_date,
        "houseId": dic["house_id"],
        "apartment_id": dic['apartment_id']}

    houseContractList = []
    try:
        houseContractList.append(empty_dict_null(myRequest(url, str(data), Value=True)["obj"][0]))
        apartment_contract["houseContractList"] = houseContractList
    except Exception as e:
        return "新签出租整租合同获取委托合同时间报错。错误返回：" + str(e)

    month_server_fee = int (int(apartment_contract["apartment_rent_price"]) * 0.07)
    # 获取应收数据
    url = "http://isz.ishangzu.com/isz_contract/ApartmentContractController/createApartmentContractReceivable.action"
    data = [{
        "firstRow": "true",
        "money": apartment_contract["apartment_rent_price"],
        "start_date": rent_start_date,
        "rowIndex": 0,
        "end_date": rent_end_date,
        "money_cycle": "SEASON",
        "payment_date": rent_start_date,
        "deposit": apartment_contract["apartment_rent_price"],
        "agencyFeeMoney": "0.00",
        "money_type": "RENT",
        "rent_start_date": rent_start_date,
        "rent_end_date": rent_end_date,
        "sign_date":now_time(-1),
        "month_server_fee": month_server_fee}]


    receivables = myRequest(url, str(data), Value=True)["obj"]
    apartment_contract["receivables"] = receivables

    # 获取 apartmentContractRentInfoList
    apartment_contract["apartmentContractRentInfoList"] = data

    # 保存出租合同
    url = "http://isz.ishangzu.com/isz_contract/ApartmentContractController/saveOrUpdateApartmentContract.action"
    result = myRequest(url, str(apartment_contract), Value=True)
    if result["code"] == 0:
        return "新签出租整租。合同号是：" + contract_num + "提交成功！"
    else:
        return "新签出租整租。合同号是：" + contract_num + "提交失败！" + "错误返回：" + result["obj"]

@log
def add_apartment_contract_share(apartment_code,phone,contract_num,rent_start_date,rent_end_date,sign_body=u"杭州爱上租科技有限公司"):
    """
    新签出租类型是合租的出租合同
    :param apartment_code:  房源编号 or 物业地址
    :param phone: 租客手机号
    :param contract_num: 出租合同号
    :param rent_start_date: 承租开始日
    :param rent_end_date: 承租到期日
    :param sign_body: 签约公司
    :return:
    """

    id_card = add_phone_number()
    try:
        sql = "select customer_id,customer_num,customer_from,customer_name from customer where phone = '%s'" % phone
        customer = searchSQL(sql)[0]
    except Exception as e:
        return "查询租客sql报错。sql:" + sql + ";错误返回：" + str(e)

    # 获取自营房源数据
    try:
        sql = "SELECT apartment_id,service_uid,service_did,rent_type from apartment where apartment_code = '%s' " % apartment_code
        apartment_id = searchSQL(sql)[0]
    except Exception as e:
        return "查询公寓sql报错。sql:" + sql + ";错误返回：" + str(e)

    #查询自营公寓详情信息
    url = "http://isz.ishangzu.com/isz_contract/ApartmentContractController/searchApartmentContractDetail.action"
    data = {"apartment_id": apartment_id[0], "contract_type": apartment_id[3]}
    dic = myRequest(url, str(data), Value=True)["obj"]["apartmentContract"]
    # print dics
    # #把字典空值去掉
    # dic = empty_dict_null(dics)
    cash_rent = int(dic['rent_price']) * 0.1
    apartment_contract = {"house_id": dic["house_id"],
               "production_address": dic["production_address"],
              "room_id" : dic["room_id"],
              "residential_id": dic['residential_id'],
              "building_id": dic['building_id'],
              "city_code": dic['city_code'],
              "area_code": dic['area_code'],
              "entrust_type": dic['entrust_type'],
              "apartment_id": dic['apartment_id'],
              "server_flag": dic['server_flag'],
              "apartment_rent_price": dic['rent_price'],
              "contract_type": "NEWSIGN",
              "apartment_code": dic['apartment_code'],
              "property_address": dic['property_address'],
              "houseRoom": dic['houseRoom'],
              "apartment_type": dic['apartment_type'],
              #"service_dep_name": dic['service_dep_name'],
              #"service_user_name": dic['service_user_name'],
              "input_dep_name": dic['input_dep_name'],
              "input_user_name": dic['input_user_name'],
              "sign_did": dic['sign_did'],
              "sign_uid": dic['sign_uid'],
              "contract_num": contract_num,
              "sign_body": get_conf("house_contract_type", sign_body.encode('utf-8')),
              "sign_date": rent_start_date,
              "apartment_check_in_date": dic['apartment_check_in_date'],
              "rent_start_date": rent_start_date,
              "rent_end_date": rent_end_date,
              "payment_date": rent_start_date,
              "deposit_type": "ONE",
              "payment_type": "NORMAL",
              "payment_cycle": "SEASON",
              "cash_rent": cash_rent,
              "deposit": dic['rent_price'],
              "agency_fee": "0.00",
              "month_server_fee": cash_rent,
              "month_server_fee_discount": "100%",
              "load_interest": dic['load_interest'],
              "remark": "测试",
              "undefined": rent_end_date,
              "dispostIn": 1,
              "sign_name": customer[3],
              "sign_id_type": "PASSPORT",
              "sign_id_no": id_card,
              "sign_phone": phone,
              "sign_is_customer": "Y",
              "address": dic['property_address'],
              "model": "4"}
    # 获取"person"列表字段值
    apartment_contract["person"] = {
        "urgent_customer_name": "租客紧急联4",
        "urgent_phone": "13855667744",
        "customer_id": customer[0],
        "customer_num": customer[1],
        "customer_from": customer[2],
        "customer_type": "PERSONALITY",
        "customer_name": customer[3],
        "card_type": "PASSPORT",
        "id_card": id_card,
        "phone": phone,
        "gender": "MALE",
        "socialQualification": "on",
        "person_type": 2,
        "social_qualification": "N"}

    # 获取houseContractList
    # 出租合同内的委托合同时间
    url = "http://isz.ishangzu.com/isz_contract/ApartmentContractController/getHouseContractByHouseId.action"
    data = {
        "rent_start_date": rent_start_date,
        "rent_end_date": rent_end_date,
        "houseId": dic["house_id"],
        "apartment_id": dic['apartment_id'],
        "room_id": dic['room_id']}
    houseContractList = []
    houseContractList.append(empty_dict_null(myRequest(url, str(data), Value=True)["obj"][0]))
    apartment_contract["houseContractList"] = houseContractList

    month_server_fee = int (int(apartment_contract["apartment_rent_price"]) * 0.07)
    # 获取应收数据
    url = "http://isz.ishangzu.com/isz_contract/ApartmentContractController/createApartmentContractReceivable.action"
    data = [{
        "firstRow": "true",
        "money": apartment_contract["apartment_rent_price"],
        "start_date": rent_start_date,
        "rowIndex": 0,
        "end_date": rent_end_date,
        "money_cycle": "SEASON",
        "payment_date": rent_start_date,
        "deposit": apartment_contract["apartment_rent_price"],
        "agencyFeeMoney": "0.00",
        "money_type": "RENT",
        "rent_start_date": rent_start_date,
        "rent_end_date": rent_end_date,
        "sign_date":rent_start_date,
        "month_server_fee": month_server_fee}]

    receivables = myRequest(url, str(data), Value=True)["obj"]
    apartment_contract["receivables"] = receivables

    # 获取 apartmentContractRentInfoList
    apartment_contract["apartmentContractRentInfoList"] = data


    # 保存出租合同
    url = "http://isz.ishangzu.com/isz_contract/ApartmentContractController/saveOrUpdateApartmentContract.action"
    result = myRequest(url, str(apartment_contract), Value=True)
    if result["code"] == 0:
        return  "新签出租合租。出租合同号：" + contract_num + "提交出租合同号成功！"
    else:
        return "新签出租合租。出租合同号：" + contract_num + "提交出租合同号失败！" + "接口返回：" + result["obj"]

@log
def reviewed_house_contract(contract_num,retrial = True):
    """
    初审，复审委托合同，默认都审核
    :param contract_num: 委托合同号
    :param retrial: 默认为真，初审复审，假为只初审
    :return: 审核成功的信息
    """
    #委托合同详情
    try:
        sql = "select contract_id from house_contract where contract_num = '%s'" % contract_num
        contract_id = searchSQL(sql)[0][0]
    except Exception as e:
        return "查询委托sql报错。sql:" + sql + "错误返回：" + str(e)

    url = "http://erp.ishangzu.com/isz_housecontract/houseContractController/searchHouseContractInfo/" + contract_id
    details = myRequest(url,method="get",Value=True)["obj"]

    #委托合同应付列表获取应付id
    url = "http://erp.ishangzu.com/isz_finance/HouseContractPayableController/getPayablesByContract/" + contract_id
    payable = myRequest(url, method="get", Value=True)["obj"]
    payableId = []
    for i in range(len(payable)):
        payableId.append(payable[i]['payable_id'])

    #初审第一个页面
    try:
        sql = "SELECT house_id,entrust_type from house_contract where contract_id='%s'" % contract_id
        house_id_entrust_type = searchSQL(sql)
    except Exception as e:
        return "委托合同查询sql报错。sql:" + sql + "错误返回：" + str(e)

    url = "http://erp.ishangzu.com/isz_housecontract/houseContractController/saveOrUpdateHouseContractDetailByPart"
    houseContractFrist = {}
    houseContractFrist["houseContractFrist"] = details["houseContractFrist"]
    houseContractFrist["entrust_type"] = house_id_entrust_type[0][1]
    houseContractFrist["house_id"] = house_id_entrust_type[0][0]
    # try:
    #     sql = "SELECT apartment_id from apartment where house_id ='%s'" % house_id_entrust_type[0][0]
    #     houseContractFrist["apartment_id"] = searchSQL(sql)[0][0]
    # except Exception as e:
    #     return "自营公寓查询sql报错。sql:" + sql + "错误返回：" + str(e)
    data = {
        "auditForm": {
            "audit_status": "PASS",
            "content": "同意!"
        },
        "action_type": "AUDIT",
        "save_part": "ONE",
        "contract_id": contract_id
    }
    data.update(houseContractFrist)
    myRequest(url,str(data),Value=True)

    #初审第二个页面
    data = {
        "auditForm": {
            "audit_status": "PASS",
            "content": "同意!"
        },
        "action_type": "AUDIT",
        "save_part": "TWO",
        "contract_id": contract_id
    }
    data["houseContractSecond"] = details["houseContractSecond"]
    myRequest(url,str(data),Value=True)

    #初审第三个页面
    data = {
	"auditForm": {
		"audit_status": "PASS",
		"content": "同意!"
	},
	"action_type": "AUDIT",
	"save_part": "THREE",
	"contract_id": contract_id}
    data["houseContractThird"] = details["houseContractThird"]
    myRequest(url,str(data),Value=True)

    #初审第四个页面
    data = {
	"auditForm": {
		"audit_status": "PASS",
		"content": "同意!"
	},
	"action_type": "AUDIT",
	"save_part": "FOUR",
	"contract_id": contract_id}
    data["houseContractFour"] = details["houseContractFour"]
    myRequest(url,str(data),Value=True)

    #租金审核
    url = "http://erp.ishangzu.com/isz_finance/HouseContractPayableController/updatePayableAuditStatusById"
    data = {
	"audit_status": "AUDITED",
	"payableIds": payableId}
    myRequest(url,str(data),Value=True,method="put")

    #初审完结
    url = "http://erp.ishangzu.com/isz_housecontract/houseContractController/houseContractAudit"
    data = {
	"audit_status": "PASS",
	"content": "同意!",
	"contract_id": contract_id}
    myRequest(url, str(data), Value=True, method="put")

    if not retrial:
        return u"初审完成"

    #复审第一页
    # 委托合同详情
    try:
        sql = "select contract_id from house_contract where contract_num = '%s'" % contract_num
        contract_id = searchSQL(sql)[0][0]
    except Exception as e:
        return "查询委托sql报错。sql:" + sql + "错误返回：" + str(e)
    url = "http://erp.ishangzu.com/isz_housecontract/houseContractController/searchHouseContractInfo/" + contract_id
    details = myRequest(url, method="get", Value=True)["obj"]

    # 委托合同应付列表获取应付id
    url = "http://erp.ishangzu.com/isz_finance/HouseContractPayableController/getPayablesByContract/" + contract_id
    payable = myRequest(url, method="get", Value=True)["obj"]
    payableId = []
    for i in range(len(payable)):
        payableId.append(payable[i]['payable_id'])

    url = "http://erp.ishangzu.com/isz_housecontract/houseContractController/saveOrUpdateHouseContractDetailByPart"
    data = {
        "auditForm": {
            "audit_status": "APPROVED",
            "content": "同意!"
        },
        "action_type": "AUDIT",
        "save_part": "ONE",
        "contract_id": contract_id
    }
    data.update(houseContractFrist)
    myRequest(url, str(data), Value=True)

    # 复审审第二个页面
    data = {
        "auditForm": {
            "audit_status": "APPROVED",
            "content": "同意!"
        },
        "action_type": "AUDIT",
        "save_part": "TWO",
        "contract_id": contract_id
    }
    data["houseContractSecond"] = details["houseContractSecond"]
    myRequest(url, str(data), Value=True)

    # 复审第三个页面
    data = {
        "auditForm": {
            "audit_status": "APPROVED",
            "content": "同意!"
        },
        "action_type": "AUDIT",
        "save_part": "THREE",
        "contract_id": contract_id}
    data["houseContractThird"] = details["houseContractThird"]
    myRequest(url, str(data), Value=True)

    # 复审第四个页面
    data = {
        "auditForm": {
            "audit_status": "APPROVED",
            "content": "同意!"
        },
        "action_type": "AUDIT",
        "save_part": "FOUR",
        "contract_id": contract_id}
    data["houseContractFour"] = details["houseContractFour"]
    myRequest(url, str(data), Value=True)

    #复审完结
    url = "http://erp.ishangzu.com/isz_housecontract/houseContractController/houseContractAudit"
    data = {"audit_status":"APPROVED","content":"同意!","contract_id":contract_id}
    result = myRequest(url, str(data), Value=True,method="put")
    if result["code"] == 0:
        return "委托合同：" + contract_num + "。复审成功！"
    else:
        return "委托合同：" + contract_num + "。复审失败！错误返回：" + result["obj"]


@log
def reviewed_apartment_contract(contract_num,Value = True):
    """
    审核出租合同
    :param contract_num: 出租合同号
    :param Value:
    :return:
    """
    #出租合同详情
    try:
        sql = "select contract_id from apartment_contract where contract_num = '%s'" % contract_num
        contract_id = searchSQL(sql)[0][0]
    except Exception as e:
        return "查询出租合同sql报错。sql:" + sql + ";错误返回：" + str(e)
    url = "http://isz.ishangzu.com/isz_contract/ApartmentContractController/searchApartmentContractDetail.action"
    data = {"contract_id":contract_id}
    result = myRequest(url, str(data), Value=True)["obj"]
    receivables = []
    for i in range(len(result["apartmentContractReceivableList"])):
        dicts = empty_dict_null(result["apartmentContractReceivableList"][i])
        dicts["rowIndex"] = i
        del dicts['houseRoom']
        del dicts['address']
        dicts["edit"] = False
        receivables.append(dicts)

    person = empty_dict_null(result['customerPerson'],Value=False)
    del person['customer_from_name']
    del person['person_type_name']
    del person['card_type_name']
    del person['customer_type_name']
    del person['gender_name']
    person["yesNo"] = "N"
    person["socialQualification"] = "on"

    apartmentContractRentInfoList = empty_dict_null(result["apartmentContractRentInfoList"][0])
    apartmentContractRentInfoList["agencyFeeMoney"] = "0.00"
    apartmentContractRentInfoList["deposit"] = result["apartmentContract"]["deposit"]
    apartmentContractRentInfoList["money_cycle"] = result["apartmentContract"]["payment_cycle"]
    apartmentContractRentInfoList["money_type"] = "RENT"
    apartmentContractRentInfoList["month_server_fee"] = result["apartmentContract"]["month_server_fee"]
    apartmentContractRentInfoList["payment_date"] = result["apartmentContract"]["payment_date"]
    apartmentContractRentInfoList["rent_end_date"] = result["apartmentContract"]["rent_end_date"]
    apartmentContractRentInfoList["rent_start_date"] = result["apartmentContract"]["rent_start_date"]
    apartmentContractRentInfoList["firstRow"] = True
    apartmentContractRentInfoList["rowIndex"] = 0
    apartmentContractRentInfoList["sign_date"] = result["apartmentContract"]["sign_date"]

    url = "http://isz.ishangzu.com/isz_contract/ApartmentContractController/saveOrUpdateApartmentContract.action"
    data = {
	"contract_id": result['apartmentContract']["contract_id"],
	"house_id": result['apartmentContract']["house_id"],
	"residential_id": result['apartmentContract']["residential_id"],
	"building_id": result['apartmentContract']["building_id"],
	"city_code": result['apartmentContract']["city_code"],
	"area_code": result['apartmentContract']["area_code"],
	"entrust_type": result['apartmentContract']["entrust_type"],
	"apartment_id": result['apartmentContract']["apartment_id"],
	"contract_status": result['apartmentContract']["contract_status"],
	"audit_uid": result['apartmentContract']["audit_uid"],
	"server_flag": result['apartmentContract']["server_flag"],
	"apartment_rent_price": result['apartmentContract']["apartment_rent_price"],
	"contract_type": result['apartmentContract']["contract_type"],
	"apartment_code": result['apartmentContract']["apartment_code"],
	"property_address": result['apartmentContract']["property_address"],
	"production_address": result['apartmentContract']["production_address"],
	"apartment_type": result['apartmentContract']["apartment_type"],
	"input_dep_name": result['apartmentContract']['sign_dep_name'],
	"input_user_name": result['apartmentContract']['sign_user_name'],
	"sign_did": result['apartmentContract']['sign_did'],
	"sign_uid": result['apartmentContract']["sign_uid"],
	"results_belong_did": result['apartmentContract']["results_belong_did"],
	"results_belong_uid": result['apartmentContract']["results_belong_uid"],
	"contract_num": result['apartmentContract']["contract_num"],
	"sign_body": result['apartmentContract']["sign_body"],
	"sign_date": result['apartmentContract']["sign_date"],
	"apartment_check_in_date": result['apartmentContract']["apartment_check_in_date"],
	"rent_start_date": result['apartmentContract']["rent_start_date"],
	"rent_end_date": result['apartmentContract']["rent_end_date"],
	"payment_date": result['apartmentContract']["payment_date"],
	"deposit_type": result['apartmentContract']["deposit_type"],
	"payment_type": result['apartmentContract']["payment_type"],
	"payment_cycle": result['apartmentContract']["payment_cycle"],
	"financing_type": result['apartmentContract']["financing_type"],
	"cash_rent": result['apartmentContract']["cash_rent"],
	"deposit": result['apartmentContract']["deposit"],
	"agency_fee": result['apartmentContract']["agency_fee"],
	"month_server_fee": result['apartmentContract']["month_server_fee"],
	"month_server_fee_discount": result['apartmentContract']["month_server_fee_discount"],
	"load_interest": result['apartmentContract']["load_interest"],
	"remark": result['apartmentContract']["remark"],
	"dispostIn": result['apartmentContract']["dispostIn"],
	"sign_name": result['apartmentContract']["sign_name"],
	"sign_id_type": result['apartmentContract']["sign_id_type"],
	"sign_id_no": result['apartmentContract']["sign_id_no"],
	"sign_phone": result['apartmentContract']["sign_phone"],
	"sign_is_customer": result['apartmentContract']["sign_is_customer"],
	"address": result['apartmentContract']["property_address"],
        "model": "4",
        "achieveid": result['apartmentContract']["contract_id"],
        "activityId": "25",
        "content": "同意"}
    houseContractList_list = []
    houseContractList_list.append(empty_dict_null(result['houseContractList'][0]))
    data['houseContractList'] = houseContractList_list
    data["receivables"] = receivables
    data["person"] = person
    apartmentContractRentInfo = []
    apartmentContractRentInfo.append(apartmentContractRentInfoList)
    data["apartmentContractRentInfoList"] = apartmentContractRentInfo
    myRequest(url,str(data),Value=True)
    if not Value:
        return u"出租合同完成初审"

    #出租合同复审
    url = "http://isz.ishangzu.com/isz_contract/ApartmentContractController/saveOrUpdateApartmentContract.action"
    # 出租合同详情
    try:
        sql = "select contract_id from apartment_contract where contract_num = '%s'" % contract_num
        contract_id = searchSQL(sql)[0][0]
    except Exception as e:
        return "查询出租合同sql报错。sql:" + sql + ";错误返回：" + str(e)
    url = "http://isz.ishangzu.com/isz_contract/ApartmentContractController/searchApartmentContractDetail.action"
    data = {"contract_id": contract_id}
    result = myRequest(url, str(data), Value=True)["obj"]
    receivables = []
    for i in range(len(result["apartmentContractReceivableList"])):
        dicts = empty_dict_null(result["apartmentContractReceivableList"][i])
        dicts["rowIndex"] = i
        del dicts['houseRoom']
        del dicts['address']
        dicts["edit"] = False
        receivables.append(dicts)

    person = empty_dict_null(result['customerPerson'], Value=False)
    del person['customer_from_name']
    del person['person_type_name']
    del person['card_type_name']
    del person['customer_type_name']
    del person['gender_name']
    person["yesNo"] = "N"
    person["socialQualification"] = "on"

    apartmentContractRentInfoList = empty_dict_null(result["apartmentContractRentInfoList"][0])
    apartmentContractRentInfoList["agencyFeeMoney"] = "0.00"
    apartmentContractRentInfoList["deposit"] = result["apartmentContract"]["deposit"]
    apartmentContractRentInfoList["money_cycle"] = result["apartmentContract"]["payment_cycle"]
    apartmentContractRentInfoList["money_type"] = "RENT"
    apartmentContractRentInfoList["month_server_fee"] = result["apartmentContract"]["month_server_fee"]
    apartmentContractRentInfoList["payment_date"] = result["apartmentContract"]["payment_date"]
    apartmentContractRentInfoList["rent_end_date"] = result["apartmentContract"]["rent_end_date"]
    apartmentContractRentInfoList["rent_start_date"] = result["apartmentContract"]["rent_start_date"]
    apartmentContractRentInfoList["firstRow"] = True
    apartmentContractRentInfoList["rowIndex"] = 0
    apartmentContractRentInfoList["sign_date"] = result["apartmentContract"]["sign_date"]

    url = "http://isz.ishangzu.com/isz_contract/ApartmentContractController/saveOrUpdateApartmentContract.action"
    data = {
        "contract_id": result['apartmentContract']["contract_id"],
        "house_id": result['apartmentContract']["house_id"],
        "residential_id": result['apartmentContract']["residential_id"],
        "building_id": result['apartmentContract']["building_id"],
        "city_code": result['apartmentContract']["city_code"],
        "area_code": result['apartmentContract']["area_code"],
        "entrust_type": result['apartmentContract']["entrust_type"],
        "apartment_id": result['apartmentContract']["apartment_id"],
        "contract_status": result['apartmentContract']["contract_status"],
        "audit_uid": result['apartmentContract']["audit_uid"],
        "server_flag": result['apartmentContract']["server_flag"],
        "apartment_rent_price": result['apartmentContract']["apartment_rent_price"],
        "contract_type": result['apartmentContract']["contract_type"],
        "apartment_code": result['apartmentContract']["apartment_code"],
        "property_address": result['apartmentContract']["property_address"],
        "production_address": result['apartmentContract']["production_address"],
        "apartment_type": result['apartmentContract']["apartment_type"],
        "input_dep_name": result['apartmentContract']['sign_dep_name'],
        "input_user_name": result['apartmentContract']['sign_user_name'],
        "sign_did": result['apartmentContract']['sign_did'],
        "sign_uid": result['apartmentContract']["sign_uid"],
        "results_belong_did": result['apartmentContract']["results_belong_did"],
        "results_belong_uid": result['apartmentContract']["results_belong_uid"],
        "contract_num": result['apartmentContract']["contract_num"],
        "sign_body": result['apartmentContract']["sign_body"],
        "sign_date": result['apartmentContract']["sign_date"],
        "apartment_check_in_date": result['apartmentContract']["apartment_check_in_date"],
        "rent_start_date": result['apartmentContract']["rent_start_date"],
        "rent_end_date": result['apartmentContract']["rent_end_date"],
        "payment_date": result['apartmentContract']["payment_date"],
        "deposit_type": result['apartmentContract']["deposit_type"],
        "payment_type": result['apartmentContract']["payment_type"],
        "payment_cycle": result['apartmentContract']["payment_cycle"],
        "financing_type": result['apartmentContract']["financing_type"],
        "cash_rent": result['apartmentContract']["cash_rent"],
        "deposit": result['apartmentContract']["deposit"],
        "agency_fee": result['apartmentContract']["agency_fee"],
        "month_server_fee": result['apartmentContract']["month_server_fee"],
        "month_server_fee_discount": result['apartmentContract']["month_server_fee_discount"],
        "load_interest": result['apartmentContract']["load_interest"],
        "remark": result['apartmentContract']["remark"],
        "dispostIn": result['apartmentContract']["dispostIn"],
        "sign_name": result['apartmentContract']["sign_name"],
        "sign_id_type": result['apartmentContract']["sign_id_type"],
        "sign_id_no": result['apartmentContract']["sign_id_no"],
        "sign_phone": result['apartmentContract']["sign_phone"],
        "sign_is_customer": result['apartmentContract']["sign_is_customer"],
        "address": result['apartmentContract']["property_address"],
        "model": "4",
        "achieveid": result['apartmentContract']["contract_id"],
        "activityId": "22",
        "content": "同意"}
    houseContractList_list = []
    houseContractList_list.append(empty_dict_null(result['houseContractList'][0]))
    data['houseContractList'] = houseContractList_list
    data["receivables"] = receivables
    data["person"] = person
    apartmentContractRentInfo = []
    apartmentContractRentInfo.append(apartmentContractRentInfoList)
    data["apartmentContractRentInfoList"] = apartmentContractRentInfo
    result = myRequest(url, str(data), Value=True)
    if result["code"] == 0:
        return "出租合同号:" + contract_num + "提交复审成功！"
    else:
        return "出租合同号:" + contract_num + "提交复审失败！错误返回：" + result["obj"]


@log
def update_sign_uid(contract_num):
    url = "http://erp.ishangzu.com/isz_housecontract/houseContractController/batchUpdateSign"
    try:
        sql = 'select contract_id from house_contract where contract_num = "%s"' % contract_num
        contract_id = searchSQL(sql)[0][0]
    except Exception as e:
        return "查询委托合同id信息sql报错。sql:" + sql + "。错误返回：" + str(e)

    data = {
	"contract_ids": [contract_id],
	"sign_did": "8A2152435E2E34E5015E30F811BB2653",
	"sign_did_name": u"测试专用组",
	"sign_uid": "1444",
	"sign_uid_name": u"测试专用 勿改"}

    result = myRequest(url,str(data),method="put",Value=True)
    if result["code"] == 0:
        return "委托合同号：" + contract_num + "。修改签约人成功！"
    else:
        return  "委托合同号：" + contract_num + "。修改签约人失败！错误返回：" + str(result["obj"])

