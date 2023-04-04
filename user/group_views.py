# -*- coding: utf-8 -*-
# @Time    :2023/2/26 5:47
# @Author  :lzh
# @File    : group_views.py
# @Software: PyCharm

"""
用户组管理
管理员可以新增班级，删除班级，修改班级信息
新增班级需要设置班级编号，班级名称，班级老师
"""
import json
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import User, ClassInfo
from django.db.models import Q
from django.forms.models import model_to_dict
import traceback


@require_http_methods(["POST"])
def add_class(request):
    """
    新增班级
    :param request:
    :return:
    """
    try:
        req_data = json.loads(request.body)
        class_no = req_data.get('class_no')
        class_name = req_data.get('class_name')
        teacher_id = req_data.get('teacher_id')
        # 根据班级id或者班级名称查询班级是否存在
        class_info = ClassInfo.objects.filter(Q(class_no=class_no) | Q(class_name=class_name))
        if class_info:
            return JsonResponse({'code': 500, 'msg': f'班级编号或者班级名称已存在，请修改后重新添加', 'data': None})
        else:
            class_info = ClassInfo(class_no=class_no, class_name=class_name, teacher_id=teacher_id)
            class_info.save()
            return JsonResponse({'code': 200, 'msg': 'success', 'data': None})
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': 'failed: ' + str(e), 'data': None})


@require_http_methods(["POST"])
def delete_class(request):
    """
    删除班级时要把班级下的学生也删除
    :param request:
    :return:
    """
    try:
        req_data = json.loads(request.body)
        class_no = req_data.get('class_no')
        # 根据班级id查询班级是否存在
        class_info = ClassInfo.objects.filter(class_no=class_no)
        if class_info:
            class_info.delete()
            # 　查询user表中class_no=class_no且role=3的学生，将其class_no设置为None
            User.objects.filter(Q(class_no=class_no) & Q(role=3)).update(class_no=None)
            return JsonResponse({'code': 200, 'msg': 'success', 'data': None})
        else:
            return JsonResponse({'code': 500, 'msg': f'班级不存在', 'data': None})
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': 'failed: ' + str(e), 'data': None})


@require_http_methods(["POST"])
def update_class(request):
    """
    修改班级信息
    :param request:
    :return:
    """
    try:
        req_data = json.loads(request.body)
        class_no = req_data.get('class_no')
        class_name = req_data.get('class_name')
        teacher_id = req_data.get('teacher_id')
        # 根据班级id查询班级是否存在
        class_info = ClassInfo.objects.filter(class_no=class_no)
        if class_info:
            class_info.update(class_name=class_name, teacher_id=teacher_id)
            return JsonResponse({'code': 200, 'msg': 'success', 'data': None})
        else:
            return JsonResponse({'code': 500, 'msg': f'班级不存在', 'data': None})
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': 'failed: ' + str(e), 'data': None})


@require_http_methods(["POST"])
def search_class_info(request):
    """
    获取班级列表
    :param request:
    :return:
    """
    try:
        req_data = json.loads(request.body)
        page = req_data.get('page', 1)
        page_size = req_data.get('page_size', 10)
        # 根据班级名称/班级编号/班级老师查询班级信息
        class_name = req_data.get('class_name')
        class_no = req_data.get('class_no')
        teacher_id = req_data.get('teacher_id')
        # 多个条件则组合查询，单个条件则直接查询，没有条件则查询所有
        search_dict = {}
        if class_name:
            search_dict['class_name__contains'] = class_name
        if class_no:
            search_dict['class_no'] = class_no
        # 根据条件查询班级信息
        if search_dict:
            class_list = ClassInfo.objects.filter(**search_dict).order_by('-class_no')
        else:
            class_list = ClassInfo.objects.all().order_by('-class_no')
        # 如果有老师id，则取user中role=2且username=teacher_id的老师id
        if teacher_id:
            teacher_id = User.objects.filter(Q(role=2) & Q(username=teacher_id)).values('id')
            class_list = class_list.filter(teacher_id__in=teacher_id)
        total = class_list.count()
        paginator = Paginator(class_list, page_size)
        try:
            class_list = paginator.page(page)
        except PageNotAnInteger:
            class_list = paginator.page(1)
        except EmptyPage:
            class_list = paginator.page(paginator.num_pages)
        class_list = list(class_list)
        data = [model_to_dict(class_info) for class_info in class_list]
        return JsonResponse({'code': 200, 'msg': 'success', 'data': data, 'total': total})
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'code': 500, 'msg': 'failed: ' + str(e), 'data': None})
