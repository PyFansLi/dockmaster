#!/usr/bin/python
#-*- coding:UTF-8 -*-
from docker import Client
from Standardlib import mem_format, datetime_format
import Standardlib

class DOCKER(Client):
    def monitor(self):
        redata = {}
        redata["containers_all"] = len(self.containers(quiet=True,all=True))
        redata["containers"] = len(self.containers(quiet=True))
        redata["images"] = len(self.images(quiet=True))
        redata["store_rate"] = self.store_usage()
        return redata

    # Get the system info    
    def get_info(self):
        host_info = {}
        infos = self.info()
        for k, v in infos.items():
            if k in ['Name', 'KernelVersion', 'ServerVersion', 'OperatingSystem', 'MemTotal',
                    'NCPU', 'Driver', 'OomKillDisable', 'IPv4Forwarding', 'DockerRootDir',]:
                host_info[k] = v
            elif k == 'DriverStatus':
                for i in v:
                    if 'Data Space Total' in i[0]:
                        host_info[i[0]] = i[1]
        return host_info
        
    # Get the images info
    def get_images(self):
        imgs = self.images()
        image_list = []
        for i in imgs:
            for t in i['RepoTags']:
                print t
                repotag = "".join(t)
                data = repotag.split(':')
                data.append(i['Id'][:12])
                data.append(datetime_format(i['Created']))
                data.append(mem_format(i['VirtualSize']))
                image_list.append(data)
        return image_list

    # Remove image
    def delete_image(self, id):
        self.remove_image(id)

    # Save_image, next version support
    def save_image(self, id, path):
        image = self.get_image(id)
        image_tar = open(path, 'w')
        image_tar.write(image.data)
        image_tar.close()

    # Create a new container
    def new_container(self, image, name, hostname, ext_port = None, 
                        int_port = None, ext_path = None,
                        int_path = None, command = None):
        if int_port and ext_port:
            port_bindings = {int(int_port):int(ext_port)}
        else:
            port_bindings = {}
        if ext_path and int_path:
            binds = {ext_path:{'bind':int_path, "mode": "rw"}}
        else:
            binds = {}
        host_config = self.create_host_config( port_bindings = port_bindings, binds = binds)

        new_container = self.create_container(image = image,
                                                name = name,
                                                hostname = hostname,
                                                host_config = host_config,
                                                command = command
                                            )
        self.start(new_container)

    # Get the containers info
    def get_containers(self):
        container_list = self.containers(all=True)
        result = []
        for container in container_list:
            redata = {}
            redata['name'] = container['Names'][0][1::]
            redata['id'] = container['Id'][:12]
            redata['image'] = container['Image']
            redata['created'] = datetime_format(container['Created'])
            redata['status'] = container['Status']
            result.append(redata)
        return result

    # Start container
    def start_container(self, id):
        self.start(id)
    # Stop container    
    def stop_container(self, id):
        self.stop(id)

    # Restart container    
    def reboot_container(self, id):
        self.restart(id)

    # Pasue container
    def pause_container(self, id):
        self.pause(id)

    # Unpuse container    
    def recover_container(self, id):
        self.unpause(id)


    # Kill container    
    def kill_container(self, id):
        self.kill(id)

    # Delete container    
    def delete_container(self, id):
        self.remove_container(id, force = True)

    # Get the container detail infomation
    @Standardlib.makebold
    def get_container_detail(self, id):
        redata = {}
        mappports = []
        mapvolumes = []
        detail = self.inspect_container(id)
        redata['name'] = detail['Name'][1::]
        redata['hostname'] = detail['Config']['Hostname']
        redata['networkmode'] = detail['HostConfig']['NetworkMode']
        redata['macaddress'] = detail['NetworkSettings']['MacAddress']
        redata['ipaddress'] = detail['NetworkSettings']['IPAddress']
        redata['gateway'] = detail['NetworkSettings']['Gateway']
        redata['entrypoint'] = detail['Config']['Entrypoint']
        if detail['Config']['Cmd']:
            redata['cmd'] =  "".join(detail['Config']['Cmd'])
        else:
            redata['cmd'] = detail['Config']['Cmd']
        redata['status'] = detail['State']['Status']
        redata['pid'] = detail['State']['Pid']

        ports = detail['NetworkSettings'].get('Ports', None)
        if ports:
            for i in ports:
                if ports[i] is not None:
                    mappports.append(ports[i][0]['HostIp']+':'+ports[i][0]['HostPort']+'->'+i)
        redata['ports'] = mappports

        volumes = detail['HostConfig'].get('Binds',None)
        if volumes:
            for i in volumes:
                 mapvolumes.append(i)
        redata['binds'] = mapvolumes

        return redata

    def store_usage(self):
        DriverStatus = self.info()['DriverStatus']
        for i in DriverStatus:
            if "Data Space Used" in i[0]:
                used = float(i[1].replace("GB",""))
            elif 'Data Space Available' in i[0]:
                free = float(i[1].replace("GB",""))
        return {"used":used, "free":free}

    def get_all_stats(self):
        redata = {}
        containers = self.containers(quiet=True)
        for id in containers:
            redata[id] = self.stats_query(id)
        return redata

    def stats_query(self,id):
        redata = {}
        data = self.stats(id, stream=False)

        CPU_USAGE_USER = data["cpu_stats"]["usage_in_usermode"] * 100.00 / data["cpu_stats"]["total_usage"]
        CPU_USAGE_USER = "%.2f" % CPU_USAGE_USER

        MEM_USAGE = data["memory_stats"]["usage"]
        MEM_LIMIT = data["memory_stats"]["limit"]
        MEM_RATE = data["memory_stats"]["usage"] * 100.00 / data["memory_stats"]["limit"]
        MEM_RATE = "%.2f" % MEM_RATE

        NET_IN = data["networks"]["rx_bytes"]
        NET_OUT = data["networks"]["tx_bytes"]

        for i in data["blkio_stats"]["io_service_bytes_recursive"]:
            if i["major"] == 253 and i["minor"] != 0:
                if i["op"] == "Read":
                    BLK_IN = i["value"]
                elif i["op"] == "Write":
                    BLK_OUT = i["value"]
        redata["time"] = data["read"]
        redata["cpu"] = CPU_USAGE_USER
        redata["mem"]["usage"] = MEM_USAGE
        redata["mem"]["limit"] = MEM_LIMIT
        redata["mem"]["rate"] = MEM_RATE
        redata["net"]["in"] = NET_IN
        redata["net"]["out"] = NET_OUT
        redata["blk"]["in"] = BLK_IN
        redata["blk"]["out"] = BLK_OUT
        return redata