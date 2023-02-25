# -*- coding: utf-8 -*-
# @Time    :2023/2/26 4:52
# @Author  :lzh
# @File    : urls.py
# @Software: PyCharm

from django.urls import path
from . import user_views, group_views,teacher_views

urlpatterns = [
    path('', user_views.login, name='login'),
    # 用户管理
    path('api/v1/login/', user_views.login, name='login'),
    path('api/v1/register/', user_views.register, name='register'),
    path('api/v1/update_user/', user_views.update_user, name='update_user'),
    path('api/v1/search_user_info/', user_views.search_user_info, name='search_user_info'),
    path('api/v1/delete_user/', user_views.delete_user, name='delete_user'),
    # 班级管理
    path('api/v1/add_class/', group_views.add_class, name='add_class'),
    path('api/v1/delete_class/', group_views.delete_class, name='delete_class'),
    path('api/v1/update_class/', group_views.update_class, name='update_class'),
    path('api/v1/search_class_info/', group_views.search_class_info, name='search_class_info'),
    # 老师操作
    path('api/v1/report_student/', teacher_views.report_student, name='report_student'),
    path('api/v1/search_student_history/', teacher_views.search_student_history, name='search_student_info'),
]
