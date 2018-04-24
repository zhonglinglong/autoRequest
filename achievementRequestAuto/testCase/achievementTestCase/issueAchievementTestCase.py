# -*- coding:UTF-8 -*-

"""
author = crazyzhong
2018年4月18日09:28:01
出单业绩接口测试用例
"""

from erpRequest import houseDevelopRequest
from erpRequest import contractRequest
from erpRequest import  decorationRequest
from erpRequest import apartmentRequest
from erpRequest import  assemblyRequest
from erpRequest import  customerRequest
from erpRequest import  achievementRequest
from erpRequest import  financeRequest
from erpRequest import contractEndRequest
from time import sleep
from common import base
import unittest



class IssueAchievementBrandEntireTestCase(unittest.TestCase):
    """品牌整租出单业绩生成用例集合"""
    def setUp(self):
        base.consoleLog("-------------------------品牌整租出单业绩生成用例集合strat----------------------")
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
        base.consoleLog("-------------------------品牌整租出单业绩生成用例集合end------------------------")

    def test_issue_case_a(self):
        """已交房.验证业绩核算界面：已交房+已有装修成本打√"""
        base.consoleLog("""已交房.验证业绩核算界面：已交房+已有装修成本打√""")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_entire(self.apartment_code, self.phone, contract_nums, "2018-02-01", "2019-01-31"))
        self.result = achievementRequest.serach_issue_node(contract_nums)
        base.consoleLog("用例执行完成。预期结果：Y  测试结果：" + self.result[u"已交房（装修部门已经填写交房日期）"])
        base.consoleLog("用例执行完成。预期结果：Y  测试结果：" + self.result[u"已有装修成本（装修部门已经填写装修成本）"])
        self.assertEqual(self.result[u"已交房（装修部门已经填写交房日期）"],"Y",msg="出租合同号："+contract_nums)
        self.assertEqual(self.result[u"已有装修成本（装修部门已经填写装修成本）"],"Y",msg="出租合同号："+contract_nums)

    def test_issue_case_b(self):
        """已交房.验证业绩核算界面：生成了一条未生效的业绩"""
        base.consoleLog("""已交房.验证业绩核算界面：生成了一条未生效的业绩""")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_entire(self.apartment_code, self.phone, contract_nums, "2018-02-01","2019-01-31"))
        for i in range(self.for_number):
            self.result = achievementRequest.serach_issue_state(contract_nums)
            if self.result == "N":
                break
            else:
                sleep(self.wait_time)
        base.consoleLog("预期结果：N 测试结果：" + self.result)
        self.assertEqual(self.result, "N", msg="出租合同号：" + contract_nums)

    def test_issue_case_c(self):
        """委托合同已复审.验证业绩核算界面：委托已复审打钩，状态是Y"""
        base.consoleLog("""委托合同已复审.验证业绩核算界面：委托已复审打钩，状态是Y""")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_entire(self.apartment_code, self.phone, contract_nums, "2018-02-01", "2019-01-31"))
        base.consoleLog(contractRequest.reviewed_house_contract(self.contract_num))
        self.result = achievementRequest.serach_issue_node(contract_nums)
        base.consoleLog("用例执行完成。预期结果： Y  测试结果：" + self.result[u"委托合同已通过复审"])
        self.assertEqual(self.result[u"委托合同已通过复审"], "Y", msg="出租合同号：" + contract_nums)

    def test_issue_case_d(self):
        """出租合同已复审.验证业绩核算界面：出租已复审打钩，状态是Y"""
        base.consoleLog("""出租合同已复审.验证业绩核算界面：出租已复审打钩，状态是Y""")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_entire(self.apartment_code, self.phone, contract_nums, "2018-02-01", "2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        self.result = achievementRequest.serach_issue_node(contract_nums)
        base.consoleLog("用例执行完成。预期结果： Y  测试结果：" + self.result[u"出租合同已通过复审"])
        self.assertEqual(self.result[u"出租合同已通过复审"], "Y", msg="出租合同号：" + contract_nums)

    def test_issue_case_e(self):
        """委托出租已复审.验证业绩核算界面：生成了一条未生效的业绩"""
        base.consoleLog("""委托出租已复审.验证业绩核算界面：生成了一条未生效的业绩""")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_entire(self.apartment_code, self.phone, contract_nums, "2018-02-01", "2019-01-31"))
        base.consoleLog(contractRequest.reviewed_house_contract(self.contract_num))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        for i in range(self.for_number):
            self.result = achievementRequest.serach_issue_state(contract_nums)
            if self.result == "Y":
                break
            else:
                sleep(self.wait_time)
        base.consoleLog("用例执行完成。预期结果：Y 测试结果：" + self.result)
        self.assertEqual(self.result,"Y",msg="出租合同号："+contract_nums)

    def test_issue_case_f(self):
        """生效的业绩.收齐首付款。验证业绩核算界面：生成了业绩核发月份"""
        base.consoleLog("""生效的业绩.收齐首付款。验证业绩核算界面：生成了业绩核发月份""")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_entire(self.apartment_code, self.phone, contract_nums, "2018-02-01", "2019-01-31"))
        base.consoleLog(contractRequest.reviewed_house_contract(self.contract_num))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(financeRequest.apartment_contract_collecting_money(contract_nums))
        for i in range(self.for_number):
            try:
                self.result = achievementRequest.serach_issue_divide_into_details(contract_nums)
                if self.result["achievementDetail"][0]["accounting_time"] != "":
                    self.result = True
                    break
            except Exception as e:
                self.result = False
                base.consoleLog("查询核发月份接口异常。错误返回：" + str(e)+ "  接口返回："+ str(self.result))
                sleep(self.wait_time)

        base.consoleLog("用例执行完成。预期结果：True  测试结果：" + str(self.result))
        self.assertEqual(self.result,True,msg="出租合同号："+contract_nums)

    def test_issue_case_g(self):
        """前承租合同终止结算类型是转租，且已通过复审。验证业绩核算界面：该节点变成Y"""
        base.consoleLog("""前承租合同终止结算类型是转租，且已通过复审。验证业绩核算界面：该节点变成Y""")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_entire(self.apartment_code, self.phone, contract_nums, "2018-02-01", "2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums, "2019-01-31", "转租", contractEndRequest.now_time(-1)))
        base.consoleLog(contractEndRequest.reviewed_apartment_contract_end(contract_nums))
        contract_numss = base.random_name()
        phones = base.add_phone_number()
        base.consoleLog(customerRequest.add_customer("testauto", phones))
        base.consoleLog(contractRequest.add_apartment_contract_entire(self.apartment_code, phones, contract_numss, contractEndRequest.now_time(),"2019-01-31"))
        self.result = achievementRequest.serach_issue_node(contract_numss)
        base.consoleLog("用例执行完成。预期结果：Y 测试结果： " + self.result[u"前承租合同终止结算已通过复审（针对转租、退租、换租和收房）"])
        self.assertEqual(self.result[u"前承租合同终止结算已通过复审（针对转租、退租、换租和收房）"],"Y",msg="出租合同号："+contract_numss)

    def test_issue_case_h(self):
        """前承租合同终止结算类型是退租，且已通过复审。验证业绩核算界面：该节点变成Y"""
        base.consoleLog("""前承租合同终止结算类型是退租，且已通过复审。验证业绩核算界面：该节点变成Y""")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_entire(self.apartment_code, self.phone, contract_nums, "2018-02-01", "2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums, "2019-01-31", "退租", contractEndRequest.now_time(-1)))
        base.consoleLog(contractEndRequest.reviewed_apartment_contract_end(contract_nums))
        contract_numss = base.random_name()
        phones = base.add_phone_number()
        base.consoleLog(customerRequest.add_customer("testauto", phones))
        base.consoleLog(contractRequest.add_apartment_contract_entire(self.apartment_code, phones, contract_numss, contractEndRequest.now_time(),"2019-01-31"))
        self.result = achievementRequest.serach_issue_node(contract_numss)
        base.consoleLog("用例执行完成。预期结果：Y  测试结果：" + self.result[u"前承租合同终止结算已通过复审（针对转租、退租、换租和收房）"])
        self.assertEqual(self.result[u"前承租合同终止结算已通过复审（针对转租、退租、换租和收房）"],"Y",msg="出租合同号："+contract_numss)

    def test_issue_case_i(self):
        """前承租合同终止结算类型是换租，且已通过复审。验证业绩核算界面：该节点变成Y"""
        base.consoleLog("""前承租合同终止结算类型是换租，且已通过复审。验证业绩核算界面：该节点变成Y""")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_entire(self.apartment_code, self.phone, contract_nums, "2018-02-01", "2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums, "2019-01-31", "换租", contractEndRequest.now_time(-1)))
        base.consoleLog(contractEndRequest.reviewed_apartment_contract_end(contract_nums))
        contract_numss = base.random_name()
        phones = base.add_phone_number()
        base.consoleLog(customerRequest.add_customer("testauto", phones))
        base.consoleLog(contractRequest.add_apartment_contract_entire(self.apartment_code, phones, contract_numss, contractEndRequest.now_time(),"2019-01-31"))
        self.result = achievementRequest.serach_issue_node(contract_numss)
        base.consoleLog("用例执行完成。预期结果：Y 测试结果：" + self.result[u"前承租合同终止结算已通过复审（针对转租、退租、换租和收房）"])
        self.assertEqual(self.result[u"前承租合同终止结算已通过复审（针对转租、退租、换租和收房）"],"Y",msg="出租合同号："+contract_numss)

    def test_issue_case_j(self):
        """前承租合同终止结算类型是收房，且已通过复审。验证业绩核算界面：该节点变成Y"""
        base.consoleLog("""前承租合同终止结算类型是收房，且已通过复审。验证业绩核算界面：该节点变成Y""")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_entire(self.apartment_code, self.phone, contract_nums, "2018-02-01", "2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums, "2019-01-31", "收房", contractEndRequest.now_time(-1)))
        base.consoleLog(contractEndRequest.reviewed_apartment_contract_end(contract_nums))
        contract_numss = base.random_name()
        phones = base.add_phone_number()
        base.consoleLog(customerRequest.add_customer("testauto", phones))
        base.consoleLog(contractRequest.add_apartment_contract_entire(self.apartment_code, phones, contract_numss, contractEndRequest.now_time(),"2019-01-31"))
        self.result = achievementRequest.serach_issue_node(contract_numss)
        base.consoleLog("用例执行完成。预期结果：Y 测试结果：" + self.result[u"前承租合同终止结算已通过复审（针对转租、退租、换租和收房）"])
        self.assertEqual(self.result[u"前承租合同终止结算已通过复审（针对转租、退租、换租和收房）"],"Y",msg="出租合同号："+contract_numss)

    def test_issue_case_k(self):
        """前承租合同终止结算类型是正退，且已通过复审。验证业绩核算界面：无此节点"""
        base.consoleLog("""前承租合同终止结算类型是正退，且已通过复审。验证业绩核算界面：无此节点""")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_entire(self.apartment_code, self.phone, contract_nums, "2018-02-01", "2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums, "2019-01-31", "正退", contractEndRequest.now_time(-1)))
        base.consoleLog(contractEndRequest.reviewed_apartment_contract_end(contract_nums))
        contract_numss = base.random_name()
        phones = base.add_phone_number()
        base.consoleLog(customerRequest.add_customer("testauto", phones))
        base.consoleLog(contractRequest.add_apartment_contract_entire(self.apartment_code, phones, contract_numss, contractEndRequest.now_time(),"2019-01-31"))
        self.result = achievementRequest.serach_issue_node(contract_numss)
        try:
            self.result[u"前承租合同终止结算已通过复审（针对转租、退租、换租和收房）"]
            self.result = False
        except:
            self.result = True
        base.consoleLog("用例执行完成。预期结果： True  测试结果：" + str(self.result))
        self.assertEqual(self.result,True,msg="出租合同号："+contract_numss)

    def test_issue_case_l(self):
        """前承租合同终止结算类型是收房，未通过复审,委托已复审，出租已复审。验证生成一条未生效的业绩"""
        base.consoleLog("""前承租合同终止结算类型是收房，未通过复审,委托已复审，出租已复审。验证生成一条未生效的业绩""")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_entire(self.apartment_code, self.phone, contract_nums, "2018-02-01", "2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums, "2019-01-31", "收房", contractEndRequest.now_time(-1)))
        contract_numss = base.random_name()
        phones = base.add_phone_number()
        base.consoleLog(customerRequest.add_customer("testauto", phones))
        base.consoleLog(contractRequest.add_apartment_contract_entire(self.apartment_code, phones, contract_numss, contractEndRequest.now_time(),"2019-01-31"))
        base.consoleLog(contractRequest.reviewed_house_contract(self.contract_num))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_numss))
        for i in range(self.for_number):
            self.result = achievementRequest.serach_issue_state(contract_numss)
            if self.result == "N":
                break
            else:
                sleep(self.for_number)
        base.consoleLog("用例执行完成。预期结果：N  测试结果：" + self.result)
        self.assertEqual(self.result,"N",msg="出租合同号："+contract_numss)

    def test_issue_case_m(self):
        """前承租合同终止结算类型是退租，通过复审,委托已复审，出租已复审。验证生成一条生效的业绩"""
        base.consoleLog("""前承租合同终止结算类型是退租，通过复审,委托已复审，出租已复审。验证生成一条生效的业绩""")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_entire(self.apartment_code, self.phone, contract_nums, "2018-02-01",
                                                      "2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums, "2019-01-31", "退租", contractEndRequest.now_time(-1)))
        base.consoleLog(contractEndRequest.reviewed_apartment_contract_end(contract_nums))
        contract_numss = base.random_name()
        phones = base.add_phone_number()
        base.consoleLog(customerRequest.add_customer("testauto", phones))
        base.consoleLog(contractRequest.add_apartment_contract_entire(self.apartment_code, phones, contract_numss,
                                                      contractEndRequest.now_time(), "2019-01-31"))
        base.consoleLog(contractRequest.reviewed_house_contract(self.contract_num))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_numss))
        for i in range(self.for_number):
            self.result = achievementRequest.serach_issue_state(contract_numss)
            if self.result == "Y":
                break
            else:
                sleep(self.wait_time)
        base.consoleLog("用例执行完成。预期结果：Y 测试结果：" + self.result)
        self.assertEqual(self.result, "Y", msg="出租合同号：" + contract_numss)

    def test_issue_case_n(self):
        """前承租合同终止结算类型是换租，通过复审,委托已复审，出租已复审,首付款完成。验证生成一条生效的业绩且有核发月份"""
        base.consoleLog( """前承租合同终止结算类型是换租，通过复审,委托已复审，出租已复审,首付款完成。验证生成一条生效的业绩且有核发月份""")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_entire(self.apartment_code, self.phone, contract_nums, "2018-02-01", "2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums, "2019-01-31", "退租", contractEndRequest.now_time(-1)))
        base.consoleLog(contractEndRequest.reviewed_apartment_contract_end(contract_nums))
        contract_numss = base.random_name()
        phones = base.add_phone_number()
        base.consoleLog(customerRequest.add_customer("testauto", phones))
        base.consoleLog(contractRequest.add_apartment_contract_entire(self.apartment_code, phones, contract_numss, contractEndRequest.now_time(),"2019-01-31"))
        base.consoleLog(contractRequest.reviewed_house_contract(self.contract_num))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_numss))
        base.consoleLog(financeRequest.apartment_contract_collecting_money(contract_numss))
        for i in range(self.for_number):
            self.result = achievementRequest.serach_issue_divide_into_details(contract_numss)
            if self.result["achievementDetail"][0]["accounting_time"] != "":
                self.result = True
                break
            else:
                sleep(self.wait_time)
        self.assertEqual(self.result, True, msg="出租合同号：" + contract_numss)
        base.consoleLog("用例执行完成。预期结果： True  测试结果：" + str(self.result))
        self.result = achievementRequest.serach_issue_state(contract_numss)
        base.consoleLog("用例执行完成。预期结果： Y  测试结果：" + self.result)
        self.assertEqual(self.result, "Y", msg="出租合同号：" + contract_numss)

class IssueAchievementManageEntireTestCase(unittest.TestCase):
    """服务整租出单业绩生成用例集合"""

    def setUp(self):
        base.consoleLog("-------------------------服务整租出单业绩生成用例集合strat----------------------")
        self.for_number = 100
        self.wait_time = 1
        base.consoleLog(houseDevelopRequest.add_house_delelop("业绩测试预发专用楼盘", 1))
        self.contract_num = base.random_name()
        base.consoleLog(contractRequest.add_house_contract("业绩测试预发专用楼盘", self.contract_num, "2018-01-01", "服务公寓", "整租", "微改"))
        for i in range(self.for_number):
            try:
                sql = "SELECT contract_num from query_house_contract where contract_num = '%s'" % self.contract_num
                base.searchSQL(sql)[0][0]
                break
            except Exception as e:
                base.consoleLog("委托合同未生成宽表，重新查询数据库。报错信息："+str(e)+ "sql:" + sql,level='e')
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
        base.consoleLog("-------------------------服务整租出单业绩生成用例集合end------------------------")
    # def test_issue_case_a(self):
    #     """已交房.验证业绩核算界面：已交房+已有装修成本打√"""
    #     base.consoleLog("""已交房.验证业绩核算界面：已交房+已有装修成本打√""")
    #     contract_nums = base.random_name()
    #     base.consoleLog(contractRequest.add_apartment_contract_entire(self.apartment_code, self.phone, contract_nums, "2018-02-01", "2019-01-31"))
    #     self.result = achievementRequest.serach_issue_node(contract_nums)
    #     self.assertEqual(self.result[u"已有装修成本（装修部门已经填写装修成本）"],"Y",msg="出租合同号："+contract_nums)
    #     base.consoleLog("用例执行完成。预期结果：Y  测试结果：" + self.result[u"已有装修成本（装修部门已经填写装修成本）"])

    def test_issue_case_b(self):
        """已交房.验证业绩核算界面：生成了一条未生效的业绩"""
        base.consoleLog("""已交房.验证业绩核算界面：生成了一条未生效的业绩""")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_entire(self.apartment_code, self.phone, contract_nums, "2018-02-01","2019-01-31"))
        for i in range(self.for_number):
            self.result = achievementRequest.serach_issue_state(contract_nums)
            if self.result == "N":
                break
            else:
                sleep(self.wait_time)
        base.consoleLog("预期结果：N 测试结果：" + self.result)
        self.assertEqual(self.result, "N", msg="出租合同号：" + contract_nums)

    def test_issue_case_c(self):
        """委托合同已复审.验证业绩核算界面：委托已复审打钩，状态是Y"""
        base.consoleLog("""委托合同已复审.验证业绩核算界面：委托已复审打钩，状态是Y""")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_entire(self.apartment_code, self.phone, contract_nums, "2018-02-01", "2019-01-31"))
        base.consoleLog(contractRequest.reviewed_house_contract(self.contract_num))
        self.result = achievementRequest.serach_issue_node(contract_nums)
        base.consoleLog("用例执行完成。预期结果： Y  测试结果：" + self.result[u"委托合同已通过复审"])
        self.assertEqual(self.result[u"委托合同已通过复审"], "Y", msg="出租合同号：" + contract_nums)

    def test_issue_case_d(self):
        """出租合同已复审.验证业绩核算界面：出租已复审打钩，状态是Y"""
        base.consoleLog("""出租合同已复审.验证业绩核算界面：出租已复审打钩，状态是Y""")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_entire(self.apartment_code, self.phone, contract_nums, "2018-02-01", "2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        self.result = achievementRequest.serach_issue_node(contract_nums)
        base.consoleLog("用例执行完成。预期结果： Y  测试结果：" + self.result[u"出租合同已通过复审"])
        self.assertEqual(self.result[u"出租合同已通过复审"], "Y", msg="出租合同号：" + contract_nums)

    def test_issue_case_e(self):
        """委托出租已复审.验证业绩核算界面：生成了一条未生效的业绩"""
        base.consoleLog("""委托出租已复审.验证业绩核算界面：生成了一条未生效的业绩""")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_entire(self.apartment_code, self.phone, contract_nums, "2018-02-01", "2019-01-31"))
        base.consoleLog(contractRequest.reviewed_house_contract(self.contract_num))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        for i in range(self.for_number):
            self.result = achievementRequest.serach_issue_state(contract_nums)
            if self.result == "Y":
                break
            else:
                sleep(self.wait_time)
        base.consoleLog("用例执行完成。预期结果：Y 测试结果：" + self.result)
        self.assertEqual(self.result,"Y",msg="出租合同号："+contract_nums)

    def test_issue_case_f(self):
        """生效的业绩.收齐首付款。验证业绩核算界面：生成了业绩核发月份"""
        base.consoleLog("""生效的业绩.收齐首付款。验证业绩核算界面：生成了业绩核发月份""")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_entire(self.apartment_code, self.phone, contract_nums, "2018-02-01", "2019-01-31"))
        base.consoleLog(contractRequest.reviewed_house_contract(self.contract_num))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(financeRequest.apartment_contract_collecting_money(contract_nums))
        for i in range(self.for_number):
            self.result = achievementRequest.serach_issue_divide_into_details(contract_nums)
            if self.result["achievementDetail"][0]["accounting_time"] != "":
                self.result = True
                break
            else:
                sleep(self.wait_time)
        base.consoleLog("用例执行完成。预期结果：True  测试结果：" + str(self.result))
        self.assertEqual(self.result,True,msg="出租合同号："+contract_nums)

    def test_issue_case_g(self):
        """前承租合同终止结算类型是转租，且已通过复审。验证业绩核算界面：该节点变成Y"""
        base.consoleLog("""前承租合同终止结算类型是转租，且已通过复审。验证业绩核算界面：该节点变成Y""")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_entire(self.apartment_code, self.phone, contract_nums, "2018-02-01", "2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums, "2019-01-31", "转租", contractEndRequest.now_time(-1)))
        base.consoleLog(contractEndRequest.reviewed_apartment_contract_end(contract_nums))
        contract_numss = base.random_name()
        phones = base.add_phone_number()
        base.consoleLog(customerRequest.add_customer("testauto", phones))
        base.consoleLog(contractRequest.add_apartment_contract_entire(self.apartment_code, phones, contract_numss, contractEndRequest.now_time(),"2019-01-31"))
        self.result = achievementRequest.serach_issue_node(contract_numss)
        base.consoleLog("用例执行完成。预期结果：Y 测试结果： " + self.result[u"前承租合同终止结算已通过复审（针对转租、退租、换租和收房）"])
        self.assertEqual(self.result[u"前承租合同终止结算已通过复审（针对转租、退租、换租和收房）"],"Y",msg="出租合同号："+contract_numss)

    def test_issue_case_h(self):
        """前承租合同终止结算类型是退租，且已通过复审。验证业绩核算界面：该节点变成Y"""
        base.consoleLog("""前承租合同终止结算类型是退租，且已通过复审。验证业绩核算界面：该节点变成Y""")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_entire(self.apartment_code, self.phone, contract_nums, "2018-02-01", "2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums, "2019-01-31", "退租", contractEndRequest.now_time(-1)))
        base.consoleLog(contractEndRequest.reviewed_apartment_contract_end(contract_nums))
        contract_numss = base.random_name()
        phones = base.add_phone_number()
        base.consoleLog(customerRequest.add_customer("testauto", phones))
        base.consoleLog(contractRequest.add_apartment_contract_entire(self.apartment_code, phones, contract_numss, contractEndRequest.now_time(),"2019-01-31"))
        self.result = achievementRequest.serach_issue_node(contract_numss)
        base.consoleLog("用例执行完成。预期结果：Y  测试结果：" + self.result[u"前承租合同终止结算已通过复审（针对转租、退租、换租和收房）"])
        self.assertEqual(self.result[u"前承租合同终止结算已通过复审（针对转租、退租、换租和收房）"],"Y",msg="出租合同号："+contract_numss)

    def test_issue_case_i(self):
        """前承租合同终止结算类型是换租，且已通过复审。验证业绩核算界面：该节点变成Y"""
        base.consoleLog("""前承租合同终止结算类型是换租，且已通过复审。验证业绩核算界面：该节点变成Y""")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_entire(self.apartment_code, self.phone, contract_nums, "2018-02-01", "2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums, "2019-01-31", "换租", contractEndRequest.now_time(-1)))
        base.consoleLog(contractEndRequest.reviewed_apartment_contract_end(contract_nums))
        contract_numss = base.random_name()
        phones = base.add_phone_number()
        base.consoleLog(customerRequest.add_customer("testauto", phones))
        base.consoleLog(contractRequest.add_apartment_contract_entire(self.apartment_code, phones, contract_numss, contractEndRequest.now_time(),"2019-01-31"))
        self.result = achievementRequest.serach_issue_node(contract_numss)
        base.consoleLog("用例执行完成。预期结果：Y 测试结果：" + self.result[u"前承租合同终止结算已通过复审（针对转租、退租、换租和收房）"])
        self.assertEqual(self.result[u"前承租合同终止结算已通过复审（针对转租、退租、换租和收房）"],"Y",msg="出租合同号："+contract_numss)

    def test_issue_case_j(self):
        """前承租合同终止结算类型是收房，且已通过复审。验证业绩核算界面：该节点变成Y"""
        base.consoleLog("""前承租合同终止结算类型是收房，且已通过复审。验证业绩核算界面：该节点变成Y""")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_entire(self.apartment_code, self.phone, contract_nums, "2018-02-01", "2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums, "2019-01-31", "收房", contractEndRequest.now_time(-1)))
        base.consoleLog(contractEndRequest.reviewed_apartment_contract_end(contract_nums))
        contract_numss = base.random_name()
        phones = base.add_phone_number()
        base.consoleLog(customerRequest.add_customer("testauto", phones))
        base.consoleLog(contractRequest.add_apartment_contract_entire(self.apartment_code, phones, contract_numss, contractEndRequest.now_time(),"2019-01-31"))
        self.result = achievementRequest.serach_issue_node(contract_numss)
        base.consoleLog("用例执行完成。预期结果：Y 测试结果：" + self.result[u"前承租合同终止结算已通过复审（针对转租、退租、换租和收房）"])
        self.assertEqual(self.result[u"前承租合同终止结算已通过复审（针对转租、退租、换租和收房）"],"Y",msg="出租合同号："+contract_numss)

    def test_issue_case_k(self):
        """前承租合同终止结算类型是正退，且已通过复审。验证业绩核算界面：无此节点"""
        base.consoleLog("""前承租合同终止结算类型是正退，且已通过复审。验证业绩核算界面：无此节点""")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_entire(self.apartment_code, self.phone, contract_nums, "2018-02-01", "2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums, "2019-01-31", "正退", contractEndRequest.now_time(-1)))
        base.consoleLog(contractEndRequest.reviewed_apartment_contract_end(contract_nums))
        contract_numss = base.random_name()
        phones = base.add_phone_number()
        base.consoleLog(customerRequest.add_customer("testauto", phones))
        base.consoleLog(contractRequest.add_apartment_contract_entire(self.apartment_code, phones, contract_numss, contractEndRequest.now_time(),"2019-01-31"))
        self.result = achievementRequest.serach_issue_node(contract_numss)
        try:
            self.result[u"前承租合同终止结算已通过复审（针对转租、退租、换租和收房）"]
            self.result = False
        except:
            self.result = True
        base.consoleLog("用例执行完成。预期结果： True  测试结果：" + str(self.result))
        self.assertEqual(self.result,True,msg="出租合同号："+contract_numss)

    def test_issue_case_l(self):
        """前承租合同终止结算类型是收房，未通过复审,委托已复审，出租已复审。验证生成一条未生效的业绩"""
        base.consoleLog("""前承租合同终止结算类型是收房，未通过复审,委托已复审，出租已复审。验证生成一条未生效的业绩""")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_entire(self.apartment_code, self.phone, contract_nums, "2018-02-01", "2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums, "2019-01-31", "收房", contractEndRequest.now_time(-1)))
        contract_numss = base.random_name()
        phones = base.add_phone_number()
        base.consoleLog(customerRequest.add_customer("testauto", phones))
        base.consoleLog(contractRequest.add_apartment_contract_entire(self.apartment_code, phones, contract_numss, contractEndRequest.now_time(),"2019-01-31"))
        base.consoleLog(contractRequest.reviewed_house_contract(self.contract_num))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_numss))
        for i in range(self.for_number):
            self.result = achievementRequest.serach_issue_state(contract_numss)
            if self.result == "N":
                break
            else:
                sleep(self.for_number)
        base.consoleLog("用例执行完成。预期结果：N  测试结果：" + self.result)
        self.assertEqual(self.result,"N",msg="出租合同号："+contract_numss)

    def test_issue_case_m(self):
        """前承租合同终止结算类型是退租，通过复审,委托已复审，出租已复审。验证生成一条生效的业绩"""
        base.consoleLog("""前承租合同终止结算类型是退租，通过复审,委托已复审，出租已复审。验证生成一条生效的业绩""")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_entire(self.apartment_code, self.phone, contract_nums, "2018-02-01",
                                                      "2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums, "2019-01-31", "退租", contractEndRequest.now_time(-1)))
        base.consoleLog(contractEndRequest.reviewed_apartment_contract_end(contract_nums))
        contract_numss = base.random_name()
        phones = base.add_phone_number()
        base.consoleLog(customerRequest.add_customer("testauto", phones))
        base.consoleLog(contractRequest.add_apartment_contract_entire(self.apartment_code, phones, contract_numss,
                                                      contractEndRequest.now_time(), "2019-01-31"))
        base.consoleLog(contractRequest.reviewed_house_contract(self.contract_num))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_numss))
        for i in range(self.for_number):
            self.result = achievementRequest.serach_issue_state(contract_numss)
            if self.result == "Y":
                break
            else:
                sleep(self.wait_time)
        base.consoleLog("用例执行完成。预期结果：Y 测试结果：" + self.result)
        self.assertEqual(self.result, "Y", msg="出租合同号：" + contract_numss)

    def test_issue_case_n(self):
        """前承租合同终止结算类型是换租，通过复审,委托已复审，出租已复审,首付款完成。验证生成一条生效的业绩且有核发月份"""
        base.consoleLog("""前承租合同终止结算类型是换租，通过复审,委托已复审，出租已复审,首付款完成。验证生成一条生效的业绩且有核发月份""")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_entire(self.apartment_code, self.phone, contract_nums, "2018-02-01", "2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums, "2019-01-31", "退租", contractEndRequest.now_time(-1)))
        base.consoleLog(contractEndRequest.reviewed_apartment_contract_end(contract_nums))
        contract_numss = base.random_name()
        phones = base.add_phone_number()
        base.consoleLog(customerRequest.add_customer("testauto", phones))
        base.consoleLog(contractRequest.add_apartment_contract_entire(self.apartment_code, phones, contract_numss, contractEndRequest.now_time(),"2019-01-31"))
        base.consoleLog(contractRequest.reviewed_house_contract(self.contract_num))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_numss))
        base.consoleLog(financeRequest.apartment_contract_collecting_money(contract_numss))
        for i in range(self.for_number):
            self.result = achievementRequest.serach_issue_divide_into_details(contract_numss)
            if self.result["achievementDetail"][0]["accounting_time"] != "":
                self.result = True
                break
            else:
                sleep(self.wait_time)
        self.assertEqual(self.result, True, msg="出租合同号：" + contract_numss)
        base.consoleLog("用例执行完成。预期结果： True  测试结果：" + str(self.result))
        self.result = achievementRequest.serach_issue_state(contract_numss)
        base.consoleLog("用例执行完成。预期结果： Y  测试结果：" + self.result)
        self.assertEqual(self.result, "Y", msg="出租合同号：" + contract_numss)

class IssueAchievementBrandShareTestCase(unittest.TestCase):
    """品牌合租出单业绩生成用例集合"""
    def setUp(self):
        base.consoleLog("-------------------------品牌合租出单业绩生成用例集合strat----------------------")
        self.for_number = 100
        self.wait_time = 1
        base.consoleLog(houseDevelopRequest.add_house_delelop("业绩测试预发专用楼盘", 1))
        self.contract_num = base.random_name()
        base.consoleLog(contractRequest.add_house_contract("业绩测试预发专用楼盘", self.contract_num, "2018-01-01", "品牌公寓", "合租", "大改"))
        for i in range(self.for_number):
            try:
                sql = "SELECT contract_num from query_house_contract where contract_num = '%s'" % self.contract_num
                base.searchSQL(sql)[0][0]
                break
            except Exception as e:
                base.consoleLog("委托合同未生成宽表，重新查询数据库。报错信息："+str(e)+ "sql:" + sql,level='e')
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
                sql = 'SELECT apartment_code from apartment where apartment_id = "%s" ' % self.apartment_id
                self.apartment_code = base.searchSQL(sql)[0][0]
                break
            except Exception as e:
                base.consoleLog("房源定价失败或者没有生成自营房源。报错信息"+ str(e))
                sleep(self.wait_time)
                pass
    def tearDown(self):
        base.consoleLog("-------------------------品牌合租出单业绩生成用例集合end------------------------")
    def test_issue_case_a(self):
        """已交房.验证业绩核算界面：已交房+已有装修成本打√"""
        base.consoleLog("""已交房.验证业绩核算界面：已交房+已有装修成本打√""")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_share(self.apartment_code, self.phone, contract_nums, "2018-02-01", "2019-01-31"))
        self.result = achievementRequest.serach_issue_node(contract_nums)
        base.consoleLog("用例执行完成。预期结果：Y  测试结果：" + self.result[u"已交房（装修部门已经填写交房日期）"])
        base.consoleLog("用例执行完成。预期结果：Y  测试结果：" + self.result[u"已有装修成本（装修部门已经填写装修成本）"])
        self.assertEqual(self.result[u"已交房（装修部门已经填写交房日期）"],"Y",msg="出租合同号："+contract_nums)
        self.assertEqual(self.result[u"已有装修成本（装修部门已经填写装修成本）"],"Y",msg="出租合同号："+contract_nums)

    def test_issue_case_b(self):
        """已交房.验证业绩核算界面：生成了一条未生效的业绩"""
        base.consoleLog("""已交房.验证业绩核算界面：生成了一条未生效的业绩""")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_share(self.apartment_code, self.phone, contract_nums, "2018-02-01","2019-01-31"))
        for i in range(self.for_number):
            self.result = achievementRequest.serach_issue_state(contract_nums)
            if self.result == "N":
                break
            else:
                sleep(self.wait_time)
        base.consoleLog("预期结果：N 测试结果：" + self.result)
        self.assertEqual(self.result, "N", msg="出租合同号：" + contract_nums)

    def test_issue_case_c(self):
        """委托合同已复审.验证业绩核算界面：委托已复审打钩，状态是Y"""
        base.consoleLog("""委托合同已复审.验证业绩核算界面：委托已复审打钩，状态是Y""")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_share(self.apartment_code, self.phone, contract_nums, "2018-02-01", "2019-01-31"))
        base.consoleLog(contractRequest.reviewed_house_contract(self.contract_num))
        self.result = achievementRequest.serach_issue_node(contract_nums)
        base.consoleLog("用例执行完成。预期结果： Y  测试结果：" + self.result[u"委托合同已通过复审"])
        self.assertEqual(self.result[u"委托合同已通过复审"], "Y", msg="出租合同号：" + contract_nums)

    def test_issue_case_d(self):
        """出租合同已复审.验证业绩核算界面：出租已复审打钩，状态是Y"""
        base.consoleLog("""出租合同已复审.验证业绩核算界面：出租已复审打钩，状态是Y""")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_share(self.apartment_code, self.phone, contract_nums, "2018-02-01", "2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        self.result = achievementRequest.serach_issue_node(contract_nums)
        base.consoleLog("用例执行完成。预期结果： Y  测试结果：" + self.result[u"出租合同已通过复审"])
        self.assertEqual(self.result[u"出租合同已通过复审"], "Y", msg="出租合同号：" + contract_nums)

    def test_issue_case_e(self):
        """委托出租已复审.验证业绩核算界面：生成了一条未生效的业绩"""
        base.consoleLog("""委托出租已复审.验证业绩核算界面：生成了一条未生效的业绩""")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_share(self.apartment_code, self.phone, contract_nums, "2018-02-01", "2019-01-31"))
        base.consoleLog(contractRequest.reviewed_house_contract(self.contract_num))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        for i in range(self.for_number):
            self.result = achievementRequest.serach_issue_state(contract_nums)
            if self.result == "Y":
                break
            else:
                sleep(self.wait_time)
        base.consoleLog("用例执行完成。预期结果：Y 测试结果：" + self.result)
        self.assertEqual(self.result,"Y",msg="出租合同号："+contract_nums)

    def test_issue_case_f(self):
        """生效的业绩.收齐首付款。验证业绩核算界面：生成了业绩核发月份"""
        base.consoleLog("""生效的业绩.收齐首付款。验证业绩核算界面：生成了业绩核发月份""")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_share(self.apartment_code, self.phone, contract_nums, "2018-02-01", "2019-01-31"))
        base.consoleLog(contractRequest.reviewed_house_contract(self.contract_num))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(financeRequest.apartment_contract_collecting_money(contract_nums))
        for i in range(self.for_number):
            self.result = achievementRequest.serach_issue_divide_into_details(contract_nums)
            if self.result["achievementDetail"][0]["accounting_time"] != "":
                self.result = True
                break
            else:
                sleep(self.wait_time)
        base.consoleLog("用例执行完成。预期结果：True  测试结果：" + str(self.result))
        self.assertEqual(self.result,True,msg="出租合同号："+contract_nums)

    def test_issue_case_g(self):
        """前承租合同终止结算类型是转租，且已通过复审。验证业绩核算界面：该节点变成Y"""
        base.consoleLog("""前承租合同终止结算类型是转租，且已通过复审。验证业绩核算界面：该节点变成Y""")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_share(self.apartment_code, self.phone, contract_nums, "2018-02-01", "2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums, "2019-01-31", "转租", contractEndRequest.now_time(-1)))
        base.consoleLog(contractEndRequest.reviewed_apartment_contract_end(contract_nums))
        contract_numss = base.random_name()
        phones = base.add_phone_number()
        base.consoleLog(customerRequest.add_customer("testauto", phones))
        base.consoleLog(contractRequest.add_apartment_contract_share(self.apartment_code, phones, contract_numss, contractEndRequest.now_time(),"2019-01-31"))
        self.result = achievementRequest.serach_issue_node(contract_numss)
        base.consoleLog("用例执行完成。预期结果：Y 测试结果： " + self.result[u"前承租合同终止结算已通过复审（针对转租、退租、换租和收房）"])
        self.assertEqual(self.result[u"前承租合同终止结算已通过复审（针对转租、退租、换租和收房）"],"Y",msg="出租合同号："+contract_numss)

    def test_issue_case_h(self):
        """前承租合同终止结算类型是退租，且已通过复审。验证业绩核算界面：该节点变成Y"""
        base.consoleLog("""前承租合同终止结算类型是退租，且已通过复审。验证业绩核算界面：该节点变成Y""")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_share(self.apartment_code, self.phone, contract_nums, "2018-02-01", "2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums, "2019-01-31", "退租", contractEndRequest.now_time(-1)))
        base.consoleLog(contractEndRequest.reviewed_apartment_contract_end(contract_nums))
        contract_numss = base.random_name()
        phones = base.add_phone_number()
        base.consoleLog(customerRequest.add_customer("testauto", phones))
        base.consoleLog(contractRequest.add_apartment_contract_share(self.apartment_code, phones, contract_numss, contractEndRequest.now_time(),"2019-01-31"))
        self.result = achievementRequest.serach_issue_node(contract_numss)
        base.consoleLog("用例执行完成。预期结果：Y  测试结果：" + self.result[u"前承租合同终止结算已通过复审（针对转租、退租、换租和收房）"])
        self.assertEqual(self.result[u"前承租合同终止结算已通过复审（针对转租、退租、换租和收房）"],"Y",msg="出租合同号："+contract_numss)

    def test_issue_case_i(self):
        """前承租合同终止结算类型是换租，且已通过复审。验证业绩核算界面：该节点变成Y"""
        base.consoleLog("""前承租合同终止结算类型是换租，且已通过复审。验证业绩核算界面：该节点变成Y""")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_share(self.apartment_code, self.phone, contract_nums, "2018-02-01", "2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums, "2019-01-31", "换租", contractEndRequest.now_time(-1)))
        base.consoleLog(contractEndRequest.reviewed_apartment_contract_end(contract_nums))
        contract_numss = base.random_name()
        phones = base.add_phone_number()
        base.consoleLog(customerRequest.add_customer("testauto", phones))
        base.consoleLog(contractRequest.add_apartment_contract_share(self.apartment_code, phones, contract_numss, contractEndRequest.now_time(),"2019-01-31"))
        self.result = achievementRequest.serach_issue_node(contract_numss)
        base.consoleLog("用例执行完成。预期结果：Y 测试结果：" + self.result[u"前承租合同终止结算已通过复审（针对转租、退租、换租和收房）"])
        self.assertEqual(self.result[u"前承租合同终止结算已通过复审（针对转租、退租、换租和收房）"],"Y",msg="出租合同号："+contract_numss)

    def test_issue_case_j(self):
        """前承租合同终止结算类型是收房，且已通过复审。验证业绩核算界面：该节点变成Y"""
        base.consoleLog("""前承租合同终止结算类型是收房，且已通过复审。验证业绩核算界面：该节点变成Y""")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_share(self.apartment_code, self.phone, contract_nums, "2018-02-01", "2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums, "2019-01-31", "收房", contractEndRequest.now_time(-1)))
        base.consoleLog(contractEndRequest.reviewed_apartment_contract_end(contract_nums))
        contract_numss = base.random_name()
        phones = base.add_phone_number()
        base.consoleLog(customerRequest.add_customer("testauto", phones))
        base.consoleLog(contractRequest.add_apartment_contract_share(self.apartment_code, phones, contract_numss, contractEndRequest.now_time(),"2019-01-31"))
        self.result = achievementRequest.serach_issue_node(contract_numss)
        base.consoleLog("用例执行完成。预期结果：Y 测试结果：" + self.result[u"前承租合同终止结算已通过复审（针对转租、退租、换租和收房）"])
        self.assertEqual(self.result[u"前承租合同终止结算已通过复审（针对转租、退租、换租和收房）"],"Y",msg="出租合同号："+contract_numss)

    def test_issue_case_k(self):
        """前承租合同终止结算类型是正退，且已通过复审。验证业绩核算界面：无此节点"""
        base.consoleLog("""前承租合同终止结算类型是正退，且已通过复审。验证业绩核算界面：无此节点""")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_share(self.apartment_code, self.phone, contract_nums, "2018-02-01", "2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums, "2019-01-31", "正退", contractEndRequest.now_time(-1)))
        base.consoleLog(contractEndRequest.reviewed_apartment_contract_end(contract_nums))
        contract_numss = base.random_name()
        phones = base.add_phone_number()
        base.consoleLog(customerRequest.add_customer("testauto", phones))
        base.consoleLog(contractRequest.add_apartment_contract_share(self.apartment_code, phones, contract_numss, contractEndRequest.now_time(),"2019-01-31"))
        self.result = achievementRequest.serach_issue_node(contract_numss)
        try:
            self.result[u"前承租合同终止结算已通过复审（针对转租、退租、换租和收房）"]
            self.result = False
        except:
            self.result = True
        base.consoleLog("用例执行完成。预期结果： True  测试结果：" + str(self.result))
        self.assertEqual(self.result,True,msg="出租合同号："+contract_numss)

    def test_issue_case_l(self):
        """前承租合同终止结算类型是收房，未通过复审,委托已复审，出租已复审。验证生成一条未生效的业绩"""
        base.consoleLog("""前承租合同终止结算类型是收房，未通过复审,委托已复审，出租已复审。验证生成一条未生效的业绩""")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_share(self.apartment_code, self.phone, contract_nums, "2018-02-01", "2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums, "2019-01-31", "收房", contractEndRequest.now_time(-1)))
        contract_numss = base.random_name()
        phones = base.add_phone_number()
        base.consoleLog(customerRequest.add_customer("testauto", phones))
        base.consoleLog(contractRequest.add_apartment_contract_share(self.apartment_code, phones, contract_numss, contractEndRequest.now_time(),"2019-01-31"))
        base.consoleLog(contractRequest.reviewed_house_contract(self.contract_num))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_numss))
        for i in range(self.for_number):
            self.result = achievementRequest.serach_issue_state(contract_numss)
            if self.result == "N":
                break
            else:
                sleep(self.for_number)
        base.consoleLog("用例执行完成。预期结果：N  测试结果：" + self.result)
        self.assertEqual(self.result,"N",msg="出租合同号："+contract_numss)

    def test_issue_case_m(self):
        """前承租合同终止结算类型是退租，通过复审,委托已复审，出租已复审。验证生成一条生效的业绩"""
        base.consoleLog("""前承租合同终止结算类型是退租，通过复审,委托已复审，出租已复审。验证生成一条生效的业绩""")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_share(self.apartment_code, self.phone, contract_nums, "2018-02-01",
                                                      "2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums, "2019-01-31", "退租", contractEndRequest.now_time(-1)))
        base.consoleLog(contractEndRequest.reviewed_apartment_contract_end(contract_nums))
        contract_numss = base.random_name()
        phones = base.add_phone_number()
        base.consoleLog(customerRequest.add_customer("testauto", phones))
        base.consoleLog(contractRequest.add_apartment_contract_share(self.apartment_code, phones, contract_numss,
                                                      contractEndRequest.now_time(), "2019-01-31"))
        base.consoleLog(contractRequest.reviewed_house_contract(self.contract_num))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_numss))
        for i in range(self.for_number):
            self.result = achievementRequest.serach_issue_state(contract_numss)
            if self.result == "Y":
                break
            else:
                sleep(self.wait_time)
        base.consoleLog("用例执行完成。预期结果：Y 测试结果：" + self.result)
        self.assertEqual(self.result, "Y", msg="出租合同号：" + contract_numss)

    def test_issue_case_n(self):
        """前承租合同终止结算类型是换租，通过复审,委托已复审，出租已复审,首付款完成。验证生成一条生效的业绩且有核发月份"""
        base.consoleLog("""前承租合同终止结算类型是换租，通过复审,委托已复审，出租已复审,首付款完成。验证生成一条生效的业绩且有核发月份""")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_share(self.apartment_code, self.phone, contract_nums, "2018-02-01", "2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums, "2019-01-31", "退租", contractEndRequest.now_time(-1)))
        base.consoleLog(contractEndRequest.reviewed_apartment_contract_end(contract_nums))
        contract_numss = base.random_name()
        phones = base.add_phone_number()
        base.consoleLog(customerRequest.add_customer("testauto", phones))
        base.consoleLog(contractRequest.add_apartment_contract_share(self.apartment_code, phones, contract_numss, contractEndRequest.now_time(),"2019-01-31"))
        base.consoleLog(contractRequest.reviewed_house_contract(self.contract_num))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_numss))
        base.consoleLog(financeRequest.apartment_contract_collecting_money(contract_numss))
        for i in range(self.for_number):
            self.result = achievementRequest.serach_issue_divide_into_details(contract_numss)
            if self.result["achievementDetail"][0]["accounting_time"] != "":
                self.result = True
                break
            else:
                sleep(self.wait_time)
        self.assertEqual(self.result, True, msg="出租合同号：" + contract_numss)
        base.consoleLog("用例执行完成。预期结果： True  测试结果：" + str(self.result))
        self.result = achievementRequest.serach_issue_state(contract_numss)
        base.consoleLog("用例执行完成。预期结果： Y  测试结果：" + self.result)
        self.assertEqual(self.result, "Y", msg="出租合同号：" + contract_numss)

class IssueAchievementManageShareTestCase(unittest.TestCase):
    """服务合租出单业绩生成用例集合"""

    def setUp(self):
        base.consoleLog("-------------------------服务合租出单业绩生成用例集合strat----------------------")
        self.for_number = 100
        self.wait_time = 1
        base.consoleLog(houseDevelopRequest.add_house_delelop("业绩测试预发专用楼盘", 1))
        self.contract_num = base.random_name()
        base.consoleLog(contractRequest.add_house_contract("业绩测试预发专用楼盘", self.contract_num, "2018-01-01", "服务公寓", "合租", "微改"))
        for i in range(self.for_number):
            try:
                sql = "SELECT contract_num from query_house_contract where contract_num = '%s'" % self.contract_num
                base.searchSQL(sql)[0][0]
                break
            except Exception as e:
                base.consoleLog("委托合同未生成宽表，重新查询数据库。报错信息："+str(e)+ "sql:" + sql,level='e')
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
                sql = 'SELECT apartment_code from apartment where apartment_id = "%s" ' % self.apartment_id
                self.apartment_code = base.searchSQL(sql)[0][0]
                break
            except Exception as e:
                base.consoleLog("房源定价失败或者没有生成自营房源。报错信息"+ str(e))
                sleep(self.wait_time)
                pass

    def tearDown(self):
        base.consoleLog("-------------------------服务合租出单业绩生成用例集合end------------------------")
    def test_issue_case_a(self):
        """已交房.验证业绩核算界面：已交房+已有装修成本打√"""
        base.consoleLog("""已交房.验证业绩核算界面：已交房+已有装修成本打√""")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_share(self.apartment_code, self.phone, contract_nums, "2018-02-01", "2019-01-31"))
        self.result = achievementRequest.serach_issue_node(contract_nums)
        base.consoleLog("用例执行完成。预期结果：Y  测试结果：" + self.result[u"已有装修成本（装修部门已经填写装修成本）"])
        self.assertEqual(self.result[u"已有装修成本（装修部门已经填写装修成本）"],"Y",msg="出租合同号："+contract_nums)

    def test_issue_case_b(self):
        """已交房.验证业绩核算界面：生成了一条未生效的业绩"""
        base.consoleLog("""已交房.验证业绩核算界面：生成了一条未生效的业绩""")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_share(self.apartment_code, self.phone, contract_nums, "2018-02-01","2019-01-31"))
        for i in range(self.for_number):
            self.result = achievementRequest.serach_issue_state(contract_nums)
            if self.result == "N":
                break
            else:
                sleep(self.wait_time)
        base.consoleLog("预期结果：N 测试结果：" + self.result)
        self.assertEqual(self.result, "N", msg="出租合同号：" + contract_nums)

    def test_issue_case_c(self):
        """委托合同已复审.验证业绩核算界面：委托已复审打钩，状态是Y"""
        base.consoleLog("""委托合同已复审.验证业绩核算界面：委托已复审打钩，状态是Y""")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_share(self.apartment_code, self.phone, contract_nums, "2018-02-01", "2019-01-31"))
        base.consoleLog(contractRequest.reviewed_house_contract(self.contract_num))
        self.result = achievementRequest.serach_issue_node(contract_nums)
        base.consoleLog("用例执行完成。预期结果： Y  测试结果：" + self.result[u"委托合同已通过复审"])
        self.assertEqual(self.result[u"委托合同已通过复审"], "Y", msg="出租合同号：" + contract_nums)

    def test_issue_case_d(self):
        """出租合同已复审.验证业绩核算界面：出租已复审打钩，状态是Y"""
        base.consoleLog("""出租合同已复审.验证业绩核算界面：出租已复审打钩，状态是Y""")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_share(self.apartment_code, self.phone, contract_nums, "2018-02-01", "2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        self.result = achievementRequest.serach_issue_node(contract_nums)
        base.consoleLog("用例执行完成。预期结果： Y  测试结果：" + self.result[u"出租合同已通过复审"])
        self.assertEqual(self.result[u"出租合同已通过复审"], "Y", msg="出租合同号：" + contract_nums)

    def test_issue_case_e(self):
        """委托出租已复审.验证业绩核算界面：生成了一条未生效的业绩"""
        base.consoleLog("""委托出租已复审.验证业绩核算界面：生成了一条未生效的业绩""")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_share(self.apartment_code, self.phone, contract_nums, "2018-02-01", "2019-01-31"))
        base.consoleLog(contractRequest.reviewed_house_contract(self.contract_num))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        for i in range(self.for_number):
            self.result = achievementRequest.serach_issue_state(contract_nums)
            if self.result == "Y":
                break
            else:
                sleep(self.wait_time)
        base.consoleLog("用例执行完成。预期结果：Y 测试结果：" + self.result)
        self.assertEqual(self.result,"Y",msg="出租合同号："+contract_nums)

    def test_issue_case_f(self):
        """生效的业绩.收齐首付款。验证业绩核算界面：生成了业绩核发月份"""
        base.consoleLog("""生效的业绩.收齐首付款。验证业绩核算界面：生成了业绩核发月份""")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_share(self.apartment_code, self.phone, contract_nums, "2018-02-01", "2019-01-31"))
        base.consoleLog(contractRequest.reviewed_house_contract(self.contract_num))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(financeRequest.apartment_contract_collecting_money(contract_nums))
        for i in range(self.for_number):
            self.result = achievementRequest.serach_issue_divide_into_details(contract_nums)
            if self.result["achievementDetail"][0]["accounting_time"] != "":
                self.result = True
                break
            else:
                sleep(self.wait_time)
        base.consoleLog("用例执行完成。预期结果：True  测试结果：" + str(self.result))
        self.assertEqual(self.result,True,msg="出租合同号："+contract_nums)

    def test_issue_case_g(self):
        """前承租合同终止结算类型是转租，且已通过复审。验证业绩核算界面：该节点变成Y"""
        base.consoleLog("""前承租合同终止结算类型是转租，且已通过复审。验证业绩核算界面：该节点变成Y""")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_share(self.apartment_code, self.phone, contract_nums, "2018-02-01", "2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums, "2019-01-31", "转租", contractEndRequest.now_time(-1)))
        base.consoleLog(contractEndRequest.reviewed_apartment_contract_end(contract_nums))
        contract_numss = base.random_name()
        phones = base.add_phone_number()
        base.consoleLog(customerRequest.add_customer("testauto", phones))
        base.consoleLog(contractRequest.add_apartment_contract_share(self.apartment_code, phones, contract_numss, contractEndRequest.now_time(),"2019-01-31"))
        self.result = achievementRequest.serach_issue_node(contract_numss)
        base.consoleLog("用例执行完成。预期结果：Y 测试结果： " + self.result[u"前承租合同终止结算已通过复审（针对转租、退租、换租和收房）"])
        self.assertEqual(self.result[u"前承租合同终止结算已通过复审（针对转租、退租、换租和收房）"],"Y",msg="出租合同号："+contract_numss)

    def test_issue_case_h(self):
        """前承租合同终止结算类型是退租，且已通过复审。验证业绩核算界面：该节点变成Y"""
        base.consoleLog("""前承租合同终止结算类型是退租，且已通过复审。验证业绩核算界面：该节点变成Y""")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_share(self.apartment_code, self.phone, contract_nums, "2018-02-01", "2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums, "2019-01-31", "退租", contractEndRequest.now_time(-1)))
        base.consoleLog(contractEndRequest.reviewed_apartment_contract_end(contract_nums))
        contract_numss = base.random_name()
        phones = base.add_phone_number()
        base.consoleLog(customerRequest.add_customer("testauto", phones))
        base.consoleLog(contractRequest.add_apartment_contract_share(self.apartment_code, phones, contract_numss, contractEndRequest.now_time(),"2019-01-31"))
        self.result = achievementRequest.serach_issue_node(contract_numss)
        base.consoleLog("用例执行完成。预期结果：Y  测试结果：" + self.result[u"前承租合同终止结算已通过复审（针对转租、退租、换租和收房）"])
        self.assertEqual(self.result[u"前承租合同终止结算已通过复审（针对转租、退租、换租和收房）"],"Y",msg="出租合同号："+contract_numss)

    def test_issue_case_i(self):
        """前承租合同终止结算类型是换租，且已通过复审。验证业绩核算界面：该节点变成Y"""
        base.consoleLog("""前承租合同终止结算类型是换租，且已通过复审。验证业绩核算界面：该节点变成Y""")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_share(self.apartment_code, self.phone, contract_nums, "2018-02-01", "2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums, "2019-01-31", "换租", contractEndRequest.now_time(-1)))
        base.consoleLog(contractEndRequest.reviewed_apartment_contract_end(contract_nums))
        contract_numss = base.random_name()
        phones = base.add_phone_number()
        base.consoleLog(customerRequest.add_customer("testauto", phones))
        base.consoleLog(contractRequest.add_apartment_contract_share(self.apartment_code, phones, contract_numss, contractEndRequest.now_time(),"2019-01-31"))
        self.result = achievementRequest.serach_issue_node(contract_numss)
        base.consoleLog("用例执行完成。预期结果：Y 测试结果：" + self.result[u"前承租合同终止结算已通过复审（针对转租、退租、换租和收房）"])
        self.assertEqual(self.result[u"前承租合同终止结算已通过复审（针对转租、退租、换租和收房）"],"Y",msg="出租合同号："+contract_numss)

    def test_issue_case_j(self):
        """前承租合同终止结算类型是收房，且已通过复审。验证业绩核算界面：该节点变成Y"""
        base.consoleLog("""前承租合同终止结算类型是收房，且已通过复审。验证业绩核算界面：该节点变成Y""")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_share(self.apartment_code, self.phone, contract_nums, "2018-02-01", "2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums, "2019-01-31", "收房", contractEndRequest.now_time(-1)))
        base.consoleLog(contractEndRequest.reviewed_apartment_contract_end(contract_nums))
        contract_numss = base.random_name()
        phones = base.add_phone_number()
        base.consoleLog(customerRequest.add_customer("testauto", phones))
        base.consoleLog(contractRequest.add_apartment_contract_share(self.apartment_code, phones, contract_numss, contractEndRequest.now_time(),"2019-01-31"))
        self.result = achievementRequest.serach_issue_node(contract_numss)
        base.consoleLog("用例执行完成。预期结果：Y 测试结果：" + self.result[u"前承租合同终止结算已通过复审（针对转租、退租、换租和收房）"])
        self.assertEqual(self.result[u"前承租合同终止结算已通过复审（针对转租、退租、换租和收房）"],"Y",msg="出租合同号："+contract_numss)

    def test_issue_case_k(self):
        """前承租合同终止结算类型是正退，且已通过复审。验证业绩核算界面：无此节点"""
        base.consoleLog("""前承租合同终止结算类型是正退，且已通过复审。验证业绩核算界面：无此节点""")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_share(self.apartment_code, self.phone, contract_nums, "2018-02-01", "2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums, "2019-01-31", "正退", contractEndRequest.now_time(-1)))
        base.consoleLog(contractEndRequest.reviewed_apartment_contract_end(contract_nums))
        contract_numss = base.random_name()
        phones = base.add_phone_number()
        base.consoleLog(customerRequest.add_customer("testauto", phones))
        base.consoleLog(contractRequest.add_apartment_contract_share(self.apartment_code, phones, contract_numss, contractEndRequest.now_time(),"2019-01-31"))
        self.result = achievementRequest.serach_issue_node(contract_numss)
        try:
            self.result[u"前承租合同终止结算已通过复审（针对转租、退租、换租和收房）"]
            self.result = False
        except:
            self.result = True
        base.consoleLog("用例执行完成。预期结果： True  测试结果：" + str(self.result))
        self.assertEqual(self.result,True,msg="出租合同号："+contract_numss)

    def test_issue_case_l(self):
        """前承租合同终止结算类型是收房，未通过复审,委托已复审，出租已复审。验证生成一条未生效的业绩"""
        base.consoleLog("""前承租合同终止结算类型是收房，未通过复审,委托已复审，出租已复审。验证生成一条未生效的业绩""")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_share(self.apartment_code, self.phone, contract_nums, "2018-02-01", "2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums, "2019-01-31", "收房", contractEndRequest.now_time(-1)))
        contract_numss = base.random_name()
        phones = base.add_phone_number()
        base.consoleLog(customerRequest.add_customer("testauto", phones))
        base.consoleLog(contractRequest.add_apartment_contract_share(self.apartment_code, phones, contract_numss, contractEndRequest.now_time(),"2019-01-31"))
        base.consoleLog(contractRequest.reviewed_house_contract(self.contract_num))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_numss))
        for i in range(self.for_number):
            self.result = achievementRequest.serach_issue_state(contract_numss)
            if self.result == "N":
                break
            else:
                sleep(self.for_number)
        base.consoleLog("用例执行完成。预期结果：N  测试结果：" + self.result)
        self.assertEqual(self.result,"N",msg="出租合同号："+contract_numss)

    def test_issue_case_m(self):
        """前承租合同终止结算类型是退租，通过复审,委托已复审，出租已复审。验证生成一条生效的业绩"""
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_share(self.apartment_code, self.phone, contract_nums, "2018-02-01",
                                                      "2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums, "2019-01-31", "退租", contractEndRequest.now_time(-1)))
        base.consoleLog(contractEndRequest.reviewed_apartment_contract_end(contract_nums))
        contract_numss = base.random_name()
        phones = base.add_phone_number()
        base.consoleLog(customerRequest.add_customer("testauto", phones))
        base.consoleLog(contractRequest.add_apartment_contract_share(self.apartment_code, phones, contract_numss,
                                                      contractEndRequest.now_time(), "2019-01-31"))
        base.consoleLog(contractRequest.reviewed_house_contract(self.contract_num))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_numss))
        for i in range(self.for_number):
            self.result = achievementRequest.serach_issue_state(contract_numss)
            if self.result == "Y":
                break
            else:
                sleep(self.wait_time)
        base.consoleLog("用例执行完成。预期结果：Y 测试结果：" + self.result)
        self.assertEqual(self.result, "Y", msg="出租合同号：" + contract_numss)

    def test_issue_case_n(self):
        """前承租合同终止结算类型是换租，通过复审,委托已复审，出租已复审,首付款完成。验证生成一条生效的业绩且有核发月份"""
        base.consoleLog("""前承租合同终止结算类型是换租，通过复审,委托已复审，出租已复审,首付款完成。验证生成一条生效的业绩且有核发月份""")
        contract_nums = base.random_name()
        base.consoleLog(contractRequest.add_apartment_contract_share(self.apartment_code, self.phone, contract_nums, "2018-02-01", "2019-01-31"))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_nums))
        base.consoleLog(contractEndRequest.apartment_contract_end(contract_nums, "2019-01-31", "退租", contractEndRequest.now_time(-1)))
        base.consoleLog(contractEndRequest.reviewed_apartment_contract_end(contract_nums))
        contract_numss = base.random_name()
        phones = base.add_phone_number()
        base.consoleLog(customerRequest.add_customer("testauto", phones))
        base.consoleLog(contractRequest.add_apartment_contract_share(self.apartment_code, phones, contract_numss, contractEndRequest.now_time(),"2019-01-31"))
        base.consoleLog(contractRequest.reviewed_house_contract(self.contract_num))
        base.consoleLog(contractRequest.reviewed_apartment_contract(contract_numss))
        base.consoleLog(financeRequest.apartment_contract_collecting_money(contract_numss))
        for i in range(self.for_number):
            self.result = achievementRequest.serach_issue_divide_into_details(contract_numss)
            if self.result["achievementDetail"][0]["accounting_time"] != "":
                self.result = True
                break
            else:
                sleep(self.wait_time)
        self.assertEqual(self.result, True, msg="出租合同号：" + contract_numss)
        base.consoleLog("用例执行完成。预期结果： True  测试结果：" + str(self.result))
        self.result = achievementRequest.serach_issue_state(contract_numss)
        base.consoleLog("用例执行完成。预期结果： Y  测试结果：" + self.result)
        self.assertEqual(self.result, "Y", msg="出租合同号：" + contract_numss)




if __name__ == "__main__":
    base.host_set("mock")
    contractRequest.get_cookie()
    unittest.main()