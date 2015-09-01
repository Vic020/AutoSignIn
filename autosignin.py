#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import re
import logging
from utils import VicConfigParser


class AutoSignIn():
    def __init__(self):
        self.filename = 'autosignin'
        self.data = VicConfigParser(self.filename)
        self._initLog()

    def _initLog(self):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(filename)s[line:\
                            %(lineno)d] %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename='autosignin.log',
                            filemode='w')

    def _getHeaders(self):
        headers = {}
        headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) App\
                                leWebKit/537.36 (KHTML, like Gecko) Chro\
                                me/39.0.2171.95 Safari/537.36'
        #headers['Host'] = ''
        headers['Connection'] = 'keep-alive'
        headers['Cache-Control'] = 'max-age=0'
        headers['Accept-Language'] = 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4'
        headers['Accept-Encoding'] = 'gzip'
        headers['Accept'] = 'text/html,application/xhtml+xml,\
                             application/xml;q=0.9,image/webp,*/*;q=0.8'
        return headers

    def _getData(self, webname):
        data = {}
        for d in self.data.get('data', webname).split('&'):
            k, v = d.strip().split('=', 1)
            data[k] = v
        if data.has_key('todaysay'):
            data['todaysay'] = u'签到，大家好！'
        return data

    def _getCookies(self, webname):
        cookies = {}
        for d in self.data.get('cookies', webname).split(';'):
            k, v = d.strip().split('=', 1)
            cookies[k] = v
        return cookies

    def signOneIn(self, webname):
        headers = self._getHeaders()
        data = self._getData(webname)
        cookies = self._getCookies(webname)
        url = self.data.get('url', webname)
        res = ''
        if self.data.get('method', webname) == 'POST':
            res = requests.post(url,
                                headers=headers,
                                data=data,
                                cookies=cookies)
        else:
            res = requests.get(url,
                               headers=headers,
                               data=data,
                               cookies=cookies)
        return res.text
        

    def signIn(self, webname):
        headers = self._getHeaders()
        data = self._getData(webname)
        cookies = self._getCookies(webname)
        url = self.data.get('url', webname)
        res = ''
        if self.data.get('method', webname) == 'POST':
            res = requests.post(url,
                                headers=headers,
                                data=data,
                                cookies=cookies)
        else:
            res = requests.get(url,
                               headers=headers,
                               data=data,
                               cookies=cookies)
        return self._ProcessResult(webname, res.text)

    def _ProcessResult(self, webname, html):
        '''
        100: 签到成功
        200: 未知错误
        201：表单错误
        202：cookie失效
        203: 已经签到
        '''
        logging.info(html)
        if len(re.findall(u'您的今日想说内容忘了填', html)) > 0:
            return u'请在data上的todaysay等号后加上%E7%AD%BE%E5%88%B0%EF%BC%8C%E5%A4%A7%E5%AE%B6%E5%A5%BD%EF%BC%81'
        elif len(re.findall(u'你选择的心情不正确', html)) > 0:
            return u'请在data上加上 &qdxq=kx'
        if len(re.findall(u'签到成功!', html)) > 0:
            return u'恭喜你签到成功!'
        elif len(re.findall(u'签到完毕', html)) > 0:
            return u'今日已经签到!'
        elif len(re.findall(u'已经签到', html)) > 0:
            return u'今日已经签到'
        elif len(re.findall(u'<div class="c">([\w\W]+)</div>', html)) > 0:
            return re.findall(u'<div class="c">([\w\W]+)</div>', html)[0]
        # elif len(re.findall(u'', html)) > 0:
        #     return 201
        # elif len(re.findall(u'', html)) > 0:
        #     return 202
        else:
            logging.warning(html)
            return u'暂时未匹配,请到网页查看是否签到'

    def list(self):
        list_ = []
        for section in self.data.sections():
            tmp = {}
            tmp['webname'] = section
            tmp['status'] = self.signIn(section)
            #tmp['status'] = u'测试状态'
            for key in self.data.keys(section):
                tmp[key] = self.data.get(key, section)
            list_.append(tmp)
        return list_

    def get(self, webname):
        list_ = {}
        for key in self.data.keys(webname):
            list_[key] = self.data.get(key, webname)
        return list_

    def setCookies(self, webname, webcookies):
        self.data.set('cookies', webcookies, webname)

    def setSignInUrl(self, webname, weburl):
        self.data.set('url', weburl, webname)

    def setData(self, webname, webdata):
        self.data.set('data', webdata, webname)

    def setMethod(self, webname, webmethod):
        self.data.set('method', webmethod, webname)

    def add(self, webname, weburl, webmethod, webcookies, webdata):
        self.data.set('method', webmethod, webname)
        self.setSignInUrl(webname, weburl)
        self.setData(webname, webdata)
        self.setCookies(webname, webcookies)

    def del_(self, webname):
        self.data.delsection(webname)


asi = AutoSignIn()
