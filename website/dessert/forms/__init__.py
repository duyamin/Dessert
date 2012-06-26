#!/usr/bin/python
#-*-coding:utf-8-*-
import hashlib
from wtforms import *
from flask import g, request
from flaskext.wtf import *
from dessert.models import *

__all__ = ['LoginForm', 'PostForm', 'PostCommentForm', 'ProfileForm']

def email_unique(form, field):
    if len(User.query.filter_by(email=field.data).all()) > 0:
        raise ValidationError(u'这个邮件地址已经有人注册了.')

def nickname_unique(form, field):
    if len(User.query.filter_by(nickname=field.data).all()) > 0:
        raise ValidationError(u'这个邮件地址已经有人注册了.')

def tags_check(form, field):
    if not field.data:
        return True
    if len(field.data.split(' ')) > 3:
        raise ValidationError(u'标签不能超过3个.')

class BaseForm(Form):
    pass

class LoginForm(BaseForm):
    email = TextField(u'邮件地址', [Required(), Length(min=6, max=30), Email()])
    password = PasswordField(u'密码', [Length(min=6, max=12), Required()])

class PostForm(BaseForm):
    title = TextField(u'标题', [Required()])
    slug = TextField(u'Slug')
    content = TextAreaField(u'内容', [Required()])
    tags = TextField(u'标签', [tags_check])
    is_private = BooleanField(u'私有')

class PostCommentForm(BaseForm):
    content = TextAreaField(u'评论', [Required(message=u"评论不能为空")])

class ProfileForm(Form):
    nickname = TextField(u'昵称', [Required(message=u'请填一个你喜欢的昵称吧'), Length(min=3, max=12), nickname_unique])
    email = TextField(u'邮件地址', [Email(message=u'请输入正确的email地址')])
    agreement = BooleanField(u'注册条款', [Required()])
    title = TextField(u'博客标题', [Required()])
