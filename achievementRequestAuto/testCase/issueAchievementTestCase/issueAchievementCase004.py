# -*- coding:UTF-8 -*-

"""
author = crazyzhong
2018年4月13日14:07:01
出单业绩接口测试用例
"""
case_description = u"品牌整租,出租合同复审验证业绩界面节点是否打√"

from erpRequest import houseDevelopRequest
from erpRequest import contractRequest
from erpRequest import  decorationRequest
from erpRequest import apartmentRequest
from erpRequest import  assemblyRequest
from erpRequest import  customerRequest
from erpRequest import  achievementRequest
from time import sleep


def issue_case_004():
    houseDevelopRequest.add_house_delelop("业绩测试预发专用楼盘", 1)
    contract_num = contractRequest.random_name()
    contractRequest.add_house_contract("业绩测试预发专用楼盘", contract_num, "2018-01-01", "品牌公寓", "整租", "大改")
    sleep(0.5)
    assemblyRequest.solr("apartment")
    decorationRequest.add_delivered_house(contract_num)
    sql = 'SELECT apartment_id from apartment where house_id =  (SELECT house_id from house_contract where contract_num = "%s") limit 1' % contract_num
    apartment_id = contractRequest.searchSQL(sql)[0][0]
    apartmentRequest.apartment_price_entire(contract_num)
    phone = customerRequest.add_phone_number()
    customerRequest.add_customer("testauto", phone)
    sql = 'SELECT apartment_code from apartment where apartment_id = "%s"' % apartment_id
    apartment_code = contractRequest.searchSQL(sql)[0][0]
    contract_nums = contractRequest.random_name()
    contractRequest.add_apartment_contract_entire(apartment_code, phone, contract_nums, "2018-02-01", "2019-01-31")
    contractRequest.reviewed_apartment_contract(contract_nums)
    result = achievementRequest.serach_issue_node(contract_nums)
    if result[u"出租合同已通过复审"] == "Y":
        return u"用例编号：issue_case_004测试通过！ 用例描述：" + case_description
    else:
        return u"用例编号：issue_case_004测试不通过！ 用例描述：" + case_description + u"测试结果：" + result

contractRequest.host_set("mock")
contractRequest.get_cookie()
print issue_case_004()
