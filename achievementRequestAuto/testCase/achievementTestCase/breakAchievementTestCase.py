# -*- coding:UTF-8 -*-

"""
author = crazyzhong
2018年4月18日09:28:01
违约业绩接口测试用例
"""

from erpRequest import houseDevelopRequest
from erpRequest import contractRequest
from erpRequest import  decorationRequest
from erpRequest import apartmentRequest
from erpRequest import  assemblyRequest
from erpRequest import  customerRequest
from erpRequest import  achievementRequest
from erpRequest import  contractEndRequest
from erpRequest import financeRequest
from common import base
from time import sleep
import unittest

class BreakAchievementTestCase(unittest.TestCase):
    """生成违约业绩测试用例集合"""
    def setUp(self):
        base.consoleLog("-------------------------违约业绩生成用例集合strat----------------------")
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

    def tearDown(self):
        base.consoleLog("-------------------------违约业绩生成用例集合end------------------------")

    def test_break_case_a(self):
        """委托终止，业主违约。验证生成一条违约业绩。"""
        base.consoleLog("""委托终止，业主违约。验证生成一条违约业绩。""")
        base.consoleLog(contractRequest.reviewed_house_contract(self.contract_num))
        base.consoleLog(contractEndRequest.house_contract_end(self.contract_num, "业主违约", contractRequest.now_time()))
        for i in range(self.for_number):
            try:
                self.result = achievementRequest.serach_break_details(self.contract_num)
                if self.result["code"] == 0:
                    break
                else:
                    base.consoleLog("查询违约详情接口异常。错误返回：" + str(self.result))
                    sleep(self.wait_time)
                    pass
            except Exception as e:
                base.consoleLog("查询违约详情异常。错误返回：" + str(e))
                sleep(self.wait_time)
                self.result = {}
                self.result["code"] = -1

        base.consoleLog("用例执行完成。预期结果：0  测试结果：" + str(self.result["code"]))
        self.assertEqual(self.result["code"],0,msg="委托合同号："+self.contract_num)

    def test_break_case_b(self):
        """委托终止，公司违约。验证生成一条违约业绩。"""
        base.consoleLog("""委托终止，公司违约。验证生成一条违约业绩。""")
        base.consoleLog(contractRequest.reviewed_house_contract(self.contract_num))
        base.consoleLog(contractEndRequest.house_contract_end(self.contract_num, "公司违约", contractRequest.now_time()))
        for i in range(self.for_number):
            try:
                self.result = achievementRequest.serach_break_details(self.contract_num)
                if self.result["code"] == 0:
                    break
                else:
                    base.consoleLog("查询违约详情接口异常。错误返回：" + str(self.result))
                    sleep(self.wait_time)
                    pass
            except Exception as e:
                base.consoleLog("查询违约详情异常。错误返回：" + str(e))
                sleep(self.wait_time)
                self.result = {}
                self.result["code"] = -1

        base.consoleLog("用例执行完成。预期结果：0  测试结果：" + str(self.result["code"]))
        self.assertEqual(self.result["code"],0,msg="委托合同号："+self.contract_num)
    #
    # def test_break_case_c(self):
    #     """委托终止，正退。不生成违约业绩"""
    #     base.consoleLog("""委托终止，正退。不生成违约业绩""")
    #     base.consoleLog(contractRequest.reviewed_house_contract(self.contract_num))
    #     base.consoleLog(contractEndRequest.house_contract_end(self.contract_num, "正退", contractRequest.now_time()))
    #     for i in range(3):
    #         try:
    #             self.result = achievementRequest.serach_break_details(self.contract_num)
    #             if self.result["code"] == 0:
    #                 break
    #             else:
    #                 base.consoleLog("查询违约详情接口异常。错误返回：" + str(self.result))
    #                 sleep(3)
    #                 pass
    #         except Exception as e:
    #             base.consoleLog("查询违约详情异常。错误返回：" + str(e))
    #             sleep(self.wait_time)
    #
    #     base.consoleLog("用例执行完成。预期结果：0  测试结果：" + str(self.result["code"]))
    #     self.assertEqual(self.result["code"],0,msg="委托合同号："+self.contract_num)

    def test_break_case_d(self):
        """出租终止,退租.生成违约业绩"""
        base.consoleLog("""出租终止,退租.生成违约业绩""")
        base.consoleLog(decorationRequest.add_delivered_house(self.contract_num))
        base.consoleLog(assemblyRequest.solr("apartment"))
        base.consoleLog(apartmentRequest.apartment_price_entire(self.contract_num))
        phone = base.add_phone_number()
        customerRequest.add_customer("autotest", phone)

        for i in range(self.for_number):
            try:
                sql = 'SELECT apartment_id from apartment where house_id =  (SELECT house_id from house_contract where contract_num = "%s") limit 1' % self.contract_num
                apartment_id = contractRequest.searchSQL(sql)[0][0]
                break
            except Exception as e:
                base.consoleLog("查询sql异常。sql:" + sql + "错误返回：" + str(e))

        for i in range(self.for_number):
            try:
                sql = 'SELECT apartment_code from apartment where apartment_id = "%s"' % apartment_id
                apartment_code = contractRequest.searchSQL(sql)[0][0]
                break
            except Exception as e:
                base.consoleLog("查询sql异常。sql:" + sql + "错误返回：" + str(e))

        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_entire(apartment_code, phone, contract_nums,contractRequest.now_time(), "2018-12-30"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums, "2018-12-30", "退租"))

        for i in range(self.for_number):
            try:
                self.result = achievementRequest.serach_break_details(self.contract_num)
                if self.result["code"] == 0:
                    break
            except:
                base.consoleLog("查询违约详情接口异常。错误返回：" + str(self.result))
                sleep(self.wait_time)
                self.result = {}
                self.result["code"] = -1
                pass
        base.consoleLog("用例执行完成。预期结果：0  测试结果：" + str(self.result["code"]))
        self.assertEqual(self.result["code"], 0, msg="出租合同号："+ contract_nums)

    def test_break_case_e(self):
        """出租终止,转租.生成一条违约业绩"""
        base.consoleLog("""出租终止,转租.生成一条违约业绩""")
        base.consoleLog(decorationRequest.add_delivered_house(self.contract_num))
        base.consoleLog(assemblyRequest.solr("apartment"))
        base.consoleLog(apartmentRequest.apartment_price_entire(self.contract_num))
        phone = base.add_phone_number()
        base.consoleLog(customerRequest.add_customer("autotest", phone))

        for i in range(self.for_number):
            try:
                sql = 'SELECT apartment_id from apartment where house_id =  (SELECT house_id from house_contract where contract_num = "%s") limit 1' % self.contract_num
                apartment_id = contractRequest.searchSQL(sql)[0][0]
                break
            except Exception as e:
                base.consoleLog("查询sql异常。sql:" + sql + "错误返回：" + str(e))

        for i in range(self.for_number):
            try:
                sql = 'SELECT apartment_code from apartment where apartment_id = "%s"' % apartment_id
                apartment_code = contractRequest.searchSQL(sql)[0][0]
                break
            except Exception as e:
                base.consoleLog("查询sql异常。sql:" + sql + "错误返回：" + str(e))

        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_entire(apartment_code, phone, contract_nums, contractRequest.now_time(), "2018-12-30"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums, "2018-12-30", "转租"))

        for i in range(self.for_number):
            try:
                self.result = achievementRequest.serach_break_details(self.contract_num)
                if self.result["code"] == 0:
                    break
            except:
                base.consoleLog("查询违约详情接口异常。错误返回：" + str(self.result))
                sleep(self.wait_time)
                self.result = {}
                self.result["code"] = -1
                pass
        base.consoleLog("用例执行完成。预期结果：0  测试结果：" + str(self.result["code"]))
        self.assertEqual(self.result["code"], 0,msg="出租合同号："+ contract_nums)

    def test_break_case_f(self):
        """出租终止,收房.生成一条违约业绩"""
        base.consoleLog("""出租终止,收房.生成一条违约业绩""")
        base.consoleLog(decorationRequest.add_delivered_house(self.contract_num))
        base.consoleLog(assemblyRequest.solr("apartment"))
        base.consoleLog(apartmentRequest.apartment_price_entire(self.contract_num))
        phone = base.add_phone_number()
        base.consoleLog(customerRequest.add_customer("autotest", phone))

        for i in range(self.for_number):
            try:
                sql = 'SELECT apartment_id from apartment where house_id =  (SELECT house_id from house_contract where contract_num = "%s") limit 1' % self.contract_num
                apartment_id = contractRequest.searchSQL(sql)[0][0]
                break
            except Exception as e:
                base.consoleLog("查询sql异常。sql:" + sql + "错误返回：" + str(e))

        for i in range(self.for_number):
            try:
                sql = 'SELECT apartment_code from apartment where apartment_id = "%s"' % apartment_id
                apartment_code = contractRequest.searchSQL(sql)[0][0]
                break
            except Exception as e:
                base.consoleLog("查询sql异常。sql:" + sql + "错误返回：" + str(e))

        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_entire(apartment_code, phone, contract_nums, contractRequest.now_time(),"2018-12-30"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums, "2018-12-30", "收房"))

        for i in range(self.for_number):
            try:
                self.result = achievementRequest.serach_break_details(self.contract_num)
                if self.result["code"] == 0:
                    break
            except:
                base.consoleLog("查询违约详情接口异常。错误返回：" + str(self.result))
                sleep(self.wait_time)
                self.result = {}
                self.result["code"] = -1
                pass
        base.consoleLog("用例执行完成。预期结果：0  测试结果：" + str(self.result["code"]))
        self.assertEqual(self.result["code"], 0, msg="出租合同号："+ contract_nums)

    def test_break_case_g(self):
        """出租终止,换租.生成一条违约业绩"""
        base.consoleLog("""出租终止,换租.生成一条违约业绩""")
        decorationRequest.add_delivered_house(self.contract_num)
        assemblyRequest.solr("apartment")
        apartmentRequest.apartment_price_entire(self.contract_num)
        phone = contractRequest.add_phone_number()
        customerRequest.add_customer("autotest", phone)

        for i in range(self.for_number):
            try:
                sql = 'SELECT apartment_id from apartment where house_id =  (SELECT house_id from house_contract where contract_num = "%s") limit 1' % self.contract_num
                apartment_id = contractRequest.searchSQL(sql)[0][0]
                break
            except Exception as e:
                base.consoleLog("查询sql异常。sql:" + sql + "错误返回：" + str(e))

        for i in range(self.for_number):
            try:
                sql = 'SELECT apartment_code from apartment where apartment_id = "%s"' % apartment_id
                apartment_code = contractRequest.searchSQL(sql)[0][0]
                break
            except Exception as e:
                base.consoleLog("查询sql异常。sql:" + sql + "错误返回：" + str(e))

        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_entire(apartment_code, phone, contract_nums, contractRequest.now_time(),"2018-12-30"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums, "2018-12-30", "换租"))

        for i in range(self.for_number):
            try:
                self.result = achievementRequest.serach_break_details(self.contract_num)
                if self.result["code"] == 0:
                    break
            except:
                base.consoleLog("查询违约详情接口异常。错误返回：" + str(self.result))
                sleep(self.wait_time)
                self.result = {}
                self.result["code"] = -1
                pass
        base.consoleLog("用例执行完成。预期结果：0 测试结果：" + str(self.result["code"]))
        self.assertEqual(self.result["code"], 0, msg="出租合同号："+ contract_nums)

    def test_break_case_h(self):
        """出租终止,正退.不生成一条违约业绩"""
        base.consoleLog("""出租终止,正退.不生成一条违约业绩""")
        decorationRequest.add_delivered_house(self.contract_num)
        assemblyRequest.solr("apartment")
        apartmentRequest.apartment_price_entire(self.contract_num)
        phone = contractRequest.add_phone_number()
        customerRequest.add_customer("autotest", phone)

        for i in range(self.for_number):
            try:
                sql = 'SELECT apartment_id from apartment where house_id =  (SELECT house_id from house_contract where contract_num = "%s") limit 1' % self.contract_num
                apartment_id = contractRequest.searchSQL(sql)[0][0]
                break
            except Exception as e:
                base.consoleLog("查询sql异常。sql:" + sql + "错误返回：" + str(e))

        for i in range(self.for_number):
            try:
                sql = 'SELECT apartment_code from apartment where apartment_id = "%s"' % apartment_id
                apartment_code = contractRequest.searchSQL(sql)[0][0]
                break
            except Exception as e:
                base.consoleLog("查询sql异常。sql:" + sql + "错误返回：" + str(e))

        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_entire(apartment_code, phone, contract_nums,
                                                                      contractRequest.now_time(), "2018-12-30"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums, "2018-12-30", "正退"))

        for i in range(3):
            try:
                self.result = achievementRequest.serach_break_details(self.contract_num)
                if self.result["code"] == 0:
                    break
            except:
                base.consoleLog("查询违约详情接口异常。错误返回：" + str(self.result))
                self.result = {}
                self.result["code"] = -1
                sleep(3)
                pass
        base.consoleLog("用例执行完成。预期结果：-1 测试结果：" + str(self.result["code"]))
        self.assertEqual(self.result["code"], -1, msg="出租合同号：" + contract_nums)

    def test_break_case_i(self):
        """下定违约金大于0.生成一条违约业绩"""
        base.consoleLog("""下定违约金大于0.生成一条违约业绩""")
        base.consoleLog(decorationRequest.add_delivered_house(self.contract_num))
        base.consoleLog(assemblyRequest.solr("apartment"))
        base.consoleLog(apartmentRequest.apartment_price_entire(self.contract_num))
        phone = base.add_phone_number()
        base.consoleLog(customerRequest.add_customer("autotest", phone))

        for i in range(self.for_number):
            try:
                sql = 'SELECT apartment_id from apartment where house_id =  (SELECT house_id from house_contract where contract_num = "%s") limit 1' % self.contract_num
                apartment_id = contractRequest.searchSQL(sql)[0][0]
                break
            except Exception as e:
                base.consoleLog("查询sql异常。sql:" + sql + "错误返回：" + str(e))

        for i in range(self.for_number):
            try:
                sql = 'SELECT apartment_code from apartment where apartment_id = "%s"' % apartment_id
                apartment_code = contractRequest.searchSQL(sql)[0][0]
                break
            except Exception as e:
                base.consoleLog("查询sql异常。sql:" + sql + "错误返回：" + str(e))

        base.consoleLog(financeRequest.pay_down_payment(apartment_code,phone))
        base.consoleLog(financeRequest.confirmation_down_payment(apartment_code))

        for i in range(self.for_number):
            try:
                self.result = achievementRequest.serach_break_details(self.contract_num)
                if self.result["code"] == 0:
                    break
            except:
                base.consoleLog("查询违约详情接口异常。错误返回：" + str(self.result))
                sleep(self.wait_time)
                self.result = {}
                self.result["code"] = -1
                pass
        base.consoleLog("用例执行完成。预期结果：0 测试结果：" + str(self.result["code"]))
        self.assertEqual(self.result["code"], 0, msg="出租合同号："+ self.contract_num)



if __name__ == "__main__":
    base.host_set("mock")
    contractRequest.get_cookie()
    unittest.main()