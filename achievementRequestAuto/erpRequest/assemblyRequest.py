# -*- coding:UTF-8 -*-

"""
author = crazyzhong
2018年4月10日17:35:32
爱上租ERP组件接口,如 solr，ES,
"""

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from common.interface import *

@log
def solr(core, condition="mock"):
    """
    房源的solr增量或者全量
    :param core: 目前为house或者apartment
    :param condition: test或者mock
    :return: 执行结果
    """
    url = {
        'house': {
            'test': 'http://192.168.0.216:8080/solr/house_core/dataimport',
            'mock': 'http://192.168.0.216:8080/solr/apartment_core/dataimport'
        },
        'apartment': {
            'test': 'http://192.168.0.203:8080/solr/house_core/dataimport',
            'mock': 'http://192.168.0.203:8080/solr/apartment_core/dataimport'
        }
    }
    data = 'command=delta-import&commit=true&wt=json&indent=true&verbose=false&clean=false&optimize=false&debug=false'
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'
    }

    try:
        re = requests.post(url[core][condition], data, headers=headers)
    except Exception as e:
        return "solr接口查询异常。错误返回：" + str(e)

    if re.status_code is 200:
        return "执行" + core +"solr增量成功！"
    else:
        return "执行" + core +"solr增量失败！ 错误返回：" + str(re.text)

@log
def ES_house_contract(number = -1):
    """
    ES委托合同列表数据更新
    :param number:
    :return:
    """

    url = "http://isz.ishangzu.com/isz_base/EsController/update.action"
    data = {"time":now_time(number)+" 00:00:01","index":"house_contract_type"}
    result = myRequest(url,str(data),Value=True)
    if result["code"] == 0:
        return "委托合同列表ES数据查询完成"
    else:
        return "委托合同列表ES数据查询异常,接口返回:" + result


@log
def ES_apartment_contract(number = -1):
    """
    ES出租合同列表数据更新
    :param number:
    :return:
    """
    url = "http://isz.ishangzu.com/isz_base/EsController/update.action"
    data = {"time": now_time(number)+" 00:00:01", "index": "apartment_contract_type"}
    result = myRequest(url, str(data), Value=True)
    if result["code"] == 0:
        return "出租合同列表ES数据查询完成"
    else:
        return "出租合同列表ES数据查询异常,接口返回:" + result


