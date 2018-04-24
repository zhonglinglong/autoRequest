#-*- coding:utf-8 -*-

'''
Created on 2018年4月10日17:13:57
@author: zhonglinglong
此模块为公共类方法
'''

import ConfigParser
import pymysql
from xlrd import open_workbook
import os,re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header
import smtplib,datetime,random
import logging
import time

log_name = time.strftime('%Y-%m-%d',time.localtime(time.time()))
logger = logging.getLogger('mylogger')
logger.setLevel(logging.DEBUG)
path = os.path.dirname(
    os.path.join(
        os.path.split(
            os.path.realpath(__file__))[0])) + '\\autotest%s.log' % str(log_name)
fileHandler = logging.FileHandler(path)
consoleHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(process)s - %(levelname)s : %(message)s')
fileHandler.setFormatter(formatter)
consoleHandler.setFormatter(formatter)
logger.addHandler(fileHandler)
logger.addHandler(consoleHandler)

currentDriver = None


def log(func):
    def wrapper(*args, **kwargs):
        info = func.__name__
        logger.info('调用函数名称 : %s' % info.decode('utf-8'))
        try:
            return func(*args, **kwargs)
        except BaseException:
            if currentDriver:
                fileName = 'D:\\errorImage\\%s-%s.png' % (
                    info.decode('utf-8'), time.strftime('%H%M%S'))
                currentDriver.driver.save_screenshot(fileName)
                currentDriver.driver.quit()
            logger.exception('Exception')
            # caseID = func.func_name.split('_')[-1]
            # caseInfo = get_yaml(int(caseID))
            # consoleLog('\n' + caseInfo) if caseInfo != '' else None
            consoleLog(func.__name__, level='e', fromAssert=False)
        finally:
            currentDriver.driver.quit() if currentDriver else None
    return wrapper


def consoleLog(msg, level='i', fromAssert=True):
    """
    对错误的记录，写进log文件中，对于error级别的适用于断言，如存在这种用例：删除合同后，判断合同表中的deleted的字段是否为1或者再查询，是否还能查到，此时，如果不为1或者还能查到
    则调用此方法，定义为error级别
    :param msg: 需要写入的描述，如’合同删除后deleted未变成0‘
    :param level: 定义日志级别，分为i:info  w:warning  e:error
    """
    if level is 'i':
        logger.info(msg)
    elif level is 'w':
        logger.warning(msg)
    elif level is 'e':
        if fromAssert:
            logger.error('one assert at : \n%s\n' % msg)
        else:
            logger.error('======================================== one error at "%s" ========================================' % msg)


def get_conf(section, option, valueType=str):
    """
    获取配置文件值
    :param section: 配置文件的片段
    :param option: 配置文件对应的key
    :param valueType: 默认值
    :return:
    """
    config = ConfigParser.ConfigParser()
    path = os.path.join(os.path.split(os.path.realpath(__file__))[0]) + '\conf.ini'
    config.read(path)
    if valueType is str:
        value = config.get(section, option)
        return value
    elif valueType is int:
        value = config.getint(section, option)
        return value
    elif valueType is bool:
        value = config.getboolean(section, option)
        return value
    elif valueType is float:
        value = config.getfloat(section, option)
        return value

    else:
        value = config.get(section, option)
        return value.decode('utf-8')

def set_conf(section, **value):
    """
    写入值到配置文件中
    :param section: 配置文件中的片段名称
    :param value: 配置文件中的key
    :return:
    """
    config = ConfigParser.ConfigParser()
    path = os.path.join(os.path.split(os.path.realpath(__file__))[0]) + '\conf.ini'
    config.read(path)
    for k,v in value.items():
        if type(v) is unicode:
            config.set(section,k,v.encode('utf-8'))
        else:
            config.set(section, k, v)
    config.write(open(path, 'w'))

def get_count(sql):
    """返回查询数量"""
    count = sqlCursor.execute(sql)
    return count

def get_xlrd(xls_name,xls_sheet,value=False):
    """
    :param xls_name: 用例表格名称
    :param xls_sheet: 用例表格页签名称
    :return:
    """
    "read xled"
    cls = []
    xlsPath = os.path.join(get_conf("caseroute","path"), "caseFile",  xls_name)
    file = open_workbook(xlsPath)
    sheets = file.sheet_by_name(xls_sheet)
    nrows = sheets.nrows
    if value:
        for i in range(nrows):
            if nrows - i > 1:
                cls.append(sheets.row_values(i+1))
    else:
        for i in range(nrows):
            cls.append(sheets.row_values(i))
    return cls

def host_set(condition):
    """
    插入地址到本地hosts
    :param condition: 预发还是测试环境的标识
    :return:
    """
    set_conf('testCondition', test=condition)
    filepath = r'C:\Windows\System32\drivers\etc\hosts'
    hosts = None
    f = open(filepath, 'w')
    if condition == 'test':
        set_conf('db', host='192.168.0.208', user='sizhenzhen', password='szz.666', db='isz_erp_npd', charset='utf8')
        set_conf('dbservice', host='192.168.0.208', user='sizhenzhen', password='szz.666', db='isz_rsm', charset='utf8')
        set_conf('decoration', host='192.168.0.208', user='sizhenzhen', password='szz.666', db='isz_decoration_test',charset='utf8')
        hosts = get_conf('host','test')
    elif condition == 'mock':
        set_conf('db', host='192.168.0.208', user='sizhenzhen', password='szz.666', db='isz_erp', charset='utf8')
        set_conf('dbservice', host='192.168.0.208', user='sizhenzhen', password='szz.666', db='isz_rsm_pre', charset='utf8')
        set_conf('decoration', host='192.168.0.208', user='sizhenzhen', password='szz.666', db='isz_decoration', charset='utf8')
        hosts = get_conf('host','mock')
    f.write(hosts)
    f.close()

def send_email(path):
    """
    发送邮件
    :return:
    """

    msg = MIMEMultipart()
    html = MIMEApplication(open(path[0], 'rb').read())
    html.add_header('Content-Disposition', 'attachment', filename=path[0])
    msg.attach(html)

    text = MIMEApplication(open(path[1], 'rb').read())
    text.add_header('Content-Disposition', 'attachment', filename=path[1])
    msg.attach(text)

    user = 'zhonglinglong@ishangzu.com'
    pwd = 'Long268244'
    smtp_server = 'smtp.mxhichina.com'
    time = str(datetime.date.today() - datetime.timedelta(days=1))
    msg['From'] = '爱上租-技术部-内部产品测试组-钟玲龙<%s>' % user
    msg['Subject'] = Header('%s业绩接口自动化测试报告' % time, 'utf-8').encode()
    to_addr = ['zhonglinglong@ishangzu.com']
    msg['To'] = ('zhonglinglong<%s>' % (to_addr[0]))
    msg['From'] = user
    server = smtplib.SMTP(smtp_server, 25)
    server.login(user, pwd)
    server.sendmail(user, to_addr, msg.as_string())
    server.quit()

def re_search(res,value):
    """
    校验输入日期是否满足规则，后期如果需要其他校验，也可以写入
    :param res: 正则表达式
    :param value:
    :return:
    """
    pattern = re.compile(res)
    if type(value) == str:
        return pattern.match(value)
    else:
        value = str(value)
        return pattern.match(value)

def empty_dict_null(dict,Value=True):
    """
    删除字典中的指定值
    :param dict:
    :return:
    """
    for k,v in dict.items():
        if Value:
            if v == None:
                del dict[k]
        else:
            if v == None or v == "":
                del dict[k]
    return dict

def add_phone_number():
    """
    随机生成电话号码
    :return: 返回手机号码
    """
    prelist = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150", "151", "152",
               "153", "155", "156", "157", "158", "159", "186", "187", "188"]
    id_card = random.choice(prelist) + "".join(random.choice("0123456789") for i in range(8))
    return id_card

def now_time(day=0):
    """
    返回年月日
    :param day: 与当前日期累加，可正负
    :return:
    """
    Time = str(datetime.date.today() + datetime.timedelta(days=day))
    return Time

def random_name():
    """
    随机名称
    :return:zll+当前年月日+3个字母+3个数字
    """
    name = "zll" + now_time()+"".join(random.choice("qwertyuiopasdfghjklzxcvbnm") for i in range(3))+"".join(random.choice("0123456789") for i in range(3))
    return name

def searchSQL(sql,db="db",type='tuple'):
    """
    查询sql
    :param sql: sql语句
    :param db: 数据库名称，默认是erp的
    :param type: 返回类型选择，默认为元组
    :return:
    """
    sqlConn = pymysql.connect(host=get_conf(db, 'host'), user=get_conf(db, 'user'),
                              password=get_conf(db, 'password'), db=get_conf(db, 'db'),
                              charset=get_conf(db, 'charset'), port=get_conf(db, 'port', int))
    sqlCursor = sqlConn.cursor()
    sqlCursor.execute(sql)
    if type == 'list':
        value = map(lambda x:x[0].encode('utf-8'),sqlCursor.fetchall())
        return value
    if type == 'dict':
        value = {}
        data = sqlCursor.fetchall()
        for i in data:
            try:
                value[i[0].encode('utf-8')] = i[1].encode('utf-8')
            except:
                value[i[0]] = str(i[1])
        return value
    if type == 'tuple':
        value = sqlCursor.fetchall()
        return value

def updateSQL(sql,db="db"):
    sqlConn = pymysql.connect(host=get_conf(db, 'host'), user=get_conf(db, 'user'),
                              password=get_conf(db, 'password'), db=get_conf(db, 'db'),
                              charset=get_conf(db, 'charset'), port=get_conf(db, 'port', int))
    sqlCursor = sqlConn.cursor()

    try:
        # 执行SQL语句
        sqlCursor.execute(sql)
        # 提交到数据库执行
        sqlConn.commit()
    except:
        # 发生错误时回滚
        sqlConn.rollback()

    # 关闭数据库连接
    sqlConn.close()
