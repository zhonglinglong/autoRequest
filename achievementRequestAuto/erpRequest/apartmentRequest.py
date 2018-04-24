# -*- coding:UTF-8 -*-

"""
author = crazyzhong
2018年4月10日17:41:05
爱上租ERP自营房源接口
"""

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from common.interface import *

@log
def apartment_price_entire(contract_num,rent_price="8000"):
    """
    自营房源整租定价
    :param contract_num:委托合同号
    :param rent_price: 价格
    :return: obj
    """
    try:
        sql = 'SELECT apartment_id from apartment where house_id = (SELECT house_id from house_contract where contract_num ="%s") limit 1 ' % contract_num
        apartment_id = searchSQL(sql)[0][0]
    except Exception as e:
        return "查询出租合同返回为空,sql:" + sql + "错误返回：" + str(e)

    try:
        url = "http://erp.ishangzu.com/isz_house/ApartmentController/confirmApatmentRentPricing.action"
        data = {"apartment_id":apartment_id,"rent_price":rent_price}
        myRequest(url,str(data),Value=True)
        return "自营房源整租定价成功。委托合同号：" + contract_num + "。整租价格：" + rent_price
    except Exception as e:
        return "自营房源整租定价异常。错误返回：" + str(e)


@log
def apartment_price_share(contract_num,rent_price):
    """
    自营房源合租定价
    :param contract_num:委托合同号
    :param rent_price:列表
    :return:
    """
    try:
        sql = 'SELECT apartment_id from apartment where house_id = (SELECT house_id from house_contract where contract_num ="%s") limit 1 ' % contract_num
        apartment_id = searchSQL(sql)[0][0]
    except Exception as e:
        return "查询自营公寓返回为空,sql:" + sql + "错误返回：" + str(e)

    #查询合租房间信息
    try:
        url = "http://erp.ishangzu.com/isz_house/ApartmentController/searchShareApartment.action"
        data = {"apartment_id":apartment_id}
        result = myRequest(url,str(data),Value=True)
    except Exception as e:
        return "查询自营房源房间数量异常。错误返回：" +  str(e)

    # 出租合同定价
    data = result["obj"]
    for i in range(len(data)):
        data[i]['canEdit'] = True
        data[i]['rent_price'] = str(rent_price[i])

    #自营公寓合租定价
    try:
        url = "http://erp.ishangzu.com/isz_house/ApartmentController/confirmPricing.action"
        result = myRequest(url,str(data),Value=True)
        return "自营房源合租定价成功。委托合同号：" + contract_num + "。合租该房间价格：" + str(rent_price[0])
    except Exception as e:
        return "自营公寓合租定价异常。错误返回：" +  str(e) + "接口返回：" +  str(result["obj"])


@log
def apartment_fire_calculate(apartmentId):
    """
    着火定时器，个人手动生成。
    :param apartmentId:
    :return:
    """
    url = "http://isz.ishangzu.com/isz_contract/ApartmentContractController/fireLossAchievement.action"
    data = {"apartmentId":apartmentId,"type":"ALL"}
    return myRequest(url,str(data),Value=True)
