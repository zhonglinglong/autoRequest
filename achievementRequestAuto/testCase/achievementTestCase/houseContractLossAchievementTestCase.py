# -*- coding:UTF-8 -*-

"""
author = crazyzhong
2018年4月22日09:07:22
亏损业绩接口测试用例
"""

from erpRequest import contractRequest
from erpRequest import  decorationRequest
from erpRequest import apartmentRequest
from erpRequest import  assemblyRequest
from erpRequest import  achievementRequest
from erpRequest import  contractEndRequest
from common import base
from time import sleep
import unittest

base.host_set("mock")
contractRequest.get_cookie()

# class HouseContractLossAchievementSignerChangeTestCase(unittest.TestCase):
#     """亏损业绩之资源划转用例测试集合"""
#     def setUp(self):
#         base.consoleLog("-------------------------亏损业绩之资源划转生成用例集合strat----------------------")
#         self.for_number = 100
#         self.wait_time = 1
#         self.contract_num = base.random_name()
#
#     def tearDown(self):
#         base.consoleLog("-------------------------亏损业绩之资源划转生成用例集合end------------------------")
#
#     def test_house_contract_loss_a(self):
#         """品牌合租,房源定价,修改签约人。验证：生成一条资源划转业绩"""
#         base.consoleLog("*******************品牌合租,房源定价,修改签约人。验证：生成一条资源划转业绩*************************")
#         base.consoleLog(
#             contractRequest.add_house_contract("业绩测试预发专用楼盘", self.contract_num, "2018-01-01", "品牌公寓", "合租", "大改"))
#         for i in range(self.for_number):
#             try:
#                 sql = "SELECT contract_num from query_house_contract where contract_num = '%s'" % self.contract_num
#                 base.searchSQL(sql)[0][0]
#                 break
#             except Exception as e:
#                 base.consoleLog("委托合同未生成宽表，重新查询数据库。报错信息：" + str(e) + "sql:" + sql, level='e')
#                 sleep(self.wait_time)
#                 pass
#         base.consoleLog(assemblyRequest.ES_house_contract())
#         base.consoleLog(decorationRequest.add_delivered_house(self.contract_num))
#         base.consoleLog(assemblyRequest.solr("apartment"))
#         base.consoleLog(contractRequest.reviewed_house_contract(self.contract_num))
#         base.consoleLog(apartmentRequest.apartment_price_share(self.contract_num,[3333,4444,5555]))
#         base.consoleLog(contractRequest.update_sign_uid(self.contract_num))
#
#         for i in range(self.for_number):
#             try:
#                 result = achievementRequest.serach_house_contract_loss_details(self.contract_num)
#                 if result["code"] == 0:
#                     break
#             except Exception as e:
#                 base.consoleLog("查询亏损业绩接口返回报错。错误信息：" + str(e))
#                 sleep(self.wait_time)
#                 result = {}
#                 result["code"] = -1
#                 pass
#         base.consoleLog("用例执行完成。预期结果：0.测试结果：" + str(result["code"]))
#         self.assertEqual(result["code"],0,msg="委托合同：" + str(self.contract_num))
#
#     def test_house_contract_loss_b(self):
#         """服务合租,房源定价,修改签约人。验证：生成一条资源划转业绩"""
#         base.consoleLog("*******************服务合租,房源定价,修改签约人。验证：生成一条资源划转业绩*************************")
#         base.consoleLog(
#             contractRequest.add_house_contract("业绩测试预发专用楼盘", self.contract_num, "2018-01-01", "服务公寓", "合租", "微改"))
#         for i in range(self.for_number):
#             try:
#                 sql = "SELECT contract_num from query_house_contract where contract_num = '%s'" % self.contract_num
#                 base.searchSQL(sql)[0][0]
#                 break
#             except Exception as e:
#                 base.consoleLog("委托合同未生成宽表，重新查询数据库。报错信息：" + str(e) + "sql:" + sql, level='e')
#                 sleep(self.wait_time)
#                 pass
#         base.consoleLog(assemblyRequest.ES_house_contract())
#         base.consoleLog(decorationRequest.add_delivered_house(self.contract_num))
#         base.consoleLog(assemblyRequest.solr("apartment"))
#         base.consoleLog(contractRequest.reviewed_house_contract(self.contract_num))
#         base.consoleLog(apartmentRequest.apartment_price_share(self.contract_num,[3333,4444,5555]))
#         base.consoleLog(contractRequest.update_sign_uid(self.contract_num))
#
#         for i in range(self.for_number):
#             try:
#                 result = achievementRequest.serach_house_contract_loss_details(self.contract_num)
#                 if result["code"] == 0:
#                     break
#             except Exception as e:
#                 base.consoleLog("查询亏损业绩接口返回报错。错误信息：" + str(e))
#                 sleep(self.wait_time)
#                 result = {}
#                 result["code"] = -1
#                 pass
#         base.consoleLog("用例执行完成。预期结果：0.测试结果：" + str(result["code"]))
#         self.assertEqual(result["code"],0,msg="委托合同：" + str(self.contract_num))
#
#     def test_house_contract_loss_c(self):
#         """品牌整租,房源定价,修改签约人。验证：生成一条资源划转业绩"""
#         base.consoleLog("*******************品牌整租,房源定价,修改签约人。验证：生成一条资源划转业绩*************************")
#         base.consoleLog(
#             contractRequest.add_house_contract("业绩测试预发专用楼盘", self.contract_num, "2018-01-01", "品牌公寓", "整租", "大改"))
#         for i in range(self.for_number):
#             try:
#                 sql = "SELECT contract_num from query_house_contract where contract_num = '%s'" % self.contract_num
#                 base.searchSQL(sql)[0][0]
#                 break
#             except Exception as e:
#                 base.consoleLog("委托合同未生成宽表，重新查询数据库。报错信息：" + str(e) + "sql:" + sql, level='e')
#                 sleep(self.wait_time)
#                 pass
#         base.consoleLog(assemblyRequest.ES_house_contract())
#         base.consoleLog(decorationRequest.add_delivered_house(self.contract_num))
#         base.consoleLog(assemblyRequest.solr("apartment"))
#         base.consoleLog(contractRequest.reviewed_house_contract(self.contract_num))
#         base.consoleLog(contractRequest.update_sign_uid(self.contract_num))
#
#         for i in range(self.for_number):
#             try:
#                 result = achievementRequest.serach_house_contract_loss_details(self.contract_num)
#                 if result["code"] == 0:
#                     break
#             except Exception as e:
#                 base.consoleLog("查询亏损业绩接口返回报错。错误信息：" + str(e))
#                 sleep(self.wait_time)
#                 result = {}
#                 result["code"] = -1
#                 pass
#         base.consoleLog("用例执行完成。预期结果：0.测试结果：" + str(result["code"]))
#         self.assertEqual(result["code"],0,msg="委托合同：" + str(self.contract_num))
#
#     def test_house_contract_loss_d(self):
#         """服务整租,房源定价,修改签约人。验证：生成一条资源划转业绩"""
#         base.consoleLog("*******************服务整租,房源定价,修改签约人。验证：生成一条资源划转业绩*************************")
#         base.consoleLog(
#             contractRequest.add_house_contract("业绩测试预发专用楼盘", self.contract_num, "2018-01-01", "服务公寓", "整租", "微改"))
#         for i in range(self.for_number):
#             try:
#                 sql = "SELECT contract_num from query_house_contract where contract_num = '%s'" % self.contract_num
#                 base.searchSQL(sql)[0][0]
#                 break
#             except Exception as e:
#                 base.consoleLog("委托合同未生成宽表，重新查询数据库。报错信息：" + str(e) + "sql:" + sql, level='e')
#                 sleep(self.wait_time)
#                 pass
#         base.consoleLog(assemblyRequest.ES_house_contract())
#         base.consoleLog(decorationRequest.add_delivered_house(self.contract_num))
#         base.consoleLog(assemblyRequest.solr("apartment"))
#         base.consoleLog(contractRequest.reviewed_house_contract(self.contract_num))
#         base.consoleLog(contractRequest.update_sign_uid(self.contract_num))
#
#         for i in range(self.for_number):
#             try:
#                 result = achievementRequest.serach_house_contract_loss_details(self.contract_num)
#                 if result["code"] == 0:
#                     break
#             except Exception as e:
#                 base.consoleLog("查询亏损业绩接口返回报错。错误信息：" + str(e))
#                 sleep(self.wait_time)
#                 result = {}
#                 result["code"] = -1
#                 pass
#         base.consoleLog("用例执行完成。预期结果：0.测试结果：" + str(result["code"]))
#         self.assertEqual(result["code"],0,msg="委托合同：" + str(self.contract_num))

class HouseContractLossAchievementFireCalculateTestCase(unittest.TestCase):
    """亏损业绩之着火结算用例测试集合"""
    def setUp(self):
        base.consoleLog("-------------------------亏损业绩之着火结算生成用例集合strat----------------------")
        self.for_number = 100
        self.wait_time = 1
        self.contract_num = base.random_name()

    def tearDown(self):
        base.consoleLog("-------------------------亏损业绩之着火结算生成用例集合end------------------------")

    def test_house_contract_loss_a(self):
        """品牌合租,房源定价,跑下着火定时器。验证：生成一条着火结算业绩"""
        base.consoleLog("*******************品牌合租,房源定价,跑下着火。验证：生成一条着火结算业绩*************************")
        base.consoleLog(
            contractRequest.add_house_contract("业绩测试预发专用楼盘", self.contract_num, "2018-01-01", "品牌公寓", "合租", "大改"))
        for i in range(self.for_number):
            try:
                sql = 'UPDATE house_contract set create_time = "2018-01-01 15:13:43" where contract_num ="%s"' % self.contract_num
                base.updateSQL(sql)
                sql = "SELECT contract_num from query_house_contract where contract_num = '%s'" % self.contract_num
                base.searchSQL(sql)[0][0]
                base.consoleLog(contractRequest.reviewed_house_contract(self.contract_num))
                base.consoleLog(assemblyRequest.ES_house_contract())
                base.consoleLog(decorationRequest.add_delivered_house(self.contract_num))
                base.consoleLog(assemblyRequest.solr("apartment"))
                break
            except Exception as e:
                base.consoleLog("委托合同未生成宽表，重新查询数据库。报错信息：" + str(e) + "sql:" + sql, level='e')
                sleep(self.wait_time)
                pass

        for i in range(self.for_number):
            try:
                sql = 'SELECT apartment_id from apartment where house_id =  (SELECT house_id from house_contract where contract_num = "%s") limit 1' % self.contract_num
                apartment_id = contractRequest.searchSQL(sql)[0][0]
                break
            except Exception as e:
                base.consoleLog("查询sql异常。sql:" + sql + "错误返回：" + str(e))
                sleep(self.wait_time)
        base.consoleLog(apartmentRequest.apartment_price_share(self.contract_num, [3333, 4444, 5555]))

        for i in range(self.for_number):
            try:
                base.consoleLog(apartmentRequest.apartment_fire_calculate(apartment_id))
                result = achievementRequest.serach_house_contract_loss_details(self.contract_num)
                if result["code"] == 0:
                    break
            except Exception as e:
                base.consoleLog("查询亏损业绩接口返回报错。错误信息：" + str(e))
                sleep(self.wait_time)
                result = {}
                result["code"] = -1
                pass
        base.consoleLog("用例执行完成。预期结果：0.测试结果：" + str(result["code"]))
        self.assertEqual(result["code"],0,msg="委托合同：" + str(self.contract_num))

    def test_house_contract_loss_b(self):
        """服务合租,房源定价,跑下着火定时器。验证：生成一条着火结算业绩"""
        base.consoleLog("*******************服务合租,房源定价,跑下着火定时器。验证：生成一条着火结算业绩*************************")
        base.consoleLog(
            contractRequest.add_house_contract("业绩测试预发专用楼盘", self.contract_num, "2018-01-01", "服务公寓", "合租", "微改"))
        for i in range(self.for_number):
            try:
                sql = 'UPDATE house_contract set create_time = "2018-01-01 15:13:43" where contract_num ="%s"' % self.contract_num
                base.updateSQL(sql)
                sql = "SELECT contract_num from query_house_contract where contract_num = '%s'" % self.contract_num
                base.searchSQL(sql)[0][0]
                base.consoleLog(contractRequest.reviewed_house_contract(self.contract_num))
                base.consoleLog(assemblyRequest.ES_house_contract())
                base.consoleLog(decorationRequest.add_delivered_house(self.contract_num))
                base.consoleLog(assemblyRequest.solr("apartment"))
                break
            except Exception as e:
                base.consoleLog("委托合同未生成宽表，重新查询数据库。报错信息：" + str(e) + "sql:" + sql, level='e')
                sleep(self.wait_time)
                pass


        for i in range(self.for_number):
            try:
                sql = 'SELECT apartment_id from apartment where house_id =  (SELECT house_id from house_contract where contract_num = "%s") limit 1' % self.contract_num
                apartment_id = contractRequest.searchSQL(sql)[0][0]
                base.consoleLog(apartmentRequest.apartment_price_share(self.contract_num, [3333, 4444, 5555]))
                break
            except Exception as e:
                base.consoleLog("查询sql异常。sql:" + sql + "错误返回：" + str(e))
                sleep(self.wait_time)


        for i in range(self.for_number):
            try:
                base.consoleLog(apartmentRequest.apartment_fire_calculate(apartment_id))
                result = achievementRequest.serach_house_contract_loss_details(self.contract_num)
                if result["code"] == 0:
                    break
            except Exception as e:
                base.consoleLog("查询亏损业绩接口返回报错。错误信息：" + str(e))
                sleep(self.wait_time)
                result = {}
                result["code"] = -1
                pass
        base.consoleLog("用例执行完成。预期结果：0.测试结果：" + str(result["code"]))
        self.assertEqual(result["code"],0,msg="委托合同：" + str(self.contract_num))

    def test_house_contract_loss_c(self):
        """品牌整租,跑下着火定时器。验证：生成一条着火结算业绩"""
        base.consoleLog("*******************品牌整租,跑下着火定时器。验证：生成一条着火结算业绩*************************")
        base.consoleLog(
            contractRequest.add_house_contract("业绩测试预发专用楼盘", self.contract_num, "2018-01-01", "品牌公寓", "整租", "大改"))
        for i in range(self.for_number):
            try:
                sql = 'UPDATE house_contract set create_time = "2018-01-01 15:13:43" where contract_num ="%s"' % self.contract_num
                base.updateSQL(sql)
                sql = "SELECT contract_num from query_house_contract where contract_num = '%s'" % self.contract_num
                base.searchSQL(sql)[0][0]
                base.consoleLog(contractRequest.reviewed_house_contract(self.contract_num))
                base.consoleLog(assemblyRequest.ES_house_contract())
                base.consoleLog(decorationRequest.add_delivered_house(self.contract_num))
                base.consoleLog(assemblyRequest.solr("apartment"))
                break
            except Exception as e:
                base.consoleLog("委托合同未生成宽表，重新查询数据库。报错信息：" + str(e) + "sql:" + sql, level='e')
                sleep(self.wait_time)
                pass


        for i in range(self.for_number):
            try:
                sql = 'SELECT apartment_id from apartment where house_id =  (SELECT house_id from house_contract where contract_num = "%s") limit 1' % self.contract_num
                apartment_id = contractRequest.searchSQL(sql)[0][0]
                base.consoleLog(apartmentRequest.apartment_price_entire(self.contract_num))
                break
            except Exception as e:
                base.consoleLog("查询sql异常。sql:" + sql + "错误返回：" + str(e))
                sleep(self.wait_time)

        for i in range(self.for_number):
            try:
                base.consoleLog(apartmentRequest.apartment_fire_calculate(apartment_id))
                result = achievementRequest.serach_house_contract_loss_details(self.contract_num)
                if result["code"] == 0:
                    break
            except Exception as e:
                base.consoleLog("查询亏损业绩接口返回报错。错误信息：" + str(e))
                sleep(self.wait_time)
                result = {}
                result["code"] = -1
                pass
        base.consoleLog("用例执行完成。预期结果：0.测试结果：" + str(result["code"]))
        self.assertEqual(result["code"],0,msg="委托合同：" + str(self.contract_num))

    def test_house_contract_loss_d(self):
        """服务整租,跑下着火定时器。验证：生成一条着火结算业绩"""
        base.consoleLog("*******************服务整租,跑下着火定时器。验证：生成一条着火结算业绩*************************")
        base.consoleLog(
            contractRequest.add_house_contract("业绩测试预发专用楼盘", self.contract_num, "2018-01-01", "服务公寓", "整租", "微改"))
        for i in range(self.for_number):
            try:
                sql = 'UPDATE house_contract set create_time = "2018-01-01 15:13:43" where contract_num ="%s"' % self.contract_num
                base.updateSQL(sql)
                sql = "SELECT contract_num from query_house_contract where contract_num = '%s'" % self.contract_num
                base.searchSQL(sql)[0][0]
                base.consoleLog(contractRequest.reviewed_house_contract(self.contract_num))
                base.consoleLog(assemblyRequest.ES_house_contract())
                base.consoleLog(decorationRequest.add_delivered_house(self.contract_num))
                base.consoleLog(assemblyRequest.solr("apartment"))
                break
            except Exception as e:
                base.consoleLog("委托合同未生成宽表，重新查询数据库。报错信息：" + str(e) + "sql:" + sql, level='e')
                sleep(self.wait_time)
                pass

        for i in range(self.for_number):
            try:
                sql = 'SELECT apartment_id from apartment where house_id =  (SELECT house_id from house_contract where contract_num = "%s") limit 1' % self.contract_num
                apartment_id = contractRequest.searchSQL(sql)[0][0]
                base.consoleLog(apartmentRequest.apartment_price_entire(self.contract_num))
                break
            except Exception as e:
                base.consoleLog("查询sql异常。sql:" + sql + "错误返回：" + str(e))
                sleep(self.wait_time)

        for i in range(self.for_number):
            try:
                base.consoleLog(apartmentRequest.apartment_fire_calculate(apartment_id))
                result = achievementRequest.serach_house_contract_loss_details(self.contract_num)
                if result["code"] == 0:
                    break
            except Exception as e:
                base.consoleLog("查询亏损业绩接口返回报错。错误信息：" + str(e))
                sleep(self.wait_time)
                result = {}
                result["code"] = -1
                pass
        base.consoleLog("用例执行完成。预期结果：0.测试结果：" + str(result["code"]))
        self.assertEqual(result["code"],0,msg="委托合同：" + str(self.contract_num))

# class HouseContractLossAchievementEndCalculateTestCase(unittest.TestCase):
#     """亏损业绩之到期结算用例测试集合"""
#     def setUp(self):
#         base.consoleLog("-------------------------亏损业绩之到期结算生成用例集合strat----------------------")
#         self.for_number = 100
#         self.wait_time = 1
#         self.contract_num = base.random_name()
#
#     def tearDown(self):
#         base.consoleLog("-------------------------亏损业绩之到期结算生成用例集合end------------------------")
#
#     def test_house_contract_loss_a(self):
#         """品牌合租,房源定价,提交终止结算类型正退，并复审。验证：生成一条到期结算业绩"""
#         base.consoleLog("*******************品牌合租,房源定价,提交终止结算类型正退，并复审。验证：生成一条到期结算业绩*************************")
#         base.consoleLog(
#             contractRequest.add_house_contract("业绩测试预发专用楼盘", self.contract_num, "2018-01-01", "品牌公寓", "合租", "大改"))
#         for i in range(self.for_number):
#             try:
#                 sql = "SELECT contract_num from query_house_contract where contract_num = '%s'" % self.contract_num
#                 base.searchSQL(sql)[0][0]
#                 sql = 'UPDATE house_contract set create_time = "2018-01-01 15:13:43" where contract_num ="%s"' % self.contract_num
#                 base.updateSQL(sql)
#                 break
#             except Exception as e:
#                 base.consoleLog("委托合同未生成宽表，重新查询数据库。报错信息：" + str(e) + "sql:" + sql, level='e')
#                 sleep(self.wait_time)
#                 pass
#         base.consoleLog(assemblyRequest.ES_house_contract())
#         base.consoleLog(decorationRequest.add_delivered_house(self.contract_num))
#         base.consoleLog(assemblyRequest.solr("apartment"))
#         base.consoleLog(contractRequest.reviewed_house_contract(self.contract_num))
#         base.consoleLog(apartmentRequest.apartment_price_share(self.contract_num,[3333,4444,5555]))
#         base.consoleLog(contractEndRequest.house_contract_end(self.contract_num,"正退",base.now_time()))
#         base.consoleLog(contractEndRequest.reviewed_house_contract_end(self.contract_num))
#
#         for i in range(self.for_number):
#             try:
#                 result = achievementRequest.serach_house_contract_loss_details(self.contract_num)
#                 if result["code"] == 0:
#                     break
#             except Exception as e:
#                 base.consoleLog("查询亏损业绩接口返回报错。错误信息：" + str(e))
#                 sleep(self.wait_time)
#                 result = {}
#                 result["code"] = -1
#                 pass
#         base.consoleLog("用例执行完成。预期结果：0.测试结果：" + str(result["code"]))
#         self.assertEqual(result["code"],0,msg="委托合同：" + str(self.contract_num))
#
#     def test_house_contract_loss_b(self):
#         """服务合租,房源定价,提交类型是正退的委托终止，并复审。验证：生成一条到期结算业绩"""
#         base.consoleLog("*******************服务合租,房源定价,提交类型是正退的委托终止，并复审。验证：生成一条到期结算业绩*************************")
#         base.consoleLog(contractRequest.add_house_contract("业绩测试预发专用楼盘", self.contract_num, "2018-01-01", "服务公寓", "合租", "微改"))
#         for i in range(self.for_number):
#             try:
#                 sql = "SELECT contract_num from query_house_contract where contract_num = '%s'" % self.contract_num
#                 base.searchSQL(sql)[0][0]
#                 sql = 'UPDATE house_contract set create_time = "2018-01-01 15:13:43" where contract_num ="%s"' % self.contract_num
#                 base.updateSQL(sql)
#                 break
#             except Exception as e:
#                 base.consoleLog("委托合同未生成宽表，重新查询数据库。报错信息：" + str(e) + "sql:" + sql, level='e')
#                 sleep(self.wait_time)
#                 pass
#         base.consoleLog(assemblyRequest.ES_house_contract())
#         base.consoleLog(decorationRequest.add_delivered_house(self.contract_num))
#         base.consoleLog(assemblyRequest.solr("apartment"))
#         base.consoleLog(contractRequest.reviewed_house_contract(self.contract_num))
#         base.consoleLog(apartmentRequest.apartment_price_share(self.contract_num,[3333,4444,5555]))
#         base.consoleLog(contractEndRequest.house_contract_end(self.contract_num,"正退",base.now_time()))
#         base.consoleLog(contractEndRequest.reviewed_house_contract_end(self.contract_num))
#
#         for i in range(self.for_number):
#             try:
#                 result = achievementRequest.serach_house_contract_loss_details(self.contract_num)
#                 if result["code"] == 0:
#                     break
#             except Exception as e:
#                 base.consoleLog("查询亏损业绩接口返回报错。错误信息：" + str(e))
#                 sleep(self.wait_time)
#                 result = {}
#                 result["code"] = -1
#                 pass
#         base.consoleLog("用例执行完成。预期结果：0.测试结果：" + str(result["code"]))
#         self.assertEqual(result["code"],0,msg="委托合同：" + str(self.contract_num))
#
#     def test_house_contract_loss_c(self):
#         """品牌整租,房源定价,提交类型是正退的终止结算,并复审。验证：生成一条到期结算业绩"""
#         base.consoleLog("*******************品牌整租,房源定价,提交类型是正退的终止结算,并复审。验证：生成一条到期结算业绩*************************")
#         base.consoleLog(
#             contractRequest.add_house_contract("业绩测试预发专用楼盘", self.contract_num, "2018-01-01", "品牌公寓", "整租", "大改"))
#         for i in range(self.for_number):
#             try:
#                 sql = "SELECT contract_num from query_house_contract where contract_num = '%s'" % self.contract_num
#                 base.searchSQL(sql)[0][0]
#                 sql = 'UPDATE house_contract set create_time = "2018-01-01 15:13:43" where contract_num ="%s"' % self.contract_num
#                 base.updateSQL(sql)
#                 break
#             except Exception as e:
#                 base.consoleLog("委托合同未生成宽表，重新查询数据库。报错信息：" + str(e) + "sql:" + sql, level='e')
#                 sleep(self.wait_time)
#                 pass
#         base.consoleLog(assemblyRequest.ES_house_contract())
#         base.consoleLog(decorationRequest.add_delivered_house(self.contract_num))
#         base.consoleLog(assemblyRequest.solr("apartment"))
#         base.consoleLog(contractRequest.reviewed_house_contract(self.contract_num))
#         base.consoleLog(contractEndRequest.house_contract_end(self.contract_num, "正退", base.now_time()))
#         base.consoleLog(contractEndRequest.reviewed_house_contract_end(self.contract_num))
#
#         for i in range(self.for_number):
#             try:
#                 sql = 'SELECT apartment_id from apartment where house_id =  (SELECT house_id from house_contract where contract_num = "%s") limit 1' % self.contract_num
#                 apartment_id = contractRequest.searchSQL(sql)[0][0]
#                 break
#             except Exception as e:
#                 base.consoleLog("查询sql异常。sql:" + sql + "错误返回：" + str(e))
#
#         base.consoleLog(apartmentRequest.apartment_fire_calculate(apartment_id))
#
#         for i in range(self.for_number):
#             try:
#                 result = achievementRequest.serach_house_contract_loss_details(self.contract_num)
#                 if result["code"] == 0:
#                     break
#             except Exception as e:
#                 base.consoleLog("查询亏损业绩接口返回报错。错误信息：" + str(e))
#                 sleep(self.wait_time)
#                 result = {}
#                 result["code"] = -1
#                 pass
#         base.consoleLog("用例执行完成。预期结果：0.测试结果：" + str(result["code"]))
#         self.assertEqual(result["code"],0,msg="委托合同：" + str(self.contract_num))
#
#     def test_house_contract_loss_d(self):
#         """服务整租,房源定价,提交类型是正退的终止结算,并复审。验证：生成一条到期结算业绩"""
#         base.consoleLog("*******************服务整租,房源定价,提交类型是正退的终止结算,并复审。验证：生成一条到期结算业绩*************************")
#         base.consoleLog(
#             contractRequest.add_house_contract("业绩测试预发专用楼盘", self.contract_num, "2018-01-01", "服务公寓", "整租", "微改"))
#         for i in range(self.for_number):
#             try:
#                 sql = "SELECT contract_num from query_house_contract where contract_num = '%s'" % self.contract_num
#                 base.searchSQL(sql)[0][0]
#                 sql = 'UPDATE house_contract set create_time = "2018-01-01 15:13:43" where contract_num ="%s"' % self.contract_num
#                 base.updateSQL(sql)
#                 break
#             except Exception as e:
#                 base.consoleLog("委托合同未生成宽表，重新查询数据库。报错信息：" + str(e) + "sql:" + sql, level='e')
#                 sleep(self.wait_time)
#                 pass
#         base.consoleLog(assemblyRequest.ES_house_contract())
#         base.consoleLog(decorationRequest.add_delivered_house(self.contract_num))
#         base.consoleLog(assemblyRequest.solr("apartment"))
#         base.consoleLog(contractRequest.reviewed_house_contract(self.contract_num))
#         base.consoleLog(contractEndRequest.house_contract_end(self.contract_num, "正退", base.now_time()))
#         base.consoleLog(contractEndRequest.reviewed_house_contract_end(self.contract_num))
#
#         for i in range(self.for_number):
#             try:
#                 sql = 'SELECT apartment_id from apartment where house_id =  (SELECT house_id from house_contract where contract_num = "%s") limit 1' % self.contract_num
#                 apartment_id = contractRequest.searchSQL(sql)[0][0]
#                 break
#             except Exception as e:
#                 base.consoleLog("查询sql异常。sql:" + sql + "错误返回：" + str(e))
#
#         base.consoleLog(apartmentRequest.apartment_fire_calculate(apartment_id))
#
#         for i in range(self.for_number):
#             try:
#                 result = achievementRequest.serach_house_contract_loss_details(self.contract_num)
#                 if result["code"] == 0:
#                     break
#             except Exception as e:
#                 base.consoleLog("查询亏损业绩接口返回报错。错误信息：" + str(e))
#                 sleep(self.wait_time)
#                 result = {}
#                 result["code"] = -1
#                 pass
#         base.consoleLog("用例执行完成。预期结果：0.测试结果：" + str(result["code"]))
#         self.assertEqual(result["code"], 0, msg="委托合同：" + str(self.contract_num))
#
#     def test_house_contract_loss_e(self):
#         """品牌合租,房源定价,提交终止结算类型公司违约，并复审。验证：生成一条到期结算业绩"""
#         base.consoleLog("*******************品牌合租,房源定价,提交终止结算类型公司违约，并复审。验证：生成一条到期结算业绩*************************")
#         base.consoleLog(
#             contractRequest.add_house_contract("业绩测试预发专用楼盘", self.contract_num, "2018-01-01", "品牌公寓", "合租", "大改"))
#         for i in range(self.for_number):
#             try:
#                 sql = "SELECT contract_num from query_house_contract where contract_num = '%s'" % self.contract_num
#                 base.searchSQL(sql)[0][0]
#                 sql = 'UPDATE house_contract set create_time = "2018-01-01 15:13:43" where contract_num ="%s"' % self.contract_num
#                 base.updateSQL(sql)
#                 break
#             except Exception as e:
#                 base.consoleLog("委托合同未生成宽表，重新查询数据库。报错信息：" + str(e) + "sql:" + sql, level='e')
#                 sleep(self.wait_time)
#                 pass
#         base.consoleLog(assemblyRequest.ES_house_contract())
#         base.consoleLog(decorationRequest.add_delivered_house(self.contract_num))
#         base.consoleLog(assemblyRequest.solr("apartment"))
#         base.consoleLog(contractRequest.reviewed_house_contract(self.contract_num))
#         base.consoleLog(apartmentRequest.apartment_price_share(self.contract_num,[3333,4444,5555]))
#         base.consoleLog(contractEndRequest.house_contract_end(self.contract_num,"公司违约",base.now_time()))
#         base.consoleLog(contractEndRequest.reviewed_house_contract_end(self.contract_num))
#
#         for i in range(self.for_number):
#             try:
#                 result = achievementRequest.serach_house_contract_loss_details(self.contract_num)
#                 if result["code"] == 0:
#                     break
#             except Exception as e:
#                 base.consoleLog("查询亏损业绩接口返回报错。错误信息：" + str(e))
#                 sleep(self.wait_time)
#                 result = {}
#                 result["code"] = -1
#                 pass
#         base.consoleLog("用例执行完成。预期结果：0.测试结果：" + str(result["code"]))
#         self.assertEqual(result["code"],0,msg="委托合同：" + str(self.contract_num))
#
#     def test_house_contract_loss_f(self):
#         """服务合租,房源定价,提交类型是公司违约的委托终止，并复审。验证：生成一条到期结算业绩"""
#         base.consoleLog("*******************服务合租,房源定价,提交类型是公司违约的委托终止，并复审。验证：生成一条到期结算业绩*************************")
#         base.consoleLog(contractRequest.add_house_contract("业绩测试预发专用楼盘", self.contract_num, "2018-01-01", "服务公寓", "合租", "微改"))
#         for i in range(self.for_number):
#             try:
#                 sql = "SELECT contract_num from query_house_contract where contract_num = '%s'" % self.contract_num
#                 base.searchSQL(sql)[0][0]
#                 sql = 'UPDATE house_contract set create_time = "2018-01-01 15:13:43" where contract_num ="%s"' % self.contract_num
#                 base.updateSQL(sql)
#                 break
#             except Exception as e:
#                 base.consoleLog("委托合同未生成宽表，重新查询数据库。报错信息：" + str(e) + "sql:" + sql, level='e')
#                 sleep(self.wait_time)
#                 pass
#         base.consoleLog(assemblyRequest.ES_house_contract())
#         base.consoleLog(decorationRequest.add_delivered_house(self.contract_num))
#         base.consoleLog(assemblyRequest.solr("apartment"))
#         base.consoleLog(contractRequest.reviewed_house_contract(self.contract_num))
#         base.consoleLog(apartmentRequest.apartment_price_share(self.contract_num,[3333,4444,5555]))
#         base.consoleLog(contractEndRequest.house_contract_end(self.contract_num,"公司违约",base.now_time()))
#         base.consoleLog(contractEndRequest.reviewed_house_contract_end(self.contract_num))
#
#         for i in range(self.for_number):
#             try:
#                 result = achievementRequest.serach_house_contract_loss_details(self.contract_num)
#                 if result["code"] == 0:
#                     break
#             except Exception as e:
#                 base.consoleLog("查询亏损业绩接口返回报错。错误信息：" + str(e))
#                 sleep(self.wait_time)
#                 result = {}
#                 result["code"] = -1
#                 pass
#         base.consoleLog("用例执行完成。预期结果：0.测试结果：" + str(result["code"]))
#         self.assertEqual(result["code"],0,msg="委托合同：" + str(self.contract_num))
#
#     def test_house_contract_loss_g(self):
#         """品牌整租,房源定价,提交类型是公司违约的终止结算,并复审。验证：生成一条到期结算业绩"""
#         base.consoleLog("*******************品牌整租,房源定价,提交类型是公司违约的终止结算,并复审。验证：生成一条到期结算业绩*************************")
#         base.consoleLog(
#             contractRequest.add_house_contract("业绩测试预发专用楼盘", self.contract_num, "2018-01-01", "品牌公寓", "整租", "大改"))
#         for i in range(self.for_number):
#             try:
#                 sql = "SELECT contract_num from query_house_contract where contract_num = '%s'" % self.contract_num
#                 base.searchSQL(sql)[0][0]
#                 sql = 'UPDATE house_contract set create_time = "2018-01-01 15:13:43" where contract_num ="%s"' % self.contract_num
#                 base.updateSQL(sql)
#                 break
#             except Exception as e:
#                 base.consoleLog("委托合同未生成宽表，重新查询数据库。报错信息：" + str(e) + "sql:" + sql, level='e')
#                 sleep(self.wait_time)
#                 pass
#         base.consoleLog(assemblyRequest.ES_house_contract())
#         base.consoleLog(decorationRequest.add_delivered_house(self.contract_num))
#         base.consoleLog(assemblyRequest.solr("apartment"))
#         base.consoleLog(contractRequest.reviewed_house_contract(self.contract_num))
#         base.consoleLog(contractEndRequest.house_contract_end(self.contract_num, "公司违约", base.now_time()))
#         base.consoleLog(contractEndRequest.reviewed_house_contract_end(self.contract_num))
#
#         for i in range(self.for_number):
#             try:
#                 sql = 'SELECT apartment_id from apartment where house_id =  (SELECT house_id from house_contract where contract_num = "%s") limit 1' % self.contract_num
#                 apartment_id = contractRequest.searchSQL(sql)[0][0]
#                 break
#             except Exception as e:
#                 base.consoleLog("查询sql异常。sql:" + sql + "错误返回：" + str(e))
#
#         base.consoleLog(apartmentRequest.apartment_fire_calculate(apartment_id))
#
#         for i in range(self.for_number):
#             try:
#                 result = achievementRequest.serach_house_contract_loss_details(self.contract_num)
#                 if result["code"] == 0:
#                     break
#             except Exception as e:
#                 base.consoleLog("查询亏损业绩接口返回报错。错误信息：" + str(e))
#                 sleep(self.wait_time)
#                 result = {}
#                 result["code"] = -1
#                 pass
#         base.consoleLog("用例执行完成。预期结果：0.测试结果：" + str(result["code"]))
#         self.assertEqual(result["code"],0,msg="委托合同：" + str(self.contract_num))
#
#     def test_house_contract_loss_h(self):
#         """服务整租,房源定价,提交类型是公司违约的终止结算,并复审。验证：生成一条到期结算业绩"""
#         base.consoleLog("*******************服务整租,房源定价,提交类型是公司违约的终止结算,并复审。验证：生成一条到期结算业绩*************************")
#         base.consoleLog(
#             contractRequest.add_house_contract("业绩测试预发专用楼盘", self.contract_num, "2018-01-01", "服务公寓", "整租", "微改"))
#         for i in range(self.for_number):
#             try:
#                 sql = "SELECT contract_num from query_house_contract where contract_num = '%s'" % self.contract_num
#                 base.searchSQL(sql)[0][0]
#                 sql = 'UPDATE house_contract set create_time = "2018-01-01 15:13:43" where contract_num ="%s"' % self.contract_num
#                 base.updateSQL(sql)
#                 break
#             except Exception as e:
#                 base.consoleLog("委托合同未生成宽表，重新查询数据库。报错信息：" + str(e) + "sql:" + sql, level='e')
#                 sleep(self.wait_time)
#                 pass
#         base.consoleLog(assemblyRequest.ES_house_contract())
#         base.consoleLog(decorationRequest.add_delivered_house(self.contract_num))
#         base.consoleLog(assemblyRequest.solr("apartment"))
#         base.consoleLog(contractRequest.reviewed_house_contract(self.contract_num))
#         base.consoleLog(contractEndRequest.house_contract_end(self.contract_num, "公司违约", base.now_time()))
#         base.consoleLog(contractEndRequest.reviewed_house_contract_end(self.contract_num))
#
#         for i in range(self.for_number):
#             try:
#                 sql = 'SELECT apartment_id from apartment where house_id =  (SELECT house_id from house_contract where contract_num = "%s") limit 1' % self.contract_num
#                 apartment_id = contractRequest.searchSQL(sql)[0][0]
#                 break
#             except Exception as e:
#                 base.consoleLog("查询sql异常。sql:" + sql + "错误返回：" + str(e))
#
#         base.consoleLog(apartmentRequest.apartment_fire_calculate(apartment_id))
#
#         for i in range(self.for_number):
#             try:
#                 result = achievementRequest.serach_house_contract_loss_details(self.contract_num)
#                 if result["code"] == 0:
#                     break
#             except Exception as e:
#                 base.consoleLog("查询亏损业绩接口返回报错。错误信息：" + str(e))
#                 sleep(self.wait_time)
#                 result = {}
#                 result["code"] = -1
#                 pass
#         base.consoleLog("用例执行完成。预期结果：0.测试结果：" + str(result["code"]))
#         self.assertEqual(result["code"], 0, msg="委托合同：" + str(self.contract_num))
#
#     def test_house_contract_loss_i(self):
#         """品牌合租,房源定价,提交终止结算类型业主违约，并复审。验证：生成一条到期结算业绩"""
#         base.consoleLog("*******************品牌合租,房源定价,提交终止结算类型业主违约，并复审。验证：生成一条到期结算业绩*************************")
#         base.consoleLog(
#             contractRequest.add_house_contract("业绩测试预发专用楼盘", self.contract_num, "2018-01-01", "品牌公寓", "合租", "大改"))
#         for i in range(self.for_number):
#             try:
#                 sql = "SELECT contract_num from query_house_contract where contract_num = '%s'" % self.contract_num
#                 base.searchSQL(sql)[0][0]
#                 sql = 'UPDATE house_contract set create_time = "2018-01-01 15:13:43" where contract_num ="%s"' % self.contract_num
#                 base.updateSQL(sql)
#                 break
#             except Exception as e:
#                 base.consoleLog("委托合同未生成宽表，重新查询数据库。报错信息：" + str(e) + "sql:" + sql, level='e')
#                 sleep(self.wait_time)
#                 pass
#         base.consoleLog(assemblyRequest.ES_house_contract())
#         base.consoleLog(decorationRequest.add_delivered_house(self.contract_num))
#         base.consoleLog(assemblyRequest.solr("apartment"))
#         base.consoleLog(contractRequest.reviewed_house_contract(self.contract_num))
#         base.consoleLog(apartmentRequest.apartment_price_share(self.contract_num,[3333,4444,5555]))
#         base.consoleLog(contractEndRequest.house_contract_end(self.contract_num,"业主违约",base.now_time()))
#         base.consoleLog(contractEndRequest.reviewed_house_contract_end(self.contract_num))
#
#         for i in range(self.for_number):
#             try:
#                 result = achievementRequest.serach_house_contract_loss_details(self.contract_num)
#                 if result["code"] == 0:
#                     break
#             except Exception as e:
#                 base.consoleLog("查询亏损业绩接口返回报错。错误信息：" + str(e))
#                 sleep(self.wait_time)
#                 result = {}
#                 result["code"] = -1
#                 pass
#         base.consoleLog("用例执行完成。预期结果：0.测试结果：" + str(result["code"]))
#         self.assertEqual(result["code"],0,msg="委托合同：" + str(self.contract_num))
#
#     def test_house_contract_loss_j(self):
#         """服务合租,房源定价,提交类型是业主违约的委托终止，并复审。验证：生成一条到期结算业绩"""
#         base.consoleLog("*******************服务合租,房源定价,提交类型是业主违约的委托终止，并复审。验证：生成一条到期结算业绩*************************")
#         base.consoleLog(contractRequest.add_house_contract("业绩测试预发专用楼盘", self.contract_num, "2018-01-01", "服务公寓", "合租", "微改"))
#         for i in range(self.for_number):
#             try:
#                 sql = "SELECT contract_num from query_house_contract where contract_num = '%s'" % self.contract_num
#                 base.searchSQL(sql)[0][0]
#                 sql = 'UPDATE house_contract set create_time = "2018-01-01 15:13:43" where contract_num ="%s"' % self.contract_num
#                 base.updateSQL(sql)
#                 break
#             except Exception as e:
#                 base.consoleLog("委托合同未生成宽表，重新查询数据库。报错信息：" + str(e) + "sql:" + sql, level='e')
#                 sleep(self.wait_time)
#                 pass
#         base.consoleLog(assemblyRequest.ES_house_contract())
#         base.consoleLog(decorationRequest.add_delivered_house(self.contract_num))
#         base.consoleLog(assemblyRequest.solr("apartment"))
#         base.consoleLog(contractRequest.reviewed_house_contract(self.contract_num))
#         base.consoleLog(apartmentRequest.apartment_price_share(self.contract_num,[3333,4444,5555]))
#         base.consoleLog(contractEndRequest.house_contract_end(self.contract_num,"业主违约",base.now_time()))
#         base.consoleLog(contractEndRequest.reviewed_house_contract_end(self.contract_num))
#
#         for i in range(self.for_number):
#             try:
#                 result = achievementRequest.serach_house_contract_loss_details(self.contract_num)
#                 if result["code"] == 0:
#                     break
#             except Exception as e:
#                 base.consoleLog("查询亏损业绩接口返回报错。错误信息：" + str(e))
#                 sleep(self.wait_time)
#                 result = {}
#                 result["code"] = -1
#                 pass
#         base.consoleLog("用例执行完成。预期结果：0.测试结果：" + str(result["code"]))
#         self.assertEqual(result["code"],0,msg="委托合同：" + str(self.contract_num))
#
#     def test_house_contract_loss_k(self):
#         """品牌整租,房源定价,提交类型是业主违约的终止结算,并复审。验证：生成一条到期结算业绩"""
#         base.consoleLog("*******************品牌整租,房源定价,提交类型是业主违约的终止结算,并复审。验证：生成一条到期结算业绩*************************")
#         base.consoleLog(
#             contractRequest.add_house_contract("业绩测试预发专用楼盘", self.contract_num, "2018-01-01", "品牌公寓", "整租", "大改"))
#         for i in range(self.for_number):
#             try:
#                 sql = "SELECT contract_num from query_house_contract where contract_num = '%s'" % self.contract_num
#                 base.searchSQL(sql)[0][0]
#                 sql = 'UPDATE house_contract set create_time = "2018-01-01 15:13:43" where contract_num ="%s"' % self.contract_num
#                 base.updateSQL(sql)
#                 break
#             except Exception as e:
#                 base.consoleLog("委托合同未生成宽表，重新查询数据库。报错信息：" + str(e) + "sql:" + sql, level='e')
#                 sleep(self.wait_time)
#                 pass
#         base.consoleLog(assemblyRequest.ES_house_contract())
#         base.consoleLog(decorationRequest.add_delivered_house(self.contract_num))
#         base.consoleLog(assemblyRequest.solr("apartment"))
#         base.consoleLog(contractRequest.reviewed_house_contract(self.contract_num))
#         base.consoleLog(contractEndRequest.house_contract_end(self.contract_num, "业主违约", base.now_time()))
#         base.consoleLog(contractEndRequest.reviewed_house_contract_end(self.contract_num))
#
#         for i in range(self.for_number):
#             try:
#                 sql = 'SELECT apartment_id from apartment where house_id =  (SELECT house_id from house_contract where contract_num = "%s") limit 1' % self.contract_num
#                 apartment_id = contractRequest.searchSQL(sql)[0][0]
#                 break
#             except Exception as e:
#                 base.consoleLog("查询sql异常。sql:" + sql + "错误返回：" + str(e))
#
#         base.consoleLog(apartmentRequest.apartment_fire_calculate(apartment_id))
#
#         for i in range(self.for_number):
#             try:
#                 result = achievementRequest.serach_house_contract_loss_details(self.contract_num)
#                 if result["code"] == 0:
#                     break
#             except Exception as e:
#                 base.consoleLog("查询亏损业绩接口返回报错。错误信息：" + str(e))
#                 sleep(self.wait_time)
#                 result = {}
#                 result["code"] = -1
#                 pass
#         base.consoleLog("用例执行完成。预期结果：0.测试结果：" + str(result["code"]))
#         self.assertEqual(result["code"],0,msg="委托合同：" + str(self.contract_num))
#
#     def test_house_contract_loss_l(self):
#         """服务整租,房源定价,提交类型是业主违约的终止结算,并复审。验证：生成一条到期结算业绩"""
#         base.consoleLog("*******************服务整租,房源定价,提交类型是业主违约的终止结算,并复审。验证：生成一条到期结算业绩*************************")
#         base.consoleLog(
#             contractRequest.add_house_contract("业绩测试预发专用楼盘", self.contract_num, "2018-01-01", "服务公寓", "整租", "微改"))
#         for i in range(self.for_number):
#             try:
#                 sql = "SELECT contract_num from query_house_contract where contract_num = '%s'" % self.contract_num
#                 base.searchSQL(sql)[0][0]
#                 sql = 'UPDATE house_contract set create_time = "2018-01-01 15:13:43" where contract_num ="%s"' % self.contract_num
#                 base.updateSQL(sql)
#                 break
#             except Exception as e:
#                 base.consoleLog("委托合同未生成宽表，重新查询数据库。报错信息：" + str(e) + "sql:" + sql, level='e')
#                 sleep(self.wait_time)
#                 pass
#         base.consoleLog(assemblyRequest.ES_house_contract())
#         base.consoleLog(decorationRequest.add_delivered_house(self.contract_num))
#         base.consoleLog(assemblyRequest.solr("apartment"))
#         base.consoleLog(contractRequest.reviewed_house_contract(self.contract_num))
#         base.consoleLog(contractEndRequest.house_contract_end(self.contract_num, "业主违约", base.now_time()))
#         base.consoleLog(contractEndRequest.reviewed_house_contract_end(self.contract_num))
#
#         for i in range(self.for_number):
#             try:
#                 sql = 'SELECT apartment_id from apartment where house_id =  (SELECT house_id from house_contract where contract_num = "%s") limit 1' % self.contract_num
#                 apartment_id = contractRequest.searchSQL(sql)[0][0]
#                 break
#             except Exception as e:
#                 base.consoleLog("查询sql异常。sql:" + sql + "错误返回：" + str(e))
#
#         base.consoleLog(apartmentRequest.apartment_fire_calculate(apartment_id))
#
#         for i in range(self.for_number):
#             try:
#                 result = achievementRequest.serach_house_contract_loss_details(self.contract_num)
#                 if result["code"] == 0:
#                     break
#             except Exception as e:
#                 base.consoleLog("查询亏损业绩接口返回报错。错误信息：" + str(e))
#                 sleep(self.wait_time)
#                 result = {}
#                 result["code"] = -1
#                 pass
#         base.consoleLog("用例执行完成。预期结果：0.测试结果：" + str(result["code"]))
#         self.assertEqual(result["code"], 0, msg="委托合同：" + str(self.contract_num))
#
#     def trst_house_contract_loss_m(self):
#         """品牌合租，委托合同到期且已复审。验证生成一条到期结算业绩"""
#         base.consoleLog("""****************************品牌合租，委托合同到期且已复审。验证生成一条到期结算业绩*********************""")
#         contract_num = base.get_conf("TestCaseData","HouseContractLossAchievementEndCalculateTestCase_trst_house_contract_loss_m")
#
#         for i in range(self.for_number):
#             try:
#                 result = achievementRequest.serach_house_contract_loss_details(contract_num)
#                 if result["code"] ==0:
#                     break
#             except Exception as e:
#                 base.consoleLog("查询亏损业绩接口报错。接口返回："+str(e))
#                 result = {}
#                 result["code"] = -1
#                 sleep(self.wait_time)
#
#         base.consoleLog("用例执行完成。预期结果：0  测试结果：" + str(result["code"]))
#         self.assertEqual(result["code"],0,msg="委托合同号："+contract_num)
#
#     def trst_house_contract_loss_n(self):
#         """服务合租，委托合同到期且已复审。验证生成一条到期结算业绩"""
#         base.consoleLog("""****************************服务合租，委托合同到期且已复审。验证生成一条到期结算业绩*********************""")
#         contract_num = base.get_conf("TestCaseData",
#                                      "HouseContractLossAchievementEndCalculateTestCase_trst_house_contract_loss_n")
#
#         for i in range(self.for_number):
#             try:
#                 result = achievementRequest.serach_house_contract_loss_details(contract_num)
#                 if result["code"] == 0:
#                     break
#             except Exception as e:
#                 base.consoleLog("查询亏损业绩接口报错。接口返回：" + str(e))
#                 result = {}
#                 result["code"] = -1
#                 sleep(self.wait_time)
#
#         base.consoleLog("用例执行完成。预期结果：0  测试结果：" + str(result["code"]))
#         self.assertEqual(result["code"], 0, msg="委托合同号：" + contract_num)
#
#     def trst_house_contract_loss_o(self):
#         """品牌整租，委托合同到期且已复审。验证生成一条到期结算业绩"""
#         base.consoleLog("""****************************品牌整租，委托合同到期且已复审。验证生成一条到期结算业绩*********************""")
#         contract_num = base.get_conf("TestCaseData",
#                                      "HouseContractLossAchievementEndCalculateTestCase_trst_house_contract_loss_o")
#
#         for i in range(self.for_number):
#             try:
#                 result = achievementRequest.serach_house_contract_loss_details(contract_num)
#                 if result["code"] == 0:
#                     break
#             except Exception as e:
#                 base.consoleLog("查询亏损业绩接口报错。接口返回：" + str(e))
#                 result = {}
#                 result["code"] = -1
#                 sleep(self.wait_time)
#
#         base.consoleLog("用例执行完成。预期结果：0  测试结果：" + str(result["code"]))
#         self.assertEqual(result["code"], 0, msg="委托合同号：" + contract_num)
#
#     def trst_house_contract_loss_p(self):
#         """服务整租，委托合同到期且已复审。验证生成一条到期结算业绩"""
#         base.consoleLog("""****************************服务整租，委托合同到期且已复审。验证生成一条到期结算业绩*********************""")
#         contract_num = base.get_conf("TestCaseData",
#                                      "HouseContractLossAchievementEndCalculateTestCase_trst_house_contract_loss_p")
#
#         for i in range(self.for_number):
#             try:
#                 result = achievementRequest.serach_house_contract_loss_details(contract_num)
#                 if result["code"] == 0:
#                     break
#             except Exception as e:
#                 base.consoleLog("查询亏损业绩接口报错。接口返回：" + str(e))
#                 result = {}
#                 result["code"] = -1
#                 sleep(self.wait_time)
#
#         base.consoleLog("用例执行完成。预期结果：0  测试结果：" + str(result["code"]))
#         self.assertEqual(result["code"], 0, msg="委托合同号：" + contract_num)

if __name__ == "__main__":
    unittest.main()

