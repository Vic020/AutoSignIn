#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import re
from flask import Flask, render_template, request, redirect, url_for, flash
from autosignin import asi
app = Flask(__name__)
app.config.from_object('config')


@app.route('/')
@app.route('/index')
def index():
    list_ = asi.list()
    return render_template('index.html', datas=list_)


@app.route('/get')
def get():
    return json.dumps(asi.list())


@app.route('/edit/<webname>')
def edit(webname):
    return render_template('edit.html', data=asi.get(webname))


@app.route('/del/<webname>')
def del_(webname):
    return render_template('del.html', webname=webname)


@app.route('/delconfirm/<webname>')
def delconfirm(webname):
    asi.del_(webname)
    flash(u'%s 删除成功' % webname)
    return redirect(url_for('index'))


@app.route('/set', methods=['POST'])
def set():
    if request.method == 'GET':
        return redirect('/')
    if request.method == 'POST':
        url = request.form['url']
        name = re.findall('[a-zA-Z]://[\w]+.([\w]+).', url)[0]
        method = request.form['method']
        data = request.form['data']
        cookies = request.form['cookies']
        if name in asi.data.sections():
            list_ = asi.get(name)
            if list_['url'] != url:
                asi.setSignInUrl(name, url)
                flash(u'%s url已修改' % name)
            if list_['data'] != data:
                asi.setData(name, data)
                flash(u'%s data已修改' % name)
            if list_['cookies'] != cookies:
                asi.setCookies(name, cookies)
                flash(u'%s cookies已修改' % name)
            if list_['method'] != method:
                asi.setMethod(name, method)
                flash(u'%s method已修改' % name)
        else:
            asi.add(name, url, method, cookies, data)
            flash(u'添加成功')
        return redirect(url_for('index'))
