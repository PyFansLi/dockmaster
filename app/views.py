# -*- coding:UTF-8 -*-
from app import app, models, db
from flask import render_template, request, session, redirect, url_for
from werkzeug.security import check_password_hash
from lib.Dockerlib import DOCKER
from lib import Standardlib
from api.functions import *

@app.route('/')
@app.route('/index')
def index():
    return "hello"

@app.route('/login', methods = ['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username',None)
        password = request.form.get('password', None)
        auth = models.User.query.filter_by(username = username).first()
        if auth and check_password_hash(auth.password, password):
            session['login_in'] = True
            session['username'] = auth.username
            return redirect(url_for("overview"))
        else:
            error = "Error 401, Authentication failed"
    return render_template('login.html', error = error)

@app.route('/logout')
def logout():
    try:
        session.pop('loggin_in')
        session.pop('username')
    except:
        None
    return redirect('/login')

@app.route('/overview')
def overview():
    if session.get('login_in',None):
        returndata = []
        Standardlib.refresh_ping(username = session['username'])
        hostlist = models.Engine.query.filter_by(user_name = session['username']).all()
        for host in hostlist:
            data = {}
            data['uuid'] = host.uuid
            data['hostname'] = host.hostname
            data['host'] = host.host
            data['port'] = host.port
            data['status'] = host.status
            data['username'] = host.user_name
            data['timestamp'] = host.timestamp
            returndata.append(data)
        return render_template('overview.html', hostlist = returndata, username = session['username'])
    else:
        return redirect('/login')

@app.route("/engine")
def engine():
    if session.get('login_in',None):
        if session.get('username',None):
            if request.values.get('uuid',None):
                uuid = request.values['uuid']
                session['uuid'] = uuid
            else:
                uuid = session['uuid']
            username = session['username']
            try:
                engine = models.Engine.query.filter_by(uuid = uuid, user_name = username).first()
                base_url = "tcp://" + engine.host + ":" + engine.port
                docker = DOCKER(base_url = base_url, timeout = 5, version = "auto")
                return render_template('engine.html', host_info = docker.get_info(), usage = docker.monitor())
            except:
                return "操作失败,服务无法完成你的请求", 503

        else:
            return "Error 401, Authentication failed", 401
    else:
        return redirect('/login')

@app.route("/image")
def image():
    if session.get('login_in',None):
        if session.get('username',None):
            try:
                uuid = session['uuid']
                username = session['username']
                engine = models.Engine.query.filter_by(uuid = uuid, user_name = username).first()
                base_url = "tcp://" + engine.host + ":" + engine.port
                docker = DOCKER(base_url = base_url, timeout = 5, version = "auto")
                return render_template('image.html', image_list = docker.get_images())
            except:
                return "操作失败,服务无法完成你的请求", 503
        else:
            return "Error 401, Authentication failed", 401
    else:
        return redirect('/login')

@app.route("/container")
def container():
    if session.get('login_in',None):
        if session.get('username',None):
            try:
                uuid = session['uuid']
                username = session['username']
                engine = models.Engine.query.filter_by(uuid = uuid, user_name = username).first()
                base_url = "tcp://" + engine.host + ":" + engine.port
                docker = DOCKER(base_url = base_url, timeout = 5, version = "auto")
                return render_template('container.html', container_list = docker.get_containers())
            except:
                return "操作失败,服务无法完成你的请求", 503
        else:
            return "Error 401, Authentication failed", 401
    else:
        return redirect('/login')

