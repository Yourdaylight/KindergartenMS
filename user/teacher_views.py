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
import pandas as pd
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
        student_id = req_data.get("student_id") if req_data.get("student_id") else -1
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
            # 保存更新数据
            return JsonResponse({"code": 200, "msg": "更新成功", "data": None})
        else:
            report_data["student_id"] = student_id
            report_data["teacher_id"] = teacher_id
            report_data["date"] = date
            report_data["update_time"] = datetime.datetime.now()
            # 提交数据库
            StudentDaily.objects.create(**report_data)
            return JsonResponse({"code": 200, "msg": "新增成功", "data": None})
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
        # start_date 默认为30天前
        start_date = req_data.get("start_date", datetime.datetime.now() - datetime.timedelta(days=30))
        # end_date 默认为今天
        end_date = req_data.get("end_date", datetime.datetime.now())
        student_name = ""
        search_dict = {}
        # 根据学生id和教师id查询
        if student_id != -1:
            search_dict["student_id"] = student_id
        if teacher_id != -1:
            search_dict["teacher_id"] = teacher_id
        # 先根据date降序，再根据update_time降序
        history_data = StudentDaily.objects.filter(**search_dict).order_by("-date", "-update_time")
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
        history_data = [{
            "id": item.id,
            "student_id": item.student_id,
            "teacher_id": item.teacher_id,
            "study_score": item.study_score,
            "eat_score": item.eat_score,
            "sleep_score": item.sleep_score,
            "social_score": item.social_score,
            "etiquette_score": item.etiquette_score,
            "sport_score": item.sport_score,
            "teacher_comment": item.teacher_comment,
            "temperature": item.temperature,
            "date": item.date,
            "update_time": datetime.datetime.strftime(item.update_time, "%Y-%m-%d %H:%M:%S"),
            "student_name": student_name
        } for item in history_data]
        for daily in history_data:
            student = User.objects.filter(id=daily["student_id"], role="3")
            if student:
                daily["student_name"] = student[0].username
        return JsonResponse({"code": 200, "msg": "success", "data": history_data})
    except Exception as e:
        print(traceback.format_exc())
        return JsonResponse({"code": 500, "msg": "failed: " + str(e), "data": None})


@require_http_methods(["POST"])
def upload_students_info(request):
    """
    上传学生信息
    :param request:
    :return:
    """
    try:
        # 　文件从vue中传过来
        file = request.FILES.get("file")
        table = request.POST.get("table")
        upload_teacher_id = request.POST.get("teacher_id", -1)
        # 读取文件
        # 检测文件后缀是否为csv和xls
        if not file.name.endswith(".csv") and not file.name.endswith(".xls"):
            raise Exception("文件格式错误，仅支持.csv和.xls格式")
        with open(file.name, "wb") as f:
            for chunk in file.chunks():
                f.write(chunk)
        file_name = file.name
        data = pd.read_csv(file_name)
        # 将数据转换为字典
        data = data.to_dict(orient="records")
        # 将数据存入数据库
        if table == "user":
            for item in data:
                # 判断学生是否存在
                student = User.objects.filter(username=item["username"], role="3")
                if student:
                    raise Exception(f"学生用户名{item['username']}已存在")
                item["role"] = "3"
                User.objects.create(**item)
        elif table == "daily":
            for item in data:
                # 判断学生是否存在
                student = User.objects.filter(id=item["student_id"], role="3")
                if not student:
                    raise Exception(f"学生id{item['student_id']}不存在，请检查后重新上传")
                item["student_id"] = student[0].id
                item["teacher_id"] = upload_teacher_id
                item["date"] = datetime.datetime.strptime(item["date"], "%Y-%m-%d")
                StudentDaily.objects.create(**item)
        return JsonResponse({"code": 200, "msg": "success", "data": None})
    except Exception as e:
        print(traceback.format_exc())
        return JsonResponse({"code": 500, "msg": "failed: " + str(e), "data": None})


@require_http_methods(["POST"])
def get_recent_days(request):
    """
    获取最近30天的StudentDaily数据
    :return:
    """
    try:
        req_data = json.loads(request.body)
        student_id = req_data.get("student_id", -1)
        recent_days = req_data.get("recent_days", 30)
        today = datetime.date.today()
        days = [(today - datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range(recent_days)]
        # 根据date升序排序
        nonull_days = []

        all_data = StudentDaily.objects.filter(date__in=days, student_id=student_id).order_by("date")
        # 将数据转换为字典
        fields = ["study_score", "sleep_score", "eat_score", "social_score", "sport_score", "etiquette_score"]
        fields_cn = ["学习", "睡眠", "饮食", "社交", "运动", "礼仪"]
        item_dict = {v: {"name": fields_cn[index], "type": "line", "stack": "Total", "data": []} for index, v in enumerate(fields)}
        for item in all_data:
            nonull_days.append(item.date.strftime("%Y-%m-%d"))
            for field in fields:
                item_dict[field]["data"].append(getattr(item, field))
        series = [item_dict[field] for field in fields]
        res = {
            "series": series,
            "data": nonull_days
        }

        return JsonResponse({"code": 200, "msg": "success", "data": res})
    except Exception as e:
        print(traceback.format_exc())
        return JsonResponse({"code": 500, "msg": "failed: " + str(e), "data": None})
