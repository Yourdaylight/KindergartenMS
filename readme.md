## 幼儿园管理系统
### 安装使用
1. 安装python3.6
2. 命令行在当前路径下打开，执行命令安装依赖包 pip install -r requirements.txt
3. 执行命令启动服务 python manage.py runserver
4. 新开命令行进入frontend目录，执行命令安装依赖包 npm install
5. 执行命令启动前端服务 npm run dev
6. 浏览器访问http://127.0.0.1:8080
7. 默认管理员账号：admin 密码：admin
```
---
|用户角色|管理员|教师|家长|
|--|--|--|--|
|对应编号|1|2|3|

## 后端接口文件
路由文件：user/urls.py
<br>每个接口的实现文件：user目录下_views.py结尾的文件

## 上传模板文件
多个学生信息的上传模板文件：students.csv
多个学生日常情况记录的上传模板文件：user_studentdaily.csv

## 公告板
公告板的接口文件：admin_views.py
公告板的展示内容全部在根目录下的board.ini文件中
基于这个配置生成的模板问会在templates/board.html中
templates/template.html是公告板的模板文件
前端获取公告板的接口内容后直接v-html渲染即可
