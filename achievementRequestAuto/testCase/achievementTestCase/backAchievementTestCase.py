# -*- coding:UTF-8 -*-

"""
author = crazyzhong
2018年4月20日17:41:51
扣回业绩接口测试用例
"""


from erpRequest import contractRequest
from erpRequest import  decorationRequest
from erpRequest import apartmentRequest
from erpRequest import  assemblyRequest
from erpRequest import  achievementRequest
from erpRequest import  contractEndRequest
from erpRequest import customerRequest
from common import base
from time import sleep
import unittest



class BackAchievementBrandEntireTestCase(unittest.TestCase):
    """品牌整租扣回业绩"""
    def setUp(self):
        base.consoleLog("-------------------------品牌整租扣回业绩生成用例集合strat----------------------")
        self.for_number = 100
        self.wait_time = 1
        self.contract_num = base.random_name()
        base.consoleLog(contractRequest.add_house_contract("业绩测试预发专用楼盘", self.contract_num, "2018-01-01", "品牌公寓", "整租", "大改"))

        for i in range(self.for_number):
            try:
                sql = "SELECT contract_num from query_house_contract where contract_num = '%s'" % self.contract_num
                base.searchSQL(sql)[0][0]
                break
            except Exception as e:
                base.consoleLog("委托合同未生成宽表，重新查询数据库。报错信息："+str(e) + "sql:" + sql,level='e')
                sleep(self.wait_time)
                pass

        base.consoleLog(assemblyRequest.ES_house_contract())
        base.consoleLog(decorationRequest.add_delivered_house(self.contract_num))

        for i in range(self.for_number):
            try:
                sql = 'SELECT apartment_id from apartment where house_id =  (SELECT house_id from house_contract where contract_num = "%s") limit 1' % self.contract_num
                self.apartment_id = base.searchSQL(sql)[0][0]
                base.consoleLog(apartmentRequest.apartment_price_entire(self.contract_num))
                self.phone = base.add_phone_number()
                base.consoleLog(customerRequest.add_customer("testauto", self.phone))
                sql = 'SELECT apartment_code from apartment where apartment_id = "%s"' % self.apartment_id
                self.apartment_code = base.searchSQL(sql)[0][0]
                break
            except Exception as e:
                base.consoleLog("房源定价失败或者没有生成自营房源。报错信息"+ str(e))
                sleep(self.wait_time)
                pass
    def tearDown(self):
        base.consoleLog("-------------------------品牌整租扣回业绩生成用例集合end------------------------")

    def test_back_case_a(self):
        """出租合同提交正退类型的终止结算，验证生成一条扣回业绩"""
        base.consoleLog("*********************出租合同提交正退类型的终止结算，验证生成一条扣回业绩***********************")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_entire(self.apartment_code, self.phone, contract_nums, "2018-02-01","2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums,"2019-01-31","正退"))

        for i in range(self.for_number):
            try:
                result = achievementRequest.serach_back_details(contract_nums)
                if result["code"] == 0:
                    break
            except Exception as e:
                base.consoleLog("查询扣回业绩接口报错。错误返回：" + str(e) + str(result))
                result = {}
                result["code"] = -1
                sleep(self.wait_time)

        base.consoleLog("用例执行完成。预期结果：0  测试结果：" + str(result["code"]))
        self.assertEqual(result["code"],0,msg="委托合同号：" + str(contract_nums))

    def test_back_case_b(self):
        """出租合同提交退租类型的终止结算，验证生成一条扣回业绩"""
        base.consoleLog("*************出租合同提交退租类型的终止结算，验证生成一条扣回业绩***************")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_entire(self.apartment_code, self.phone, contract_nums, "2018-02-01","2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums,"2019-01-31","退租"))

        for i in range(self.for_number):
            try:
                result = achievementRequest.serach_back_details(contract_nums)
                if result["code"] == 0:
                    break
            except Exception as e:
                base.consoleLog("查询扣回业绩接口报错。错误返回：" + str(e))
                result = {}
                result["code"] = -1
                sleep(self.wait_time)

        base.consoleLog("用例执行完成。预期结果：0  测试结果：" + str(result["code"]))
        self.assertEqual(result["code"],0,msg="委托合同号：" + str(contract_nums))

    def test_back_case_c(self):
        """出租合同提交转租类型的终止结算，验证生成一条扣回业绩"""
        base.consoleLog("******************出租合同提交转租类型的终止结算，验证生成一条扣回业绩*****************")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_entire(self.apartment_code, self.phone, contract_nums, "2018-02-01","2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums,"2019-01-31","转租"))

        for i in range(self.for_number):
            try:
                result = achievementRequest.serach_back_details(contract_nums)
                if result["code"] == 0:
                    break
            except Exception as e:
                base.consoleLog("查询扣回业绩接口报错。错误返回：" + str(e))
                result = {}
                result["code"] = -1
                sleep(self.wait_time)

        base.consoleLog("用例执行完成。预期结果：0  测试结果：" + str(result["code"]))
        self.assertEqual(result["code"],0,msg="委托合同号：" + str(contract_nums))

    def test_back_case_d(self):
        """出租合同提交换租类型的终止结算，验证生成一条扣回业绩"""
        base.consoleLog("****************出租合同提交换租类型的终止结算，验证生成一条扣回业绩*****************")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_entire(self.apartment_code, self.phone, contract_nums, "2018-02-01","2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums,"2019-01-31","换租"))

        for i in range(self.for_number):
            try:
                result = achievementRequest.serach_back_details(contract_nums)
                if result["code"] == 0:
                    break
            except Exception as e:
                base.consoleLog("查询扣回业绩接口报错。错误返回：" + str(e))
                result = {}
                result["code"] = -1
                sleep(self.wait_time)

        base.consoleLog("用例执行完成。预期结果：0  测试结果：" + str(result["code"]))
        self.assertEqual(result["code"],0,msg="委托合同号：" + str(contract_nums))

    def test_back_case_e(self):
        """出租合同提交收房类型的终止结算，验证生成一条扣回业绩"""
        base.consoleLog("*******************出租合同提交收房类型的终止结算，验证生成一条扣回业绩*****************")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_entire(self.apartment_code, self.phone, contract_nums, "2018-02-01","2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums,"2019-01-31","收房"))

        for i in range(self.for_number):
            try:
                result = achievementRequest.serach_back_details(contract_nums)
                if result["code"] == 0:
                    break
            except Exception as e:
                base.consoleLog("查询扣回业绩接口报错。错误返回：" + str(e))
                result = {}
                result["code"] = -1
                sleep(self.wait_time)

        base.consoleLog("用例执行完成。预期结果：0  测试结果：" + str(result["code"]))
        self.assertEqual(result["code"],0,msg="委托合同号：" + str(contract_nums))

class BackAchievementManageEntireTestCase(unittest.TestCase):
    """服务整租扣回业绩"""
    def setUp(self):
        base.consoleLog("-------------------------服务整租扣回业绩生成用例集合strat----------------------")
        self.for_number = 100
        self.wait_time = 1
        self.contract_num = base.random_name()
        base.consoleLog(contractRequest.add_house_contract("业绩测试预发专用楼盘", self.contract_num, "2018-01-01", "服务公寓", "整租", "微改"))

        for i in range(self.for_number):
            try:
                sql = "SELECT contract_num from query_house_contract where contract_num = '%s'" % self.contract_num
                base.searchSQL(sql)[0][0]
                break
            except Exception as e:
                base.consoleLog("委托合同未生成宽表，重新查询数据库。报错信息："+str(e) + "sql:" + sql,level='e')
                sleep(self.wait_time)
                pass

        base.consoleLog(assemblyRequest.ES_house_contract())
        base.consoleLog(decorationRequest.add_delivered_house(self.contract_num))

        for i in range(self.for_number):
            try:
                sql = 'SELECT apartment_id from apartment where house_id =  (SELECT house_id from house_contract where contract_num = "%s") limit 1' % self.contract_num
                self.apartment_id = base.searchSQL(sql)[0][0]
                base.consoleLog(apartmentRequest.apartment_price_entire(self.contract_num))
                self.phone = base.add_phone_number()
                base.consoleLog(customerRequest.add_customer("testauto", self.phone))
                sql = 'SELECT apartment_code from apartment where apartment_id = "%s"' % self.apartment_id
                self.apartment_code = base.searchSQL(sql)[0][0]
                break
            except Exception as e:
                base.consoleLog("房源定价失败或者没有生成自营房源。报错信息"+ str(e))
                sleep(self.wait_time)
                pass
    def tearDown(self):
        base.consoleLog("-------------------------服务整租扣回业绩生成用例集合end------------------------")

    def test_back_case_a(self):
        """出租合同提交正退类型的终止结算，验证生成一条扣回业绩"""
        base.consoleLog("*********************出租合同提交正退类型的终止结算，验证生成一条扣回业绩***********************")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_entire(self.apartment_code, self.phone, contract_nums, "2018-02-01","2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums,"2019-01-31","正退"))

        for i in range(self.for_number):
            try:
                result = achievementRequest.serach_back_details(contract_nums)
                if result["code"] == 0:
                    break
            except Exception as e:
                base.consoleLog("查询扣回业绩接口报错。错误返回：" + str(e))
                result = {}
                result["code"] = -1
                sleep(self.wait_time)

        base.consoleLog("用例执行完成。预期结果：0  测试结果：" + str(result["code"]))
        self.assertEqual(result["code"],0,msg="委托合同号：" + str(contract_nums))

    def test_back_case_b(self):
        """出租合同提交退租类型的终止结算，验证生成一条扣回业绩"""
        base.consoleLog("*************出租合同提交退租类型的终止结算，验证生成一条扣回业绩***************")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_entire(self.apartment_code, self.phone, contract_nums, "2018-02-01","2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums,"2019-01-31","退租"))

        for i in range(self.for_number):
            try:
                result = achievementRequest.serach_back_details(contract_nums)
                if result["code"] == 0:
                    break
            except Exception as e:
                base.consoleLog("查询扣回业绩接口报错。错误返回：" + str(e))
                result = {}
                result["code"] = -1
                sleep(self.wait_time)

        base.consoleLog("用例执行完成。预期结果：0  测试结果：" + str(result["code"]))
        self.assertEqual(result["code"],0,msg="委托合同号：" + str(contract_nums))

    def test_back_case_c(self):
        """出租合同提交转租类型的终止结算，验证生成一条扣回业绩"""
        base.consoleLog("******************出租合同提交转租类型的终止结算，验证生成一条扣回业绩*****************")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_entire(self.apartment_code, self.phone, contract_nums, "2018-02-01","2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums,"2019-01-31","转租"))

        for i in range(self.for_number):
            try:
                result = achievementRequest.serach_back_details(contract_nums)
                if result["code"] == 0:
                    break
            except Exception as e:
                base.consoleLog("查询扣回业绩接口报错。错误返回：" + str(e))
                result = {}
                result["code"] = -1
                sleep(self.wait_time)

        base.consoleLog("用例执行完成。预期结果：0  测试结果：" + str(result["code"]))
        self.assertEqual(result["code"],0,msg="委托合同号：" + str(contract_nums))

    def test_back_case_d(self):
        """出租合同提交换租类型的终止结算，验证生成一条扣回业绩"""
        base.consoleLog("****************出租合同提交换租类型的终止结算，验证生成一条扣回业绩*****************")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_entire(self.apartment_code, self.phone, contract_nums, "2018-02-01","2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums,"2019-01-31","换租"))

        for i in range(self.for_number):
            try:
                result = achievementRequest.serach_back_details(contract_nums)
                if result["code"] == 0:
                    break
            except Exception as e:
                base.consoleLog("查询扣回业绩接口报错。错误返回：" + str(e))
                result = {}
                result["code"] = -1
                sleep(self.wait_time)

        base.consoleLog("用例执行完成。预期结果：0  测试结果：" + str(result["code"]))
        self.assertEqual(result["code"],0,msg="委托合同号：" + str(contract_nums))

    def test_back_case_e(self):
        """出租合同提交收房类型的终止结算，验证生成一条扣回业绩"""
        base.consoleLog("*******************出租合同提交收房类型的终止结算，验证生成一条扣回业绩*****************")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_entire(self.apartment_code, self.phone, contract_nums, "2018-02-01","2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums,"2019-01-31","收房"))

        for i in range(self.for_number):
            try:
                result = achievementRequest.serach_back_details(contract_nums)
                if result["code"] == 0:
                    break
            except Exception as e:
                base.consoleLog("查询扣回业绩接口报错。错误返回：" + str(e))
                result = {}
                result["code"] = -1
                sleep(self.wait_time)

        base.consoleLog("用例执行完成。预期结果：0  测试结果：" + str(result["code"]))
        self.assertEqual(result["code"],0,msg="委托合同号：" + str(contract_nums))

class BackAchievementBrandShareTestCase(unittest.TestCase):
    """品牌合租扣回业绩"""
    def setUp(self):
        base.consoleLog("-------------------------品牌合租扣回业绩生成用例集合strat----------------------")
        self.for_number = 100
        self.wait_time = 1
        self.contract_num = base.random_name()
        base.consoleLog(contractRequest.add_house_contract("业绩测试预发专用楼盘", self.contract_num, "2018-01-01", "品牌公寓", "合租", "大改"))

        for i in range(self.for_number):
            try:
                sql = "SELECT contract_num from query_house_contract where contract_num = '%s'" % self.contract_num
                base.searchSQL(sql)[0][0]
                break
            except Exception as e:
                base.consoleLog("委托合同未生成宽表，重新查询数据库。报错信息："+str(e) + "sql:" + sql,level='e')
                sleep(self.wait_time)
                pass

        base.consoleLog(assemblyRequest.ES_house_contract())
        base.consoleLog(decorationRequest.add_delivered_house(self.contract_num))

        for i in range(self.for_number):
            try:
                sql = 'SELECT apartment_id from apartment where house_id =  (SELECT house_id from house_contract where contract_num = "%s") limit 1' % self.contract_num
                self.apartment_id = base.searchSQL(sql)[0][0]
                base.consoleLog(apartmentRequest.apartment_price_share(self.contract_num,[3333,4444,5555]))
                self.phone = base.add_phone_number()
                base.consoleLog(customerRequest.add_customer("testauto", self.phone))
                sql = 'SELECT apartment_code from apartment where apartment_id = "%s"' % self.apartment_id
                self.apartment_code = base.searchSQL(sql)[0][0]
                break
            except Exception as e:
                base.consoleLog("房源定价失败或者没有生成自营房源。报错信息"+ str(e))
                sleep(self.wait_time)
                pass
    def tearDown(self):
        base.consoleLog("-------------------------品牌合租扣回业绩生成用例集合end------------------------")

    def test_back_case_a(self):
        """出租合同提交正退类型的终止结算，验证生成一条扣回业绩"""
        base.consoleLog("*********************出租合同提交正退类型的终止结算，验证生成一条扣回业绩***********************")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_share(self.apartment_code, self.phone, contract_nums, "2018-02-01","2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums,"2019-01-31","正退"))

        for i in range(self.for_number):
            try:
                result = achievementRequest.serach_back_details(contract_nums)
                if result["code"] == 0:
                    break
            except Exception as e:
                base.consoleLog("查询扣回业绩接口报错。错误返回：" + str(e))
                result = {}
                result["code"] = -1
                sleep(self.wait_time)

        base.consoleLog("用例执行完成。预期结果：0  测试结果：" + str(result["code"]))
        self.assertEqual(result["code"],0,msg="委托合同号：" + str(contract_nums))

    def test_back_case_b(self):
        """出租合同提交退租类型的终止结算，验证生成一条扣回业绩"""
        base.consoleLog("*************出租合同提交退租类型的终止结算，验证生成一条扣回业绩***************")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_share(self.apartment_code, self.phone, contract_nums, "2018-02-01","2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums,"2019-01-31","退租"))

        for i in range(self.for_number):
            try:
                result = achievementRequest.serach_back_details(contract_nums)
                if result["code"] == 0:
                    break
            except Exception as e:
                base.consoleLog("查询扣回业绩接口报错。错误返回：" + str(e))
                result = {}
                result["code"] = -1
                sleep(self.wait_time)

        base.consoleLog("用例执行完成。预期结果：0  测试结果：" + str(result["code"]))
        self.assertEqual(result["code"],0,msg="委托合同号：" + str(contract_nums))

    def test_back_case_c(self):
        """出租合同提交转租类型的终止结算，验证生成一条扣回业绩"""
        base.consoleLog("******************出租合同提交转租类型的终止结算，验证生成一条扣回业绩*****************")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_share(self.apartment_code, self.phone, contract_nums, "2018-02-01","2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums,"2019-01-31","转租"))

        for i in range(self.for_number):
            try:
                result = achievementRequest.serach_back_details(contract_nums)
                if result["code"] == 0:
                    break
            except Exception as e:
                base.consoleLog("查询扣回业绩接口报错。错误返回：" + str(e))
                result = {}
                result["code"] = -1
                sleep(self.wait_time)

        base.consoleLog("用例执行完成。预期结果：0  测试结果：" + str(result["code"]))
        self.assertEqual(result["code"],0,msg="委托合同号：" + str(contract_nums))

    def test_back_case_d(self):
        """出租合同提交换租类型的终止结算，验证生成一条扣回业绩"""
        base.consoleLog("****************出租合同提交换租类型的终止结算，验证生成一条扣回业绩*****************")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_share(self.apartment_code, self.phone, contract_nums, "2018-02-01","2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums,"2019-01-31","换租"))

        for i in range(self.for_number):
            try:
                result = achievementRequest.serach_back_details(contract_nums)
                if result["code"] == 0:
                    break
            except Exception as e:
                base.consoleLog("查询扣回业绩接口报错。错误返回：" + str(e))
                result = {}
                result["code"] = -1
                sleep(self.wait_time)

        base.consoleLog("用例执行完成。预期结果：0  测试结果：" + str(result["code"]))
        self.assertEqual(result["code"],0,msg="委托合同号：" + str(contract_nums))

    def test_back_case_e(self):
        """出租合同提交收房类型的终止结算，验证生成一条扣回业绩"""
        base.consoleLog("*******************出租合同提交收房类型的终止结算，验证生成一条扣回业绩*****************")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_share(self.apartment_code, self.phone, contract_nums, "2018-02-01","2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums,"2019-01-31","收房"))

        for i in range(self.for_number):
            try:
                result = achievementRequest.serach_back_details(contract_nums)
                if result["code"] == 0:
                    break
            except Exception as e:
                base.consoleLog("查询扣回业绩接口报错。错误返回：" + str(e))
                result = {}
                result["code"] = -1
                sleep(self.wait_time)

        base.consoleLog("用例执行完成。预期结果：0  测试结果：" + str(result["code"]))
        self.assertEqual(result["code"],0,msg="委托合同号：" + str(contract_nums))

class BackAchievementManageShareTestCase(unittest.TestCase):
    """服务合租扣回业绩"""
    def setUp(self):
        base.consoleLog("-------------------------品牌合租扣回业绩生成用例集合strat----------------------")
        self.for_number = 100
        self.wait_time = 1
        self.contract_num = base.random_name()
        base.consoleLog(contractRequest.add_house_contract("业绩测试预发专用楼盘", self.contract_num, "2018-01-01", "服务公寓", "合租", "微改"))

        for i in range(self.for_number):
            try:
                sql = "SELECT contract_num from query_house_contract where contract_num = '%s'" % self.contract_num
                base.searchSQL(sql)[0][0]
                break
            except Exception as e:
                base.consoleLog("委托合同未生成宽表，重新查询数据库。报错信息："+str(e) + "sql:" + sql,level='e')
                sleep(self.wait_time)
                pass

        base.consoleLog(assemblyRequest.ES_house_contract())
        base.consoleLog(decorationRequest.add_delivered_house(self.contract_num))

        for i in range(self.for_number):
            try:
                sql = 'SELECT apartment_id from apartment where house_id =  (SELECT house_id from house_contract where contract_num = "%s") limit 1' % self.contract_num
                self.apartment_id = base.searchSQL(sql)[0][0]
                base.consoleLog(apartmentRequest.apartment_price_share(self.contract_num,[3333,4444,5555]))
                self.phone = base.add_phone_number()
                base.consoleLog(customerRequest.add_customer("testauto", self.phone))
                sql = 'SELECT apartment_code from apartment where apartment_id = "%s"' % self.apartment_id
                self.apartment_code = base.searchSQL(sql)[0][0]
                break
            except Exception as e:
                base.consoleLog("房源定价失败或者没有生成自营房源。报错信息"+ str(e))
                sleep(self.wait_time)
                pass
    def tearDown(self):
        base.consoleLog("-------------------------品牌合租扣回业绩生成用例集合end------------------------")

    def test_back_case_a(self):
        """出租合同提交正退类型的终止结算，验证生成一条扣回业绩"""
        base.consoleLog("*********************出租合同提交正退类型的终止结算，验证生成一条扣回业绩***********************")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_share(self.apartment_code, self.phone, contract_nums, "2018-02-01","2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums,"2019-01-31","正退"))

        for i in range(self.for_number):
            try:
                result = achievementRequest.serach_back_details(contract_nums)
                if result["code"] == 0:
                    break
            except Exception as e:
                base.consoleLog("查询扣回业绩接口报错。错误返回：" + str(e))
                result = {}
                result["code"] = -1
                sleep(self.wait_time)

        base.consoleLog("用例执行完成。预期结果：0  测试结果：" + str(result["code"]))
        self.assertEqual(result["code"],0,msg="委托合同号：" + str(contract_nums))

    def test_back_case_b(self):
        """出租合同提交退租类型的终止结算，验证生成一条扣回业绩"""
        base.consoleLog("*************出租合同提交退租类型的终止结算，验证生成一条扣回业绩***************")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_share(self.apartment_code, self.phone, contract_nums, "2018-02-01","2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums,"2019-01-31","退租"))

        for i in range(self.for_number):
            try:
                result = achievementRequest.serach_back_details(contract_nums)
                if result["code"] == 0:
                    break
            except Exception as e:
                base.consoleLog("查询扣回业绩接口报错。错误返回：" + str(e))
                result = {}
                result["code"] = -1
                sleep(self.wait_time)

        base.consoleLog("用例执行完成。预期结果：0  测试结果：" + str(result["code"]))
        self.assertEqual(result["code"],0,msg="委托合同号：" + str(contract_nums))

    def test_back_case_c(self):
        """出租合同提交转租类型的终止结算，验证生成一条扣回业绩"""
        base.consoleLog("******************出租合同提交转租类型的终止结算，验证生成一条扣回业绩*****************")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_share(self.apartment_code, self.phone, contract_nums, "2018-02-01","2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums,"2019-01-31","转租"))

        for i in range(self.for_number):
            try:
                result = achievementRequest.serach_back_details(contract_nums)
                if result["code"] == 0:
                    break
            except Exception as e:
                base.consoleLog("查询扣回业绩接口报错。错误返回：" + str(e))
                result = {}
                result["code"] = -1
                sleep(self.wait_time)

        base.consoleLog("用例执行完成。预期结果：0  测试结果：" + str(result["code"]))
        self.assertEqual(result["code"],0,msg="委托合同号：" + str(contract_nums))

    def test_back_case_d(self):
        """出租合同提交换租类型的终止结算，验证生成一条扣回业绩"""
        base.consoleLog("****************出租合同提交换租类型的终止结算，验证生成一条扣回业绩*****************")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_share(self.apartment_code, self.phone, contract_nums, "2018-02-01","2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums,"2019-01-31","换租"))

        for i in range(self.for_number):
            try:
                result = achievementRequest.serach_back_details(contract_nums)
                if result["code"] == 0:
                    break
            except Exception as e:
                base.consoleLog("查询扣回业绩接口报错。错误返回：" + str(e))
                result = {}
                result["code"] = -1
                sleep(self.wait_time)

        base.consoleLog("用例执行完成。预期结果：0  测试结果：" + str(result["code"]))
        self.assertEqual(result["code"],0,msg="委托合同号：" + str(contract_nums))

    def test_back_case_e(self):
        """出租合同提交收房类型的终止结算，验证生成一条扣回业绩"""
        base.consoleLog("*******************出租合同提交收房类型的终止结算，验证生成一条扣回业绩*****************")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_share(self.apartment_code, self.phone, contract_nums, "2018-02-01","2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums,"2019-01-31","收房"))

        for i in range(self.for_number):
            try:
                result = achievementRequest.serach_back_details(contract_nums)
                if result["code"] == 0:
                    break
            except Exception as e:
                base.consoleLog("查询扣回业绩接口报错。错误返回：" + str(e))
                result = {}
                result["code"] = -1
                sleep(self.wait_time)

        base.consoleLog("用例执行完成。预期结果：0  测试结果：" + str(result["code"]))
        self.assertEqual(result["code"],0,msg="委托合同号：" + str(contract_nums))

if  __name__ == "__main__":
    base.host_set("mock")
    contractRequest.get_cookie()
    unittest.main()