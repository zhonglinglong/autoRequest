# -*- coding:UTF-8 -*-

"""
author = crazyzhong
2018年4月16日18:08:59
出单业绩接口测试用例
前承租合同终止结算已通过复审（针对转租、退租、换租和收房）
"""
case_description = u"品牌整租,前承租合同终止结算类型是收房，已复审。首付款完成。已交房，已有装修装成本，出租合同复审，委托合同复审。满足所有条件，验证生成一条已生效的业绩"

from erpRequest import houseDevelopRequest
from erpRequest import contractRequest
from erpRequest import  decorationRequest
from erpRequest import apartmentRequest
from erpRequest import  assemblyRequest
from erpRequest import  customerRequest
from erpRequest import  achievementRequest
from erpRequest import  contractEndRequest
from erpRequest import financeRequest
from time import sleep


def issue_case_015():
    houseDevelopRequest.add_house_delelop("业绩测试预发专用楼盘", 1)
    contract_num = contractRequest.random_name()
    contractRequest.add_house_contract("业绩测试预发专用楼盘", contract_num, "2018-01-01", "品牌公寓", "整租", "大改")
    sleep(0.5)
    assemblyRequest.solr("apartment")
    contractRequest.reviewed_house_contract(contract_num)
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
    sleep(1)
    contractRequest.reviewed_apartment_contract(contract_nums)
    contractEndRequest.apartment_contract_end(contract_nums,"2019-01-31","收房","2018-04-01")
    sleep(1)
    contractEndRequest.reviewed_apartment_contract_end(contract_nums)
    contract_numss = contractRequest.random_name()
    phones = contractRequest.add_phone_number()
    customerRequest.add_customer("testauto", phones)
    contractRequest.add_apartment_contract_entire(apartment_code, phones, contract_numss, "2018-04-16", "2019-01-31")
    sleep(1)
    contractRequest.reviewed_apartment_contract(contract_numss)
    financeRequest.apartment_contract_collecting_money(contract_numss)
    for i in range(10):
        result = achievementRequest.serach_issue_state(contract_numss)
        if result != "Y":
            sleep(3)
        else:
            break
    if result == "Y":
        return u"用例编号：issue_case_015测试通过！ 用例描述：" + case_description
    else:
        return u"用例编号：issue_case_015测试不通过！ 用例描述：" + case_description + u"测试结果：" + result

contractRequest.host_set("mock")
contractRequest.get_cookie()
print issue_case_015()