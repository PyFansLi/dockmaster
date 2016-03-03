# -*- coding:UTF-8 -*-
from app import app, models, db
from flask import render_template, request, session, redirect, url_for, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from lib.Dockerlib import DOCKER
from lib import Standardlib

@app.route('/registry', methods = ['GET', 'POST'])
def registry():
    if request.method == 'POST':
        user_id = Standardlib.create_uuid()
        username = request.form.get('username',None)
        password = request.form.get('password', None)
        email = request.form.get('email', None)
        try:
            newuser = models.User(uuid = user_id, username = username, 
                                    password = generate_password_hash(password),
                                    email = email, timestamp = datetime.utcnow())
            db.session.add(newuser)
            db.session.commit()
            return jsonify(result="sucessfull")
        except:
            return jsonify(result = "failed")
        finally:
            db.session.close()
    return redirect('login')

@app.route("/change_passwd")
def change_passwd():
    if session.get('login_in',None):
        if session.get('username',None):
            oldpassword = request.values['oldpassword']
            newpassword = request.values['newpassword']
            try:
                user = models.User.query.filter_by(username = session['username']).first()
                if check_password_hash(user.password, oldpassword):
                    user.password = generate_password_hash(newpassword)
                    db.session.add(user)
                    db.session.commit()
                    return jsonify(result="change sucessfull")
                else:
                    return jsonify(result="change failed")
            except:
                db.session.rollback()
                return jsonify(result="change failed")
            finally:
                db.session.close()
        else:
            return redirect('/login')
    else:
        return redirect('/login')

@app.route('/_add_host', methods = ['POST'])
def _add_host():
    if session.get('login_in',None):
        if session.get('username',None):
            if request.method == 'POST':
                auth = models.User.query.filter_by(username = session['username']).first()
                hostname = request.form.get("hostname", None)
                host = request.form.get("host", None)
                port = request.form.get("port", None)
                status = Standardlib.host_ping(host, port)
                try:
                    newhost = models.Engine(uuid = Standardlib.create_uuid(),
                                            hostname = hostname,
                                            host = host,
                                            port = port,
                                            status = status,
                                            timestamp = datetime.utcnow(),
                                            user = auth)
                    db.session.add(newhost)
                    db.session.commit()
                except:
                    return "操作失败,服务无法完成你的请求", 503
                finally:
                    db.session.close()
        return redirect('/overview')
    else:
        return redirect('/login')

@app.route('/_del_host', methods = ['POST'])
def _del_host():
    if session.get('login_in',None):
        if session.get('username',None):
            if request.method == 'POST':
                uuid = request.form['uuid']
                username = session['username']
                try:
                    engine = models.Engine.query.filter_by(uuid = uuid, user_name = username).first()
                    db.session.delete(engine)
                    db.session.commit()
                    return jsonify(result="sucessfull_delete")
                except:
                    return jsonify(result="failed_delete")
                finally:
                    db.session.close()
        else:
            return "Error 401, Authentication failed", 401
    else:
        return redirect('/login')

@app.route("/_create_container", methods = ['POST'])
def _create_container():
    if session.get('login_in',None):
        if session.get('username',None):
            if request.method == 'POST':
                uuid = session['uuid']
                username = session['username']
                engine = models.Engine.query.filter_by(uuid = uuid, user_name = username).first()
                base_url = "tcp://" + engine.host + ":" + engine.port
                docker = DOCKER(base_url = base_url, timeout = 5, version = "auto")
                image = request.form.get('image',)
                name = request.form.get('name',None)
                hostname = request.form.get('name',None)
                int_port = request.form.get('int_port',None)
                ext_port = request.form.get('ext_port',None)
                int_path = request.form.get('int_path',None)
                ext_path = request.form.get('ext_path',None)
                command = request.form.get('command',None)
                docker.new_container(image = image, name = name, hostname = hostname,
                                    int_port = int_port, ext_port = ext_port,
                                    int_path = int_path, ext_path = ext_path,
                                    command = command
                                    )
                return redirect('/container')
        else:
            return "Error 401, Authentication failed", 401
    else:
        return redirect('/login')

@app.route("/_del_image", methods = ['POST'])
def _del_image():
    if session.get('login_in',None):
        if session.get('username',None):
            if request.method == 'POST':
                uuid = session['uuid']
                username = session['username']
                engine = models.Engine.query.filter_by(uuid = uuid, user_name = username).first()
                base_url = "tcp://" + engine.host + ":" + engine.port
                docker = DOCKER(base_url = base_url, timeout = 5, version = "auto")
                repotag = request.form.get('repotag')
                docker.delete_image(repotag)
                return redirect("/image")
        else:
            return "Error 401, Authentication failed", 401
    else:
        return redirect('/login')

@app.route('/_container_detail')
def _container_detail():
    if session.get('login_in',None):
        if session.get('username',None):
            uuid = session['uuid']
            username = session['username']
            container_id = request.values['id']
            engine = models.Engine.query.filter_by(uuid = uuid, user_name = username).first()
            base_url = "tcp://" + engine.host + ":" + engine.port
            docker = DOCKER(base_url = base_url, timeout = 5, version = "auto")
            html = docker.get_container_detail(container_id)
            return jsonify(result = html)
        else:
            return "Error 401, Authentication failed", 401
    else:
        return redirect('/login')

@app.route('/_container_action')
def _container_action():
    if session.get('login_in',None):
        if session.get('username',None):
            uuid = session['uuid']
            username = session['username']
            container_id = request.values['id']
            action = request.values['action']
            engine = models.Engine.query.filter_by(uuid = uuid, user_name = username).first()
            base_url = "tcp://" + engine.host + ":" + engine.port
            docker = DOCKER(base_url = base_url, timeout = 10, version = "auto")
            try:
                if action == 'boot':
                    docker.start_container(container_id)
                elif action == 'stop':
                    docker.stop_container(container_id)
                elif action == 'reboot':
                    docker.reboot_container(container_id)
                elif action == 'pause':
                    docker.pause_container(container_id)
                elif action == 'unpause':
                    docker.recover_container(container_id)
                elif action == 'kill':
                    docker.kill_container(container_id)
                elif action == 'delete':
                    docker.delete_container(container_id)
                return redirect('/container')
            except:
                return "请求超时,timeout", 408
        else:
            return "Error 401, Authentication failed", 401
    else:
        return redirect('/login')