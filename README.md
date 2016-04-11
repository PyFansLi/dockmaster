#DockMaster

作者:Lioncui

##关于我
>本项目完全出去兴趣使然而做的,之前粗略地写了dockerweb    
>后来应几个朋友要求,重写了一次,优化了代码结构,增加了多主机管理,并且把前端页面效果丰富了一下.  
>本人为非专业开发人员,爱好编码,做这个项目主要是为了练手,独立完成设计与开发.  
>在使用中有遇到BUG或者希望实现某功能的,可以在issues中提出来.  

##关于项目
>整个项目基于python2.7, flask web框架, bootstrap前端框架  
>依赖模块记录在requirements.txt, 可以使用pip全部导入
>完全免费,完全开源,支持容器方式运行,包含完整Dockerfile  

##运行方式
>直接运行容器,启动时加入mysql的配置,具体配置请以实际为准
```
docker run -d -p 8080:8080 -e DBUSER="dbuser" -e DBPASS="dbpass" -e DBHOST="dbhost" -e DBPORT="dbport" -e DBNAME="dbname" lioncui/dockmaster
```

>自行构建镜像
```
git clone https://github.com/lioncui/dockmaster
cd dockmaster
docker build -t dockmaster .
```

##特别感谢
>感谢同事老谭的支持,教会了我jquery使用,ajax异步调用,前端页面数据的处理

##使用截图
![Alt text](./imgs/登录.png)
![Alt text](./imgs/总览.png)
![Alt text](./imgs/主机.png)
![Alt text](./imgs/镜像.png)
![Alt text](./imgs/容器.png)