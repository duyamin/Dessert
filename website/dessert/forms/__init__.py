#!/usr/bin/python
#-*-coding:utf-8-*-
import hashlib
from wtforms import *
from flask import g, request
from flaskext.wtf import *
from daimaduan.models import *
from daimaduan.utils.functions import *

__all__ = ['LoginForm', 'PostForm', 'PostCommentForm']

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
    title = TextField(u'标题')
    content = TextAreaField(u'代码')
    tags = TextField(u'标签', [tags_check])
    is_private = BooleanField(u'私有')

class PostCommentForm(BaseForm):
    content = TextAreaField(u'评论', [Required(message=u"评论不能为空")])