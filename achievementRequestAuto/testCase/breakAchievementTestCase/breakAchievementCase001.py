# -*- coding:UTF-8 -*-

"""
author = crazyzhong
2018年4月17日10:33:31
违约业绩接口测试用例
"""
case_description = u"委托合同提交终止结算，选择业主违约。验证生成一条违约业绩"

from erpRequest import houseDevelopRequest
from erpRequest import contractRequest
from erpRequest import  achievementRequest
from erpRequest import  contractEndRequest
from time import sleep


def break_case_001():
    houseDevelopRequest.add_house_delelop("业绩测试预发专用楼盘", 1)
    contract_num = contractRequest.random_name()
    contractRequest.add_house_contract("业绩测试预发专用楼盘", contract_num, "2018-01-01", "品牌公寓", "整租", "大改")
    sleep(0.5)
    contractRequest.reviewed_house_contract(contract_num)
    contractEndRequest.house_contract_end(contract_num,"业主违约","2018-04-16")
    for i in range(10):
        result = achievementRequest.serach_break_details(contract_num)
        if result:
            break
        else:
            sleep(2)
    if result:
        return u"用例编号：break_case_001测试通过！ 用例描述：" + case_description
    else:
        return u"用例编号：break_case_001测试不通过！ 用例描述：" + case_description + u"测试结果：" + str(result)

contractRequest.host_set("mock")
contractRequest.get_cookie()
print break_case_001()