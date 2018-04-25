# -*- coding:UTF-8 -*-

"""
author = crazyzhong
2018年4月17日13:26:16
一键执行所有用例
"""

import unittest,time
from HTMLTestRunnerCN import HTMLTestRunner
from common import base
from erpRequest import contractRequest
from erpRequest import houseDevelopRequest
from erpRequest import decorationRequest
from erpRequest import apartmentRequest
from time import sleep
import os

test_dir = "./"
discover = unittest.defaultTestLoader.discover(test_dir,pattern="*TestCase.py")

base.host_set("mock")
contractRequest.get_cookie()


value = True
while value:
    if str(time.strftime("%H-%M-%S")) == "19-08-00":
        now = time.strftime("%Y-%m-%d %H_%M_%S")
        filename = test_dir + '/' + now + "result.html"
        fp = open(filename,"wb")
        runner = HTMLTestRunner(stream=fp,title=u"业绩接口自动化测试报告",description="用例执行情况：",tester="zhonglinglong")
        runner.run(discover)
        fp.close()

        path = []
        path.append(filename)
        path.append("D:\\PythonProject\\autoRequest\\achievementRequestAuto\\" + "autotest.log" )
        base.send_email(path)

        #发完邮件之后，删除日志及自动化报告
        os.remove("D:\\PythonProject\\autoRequest\\achievementRequestAuto\\" + "autotest.log")
        os.remove(filename)
        
        #执行完成用例之后构造下一次测试需要的数据
        contract_nums = []
        for i in range(4):
            contract_num = base.random_name()
            contract_nums.append(contract_num)

        print contractRequest.add_house_contract("业绩测试预发专用楼盘", contract_nums[0], base.now_time(-730), "品牌公寓", "整租", "大改")
        sleep(10)
        print decorationRequest.add_delivered_house(contract_nums[0])
        sleep(2)
        print contractRequest.reviewed_house_contract(contract_nums[0])
        sleep(2)
        print apartmentRequest.apartment_price_entire(contract_nums[0])

        print contractRequest.add_house_contract("业绩测试预发专用楼盘", contract_nums[1], base.now_time(-730), "品牌公寓", "合租", "大改")
        sleep(10)
        print decorationRequest.add_delivered_house(contract_nums[1])
        sleep(2)
        print contractRequest.reviewed_house_contract(contract_nums[1])
        sleep(2)
        print apartmentRequest.apartment_price_share(contract_nums[0],[3333,4444,5555])

        print contractRequest.add_house_contract("业绩测试预发专用楼盘", contract_nums[2], base.now_time(-730), "服务公寓", "整租", "微改")
        sleep(10)
        print decorationRequest.add_delivered_house(contract_nums[2])
        sleep(2)
        print contractRequest.reviewed_house_contract(contract_nums[2])
        sleep(2)
        print apartmentRequest.apartment_price_entire(contract_nums[2])

        print contractRequest.add_house_contract("业绩测试预发专用楼盘", contract_nums[3], base.now_time(-730), "服务公寓", "合租", "微改")
        sleep(2)
        print decorationRequest.add_delivered_house(contract_nums[3])
        sleep(2)
        print contractRequest.reviewed_house_contract(contract_nums[3])
        sleep(2)
        print apartmentRequest.apartment_price_share(contract_nums[3],[3333,4444,5555])

        base.set_conf("TestCaseDada",
                      HouseContractLossAchievementEndCalculateTestCase_trst_house_contract_loss_m=contract_nums[1])
        base.set_conf("TestCaseDada",
                      HouseContractLossAchievementEndCalculateTestCase_trst_house_contract_loss_n=contract_nums[3])
        base.set_conf("TestCaseDada",
                      HouseContractLossAchievementEndCalculateTestCase_trst_house_contract_loss_o=contract_nums[0])
        base.set_conf("TestCaseDada",
                      HouseContractLossAchievementEndCalculateTestCase_trst_house_contract_loss_p=contract_nums[2])

        houseDevelopRequest.add_house_delelop("业绩测试预发专用楼盘", 100)
    else:
        sleep(1)

