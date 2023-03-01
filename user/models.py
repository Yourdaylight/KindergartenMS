from django.db import models


# Create your models here.
# user model with 3 different types of users
class User(models.Model):
    user_type_choices = (
        (1, "Admin"),
        (2, "Teacher"),
        (3, "Parent"),
    )
    role = models.CharField(max_length=10, choices=user_type_choices)
    full_name = models.CharField(max_length=100,)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=100)
    class_no = models.CharField(max_length=100)
    #设置性别只能是男或女
    sex_choices = (
        ("女", "女"),
        ("男", "男"),

    )
    sex = models.CharField(max_length=3,choices=sex_choices,default="男")
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


# 班级信息表
class ClassInfo(models.Model):
    class_no = models.CharField(max_length=100)
    class_name = models.CharField(max_length=100)
    teacher_id = models.CharField(max_length=100)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.class_name


# 学生情况每日统计表
class StudentDaily(models.Model):
    student_id = models.CharField(max_length=100)
    teacher_id = models.CharField(max_length=100)
    class_no = models.CharField(max_length=100)
    date = models.DateField(default='2020-01-01')
    temperature = models.FloatField(null=True, blank=True)
    # 学生的今日学习评分，吃饭评分，睡觉评分，社交评分，礼仪举止评分，体育锻炼评分。
    study_score = models.FloatField(null=True)
    eat_score = models.FloatField(null=True)
    sleep_score = models.FloatField(null=True)
    social_score = models.FloatField(null=True)
    etiquette_score = models.FloatField(null=True)
    sport_score = models.FloatField(null=True)
    # 老师今日对学生的评价
    teacher_comment = models.CharField(max_length=2048)

    def __str__(self):
        return self.student_id


# 家长留言板
class ParentMessage(models.Model):
    student_id = models.CharField(max_length=100)
    message = models.CharField(max_length=2048)
    date = models.DateField()

    def __str__(self):
        return self.student_id
