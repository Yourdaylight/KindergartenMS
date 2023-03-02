# -*- coding: utf-8 -*-
# @Time    :2023/3/1 7:22
# @Author  :lzh
# @File    : admin_views.py
# @Software: PyCharm
import os
import json
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
import traceback
import configparser


@require_http_methods(["POST", "GET"])
def get_board_config(request):
    """
    获取公告配置
    :param request:
    :return:
    """
    try:
        with open("board.ini", "r", encoding="utf-8") as f:
            board_config = f.read()
        return JsonResponse({'code': 200, 'msg': 'success', 'data': board_config})
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'code': 500, 'msg': 'failed: ' + str(e), 'data': None})


@require_http_methods(["POST"])
def update_board_config(request):
    """
    修改公告配置
    :param request:
    :return:
    """
    try:
        req_data = json.loads(request.body)
        board_config = req_data.get('board_config')
        with open("board.ini", "w", encoding="utf-8") as f:
            f.write(board_config)
        return JsonResponse({'code': 200, 'msg': 'success', 'data': None})
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'code': 500, 'msg': 'failed: ' + str(e), 'data': None})


@require_http_methods(["POST", "GET"])
def get_board_html(request):
    """
    获取公告页面
    :param request:
    :return:
    """
    try:

        # 读取配置文件
        config = configparser.ConfigParser()
        config.read("./board.ini", encoding="utf-8")
        sections = config.sections()
        basic_html = []
        subsection_html = []
        # 遍历所有section写入html
        for section in sections:
            items = config.items(section)
            # 只有基本情况这个section的长度大于1
            if len(items) > 1:
                for k, v in items:
                    if k == "内容":
                        basic_html.append(f"<p>{v}</p>")
                    else:
                        info_item = f"""
                      <div class="info-item">
                        <div class="info-label">{k}：</div>
                        <div class="info-value">{v}</div>
                      </div>
                        """
                        basic_html.append(info_item)
            else:
                sub_section = f"""<section><h2>{section}</h2><p>{items[0][1]}</p></section>"""
                subsection_html.append(sub_section)

        # 读取模板html然后写入到返回html中
        with open("templates/template.html", "r", encoding="utf-8") as f:
            template_html = f.read()
        template_html = template_html.replace("{{basic_info}}", "".join(basic_html))
        template_html = template_html.replace("{{sub_info}}", "".join(subsection_html))
        with open("templates/board.html", "w", encoding="utf-8") as f:
            f.write(template_html)
        # get my server ip

        href = "http://{}/board".format(request.META['HTTP_HOST'])
        return JsonResponse({'code': 200, 'msg': 'success', 'data': {"html":template_html,"href": href}})

    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'code': 500, 'msg': 'failed: ' + str(e), 'data': os.path.abspath("./")})


@require_http_methods(["POST", "GET"])
def board(request):
    """
    公告页面
    :param request:
    :return:
    """
    return render(request, 'board.html')


@require_http_methods(["POST", "GET"])
def restore_board_config(request):
    """
    恢复公告配置
    :param request:
    :return:
    """
    try:
        with open("board.bak", "r", encoding="utf-8") as f:
            board_config = f.read()
        with open("board.ini", "w", encoding="utf-8") as f:
            f.write(board_config)
        return JsonResponse({'code': 200, 'msg': 'success', 'data': None})
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'code': 500, 'msg': 'failed: ' + str(e), 'data': None})


if __name__ == '__main__':
    get_board_html(None)
