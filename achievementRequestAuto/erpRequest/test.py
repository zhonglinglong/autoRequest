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
from erpRequest import contractRequest
from erpRequest import  decorationRequest
from erpRequest import assemblyRequest
from erpRequest import apartmentRequest
from erpRequest import customerRequest
from erpRequest import contractEndRequest
from erpRequest import achievementRequest
from time import sleep
import time

host_set("mock")
get_cookie()
contract_num = random_name()
print contract_num
print contractRequest.add_house_contract("业绩测试预发专用楼盘", contract_num, "2018-01-01", "服务公寓", "整租", "微改")
sql = 'UPDATE house_contract set create_time = "2018-01-01 15:13:43" where contract_num ="%s"' % contract_num
sleep(2)
#print decorationRequest.add_delivered_house(contract_num)
print updateSQL(sql)
sleep(5)
sql = 'SELECT apartment_id from apartment where house_id =  (SELECT house_id from house_contract where contract_num = "%s") ' % contract_num
apartment_id = searchSQL(sql)[0][0]
sleep(2)
print contractRequest.reviewed_house_contract(contract_num)
print apartment_id
print apartmentRequest.apartment_price_entire(contract_num)
sleep(2)
print apartmentRequest.apartment_fire_calculate(apartment_id)
