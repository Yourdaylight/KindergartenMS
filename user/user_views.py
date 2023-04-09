import json
import datetime
import traceback
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.forms import model_to_dict
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import User, LeaveMessage

# Create your views here.
"""
不同角色用户信息的管理
"""


@require_http_methods(["POST"])
def login(request):
    """
    登陆 input username,password and role
    :param request:
    :return:
    """
    try:
        # 从请求json中获取参数
        req_data = json.loads(request.body)
        username = req_data.get('username')
        password = req_data.get('password')
        role = req_data.get('role')
        # search in database
        user = User.objects.filter(username=username, password=password, role=role)
        if user:
            # get user id
            user_id = user[0].id
            return JsonResponse({'code': 200, 'msg': 'success', 'data': {'user_id': user_id}})
        else:
            return JsonResponse({'code': 500, 'msg': '用户名或者密码错误', 'data': None})
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': 'failed: ' + str(e), 'data': None})


@require_http_methods(["POST"])
def register(request):
    """
    注册 ,用于管理员注册教师和家长，教师注册家长
    :param request:
    :return:
    """
    try:
        req_data = json.loads(request.body)
        username = req_data.get('username')
        password = req_data.get('password')
        role = req_data.get('role')
        class_no = req_data.get('class_no','')
        # search in database
        user = User.objects.filter(username=username, role=role)
        if user:
            return JsonResponse({'code': 500, 'msg': f'用户名{username}已存在', 'data': None})
        else:
            user = User(username=username, password=password, role=role,class_no=class_no)
            user.save()
            return JsonResponse({'code': 200, 'msg': 'success', 'data': None})
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': 'failed: ' + str(e), 'data': None})


@require_http_methods(["POST"])
def update_user(request):
    """
    更新用户信息
    :param request:
    :return:
    """
    try:
        req_data = json.loads(request.body)
        user_id = req_data.get('user_id')
        role = req_data.get('role')
        username = req_data.get('username')
        password = req_data.get('password')

        # search in database
        user = User.objects.filter(id=user_id)
        if user:
            user = user[0]
            user.role = role
            user.username = username
            user.password = password
            user.save()
            return JsonResponse({'code': 200, 'msg': 'success', 'data': None})
        else:
            return JsonResponse({'code': 500, 'msg': '用户不存在', 'data': None})
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': 'failed: ' + str(e), 'data': None})


@require_http_methods(["POST"])
def search_user_info(request):
    """
    搜索用户信息,根据用户id，用户名，角色，班级号
    多个参数组合查询，参数不存在时，查询所有
    分页参数默认第一页，每页10条
    :param request:
    :return:
    """
    try:
        req_data = json.loads(request.body)
        # 获取分页参数，默认第一页，每页10条
        page = req_data.get('page', 1)
        page_size = req_data.get('page_size', 10)
        user_id = req_data.get('user_id')
        username = req_data.get('username')
        full_name = req_data.get('full_name')
        role = req_data.get('role')
        class_no = req_data.get('class_no')
        # 上述参数存在时，拼接组合查询，否则查询所有
        search_dict = {}
        if user_id:
            search_dict['id'] = user_id
        if username:
            search_dict['username'] = username
        if role in [1, 2, 3]:
            search_dict['role'] = role
        if class_no:
            search_dict['class_no'] = class_no
        if full_name:
            search_dict['full_name'] = full_name
        # 根据分页参数和搜索条件查询
        users = User.objects.filter(**search_dict).order_by('-id')
        # 总数
        total = users.count()
        # 分页
        paginator = Paginator(users, page_size)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        # 返回结果
        data = []
        for user in users:
            data.append({
                'user_id': user.id,
                'full_name': user.full_name,
                'email': user.email,
                'phone': user.phone,
                'class_no': user.class_no,
                'username': user.username,
                'password': user.password,
                'role': user.role
            })
        return JsonResponse({'code': 200, 'msg': 'success', 'data': data, 'total': total})

    except Exception as e:
        return JsonResponse({'code': 500, 'msg': 'failed: ' + str(e), 'data': None})


@require_http_methods(["POST"])
def delete_user(request):
    """
    删除用户
    :param request:
    :return:
    """
    try:
        req_data = json.loads(request.body)
        user_id = req_data.get('user_id')
        # search in database
        user = User.objects.filter(id=user_id)
        if user:
            user.delete()
            return JsonResponse({'code': 200, 'msg': 'success', 'data': None})
        else:
            return JsonResponse({'code': 500, 'msg': '用户不存在', 'data': None})
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': 'failed: ' + str(e), 'data': None})


@require_http_methods(["POST"])
def leave_message(request):
    """
    :param request:
    :return:
    """
    try:
        req_data = json.loads(request.body)
        user_id = req_data.get('student_id')
        message = req_data.get('message')
        # search in database
        user = User.objects.filter(id=user_id)
        if user:
            # 保存留言
            today = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            LeaveMessage.objects.create(student_id=user_id, message=message, update_time=today, email=user[0].email, phone=user[0].phone)
            return JsonResponse({'code': 200, 'msg': 'success', 'data': None})
        raise Exception('用户不存在')
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': 'failed: ' + str(e), 'data': None})


@require_http_methods(["POST"])
def get_leave_messages(request):
    """
    获取留言
    :param request:
    :return:
    """
    try:
        req_data = json.loads(request.body)
        # 获取分页参数，默认第一页，每页10条
        page = req_data.get('page', 1)
        page_size = req_data.get('page_size', 10)
        # 根据分页参数和搜索条件查询
        messages = LeaveMessage.objects.all().order_by('-update_time')
        # 总数
        total = messages.count()
        # 分页
        paginator = Paginator(messages, page_size)
        try:
            messages = paginator.page(page)
        except PageNotAnInteger:
            messages = paginator.page(1)
        except EmptyPage:
            messages = paginator.page(paginator.num_pages)
        # 返回结果
        data = []
        for message in messages:
            data.append({
                'message_id': message.id,
                'student_id': message.student_id,
                'message': message.message,
                'update_time': datetime.datetime.strftime(message.update_time, '%Y-%m-%d %H:%M:%S'),
                'email': message.email,
                'phone': message.phone
            })
        return JsonResponse({'code': 200, 'msg': 'success', 'data': data, 'total': total})

    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'code': 500, 'msg': 'failed: ' + str(e), 'data': None})


@require_http_methods(["POST"])
def delete_leave_message(request):
    """
    删除留言
    :param request:
    :return:
    """
    try:
        req_data = json.loads(request.body)
        message_id = req_data.get('message_id')
        # search in database
        message = LeaveMessage.objects.filter(id=message_id)
        if message:
            message.delete()
            return JsonResponse({'code': 200, 'msg': 'success', 'data': None})
        else:
            return JsonResponse({'code': 500, 'msg': '留言不存在', 'data': None})
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': 'failed: ' + str(e), 'data': None})
