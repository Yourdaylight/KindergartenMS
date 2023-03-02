# -*- coding: utf-8 -*-
# @Time    :2023/2/26 4:52
# @Author  :lzh
# @File    : urls.py
# @Software: PyCharm

from django.urls import path
from . import user_views, group_views,teacher_views,admin_views

urlpatterns = [
    path('', user_views.login, name='login'),
    # 用户管理
    path('api/v1/login/', user_views.login, name='login'),
    path('api/v1/register/', user_views.register, name='register'),
    path('api/v1/update_user/', user_views.update_user, name='update_user'),
    path('api/v1/search_user_info/', user_views.search_user_info, name='search_user_info'),
    path('api/v1/delete_user/', user_views.delete_user, name='delete_user'),
    # 留言板相关
    path('api/v1/get_leave_messages/', user_views.get_leave_messages, name='get_leave_messages'),
    path('api/v1/leave_message/', user_views.leave_message, name='leave_message'),
    path('api/v1/delete_leave_message/', user_views.delete_leave_message, name='delete_message'),
    # 班级管理
    path('api/v1/add_class/', group_views.add_class, name='add_class'),
    path('api/v1/delete_class/', group_views.delete_class, name='delete_class'),
    path('api/v1/update_class/', group_views.update_class, name='update_class'),
    path('api/v1/search_class_info/', group_views.search_class_info, name='search_class_info'),
    # 老师操作
    path('api/v1/report_student/', teacher_views.report_student, name='report_student'),
    path('api/v1/search_student_history/', teacher_views.search_student_history, name='search_student_info'),
    path('api/v1/upload_students_info/', teacher_views.upload_students_info, name='search_student_info'),
    path('api/v1/get_recent_days/', teacher_views.get_recent_days, name='get_recent_30_days'),
    # 公告板相关
    path('api/v1/get_board_html/', admin_views.get_board_html, name='get_board_html'),
    path('api/v1/get_board_config/', admin_views.get_board_config, name='get_board_config'),
    path('api/v1/update_board_config/', admin_views.update_board_config, name='update_board_config'),
    path('api/v1/restore_board_config/', admin_views.restore_board_config, name='restored_board_config'),
    # render to board_html
    path('board/', admin_views.board, name='board'),
    # 留言板管理
    path('api/v1/get_leave_messages/', user_views.get_leave_messages, name='get_leave_messages'),
    path('api/v1/leave_message/', user_views.leave_message, name='leave_message'),
    path('api/v1/delete_leave_message/', user_views.delete_leave_message, name='delete_message'),

]
