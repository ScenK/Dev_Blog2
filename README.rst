:Info: Dev_Blog Python-Release Based On Flask and MongoDB.
:Repository: https://github.com/ScenK/Dev_Blog2
:Author: Scen.K (http://tuzii.me).
:License: MIT License.

文件目录结构:
---------
::

    Dev_Blog2/
        .
        ├── admin                                 后端Blueprint
        │   ├── __init__.py
        │   ├── admin.py                          后端Handler
        │   ├── static                            静态文件夹
        │   │   ├── css
        │   │   ├── images
        │   │   ├── js
        │   │   └── lib
        │   ├── templates                         页面文件夹
        │   │   └── admin
        ├── fabfile
        │   ├── __init__.py                       集成发布Fabric命令
        │   └── dbmover.py                        博客版本数据库迁移助手
        ├── frontend                              前端Blueprint
        │   ├── __init__.py
        │   ├── frontend.py                       前端Handler
        │   ├── templates                         页面文件夹
        │   │   └── frontend
        ├── Model
        │   ├── __init__.py
        │   └── models.py
        ├── static                                静态文件夹
        │   ├── css
        │   ├── less
        │   ├── images
        │   ├── js
        │   ├── lib
        │   ├── favicon.ico
        │   └── robots.txt
        ├── __init__.py
        ├── README.md                             帮助文件
        ├── requirements.txt                      Python基础安装包列表
        ├── runserver.py                          用来启动web服务器
        ├── yuicompressor.jar                     YUI js,css压缩器
        ├── config.py                             网站初始化设置文件
        └── utils                                 第三方及助手文件夹
            ├── __init__.py
            ├── email_util.py                     邮件发送器
            ├── helper                            助手文件夹
            │   ├── __init__.py
            │   ├── html_helper.py                html处理助手
            │   └── upyun_helper.py               又拍云图片上传助手
            └── upyun.py                          又拍云SDK(v1.0)



+ 版本更替说明:

   本项目代码为dev_blog第一版制作并上线半年后重新开发而成

   第一版代码库地址:<https://github.com/ScenK/dev_blog/>

   在完成第一版本之后 在更多的对python的进一步认识的基础上 考虑到之前第一版继续开发的扩展性受到很大限制 于是开发第二个博客代码版本

    * 技术改进:
       - 第二个版本后端上仍然采用MongoDB作为数据库 但是增加了新的MongnEngine作为Orm 提供强大的Model层
       - 网站从tornado搭建改为flask版本 而tornado退居后台 只进行作为非阻塞服务器使用
       - Admin后端放弃使用foundation的框架 而使用了一个全新的模版(colorful life)
       - Admin后端放弃使用Markdown的写作方式 而采用了wysiwyg编辑器
       - Admin后端放弃使用fineuploader图片上传组建 而采用uploadifive作为替代
       - 第一版数据结构优化

+ 版本迁移须知:

    第一版本的博客代码 使用一键数据库脚本(已集成在fab命令中)
    
    * 使用步骤:
       - config.py设置好目标数据库名称(避免跟原始数据库名称一致)
       - 备份导出原始数据库: fab backup_database
       - 导入数据库: mongorestore -d dev_blog --drop ~/mongobak/dev_blog
       - 执行迁移命令: fab dbmove
       - 等待脚本结束

+ 安装须知:

    * 项目Wiki地址: (待完成)
    * 博客地址: <http://tuzii.me/>
    * 推荐使用独立VPS
        本博客线上环境: Amazon EC2 + Ubuntu12.04 + Python2.7.3 + Nginx + Tornado + MongoDB2.0.2
    * 基础环境:
        Linux + Tornado + Python + MongoDB
    * 可选环境:
        前端使用nginx做多线程反向代理
    * 基础环境配好后按照requirements.txt里列出的相关软件包装好
        推荐使用pip批量安装
    * 启动相关进程(MongoDB, Nginx, Tornado)

+ 安装简介(Ubuntu 12.04为例):

    * sudo apt-get install python-pip mongodb gcc openjdk-6-jre-headless lessc
    * cd ~/ dev_blog2/
    * sudo pip install -r requirements.txt
    * sudo pip install tornado
    * cd ~/dev-blog2/
        - 拷贝 Config/config.py.sample 到 Config/config.py 并更改网站相关设置
        - 执行fab build 进行初始化部属(此时会默认生成默认的后台管理员账户密码均为'admin' 请登录后自行修改)
        - 执行fab test 开启服务器进程(或者在Supervisor开启python多进程)
        - 每次改动的代码更新都可以使用fab update 进行服务端代码自动更新

+ 开发须知:

    * 遵循已有代码风格和文件夹风格 欢迎提pull request
    * MIT License.

*Do it yourself and make joy :)*
