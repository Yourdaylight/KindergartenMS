# -*- coding: utf-8 -*-
# @Time    :2023/2/26 6:39
# @Author  :lzh
# @File    : teacher_views.py
# @Software: PyCharm

"""
教师管理操作
主要包括：给学生打分，批量导入学生
"""
import json
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import User, StudentDaily
from django.db.models import Q
from django.forms.models import model_to_dict
import datetime
import traceback


@require_http_methods(["POST"])
def report_student(request):
    """
    教师给学生打分,date不传默认为当天
    :param request:
    :return:
    """
    try:
        req_data = json.loads(request.body)
        # 获取studentdaily表中的所有字段，分数默认为0
        student_id = req_data.get("student_id", -1)
        teacher_id = req_data.get("teacher_id")
        study_score = req_data.get("study_score", 0)
        eat_score = req_data.get("eat_score", 0)
        sleep_score = req_data.get("sleep_score", 0)
        social_score = req_data.get("social_score", 0)
        etiquette_score = req_data.get("etiquette_score", 0)
        sports_score = req_data.get("sport_score", 0)
        temperature = req_data.get("temperature", 36.8)
        teacher_comment = req_data.get("teacher_comment", "")
        date = req_data.get("date", -1)
        if date == -1:
            date = datetime.datetime.now()
        else:
            date = datetime.datetime.strptime(date, "%Y-%m-%d")
        # 学生id不能为空
        if student_id == -1:
            return JsonResponse({"code": 500, "msg": "学生id不能为空", "data": None})
        # 查询学生是否存在
        student = User.objects.filter(id=student_id, role="3")
        if not student:
            return JsonResponse({"code": 500, "msg": f"该学生不存在", "data": None})
        # 获取今天的日期
        day = date.day
        # 根据学生id和班级id查询学生是否存在
        student_daily = StudentDaily.objects.filter(student_id=student_id, date__day=day)
        report_data = {
            "study_score": study_score,
            "eat_score": eat_score,
            "sleep_score": sleep_score,
            "social_score": social_score,
            "etiquette_score": etiquette_score,
            "sport_score": sports_score,
            "teacher_comment": teacher_comment,
            "temperature": temperature,
        }
        # 存在则更新
        if student_daily:
            student_daily.update(**report_data)
            return JsonResponse({"code": 200, "msg": "success", "data": None})
        else:
            report_data["student_id"] = student_id
            report_data["teacher_id"] = teacher_id
            report_data["date"] = date
            # 提交数据库
            StudentDaily.objects.create(**report_data)
            return JsonResponse({"code": 500, "msg": f"学生不存在", "data": None})
    except Exception as e:
        print(traceback.format_exc())
        return JsonResponse({"code": 500, "msg": "failed: " + str(e), "data": None})


@require_http_methods(["POST"])
def search_student_history(request):
    """
    教师查询学生的历史打分
    只输入学生id为学生端的查询
    教师端查询需要输入学生id和教师id
    student_id: 学生id,选填
    teacher_id: 教师id，必填
    start_date: 开始日期，选填(当起止日期都填写时，才触发日期查询)
    end_date: 结束日期，选填
    :param request:
    :return:
    """
    try:
        req_data = json.loads(request.body)
        # 根据student_id和teacher_id查询
        student_id = req_data.get("student_id", -1)
        teacher_id = req_data.get("teacher_id", -1)
        start_date = req_data.get("start_date", "")
        end_date = req_data.get("end_date", "")
        # 根据学生id和教师id查询
        search_dict = {}
        if student_id != -1:
            search_dict["student_id"] = student_id
        if teacher_id != -1:
            search_dict["teacher_id"] = teacher_id
        history_data = StudentDaily.objects.filter(**search_dict)
        # 根据日期查询
        if start_date and end_date:
            history_data = history_data.filter(date__range=[start_date, end_date])
        # 分页
        page = req_data.get("page", 1)
        page_size = req_data.get("page_size", 10)
        paginator = Paginator(history_data, page_size)
        try:
            history_data = paginator.page(page)
        except PageNotAnInteger:
            history_data = paginator.page(1)
        except EmptyPage:
            history_data = paginator.page(paginator.num_pages)
        # 将数据转换为字典
        history_data = [model_to_dict(item) for item in history_data]
        return JsonResponse({"code": 200, "msg": "success", "data": history_data})
    except Exception as e:
        print(traceback.format_exc())
        return JsonResponse({"code": 500, "msg": "failed: " + str(e), "data": None})
