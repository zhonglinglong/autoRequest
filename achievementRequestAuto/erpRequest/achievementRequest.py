# -*- coding:UTF-8 -*-

"""
author = crazyzhong
2018年4月12日13:15:44
爱上租业绩查询接口
"""

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from common.interface import *


@log
def serach_issue_node(contract_num):
    """
    查看出租合同业绩节点
    :param contract_num: 出租合同号
    :return: 节点名称+状态
    """
    try:
        sql = "select contract_id from apartment_contract where contract_num = '%s'" % contract_num
        contract_id = searchSQL(sql)[0][0]
    except Exception as e:
        return "查询出租合同返回为空,sql:" + sql + "错误返回："  + str(e)

    try:
        url = "http://isz.ishangzu.com/isz_contract/ApartmentContractController/searchFinishAchievementElement.action"
        data = {"contract_id":contract_id }
        result = myRequest(url,str(data),Value=True)["obj"]["achievementElementList"]
    except Exception as e:
        return  u"查看出租合同业绩接口异常。错误返回：" + str(e)

    #返回字典，key为节点名称，值为Y,N
    Node = {}
    for i in range(len(result)):
        Node[result[i]["descript"]] = result[i]["is_finish"]
    return  Node

@log
def serach_issue_state(contract_num):
    """
    查询出租合同业绩状态 未生效，生效
    :param contract_num: 出租合同
    :return: Y 生效，N未生效
    """
    try:
        sql = "select contract_id from apartment_contract where contract_num = '%s'" % contract_num
        contract_id = searchSQL(sql)[0][0]
    except Exception as e:
        return "查询出租合同返回为空,sql:" + sql + "错误返回：" + str(e)

    try:
        url = "http://isz.ishangzu.com/isz_achievement/ApartmentContractAchievementController/searchApartmentContractAchievementRecord.action"
        data = {"contract_id":contract_id}
        result = myRequest(url,str(data),Value=True)["obj"][0]
    except Exception as e:
        return u"查询出租合同业绩状态报错。错误返回：" + str(e)
    return result["is_active"]

@log
def serach_issue_divide_into_details(contract_num):
    """
    查看出租合同业绩详情
    :param contract_num: 出租合同号
    :return:
    """
    try:
        sql = "select contract_id from apartment_contract where contract_num = '%s'" % contract_num
        contract_id = searchSQL(sql)[0][0]
    except Exception as e:
        return "查询出租合同返回为空,sql:" + sql + "错误返回：" + str(e)

    try:
        sql = "select achievement_id from apartment_contract_achievement where contract_id = '%s'  limit 1" % contract_id
        achievement_id = searchSQL(sql)[0][0]
    except Exception as e:
        return "查询出租合同返回为空,sql:" + sql + "错误返回：" + str(e)

    #查询出租合同业绩详情
    url = "http://isz.ishangzu.com/isz_achievement/ApartmentContractAchievementController/searchAchievement.action"
    data = {"achievement_id":achievement_id,"contract_id":contract_id}
    return myRequest(url, str(data),Value=True)["obj"][0]

@log
def serach_break_details(contract_num):
    """
    查询违约业绩详情
    :param contract_num:终止结算对应的委托合同号
    :return:
    """
    try:
        sql = "select achieve_id from breach_achievement where contract_num = '%s'" % contract_num
        achieve_id = searchSQL(sql)[0][0]
    except Exception as e:
        return "查询出租合同返回为空,sql:" + sql + "错误返回：" + str(e)


    url = "http://isz.ishangzu.com/isz_achievement/ContractAchievementController/searchDefaultAchievement.action"
    data = {"achieve_id":achieve_id}
    return myRequest(url,str(data),Value=True)

@log
def serach_house_contract_loss_details(contract_num):
    """
    查询亏损业绩
    :param contract_num:委托合同号
    :return:
    """

    try:
        sql = 'SELECT loss_achieve_id from house_contract_loss_achievement where house_contract_num = "%s" ' % contract_num
        loss_achieve_id = searchSQL(sql)[0][0]
    except Exception as e:
        return "查询出租合同返回为空,sql:" + sql + "错误返回：" + str(e)

    url = "http://isz.ishangzu.com/isz_achievement/ContractAchievementController/searchVacancyAchievement.action"
    data = {"achieve_id":loss_achieve_id}

    return myRequest(url,str(data),Value=True)

@log
def serach_back_details(contract_num):
    """
    查看扣回业绩详情
    :param:contract_num 出租合同
    :return:
    """
    try:
        sql = 'SELECT achieve_id  from back_achievement where  contract_num = "%s" '  % contract_num
        achieve_id = searchSQL(sql)[0][0]
    except Exception as e:
        return "查询扣回业绩sql报错。错误返回：" + str(e) + "sql:" + sql

    url = "http://isz.ishangzu.com/isz_achievement/ContractAchievementController/searchBackAchievement.action"
    data = {"achieve_id":achieve_id}
    return myRequest(url,str(data),Value=True)
