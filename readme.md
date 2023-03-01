## 幼儿园管理系统
接口文档
https://documenter.getpostman.com/view/13268592/2s93CPqrqt#9d570996-db98-4f75-b8d3-ed082af3db37
---
|用户角色|管理员|教师|家长|
|--|--|--|--|
|对应编号|1|2|3|

## 后端接口文件
路由文件：user/urls.py
<br>每个接口的实现文件：user目录下_views.py结尾的文件

## 上传模板文件
多个学生信息的上传模板文件：students.csv
多个学生日常情况记录的上传模板文件：

## 公告板
公告板的接口文件：admin_views.py
公告板的展示内容全部在根目录下的board.ini文件中
基于这个配置生成的模板问会在templates/board.html中
templates/template.html是公告板的模板文件
前端获取公告板的接口内容后直接v-html渲染即可
