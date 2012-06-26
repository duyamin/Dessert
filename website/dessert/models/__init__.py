#!/usr/bin/python
#-*-coding:utf-8-*-
import time
import hashlib
from datetime import datetime
from flask import url_for, request, session
from dessert.extensions import db

__all__ = ['User', 'Post', 'Tag', 'PostComment', 'getUserObject']

def getUserObject(slug=None, user_id=None):
    user = None
    if not slug and not user_id:
        if 'user' in session:
            user = g.user
    elif slug:
        user = User.query.filter_by(slug=slug).first()
    elif user_id:
        user = User.query.filter_by(id=user_id).first()
    return user

# 这个表存储代码拥有的标签
post_tag = db.Table('posts_tags',
            db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
            db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
        )

class Tag(db.Model):
    """
    标签表
    要求:
    1. 以小写存储
    2. 空格要替换成为'-'
    3. '和"都去掉
    """
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), unique=True, nullable=False)
    times = db.Column(db.Integer)
    created_time = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, name):
        self.name = name.replace(' ', '-').replace('"', '').replace("'", '')
        self.times = 1

    def __repr__(self):
        return "Tag <%s>" % self.name

    @classmethod
    def getTags(self, num):
        tags = Tag.query.all()[:num]
        return [tag.name for tag in tags]

    @classmethod
    def updateTags(self, model, tags=[]):
        old_tags = [tag.name for tag in model.tags]
        tags_to_add = set(tags) - set(old_tags)
        tags_to_del = set(old_tags) - set(tags)
        for tag in tags_to_add:
            t = Tag.query.filter_by(name='%s' % tag.strip().lower()).first()
            if not t:
                t = Tag(tag.strip("'\", ").replace(",", '').replace("_", '-'))
                db.session.add(t)
            else:
                t.times = t.times + 1
                db.session.add(t)
            model.tags.append(t)
        for tag in tags_to_del:
            t = Tag.query.filter_by(name='%s' % tag.strip().lower()).first()
            if t:
                model.tags.remove(t)
                t.times = t.times - 1
                db.session.add(t)
        db.session.add(model)

class User(db.Model):
    """
    用户表
    修改email地址时需要经过验证
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    openid = db.Column(db.Text, nullable=True)
    email = db.Column(db.String(45), unique=True, nullable=False)
    nickname = db.Column(db.String(45), unique=True, nullable=False)
    created_time = db.Column(db.DateTime, nullable=False)
    modified_time = db.Column(db.DateTime, nullable=False)

    blog = db.relationship('Blog', uselist=False)

    def __init__(self, nickname, email):
        self.nickname = nickname
        self.email = email
        self.created_time = self.modified_time = datetime.now()

    def __repr__(self):
        return "<User (%s|%s)>" % (self.nickname, self.email)

class Blog(db.Model):
    __tablename__ = 'blogs'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(45))

class Post(db.Model):
    """
    代码表
    """
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    slug = db.Column(db.String(45), nullable=True)
    title = db.Column(db.String(255), nullable=False) # 标题, 默认为"未知标题"
    content = db.Column(db.Text, nullable=False) # 代码内容, 不能为空
    view_num = db.Column(db.Integer, default=0)
    created_time = db.Column(db.DateTime, nullable=False)
    modified_time = db.Column(db.DateTime, nullable=False)

    user = db.relationship(User, backref=db.backref('posts'))
    tags = db.relationship('Tag', secondary=post_tag,
                            order_by=Tag.name, backref="posts")
    comments = db.relationship('PostComment', order_by="PostComment.created_time")

    def __init__(self, user_id, title, content):
        self.title = title
        self.content = content
        self.user_id = user_id
        self.view_num = 0
        self.created_time = self.modified_time = datetime.now()

    def __repr__(self):
        return "<Post (%s@%s)>" % (self.title, self.user_id)

class PostComment(db.Model):
    """
    评论表
    """
    __tablename__ = 'post_comments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_time = db.Column(db.DateTime, nullable=False)
    modified_time = db.Column(db.DateTime, nullable=False)

    def __init__(self, post_id, email, nickname, url, content):
        self.post_id = post_id
        self.email = email
        self.nickname = nickname
        self.url = url
        self.content = content
        self.created_time = self.modified_time = datetime.now()

    def __repr__(self):
        return "<PostComment %s>" % self.id
