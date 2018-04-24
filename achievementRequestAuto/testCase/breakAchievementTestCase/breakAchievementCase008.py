# -*- coding:UTF-8 -*-

"""
author = crazyzhong
2018年4月17日10:33:15
违约业绩接口测试用例
"""
case_description = u"出租提交终止结算，选择正租。验证不生成一条违约业绩"

from erpRequest import houseDevelopRequest
from erpRequest import contractRequest
from erpRequest import  achievementRequest
from erpRequest import  customerRequest
from erpRequest import  contractEndRequest
from erpRequest import assemblyRequest
from erpRequest import  apartmentRequest
from time import sleep


def break_case_008():
    houseDevelopRequest.add_house_delelop("业绩测试预发专用楼盘", 1)
    contract_num = contractRequest.random_name()
    contractRequest.add_house_contract("业绩测试预发专用楼盘", contract_num, "2018-01-01", "品牌公寓", "整租", "大改")
    sleep(0.5)
    assemblyRequest.solr("apartment")
    apartmentRequest.apartment_price_entire(contract_num)
    phone = contractRequest.add_phone_number()
    customerRequest.add_customer("autotest", phone)
    sql = 'SELECT apartment_id from apartment where house_id =  (SELECT house_id from house_contract where contract_num = "%s") limit 1' % contract_num
    apartment_id = contractRequest.searchSQL(sql)[0][0]
    sql = 'SELECT apartment_code from apartment where apartment_id = "%s"' % apartment_id
    apartment_code = contractRequest.searchSQL(sql)[0][0]
    contract_nums = contractRequest.random_name()
    contractRequest.add_apartment_contract_entire(apartment_code,phone,contract_nums,"2018-04-16","2018-12-30")
    contractRequest.reviewed_apartment_contract(contract_nums)
    contractEndRequest.apartment_contract_end(contract_nums,"2018-12-30","正退")
    for i in range(10):
        result = achievementRequest.serach_break_details(contract_nums)
        if result:
            break
        else:
            sleep(2)
    if not result:
        return u"用例编号：break_case_008测试通过！ 用例描述：" + case_description
    else:
        return u"用例编号：break_case_008测试不通过！ 用例描述：" + case_description + u"测试结果：" + str(result)+ u"测试数据。出租合同号："+contract_nums

contractRequest.host_set("mock")
contractRequest.get_cookie()
print break_case_008()