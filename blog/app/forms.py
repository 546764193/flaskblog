# -*- coding:utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo
from wtforms import ValidationError


class LoginForm(FlaskForm):
    UserEmail = StringField(u'useremail', validators=[DataRequired(message=u'请输入邮箱'), Email(message=u'请输入正确的邮箱')])
    PassWord = PasswordField(u'passworld', validators=[DataRequired(message=u'请输入密码'), Length(6, 16, message=u'密码长度错误')])


class SignUpForm(FlaskForm):
    UserEmail = StringField(u'email', validators=[DataRequired(u'请输入邮箱'), Email(message=u'请输入正确的邮箱 例：123456@qq.com'), Length(1, 20)])
    UserName = StringField(u'username', validators=[DataRequired()])
    PassWord = PasswordField(u'passworld', validators=[DataRequired(message=u'密码不能为空')])
    # def ValidateEmail(self, field):


class BlogForm(FlaskForm):
    BlogTitle = StringField(u'blogtitle', validators=[DataRequired(u'不能为空')])
    BlogContent = TextAreaField(u'blogcontent')


class AboutMeForm(FlaskForm):
    describe = TextAreaField(u'about me', validators=[Length(max=140)])