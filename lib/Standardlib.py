from uuid import uuid4
import urllib2, time
from app import models, db

def create_uuid():
    id_team = str(uuid4()).split("-")
    sort_id = "".join(id_team)
    return sort_id[:16]

def host_ping(host, port):
    url = "http://" + host + ":" + port + "/_ping"
    req = urllib2.Request(url)
    try:
        html = urllib2.urlopen(req,timeout = 1)
        return html.read()
    except:
        return "ERROR"

# The MEM util format
def mem_format(mem):
    if mem >= 1024**3:
        mem = str(mem / (1024**3))+'G'
    elif mem >= 1024**2:
        mem = str(mem / (1024**2))+'M'
    elif mem >= 1024:
        mem = str(mem / 1024)+'K'
    else:
        mem = str(mem)+'B'
    return mem

# Date and time format
def datetime_format(asctime):
    return time.strftime("%Y/%m/%d %H:%M ", time.localtime(asctime))

#wrapped docker.get_container_detail
def makebold(fn):
    def wrapped(self, id):
        html = ""
        for i in fn(self,id):
            tag = '<li><strong style="font-size:15px">%s: </strong><p style="display: inline">%s</p></li>\n' % (i, fn(self,id)[i])
            html += tag
        return html
    return wrapped

def refresh_ping(username):
    hostlist = models.Engine.query.filter_by(user_name = username).all()
    for host in hostlist:
        status = host_ping(host.host, host.port)
        if host.status != status:
            host.status = status
            try:
                db.session.add(host)
                db.session.commit()
            except:
                db.session.rollback()
            finally:
                db.session.commit()

