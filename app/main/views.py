from flask import render_template, redirect, request, url_for, flash,\
                    abort, current_app, make_response
from flask_login import login_user, logout_user, login_required, current_user
from .. import db
from ..models import User,allowed_file,Teacher,Role,Lesson, Permission, Post, New, Oldnew,\
                    Comment,NewLesson,Student,CollectPost,Follow,LessonFile,\
                    AtMe,date2sec, hour2date, date2sec, hour2date, imgsize, body2html, insert
from ..email import send_email
from .forms import LoginForm, RegistrationForm, ChangePasswordForm,\
    PasswordResetRequestForm, PasswordResetForm, ChangeEmailForm,AddTeacherForm,\
    EditProfileForm, EditProfileAdminForm, UpdateTopicForm,\
    PostForm, CommentForm, PostForm2,AddLessonForm,NewLessonForm,\
    LoginFormE, RegistrationFormE, ChangePasswordFormE, NewsForm, NewsFormE,\
    PasswordResetRequestFormE, PasswordResetFormE, ChangeEmailFormE,AddTeacherFormE,\
    EditProfileFormE, EditProfileAdminFormE, UpdateTopicFormE,\
    PostFormE, CommentFormE, PostFormE2,AddLessonFormE,NewLessonFormE,\
    LessonFileForm,LessonFileFormE,CriticismForm,CriticismFormE,\
    PostFormNewlesson, PostFormNewlessonE, PostFormNewlesson2,PostFormNewlesson2E,\
    PostForm0,PostForm0E, PostForm02, PostForm02E, SearchForm, SearchFormE,CheckForm, \
    UrlForm, UrlFormE, GoogleForm, GoogleFormE
from ..decorators import admin_required
from PIL import Image
from flask_sqlalchemy import get_debug_queries
from . import main
from ..decorators import permission_required
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
# from werkzeug import secure_filename
from werkzeug.datastructures import CombinedMultiDict
import flask,os,random,time
from sqlalchemy import not_,or_,and_

import requests,socket,time
import datetime as dt
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from markdown import markdown
import random
from dateutil.parser import parse

@main.route('/show-all')
def show_all():
    resp = make_response(redirect(url_for('.media')))
    resp.set_cookie('show', 'all', max_age=30*24*60*60)
    return resp

@main.route('/show-newsflash')
def show_newsflash():
    resp = make_response(redirect(url_for('.media')))
    resp.set_cookie('show', 'newsflash', max_age=30*24*60*60)
    return resp


@main.route('/show-toutiao')
def show_toutiao():
    resp = make_response(redirect(url_for('.media')))
    resp.set_cookie('show', 'toutiao', max_age=30*24*60*60)
    return resp

@main.route('/show-toutiao-english')
def show_toutiao_english():
    resp = make_response(redirect(url_for('.media')))
    resp.set_cookie('show', 'toutiao_english', max_age=30*24*60*60)
    return resp

@main.route('/show-local')
def show_local():
    resp = make_response(redirect(url_for('.media')))
    resp.set_cookie('show', 'local', max_age=30*24*60*60)
    return resp


@main.route('/media', methods=['GET', 'POST'])
def media():
    english=request.cookies.get('english')
    resp = request.cookies.get('show')  
    if resp == None:
        resp = "all"  
    page = request.args.get('page', 1, type=int)
    if resp=="newsflash":
        pagination =New.query.filter(New.tag.like('%newsflash')).filter(New.lang=="cn").order_by(New.timestamp.desc()).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
    elif resp=="toutiao":
        pagination =New.query.filter(New.tag.like('%news')).filter(New.lang=="cn").order_by(New.timestamp.desc()).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
    elif resp=="toutiao_english":
        pagination =New.query.filter(New.tag.like('%news')).filter(New.lang=="en").order_by(New.timestamp.desc()).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)            
    elif resp=="all":
        pagination =New.query.order_by(New.timestamp.desc()).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
    elif resp=="local":
        pagination =New.query.filter(New.tag.in_(['news','research'])).filter(New.lang=="cn").order_by(New.timestamp.desc()).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)

    else:
        pagination =New.query.filter(New.tag.in_(['news','research'])).filter(New.lang=="cn").order_by(New.timestamp.desc()).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)     
    posts = pagination.items
    return render_template('media.html', posts=posts, resp=resp, pagination=pagination, english=english)


@main.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    english=request.cookies.get('english')
    if english == "yes":
        form = SearchFormE()
    else:
        form = SearchForm()
    if form.validate_on_submit():
        keyword = form.search.data
        return redirect(url_for('main.found', keyword=keyword))
    return render_template('search.html', form=form, english=english)


@main.route('/found/<string:keyword>', methods=['GET', 'POST'])
def found(keyword):
    english=request.cookies.get('english')
    page = request.args.get('page', 1, type=int)
    if english == "yes":
        form = SearchFormE()
    else:
        form = SearchForm()
    if form.search.data is not None:
        keyword = form.search.data
    k = keyword.strip().split(' ')
    if len(k) == 1:
        if '-' not in k[0]:
            pagination =Oldnew.query.filter(Oldnew.topic.like('%' + k[0] + '%')).order_by(Oldnew.timestamp.desc()).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
            count =Oldnew.query.filter(Oldnew.topic.like('%' + k[0] + '%')).count()
        else:
            flash('第一个必须是非排除搜索关键词。')
            return redirect(url_for('main.search'))
    elif len(k) == 2:
        if '-' not in k[0] and '-' in k[1]:
            pagination =Oldnew.query.filter(Oldnew.topic.like('%' + k[0] + '%')).filter(not_(Oldnew.topic.like('%' + k[1].replace('-','') + '%'))).order_by(Oldnew.timestamp.desc()).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
            count =Oldnew.query.filter(Oldnew.topic.like('%' + k[0] + '%')).filter(not_(Oldnew.topic.like('%' + k[1].replace('-','') + '%'))).count()
        elif '-' not in k[0] and '-' not in k[1]:
            pagination =Oldnew.query.filter(and_(Oldnew.topic.like('%' + k[0] + '%'),Oldnew.topic.like('%' + k[1] + '%'))).order_by(Oldnew.timestamp.desc()).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
            count =Oldnew.query.filter(Oldnew.topic.like('%' + k[0] + '%')).filter(Oldnew.topic.like('%' + k[1] + '%')).count()
        else:
            flash('-' not in k[0] and '-' in k[1])
            flash('排除项放到关键词最后。第一个必须是非排除搜索关键词。')
            return redirect(url_for('main.search'))
    elif len(k) == 3:
        if '-' not in k[0] and '-' in k[1] and '-' in k[2]:
            pagination =Oldnew.query.filter(Oldnew.topic.like('%' + k[0] + '%')).filter(not_(Oldnew.topic.like('%' + k[1].replace('-','') + '%'))).filter(not_(Oldnew.topic.like('%' + k[2].replace('-','') + '%'))).order_by(Oldnew.timestamp.desc()).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
            count =Oldnew.query.filter(Oldnew.topic.like('%' + k[0] + '%')).filter(not_(Oldnew.topic.like('%' + k[1].replace('-','') + '%'))).filter(not_(Oldnew.topic.like('%' + k[2].replace('-','') + '%'))).count()
        elif '-' not in k[0] and '-' not in k[1] and '-' in k[2]:
            pagination =Oldnew.query.filter(Oldnew.topic.like('%' + k[0] + '%')).filter(Oldnew.topic.like('%' + k[1] + '%')).filter(not_(Oldnew.topic.like('%' + k[2].replace('-','') + '%'))).order_by(Oldnew.timestamp.desc()).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
            count =Oldnew.query.filter(Oldnew.topic.like('%' + k[0] + '%')).filter(Oldnew.topic.like('%' + k[1] + '%')).filter(not_(Oldnew.topic.like('%' + k[2].replace('-','') + '%'))).count()        
        elif '-' not in k[0]  and '-' not in k[1] and '-' not in k[2]:
            pagination =Oldnew.query.filter(Oldnew.topic.like('%' + k[0] + '%')).filter(Oldnew.topic.like('%' + k[1] + '%')).filter(Oldnew.topic.like('%' + k[2] + '%')).order_by(Oldnew.timestamp.desc()).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
            count =Oldnew.query.filter(Oldnew.topic.like('%' + k[0] + '%')).filter(Oldnew.topic.like('%' + k[1] + '%')).filter(Oldnew.topic.like('%' + k[2] + '%')).count()
        else:
            flash('你有三个关键词，最多支持两个排除项(用‘-’表示)，排除项放到关键词最后，第一个必须是非排除搜索关键词。')
            return redirect(url_for('main.search'))
    elif len(k) == 4:
        if '-' not in k[0] and '-' in k[1] and '-' in k[2] and '-' in k[3]:
            pagination =Oldnew.query.filter(Oldnew.topic.like('%' + k[0] + '%')).filter(not_(Oldnew.topic.like('%' + k[1].replace('-','') + '%'))).filter(not_(Oldnew.topic.like('%' + k[2].replace('-','') + '%'))).filter(not_(Oldnew.topic.like('%' + k[3].replace('-','') + '%'))).order_by(Oldnew.timestamp.desc()).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
            count =Oldnew.query.filter(Oldnew.topic.like('%' + k[0] + '%')).filter(not_(Oldnew.topic.like('%' + k[1] + '%'))).filter(not_(Oldnew.topic.like('%' + k[2] + '%'))).filter(not_(Oldnew.topic.like('%' + k[3] + '%'))).count()
        elif '-' not in k[0] and '-' not in k[1] and '-' in k[2] and '-' in k[3]:
            pagination =Oldnew.query.filter(Oldnew.topic.like('%' + k[0] + '%')).filter(Oldnew.topic.like('%' + k[1] + '%')).filter(not_(Oldnew.topic.like('%' + k[2].replace('-','') + '%'))).filter(not_(Oldnew.topic.like('%' + k[3].replace('-','') + '%'))).order_by(Oldnew.timestamp.desc()).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
            count =Oldnew.query.filter(Oldnew.topic.like('%' + k[0] + '%')).filter(Oldnew.topic.like('%' + k[1] + '%')).filter(not_(Oldnew.topic.like('%' + k[2].replace('-','') + '%'))).filter(not_(Oldnew.topic.like('%' + k[3].replace('-','') + '%'))).count()        
        elif '-' not in k[0] and '-' not in k[1] and '-' not in k[2] and '-' in k[3]:
            pagination =Oldnew.query.filter(Oldnew.topic.like('%' + k[0] + '%')).filter(Oldnew.topic.like('%' + k[1] + '%')).filter(Oldnew.topic.like('%' + k[2] + '%')).filter(not_(Oldnew.topic.like('%' + k[3].replace('-','') + '%'))).order_by(Oldnew.timestamp.desc()).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
            count =Oldnew.query.filter(Oldnew.topic.like('%' + k[0] + '%')).filter(Oldnew.topic.like('%' + k[1] + '%')).filter(Oldnew.topic.like('%' + k[2] + '%')).filter(not_(Oldnew.topic.like('%' + k[3].replace('-','') + '%'))).count()        
        elif '-' not in k[0] and '-' not in k[0] and '-' not in k[1] and '-' not in k[2] and '-' in k[3]:
            pagination =Oldnew.query.filter(Oldnew.topic.like('%' + k[0] + '%')).filter(Oldnew.topic.like('%' + k[1] + '%')).filter(Oldnew.topic.like('%' + k[2] + '%')).filter(Oldnew.topic.like('%' + k[3] + '%')).order_by(Oldnew.timestamp.desc()).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
            count =Oldnew.query.filter(Oldnew.topic.like('%' + k[0] + '%')).filter(Oldnew.topic.like('%' + k[1] + '%')).filter(Oldnew.topic.like('%' + k[2] + '%')).filter(Oldnew.topic.like('%' + k[3] + '%')).count()
        else:
            flash('只支持最多4个关键词,关键词用空格隔开。最多支持两个排除项(用‘-’表示)，排除项放到关键词最后。第一个必须是非排除搜索关键词。')
            return redirect(url_for('main.search'))
    else:
        flash('只支持最多4个关键词。')
        return redirect(url_for('main.search'))
    posts = pagination.items
    if int(page) == 1 and form.search.data is None :
        if  count >= 1:
            if english == "yes":
                flash('Found ' + str(count) + ' items about "' + keyword + '"')
            else:
                flash('搜到' + str(count) + '条关于“' + keyword + '”结果!')
        else:
            if english == "yes":
                flash('No related results about "' + keyword + '"!')
            else:
                flash('没有关于“' + keyword + '”相关结果!')
    if form.validate_on_submit():
        keyword = form.search.data
        return redirect(url_for('main.found', keyword=keyword))
    return render_template('found.html', form=form, posts=posts, pagination=pagination,keyword=keyword,english=english)


@main.route('/search-blog', methods=['GET', 'POST'])
@login_required
def search_blog():
    english=request.cookies.get('english')
    if english == "yes":
        form = SearchFormE()
    else:
        form = SearchForm()
    if form.validate_on_submit():
        keyword = form.search.data
        return redirect(url_for('main.found_blog', keyword=keyword))
    return render_template('search_blog.html', form=form, english=english)


@main.route('/found-blog/<string:keyword>', methods=['GET', 'POST'])
def found_blog(keyword):
    english=request.cookies.get('english')
    page = request.args.get('page', 1, type=int)
    if english == "yes":
        form = SearchFormE()
    else:
        form = SearchForm()
    if form.search.data is not None:
        keyword = form.search.data
    k = keyword.strip().split(' ')
    if len(k) == 1:
        if '-' not in k[0]:
            pagination =Post.query.filter(Post.topic.like('%' + k[0] + '%')).order_by(Post.timestamp.desc()).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
            count =Post.query.filter(Post.topic.like('%' + k[0] + '%')).count()
        else:
            flash('第一个必须是非排除搜索关键词。')
            return redirect(url_for('main.search_blog'))
    elif len(k) == 2:
        if '-' not in k[0] and '-' in k[1]:
            pagination =Post.query.filter(Post.topic.like('%' + k[0] + '%')).filter(not_(Post.topic.like('%' + k[1].replace('-','') + '%'))).order_by(Post.timestamp.desc()).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
            count =Post.query.filter(Post.topic.like('%' + k[0] + '%')).filter(not_(Post.topic.like('%' + k[1].replace('-','') + '%'))).count()
        elif '-' not in k[0] and '-' not in k[1]:
            pagination =Post.query.filter(and_(Post.topic.like('%' + k[0] + '%'),Post.topic.like('%' + k[1] + '%'))).order_by(Post.timestamp.desc()).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
            count =Post.query.filter(Post.topic.like('%' + k[0] + '%')).filter(Post.topic.like('%' + k[1] + '%')).count()
        else:
            flash('-' not in k[0] and '-' in k[1])
            flash('排除项放到关键词最后。第一个必须是非排除搜索关键词。')
            return redirect(url_for('main.search_blog'))
    elif len(k) == 3:
        if '-' not in k[0] and '-' in k[1] and '-' in k[2]:
            pagination =Post.query.filter(Post.topic.like('%' + k[0] + '%')).filter(not_(Post.topic.like('%' + k[1].replace('-','') + '%'))).filter(not_(Post.topic.like('%' + k[2].replace('-','') + '%'))).order_by(Post.timestamp.desc()).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
            count =Post.query.filter(Post.topic.like('%' + k[0] + '%')).filter(not_(Post.topic.like('%' + k[1].replace('-','') + '%'))).filter(not_(Post.topic.like('%' + k[2].replace('-','') + '%'))).count()
        elif '-' not in k[0] and '-' not in k[1] and '-' in k[2]:
            pagination =Post.query.filter(Post.topic.like('%' + k[0] + '%')).filter(Post.topic.like('%' + k[1] + '%')).filter(not_(Post.topic.like('%' + k[2].replace('-','') + '%'))).order_by(Post.timestamp.desc()).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
            count =Post.query.filter(Post.topic.like('%' + k[0] + '%')).filter(Post.topic.like('%' + k[1] + '%')).filter(not_(Post.topic.like('%' + k[2].replace('-','') + '%'))).count()        
        elif '-' not in k[0]  and '-' not in k[1] and '-' not in k[2]:
            pagination =Post.query.filter(Post.topic.like('%' + k[0] + '%')).filter(Post.topic.like('%' + k[1] + '%')).filter(Post.topic.like('%' + k[2] + '%')).order_by(Post.timestamp.desc()).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
            count =Post.query.filter(Post.topic.like('%' + k[0] + '%')).filter(Post.topic.like('%' + k[1] + '%')).filter(Post.topic.like('%' + k[2] + '%')).count()
        else:
            flash('你有三个关键词，最多支持两个排除项(用‘-’表示)，排除项放到关键词最后，第一个必须是非排除搜索关键词。')
            return redirect(url_for('main.search_blog'))
    elif len(k) == 4:
        if '-' not in k[0] and '-' in k[1] and '-' in k[2] and '-' in k[3]:
            pagination =Post.query.filter(Post.topic.like('%' + k[0] + '%')).filter(not_(Post.topic.like('%' + k[1].replace('-','') + '%'))).filter(not_(Post.topic.like('%' + k[2].replace('-','') + '%'))).filter(not_(Post.topic.like('%' + k[3].replace('-','') + '%'))).order_by(Post.timestamp.desc()).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
            count =Post.query.filter(Post.topic.like('%' + k[0] + '%')).filter(not_(Post.topic.like('%' + k[1] + '%'))).filter(not_(Post.topic.like('%' + k[2] + '%'))).filter(not_(Post.topic.like('%' + k[3] + '%'))).count()
        elif '-' not in k[0] and '-' not in k[1] and '-' in k[2] and '-' in k[3]:
            pagination =Post.query.filter(Post.topic.like('%' + k[0] + '%')).filter(Post.topic.like('%' + k[1] + '%')).filter(not_(Post.topic.like('%' + k[2].replace('-','') + '%'))).filter(not_(Post.topic.like('%' + k[3].replace('-','') + '%'))).order_by(Post.timestamp.desc()).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
            count =Post.query.filter(Post.topic.like('%' + k[0] + '%')).filter(Post.topic.like('%' + k[1] + '%')).filter(not_(Post.topic.like('%' + k[2].replace('-','') + '%'))).filter(not_(Post.topic.like('%' + k[3].replace('-','') + '%'))).count()        
        elif '-' not in k[0] and '-' not in k[1] and '-' not in k[2] and '-' in k[3]:
            pagination =Post.query.filter(Post.topic.like('%' + k[0] + '%')).filter(Post.topic.like('%' + k[1] + '%')).filter(Post.topic.like('%' + k[2] + '%')).filter(not_(Post.topic.like('%' + k[3].replace('-','') + '%'))).order_by(Post.timestamp.desc()).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
            count =Post.query.filter(Post.topic.like('%' + k[0] + '%')).filter(Post.topic.like('%' + k[1] + '%')).filter(Post.topic.like('%' + k[2] + '%')).filter(not_(Post.topic.like('%' + k[3].replace('-','') + '%'))).count()        
        elif '-' not in k[0] and '-' not in k[0] and '-' not in k[1] and '-' not in k[2] and '-' in k[3]:
            pagination =Post.query.filter(Post.topic.like('%' + k[0] + '%')).filter(Post.topic.like('%' + k[1] + '%')).filter(Post.topic.like('%' + k[2] + '%')).filter(Post.topic.like('%' + k[3] + '%')).order_by(Post.timestamp.desc()).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
            count =Post.query.filter(Post.topic.like('%' + k[0] + '%')).filter(Post.topic.like('%' + k[1] + '%')).filter(Post.topic.like('%' + k[2] + '%')).filter(Post.topic.like('%' + k[3] + '%')).count()
        else:
            flash('只支持最多4个关键词,关键词用空格隔开。最多支持两个排除项(用‘-’表示)，排除项放到关键词最后。第一个必须是非排除搜索关键词。')
            return redirect(url_for('main.search_blog'))
    else:
        flash('只支持最多4个关键词。')
        return redirect(url_for('main.search_blog'))
    posts = pagination.items
    if int(page) == 1 and form.search.data is None :
        if  count >= 1:
            if english == "yes":
                flash('Found ' + str(count) + ' items about "' + keyword + '"')
            else:
                flash('搜到' + str(count) + '条关于“' + keyword + '”结果!')
        else:
            if english == "yes":
                flash('No related results about "' + keyword + '"!')
            else:
                flash('没有关于“' + keyword + '”相关结果!')
    if form.validate_on_submit():
        keyword = form.search.data
        return redirect(url_for('main.found_blog', keyword=keyword))
    return render_template('foundblogs.html', form=form, posts=posts, pagination=pagination,keyword=keyword,english=english)


@main.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint \
                and request.endpoint[:5] != 'main.' \
                and request.endpoint != 'static':
            return redirect(url_for('main.unconfirmed'))


@main.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('unconfirmed.html')

@main.route('/.well-known/pki-validation/fileauth.txt')
def authfile():
    return render_template('fileauth.txt')

@main.route('/login', methods=['GET', 'POST'])
def login():
    english=request.cookies.get('english')
    if english == "yes":
        form = LoginFormE()
    else:
        form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            if user.confirmed:
                login_user(user, form.remember_me.data)
                try:
                    #socket.setdefaulttimeout(5)
                    if user.avatar_file == None:
                        size = 200
                        default='identicon'
                        rating='g'
                        url = 'http://www.gravatar.com/avatar'
                        img_url = '{url}/{hash}?s={size}&d={default}&r={rating}'.format(url=url, hash=user.avatar_hash, size=size, default=default, rating=rating)
                        # http://www.gravatar.com/avatar/b873c31f4b49a64628d3eb1311afb80c?s=100&d=identicon&r=g
                        response = requests.get(img_url, timeout=5)
                        filename1 = user.email.replace('@','__').replace('.','__') + str(random.randint(0,10000)) + '.png'

                        with open(os.path.join('app/static', 'avatar', filename1), 'wb') as f:
                            f.write(response.content)
                            f.close()

                        user.avatar_file = url_for('static', filename='%s/%s' % ('avatar', filename1))
                        db.session.commit()
                except:
                    if user.avatar_file == None:
                        if english == "yes":
                            flash('Please upload avatar.')
                        else:
                            flash('请上传头像。')
                if user.teacher == 1:
                    lessons = Lesson.query.filter_by(teacher_id = user.id)
                    for lesson in lessons:
                        newlessons = NewLesson.query.filter_by(lesson_id = lesson.id)
                        for newlesson in newlessons:
                            students = Student.query.filter(Student.newlesson_id == newlesson.id).filter(Student.confirm == 0)
                            for student in students:
                                flash(student.id)
                                flash(newlesson.about)
                                flash("https://wujiangang.space/current-lesson/"+str(newlesson.id))
                return redirect(request.args.get('next') or url_for('main.index'))
            else:
                login_user(user, form.remember_me.data)
                if english == "yes":
                    flash("Please enter you mailbox to click to confirm or you may need to resend an Email to confirmed your email.")
                else:
                    flash('请进入邮箱点击确认即可登陆或者再次发送邮件确认您的账户。')
                return render_template('unconfirmed.html', form=form, english=english)
        if english == "yes":
            flash('Invalid username or password.')
        else:
            flash('用户名或密码不准确。')
    return render_template('login.html', form=form, english=english)
            


@main.route('/logout')
@login_required
def logout():
    english=request.cookies.get('english')
    logout_user()
    if english == "yes":
        flash('You have logged out.')
    else:
        flash('您已经登出了。')
    return redirect(url_for('main.index'))

@main.route('/set-cookie-english')
def set_cookie_english():
    english=request.cookies.get('english')
    outdate=datetime.today() + timedelta(days=30)  
    resp = current_app.make_response(redirect(url_for('main.index',english=english)))
    if english == "yes":
        resp.set_cookie('english','no',expires=outdate)
    else:
        resp.set_cookie('english','yes',expires=outdate)
    return  resp


@main.route('/register', methods=['GET', 'POST'])
def register():
    english=request.cookies.get('english')
    if english == "yes":
        form = RegistrationFormE()
    else:
        form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        u = User.query.filter_by(username=form.username.data).first()
        f = Follow.query.filter_by(followed_id=u.id).filter_by(follower_id=u.id).first()
        if f != None:
            db.session.delete(f)
            db.session.commit()
        token = user.generate_confirmation_token()
        if english == "yes":
            send_email(user.email, 'Please confirm your account.',
                   'email/confirm', user=user, token=token)
            flash('Email has been sent. Please confirm your account.')
        else:
            send_email(user.email, '请确认您的登陆帐户',
                   'email/confirm', user=user, token=token)
            flash('确认邮件已经发出，请到您的邮箱确认您的账户。')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form,english=english)


@main.route('/confirm/<email>/<token>')
def confirm(email, token):
    english=request.cookies.get('english')
    user = User.query.filter(User.email==email).first()
    if user.confirmed:
        return redirect(url_for('main.index'))
    if english == "yes":
        if user.confirm(token):

            try:
                size = 200
                default='identicon'
                rating='g'
                if request.is_secure:
                    url = 'https://secure.gravatar.com/avatar'
                else:
                    url = 'http://www.gravatar.com/avatar'
                    hash = user.avatar_hash or hashlib.md5(
                        user.email.encode('utf-8')).hexdigest()
                img_url = '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
                        url=url, hash=hash, size=size, default=default, rating=rating)
                # http://www.gravatar.com/avatar/b873c31f4b49a64628d3eb1311afb80c?s=100&d=identicon&r=g
                response = requests.get(img_url, timeout=3)
                filename1 = user.email.replace('@','__').replace('.','__') + str(random.randint(0,10000)) + '.png'

                with open(os.path.join('app/static', 'avatar', filename1), 'wb') as f:
                    f.write(response.content)
                    f.close()
                user.avatar_file = url_for('static', filename='%s/%s' % ('avatar', filename1))
            except:
                pass


            db.session.commit()
 

            flash('You have confirmed your account. Please update your profile before you can select any class.')
        else:
            flash('The link for confirmation has become invalid.')
            return redirect(url_for('main.unconfirmed'))            
    else:
        if user.confirm(token):
            try:
                size = 200
                default='identicon'
                rating='g'
                if request.is_secure:
                    url = 'https://secure.gravatar.com/avatar'
                else:
                    url = 'http://www.gravatar.com/avatar'
                    hash = user.avatar_hash or hashlib.md5(
                        user.email.encode('utf-8')).hexdigest()
                img_url = '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
                        url=url, hash=hash, size=size, default=default, rating=rating)
                # http://www.gravatar.com/avatar/b873c31f4b49a64628d3eb1311afb80c?s=100&d=identicon&r=g
                response = requests.get(img_url, timeout=3)
                filename1 = user.email.replace('@','__').replace('.','__') + str(random.randint(0,10000)) + '.png'

                with open(os.path.join('app/static', 'avatar', filename1), 'wb') as f:
                    f.write(response.content)
                    f.close()
                user.avatar_file = url_for('static', filename='%s/%s' % ('avatar', filename1))
            except:
                pass

            db.session.commit()
 
            flash('您已经确认了您的账户。谢谢！另外，完善资料后可以选课或登记为老师。')

        else:
            flash('确认链接已经失效或过期。')
            return redirect(url_for('main.unconfirmed'))
    return redirect(url_for('main.login'))


@main.route('/confirm')
@login_required
def resend_confirmation():
    english=request.cookies.get('english')
    token = current_user.generate_confirmation_token()
    if english == "yes":
        send_email(current_user.email, 'Please confirm your account.',
                   'email/confirm', user=current_user, token=token)
        flash('A new confirmaiton Email has sent to your mailbox.')
    else:
        send_email(current_user.email, '请确认您的登陆账户',
           'email/confirm', user=current_user, token=token)
        flash('一个新的确认邮件已经发送到您的邮箱。')

    return redirect(url_for('main.index'))

@main.route('/baidu_verify_6dD5VXSUuK.html')
def baidu_verify_6dD5VXSUuK():
    return render_template("baidu_verify_6dD5VXSUuK.html")

@main.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    english=request.cookies.get('english')
    if english == "yes":
        form = ChangePasswordFormE()
    else:
        form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            if english == "yes":
                flash('Your password has been updated.')
            else:
                flash('您的密码已经更新了。')
            return redirect(url_for('main.index'))
        else:
            if english == "yes":
                flash('Invalid password.')
            else:
                flash('密码无效。')
    return render_template("change_password.html", form=form,english=english)


@main.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    english=request.cookies.get('english')
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    if english == "yes":
        form = PasswordResetRequestFormE()
    else:
        form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            if english == "yes":
                send_email(user.email, 'Please confirm your password resetting.',
                       'email/reset_password',
                       user=user, token=token,
                       next=request.args.get('next'))
                flash('The password resetting Email has been sent to your mailbox.')
            else:
                send_email(user.email, '请确认密码的重设',
                       'email/reset_password',
                       user=user, token=token,
                       next=request.args.get('next'))
                flash('重设密码的确认邮件已经发送到您的邮箱。')
        return redirect(url_for('main.login'))
    return render_template('reset_password.html', form=form,english=english)


@main.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    english=request.cookies.get('english')
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    if english == "yes":
        form = PasswordResetFormE()
    else:
        form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            return redirect(url_for('main.index'))
        if user.reset_password(token, form.password.data):
            if english == "yes":
                flash('The password has been updated.')
            else:
                flash('密码已经更新。')
            return redirect(url_for('main.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('reset_password.html', form=form,english=english)


@main.route('/change-email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    english=request.cookies.get('english')
    if english == "yes":
        form = ChangeEmailFormE()
    else:
        form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            if english == "yes":
                send_email(new_email, 'Please confirm your new Email.',
                           'email/change_email',
                           user=current_user, token=token)
                flash('A confirmation Email has been sent to you mailbox.')
            else:
                send_email(new_email, '请确认您的邮箱更换',
                           'email/change_email',
                           user=current_user, token=token)
                flash('确认新邮箱的电子邮件已经发送到您的新邮箱。')
                
            return redirect(url_for('main.index'))
        else:
            if english == "yes":
                flash('Invalid password or username.')
            else:
                flash('用户名或密码无效。')
    return render_template("change_email.html", form=form,english=english)


@main.route('/change-email/<token>')
@login_required
def change_email(token):
    english=request.cookies.get('english')
    if current_user.change_email(token):
        if english == "yes":
            flash('Your new Email has been updated.')
        else:
            flash('您的邮箱已经更新了。')
    else:
        if english == "yes":
            flash('Invalid request.')
        else:
            flash('请求无效。')
    return redirect(url_for('main.index'))


@main.route('/edit-avatar', methods=['GET', 'POST'])
@login_required
def change_avatar():
    english=request.cookies.get('english')
    if request.method == 'POST':
        file = request.files['file']
        size = (1024, 1024)
        im = Image.open(file)
        im.thumbnail(size)
        
        if file and allowed_file(file.filename):
            filename1 = current_user.email.replace('@','__').replace('.','__') + str(random.randint(0,10000)) + '.' + file.filename.split('.')[-1]
            im.save(os.path.join('app/static', 'avatar', filename1))
            current_user.avatar_file = url_for('static', 
                                               filename='%s/%s' % ('avatar', filename1))
            db.session.commit()
            current_user.is_avatar_default = False
            if english == "yes":
                flash('The portrait has been updated.')
            else:
                flash('头像修改成功')
            return redirect(url_for('main.user', username=current_user.username))
    return render_template('change_avatar.html',english=english)


@main.route('/edit-pic', methods=['GET', 'POST'])
@login_required
def change_pic():
    english=request.cookies.get('english')
    if request.method == 'POST':
        file = request.files['file']
        size = (1024, 1024)
        im = Image.open(file)
        im.thumbnail(size)
        teacher = Teacher.query.filter_by(teacher_id=current_user.id).first()
        
        if file and allowed_file(file.filename):
            filename1 = current_user.email.replace('@','__').replace('.','__') + '.' + file.filename.split('.')[-1]
            im.save(os.path.join('app/static', 'teacher_pic', filename1))
            teacher.pic = url_for('static',filename='%s/%s' % ('teacher_pic', filename1))
            db.session.commit()
            current_user.is_avatar_default = False
            if english == "yes":
                flash('The portrait has been updated.')
            else:
                flash('头像修改成功')
            return redirect(url_for('main.teacher', id=current_user.id))
    return render_template('change_pic.html',english=english)

@main.route('/edit-lesson-pic/<int:id>', methods=['GET', 'POST'])
@login_required
def change_lesson_pic(id):
    english=request.cookies.get('english')
    if request.method == 'POST':
        file = request.files['file']
        size = (1024, 1024)
        im = Image.open(file)
        im.thumbnail(size)
        lesson = Lesson.query.filter_by(id=id).first()    
        if file and allowed_file(file.filename):
            filename = file.filename
            filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' + str(time.time()).replace('.','_') + '.' + filename.split('.')[-1]
            im.save(os.path.join('app/static', 'lesson', filename1))
            try:
                os.remove("/root/cryptoepoch/app"+lesson.pic)
            except:
                pass

            lesson.pic = url_for('static',filename='%s/%s' % ('lesson', filename1))
            db.session.commit()
            current_user.is_avatar_default = False
            if english == "yes":
                flash('The portrait has been updated.')
            else:
                flash('课程封面修改成功')
            return redirect(url_for('main.lesson', id=id))
    return render_template('change_lesson_pic.html',english=english)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    english=request.cookies.get('english')
    if english == "yes":
        form = EditProfileFormE()
    else:
        form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.student_no = form.student_no.data
        current_user.tel = form.tel.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        if english == "yes":
            flash('Your profile has been updated.')
        else:
            flash('您的资料已经更新了。现在您可以选课或登记为老师。')
        return redirect(url_for('main.user', username=current_user.username))
    form.name.data = current_user.name
    form.student_no.data = current_user.student_no
    form.tel.data = current_user.tel
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form,english=english)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    english=request.cookies.get('english')
    user = User.query.get_or_404(id)
    if english == "yes":
        form = EditProfileAdminFormE(user=user)
    else:
        form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        if english == "yes":
            flash('The profile has been updated.')
        else:
            flash('您的资料已经更新了。')
        return redirect(url_for('main.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user,english=english)


@main.route('/add-teacher', methods=['GET', 'POST'])
@login_required
def add_teacher():
    english=request.cookies.get('english')
    if english == "yes":
        form = AddTeacherFormE()
    else:
        form = AddTeacherForm()
    teacher = Teacher()
    if form.validate_on_submit():
        teacher.teacher_id = current_user.id
        teacher.school = form.school.data
        teacher.field = form.field.data
        teacher.about_teacher = form.about_teacher.data
        current_user.teacher = True
        if english == "yes":
            flash("Your teacher's profile has been created.")
        else:
            flash('您的教师资料已经登记，你可以进入老师主页开课了。')
        db.session.add(teacher)        
        return redirect(url_for('main.teacher',id=current_user.id))
    return render_template("add_teacher.html",form=form,english=english)


@main.route('/edit-teacher/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_teacher(id):
    english=request.cookies.get('english')
    teacher = Teacher.query.filter_by(teacher_id=id).first()
    if english == "yes":
        form = AddTeacherFormE()
    else:
        form = AddTeacherForm()
    if form.validate_on_submit():
        teacher.school = form.school.data
        teacher.field = form.field.data
        teacher.about_teacher = form.about_teacher.data
        db.session.commit()
        if english == "yes":
            flash('The profile has been updated.')
        else:
            flash('您的资料已经更新了。') 
        return redirect(url_for('main.teacher',id=current_user.id))
    form.school.data = teacher.school
    form.field.data = teacher.field
    form.about_teacher.data = teacher.about_teacher
    return render_template("edit_teacher.html",form=form,teacher=teacher,english=english)
           
           
           
@main.after_app_request
def after_request(response):
    english=request.cookies.get('english')
    for query in get_debug_queries():
        if query.duration >= current_app.config['FLASKY_SLOW_DB_QUERY_TIME']:
            if english == "yes":
                current_app.logger.warning(
                'Query is slow %s\n Parmeters: %s\n Time: %fs\ Context: %s\n'
                % (query.statement, query.parameters, query.duration,
                   query.context))
            else:
                current_app.logger.warning(
                '查询缓慢：%s\n参数：%s\n时间：%fs\n上下文：%s\n'
                % (query.statement, query.parameters, query.duration,
                   query.context))
    return response


@main.route('/shutdown')
def server_shutdown():
    english=request.cookies.get('english')
    if not current_app.testing:
        abort(404)
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if not shutdown:
        abort(500)
    shutdown()
    if english == "yes":
        return "Closing..."
    else:
        return '关闭中...'


@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('moderate.html', comments=comments,
                           pagination=pagination, page=page)


@main.route('/moderate/enable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_enable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    return redirect(url_for('.moderate',
                            page=request.args.get('page', 1, type=int)))


@main.route('/moderate/disable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_disable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    return redirect(url_for('.moderate',
                            page=request.args.get('page', 1, type=int)))



@main.route('/markdown')
def markdown():
    english=request.cookies.get('english')
    return render_template("markdown.html", english=english)

@main.route('/about2')
def about2():
    english=request.cookies.get('english')
    return render_template("about.html", english=english)

@main.route('/wujiangang')
def wujiangang():
    english=request.cookies.get('english')
    return render_template("wujiangang.html", english=english)

@main.route('/jiangangwu')
def jiangangwu():
    english=request.cookies.get('english')
    return render_template("jiangangwu.html", english=english)


@main.route('/blog', methods=['GET', 'POST'])
def blog():
    english=request.cookies.get('english')
    values = CombinedMultiDict([flask.request.files,flask.request.form])
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.filter(Post.private == False).\
                          order_by(Post.timestamp.desc()).paginate(
                          page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                                                           error_out=False)
    posts = pagination.items
    return render_template('blog.html', posts=posts,
                           show_followed=show_followed, pagination=pagination, english=english)

@main.route('/', methods=['GET', 'POST'])
def index():
    english=request.cookies.get('english')
    values = CombinedMultiDict([flask.request.files,flask.request.form])
    page = request.args.get('page', 1, type=int)
    pagination =New.query.order_by(New.timestamp.desc()).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
    # pagination = Post.query.filter(Post.private == False).\
                          # order_by(Post.timestamp.desc()).paginate(
                          # page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                          #                                  error_out=False)
    posts = pagination.items
    return render_template('index.html', posts=posts,
                           show_followed=show_followed, pagination=pagination, english=english)

@main.route('/followed', methods=['GET', 'POST'])
def followed():
    english=request.cookies.get('english')
    values = CombinedMultiDict([flask.request.files,flask.request.form])
    page = request.args.get('page', 1, type=int)
    show_followed = False
    if current_user.is_authenticated:
        pagination = current_user.followed_posts.filter(Post.private == False).\
                          order_by(Post.timestamp.desc()).paginate(
                          page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                                                           error_out=False)
    posts = pagination.items
    return render_template('followed.html', posts=posts,
                           show_followed=show_followed, pagination=pagination, english=english)


@main.route('/news', methods=['GET', 'POST'])
def news():
    english=request.cookies.get('english')
    page = request.args.get('page', 1, type=int)
    if english == "yes":
        pagination = Post.query.filter(Post.private == False).filter(Post.tag.in_(["news"])).filter(Post.lang=="en").\
                          order_by(Post.timestamp.desc()).paginate(
                          page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                                                           error_out=False)
    else:
        pagination = Post.query.filter(Post.private == False).filter(Post.tag.in_(['news'])).filter(Post.lang=="cn").\
                          order_by(Post.timestamp.desc()).paginate(
                          page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                                                           error_out=False)
    posts = pagination.items
    return render_template('news.html', posts=posts,
                           show_followed=show_followed, pagination=pagination, english=english)



@main.route('/research', methods=['GET', 'POST'])
def research():
    english=request.cookies.get('english')
    page = request.args.get('page', 1, type=int)
    if english == "yes":
        pagination = Post.query.filter(Post.private == False).filter(Post.tag == "research").filter(Post.lang=="en").\
                          order_by(Post.timestamp.desc()).paginate(
                          page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
    else:
        pagination = Post.query.filter(Post.private == False).filter(Post.tag == "research").filter(Post.lang=="cn").\
                          order_by(Post.timestamp.desc()).paginate(
                          page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
    posts = pagination.items
    return render_template('research.html', posts=posts,
                           show_followed=show_followed, pagination=pagination, english=english)


@main.route('/rating', methods=['GET', 'POST'])
def rating():
    english=request.cookies.get('english')
    values = CombinedMultiDict([flask.request.files,flask.request.form])
    page = request.args.get('page', 1, type=int)
    if english == "yes":
        pagination = Post.query.filter(Post.private == False).filter(Post.tag == "rating").filter(Post.lang=="en").\
                          order_by(Post.timestamp.desc()).paginate(
                          page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False)
    else:
        pagination = Post.query.filter(Post.private == False).filter(Post.tag == "rating").filter(Post.lang=="cn").\
                          order_by(Post.timestamp.desc()).paginate(
                          page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False)

    posts = pagination.items
    return render_template('rating.html',  posts=posts,
                           show_followed=show_followed, pagination=pagination, english=english)

@main.route('/guide', methods=['GET', 'POST'])
def guide():
    english=request.cookies.get('english')
    values = CombinedMultiDict([flask.request.files,flask.request.form])
    page = request.args.get('page', 1, type=int)
    if english == "yes":
        pagination = Post.query.filter(Post.private == False).filter(Post.tag == "guide").filter(Post.lang=="en").\
                          order_by(Post.timestamp.desc()).paginate(
                          page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                                                           error_out=False)
    else:
        pagination = Post.query.filter(Post.private == False).filter(Post.tag == "guide").filter(Post.lang=="cn").\
                          order_by(Post.timestamp.desc()).paginate(
                          page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                                                           error_out=False)
    posts = pagination.items
    return render_template('guide.html',  posts=posts,
                           show_followed=show_followed, pagination=pagination, english=english)



@main.route('/document', methods=['GET', 'POST'])
def document():
    english=request.cookies.get('english')
    values = CombinedMultiDict([flask.request.files,flask.request.form])
    page = request.args.get('page', 1, type=int)
    if english == "yes":
        pagination = Post.query.filter(Post.private == False).filter(Post.tag == "document").filter(Post.lang=="en").\
                          order_by(Post.timestamp.desc()).paginate(
                          page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                                                           error_out=False)
    else:
        pagination = Post.query.filter(Post.private == False).filter(Post.tag == "document").filter(Post.lang=="cn").\
                          order_by(Post.timestamp.desc()).paginate(
                          page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                                                           error_out=False)
    posts = pagination.items
    return render_template('document.html', posts=posts,
                           show_followed=show_followed, pagination=pagination, english=english)



@main.route('/basic', methods=['GET', 'POST'])
def basic():
    english=request.cookies.get('english')
    values = CombinedMultiDict([flask.request.files,flask.request.form])
    page = request.args.get('page', 1, type=int)
    if english == "yes":
        pagination = Post.query.filter(Post.private == False).filter(Post.tag == "basic").filter(Post.lang=="en").\
                          order_by(Post.timestamp.desc()).paginate(
                          page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                                                           error_out=False)
    else:
        pagination = Post.query.filter(Post.private == False).filter(Post.tag == "basic").filter(Post.lang=="cn").\
                          order_by(Post.timestamp.desc()).paginate(
                          page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                                                           error_out=False)
    posts = pagination.items
    return render_template('basic.html', posts=posts,
                           show_followed=show_followed, pagination=pagination, english=english)

@main.route('/suggestion')
@login_required
def suggestion():
    english=request.cookies.get('english')
    page = request.args.get('page', 1, type=int)
    if english == "yes":
        pagination = current_user.posts.filter(Post.tag == 'suggestion').filter(Post.lang=="en").\
                          order_by(Post.timestamp.desc()).paginate(
                          page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                                                           error_out=False)
    else:
        pagination = current_user.posts.filter(Post.tag == 'suggestion').filter(Post.lang=="cn").\
                          order_by(Post.timestamp.desc()).paginate(
                          page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                                                           error_out=False)
    posts = pagination.items
    return render_template('suggestion.html', posts=posts,
                           pagination=pagination, english=english)

@main.route('/conference')
def conference():
    english=request.cookies.get('english')
    page = request.args.get('page', 1, type=int)
    if english == "yes":
        pagination = Post.query.filter(Post.tag == 'conference').filter(Post.lang=="en").\
                          order_by(Post.timestamp.desc()).paginate(
                          page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                                                           error_out=False)
    else:
        pagination = Post.query.filter(Post.tag == 'conference').filter(Post.lang=="cn").\
                          order_by(Post.timestamp.desc()).paginate(
                          page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                                                           error_out=False)
    posts = pagination.items
    return render_template('conference.html', posts=posts,
                           pagination=pagination, english=english)


@main.route('/about', methods=['GET', 'POST'])
def about():
    english=request.cookies.get('english')
    page = request.args.get('page', 1, type=int)
    if english == "yes":
        pagination = Post.query.filter(Post.private == False).filter(Post.tag == "about").filter(Post.lang=="en").\
                          order_by(Post.timestamp.desc()).paginate(
                          page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                                                           error_out=False)
    else:
        pagination = Post.query.filter(Post.private == False).filter(Post.tag == "about").filter(Post.lang=="cn").\
                          order_by(Post.timestamp.desc()).paginate(
                          page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                                                           error_out=False)
    posts = pagination.items
    return render_template('about.html', posts=posts,
                           show_followed=show_followed, pagination=pagination, english=english)



@main.route('/show-followed')
@login_required
def show_followed():
    resp = make_response(redirect(url_for('.blog')))
    resp.set_cookie('show_followed', '1', max_age=30*24*60*60)
    return resp


@main.route('/user/<username>')
@login_required
def user(username):
    english=request.cookies.get('english')
    page = request.args.get('page', 1, type=int)
    users = User.query.filter(User.id > 0).order_by(User.id.desc()).all()
    user = User.query.filter_by(username=username).first_or_404()
    atme_bodies = []
    mylessons = []
    openedlessons = Lesson.query.filter_by(teacher_id=user.id).order_by(Lesson.timestamp.desc()).all()
    students = []
    students = Student.query.filter_by(student_id=user.id).order_by(Student.timestamp.desc()).all() 
    mylessons = []
    if students:    
        for s in students:
            newlesson = NewLesson.query.filter_by(id=s.newlesson_id).first()
            if newlesson:
                lesson = Lesson.query.filter_by(id=newlesson.lesson_id).first()
                if lesson:
                    mylessons.append([newlesson,lesson])
    show_my_private = request.cookies.get('show_my_private')
    if show_my_private == None:
        show_my_private = "0"
    if current_user.username != username and show_my_private == "1":
        show_my_private = "0"
    if username in ['链得得','币快报','Coindex','金色财经','Cryptopotato','Cointelegraph','巴比特','Thebitcoinnews']:
        pagination = user.news.order_by(New.timestamp.desc()).paginate(
            page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
            error_out=False)
        postlength = len(user.news.all())
        posts = pagination.items
        show_news = 1
    else:        
        pagination = user.posts.filter(Post.private == False).order_by(Post.timestamp.desc()).paginate(
            page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
            error_out=False)
        postlength = len(user.posts.all())
        posts = pagination.items
        show_news = 0
    atmes = AtMe.query.filter_by(username_ated=username).order_by(AtMe.timestamp.desc()).all()

    pagination_private = user.posts.filter(Post.private == True).order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts_private = pagination_private.items

    pagination_posts_atme = Post.query.filter(Post.at_names.ilike('%'+current_user.username+'%')).order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts_atme = pagination_posts_atme.items

    
    if atmes != None:
        for atme in atmes:
            comment = Comment.query.filter_by(id=atme.comment_id).first()
            atme_bodies.append([atme,comment])
    pagination_atme = AtMe.query.filter_by(username_ated=username).paginate(page, \
                                        per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                                                           error_out=False)
    if user.teacher == 1:
        lessons = Lesson.query.filter_by(teacher_id = user.id)
        for lesson in lessons:
            newlessons = NewLesson.query.filter_by(lesson_id = lesson.id)
            for newlesson in newlessons:
                students = Student.query.filter(Student.newlesson_id == newlesson.id).filter(Student.confirm == 0)
                for student in students:
                    flash(student.id)
                    flash(newlesson.about)
                    flash("https://wujiangang.space/current-lesson/"+str(newlesson.id))


    return render_template('user.html', user=user, users=users, atme_bodies=atme_bodies,posts=posts,posts_private=posts_private,openedlessons=openedlessons, postlength=postlength,show_news=show_news,pagination=pagination,pagination_private=pagination_private,pagination_atme=pagination_atme,pagination_posts_atme=pagination_posts_atme,posts_atme=posts_atme,show_my_private=show_my_private, mylessons=mylessons,english=english)


@main.route('/user3/<username>')
@login_required
def user3(username):
    english=request.cookies.get('english')
    page = request.args.get('page', 1, type=int)
    users = User.query.filter(User.id > 0).order_by(User.id.desc()).all()
    user = User.query.filter_by(username=username).first_or_404()
    atme_bodies = []
    mylessons = []
    openedlessons = Lesson.query.filter_by(teacher_id=user.id).order_by(Lesson.timestamp.desc()).all()
    students = []
    students = Student.query.filter_by(student_id=user.id).order_by(Student.timestamp.desc()).all() 
    mylessons = []
    if students != []:    
        for s in students:
            newlesson = NewLesson.query.filter_by(id=s.newlesson_id).first()
            lesson = Lesson.query.filter_by(id=newlesson.lesson_id).first()
            mylessons.append([newlesson,lesson])
    show_my_private = request.cookies.get('show_my_private', '')
    if show_my_private == None:
        show_my_private = "0"
    if current_user.username != username and show_my_private == "1":
        show_my_private = "0"        
    pagination = user.posts.filter(Post.private == False).order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    atmes = AtMe.query.filter_by(username_ated=username).order_by(AtMe.timestamp.desc()).all()

    pagination_private = user.posts.filter(Post.private == True).order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts_private = pagination_private.items

    if atmes != None:
        for atme in atmes:
            comment = Comment.query.filter_by(id=atme.comment_id).first()
            atme_bodies.append([atme,comment])
    pagination_atme = AtMe.query.filter_by(username_ated=username).paginate(page, \
                                        per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                                                           error_out=False)



    ##########################
    # 将数据导出到mysql数据库  #
    ##########################

    if current_user.can(Permission.ADMINISTER):
        
        ## 删除不想要的帖子

        # posts_to_del = [11101, 12822, 18760, 19988, 25529, 25540, 25544, 27444, 30975, 32096, 28490,	28491,	28492,	28493,	28494,	28495,	28496,	28497,	28498,	28499,	28500,	28501,	28502,	28503,	28504,	28505,	28506, 32958, 32921]
        # for id1 in posts_to_del:
        #     try:
        #         post1 = Post.query.filter(Post.id == id1).first()
        #         db.session.delete(post1)
        #         db.session.commit()
        #     except Exception as e:
        #         flash(str(e)+"--删除失败" + ": " + str(id1))

        # # 清理外键不一致的表

        # students = Student.query.filter(Student.id > 0).all()
        # for s in students:
        #     user = User.query.filter(User.id==s.student_id).first()
        #     if user is None:
        #         flash("student:"+str(s.id)) #student:262
        #         db.session.delete(s)
        #         db.session.commit()
        # newlessons = NewLesson.query.filter(NewLesson.id > 0).all()
        # for n in newlessons:
        #     newlesson = Lesson.query.filter(Lesson.id==n.lesson_id).first()
        #     if newlesson is None:
        #         flash("newlesson:"+str(n.id)) # 
        #         db.session.delete(n)
        #         db.session.commit()
        # atmes = AtMe.query.filter(AtMe.id > 0).all()
        # for a in atmes:
        #     atme1 = User.query.filter(User.username==a.username_ated).first()
        #     atme2 = Comment.query.filter(Comment.id==a.comment_id).first()
        #     if atme1 is None or atme2 is None:
        #         flash("atmes:"+str(a.id)) # 
        #         db.session.delete(a)
        #         db.session.commit()
        # comments = Comment.query.filter(Comment.id > 0).all()
        # for c in comments:
        #     comment1 = User.query.filter(User.id==c.author_id).first()
        #     comment2 = Post.query.filter(Post.id==c.post_id).first()
        #     if comment1 is None or comment2 is None:
        #         flash("comment:"+str(c.id)) # 
        #         db.session.delete(c)
        #         db.session.commit()
        # comments = Comment.query.filter(Comment.id > 0).all()
        # for c in comments:
        #     comment1 = User.query.filter(User.id==c.author_id).first()
        #     comment2 = Post.query.filter(Post.id==c.post_id).first()
        #     if comment1 is None or comment2 is None:
        #         flash("comment:"+str(c.id)) # 
        #         db.session.delete(c)
        #         db.session.commit()
        # follows = Follow.query.filter(Follow.follower_id > 0).all()
        # for f in follows:
        #     follow1 = User.query.filter(User.id==f.follower_id).first()
        #     follow2 = User.query.filter(User.id==f.followed_id).first()
        #     if follow1 is None or follow2 is None:
        #         flash("follow follower_id:"+str(f.follower_id)) # 
        #         db.session.delete(f)
        #         db.session.commit()
        # collectposts = CollectPost.query.filter(CollectPost.user_id > 0).all()
        # # 不知道为什么，要进行两次atmes检查，才能删除完成
        # for a in atmes:
        #     atme1 = User.query.filter(User.username==a.username_ated).first()
        #     atme2 = Comment.query.filter(Comment.id==a.comment_id).first()
        #     if atme1 is None or atme2 is None:
        #         flash("atmes:"+str(a.id)) # 
        #         db.session.delete(a)
        #         db.session.commit()
        # for c in collectposts:
        #     collectpost1 = User.query.filter(User.id==c.user_id).first()
        #     collectpost2 = Post.query.filter(Post.id==c.post_id).first()
        #     if collectpost1 is None or collectpost2 is None:
        #         flash("collection user_id:"+str(c.user_id)) # 
        #         db.session.delete(c)
        #         db.session.commit()
                
        # posts = Post.query.filter(Post.id > 0).all()
        # for p in posts:
        #     user1 = User.query.filter(User.id==p.author_id).first()
        #     if user1 is None:
        #         flash("post:"+str(p.id)) # post:5221
        #         db.session.delete(p)
        #         db.session.commit()
        
        # post1 = Post.query.filter_by(id=5221).first()
        # post1.auther_id = 437
        # post1.time = "2019-11-18 20:43:29"
        # db.session.commit()
        # flash("已经理新post：5221")


        # 准备mysql
        import pymysql
        pymysql.install_as_MySQLdb()
        # import MySQLdb
        mysql_database = "myspace_dev"
        db_mysql = pymysql.connect(host="localhost", user="wjg", password="Wjg@19760209", database=mysql_database, charset='utf8' )
        cursor = db_mysql.cursor()
        cursor.execute("SET GLOBAL FOREIGN_KEY_CHECKS=0;") 
        db_mysql.commit()
        db_mysql.close()
        db_mysql = pymysql.connect(host="localhost", user="wjg", password="Wjg@19760209", database=mysql_database, charset='utf8' )
        db_mysql.text_factory = str
        cursor = db_mysql.cursor()

        # 删除外键约束
        fk_names = ["users_ibfk_1","teachers_ibfk_1","students_ibfk_1","students_ibfk_2","posts_ibfk_1","newlessons_ibfk_1","lessons_ibfk_1","lessonfiles_ibfk_1","follows_ibfk_1","follows_ibfk_2","comments_ibfk_1","comments_ibfk_2","collectposts_ibfk_1","collectposts_ibfk_2","atmes_ibfk_1","atmes_ibfk_2","atmes_ibfk_3"]
        for f in fk_names:
            try:
                sql = "alter table `" + f.split("_")[0] + "` drop constraint `" + f + "`;"
                cursor.execute(sql)
                flash(sql)
            except Exception as e:
                flash(str(e) + ": " + sql)

        # 将自临时删除自增加约束
        ai_tables = ['atmes','comments','collectposts','follows','lessonfiles','lessons','newlessons','posts','roles','students','teachers','users']
        for ai in ai_tables:
            sql = "ALTER TABLE `" + ai + "` CHANGE COLUMN `id` `id` INT NOT NULL;"
            try:
                cursor.execute(sql)
            except Exception as e:
                flash(str(e) + ": " + sql)
        db_mysql.commit()

        # 将body从TEXT（只能写64K）调整为MEDIUMTEXT
        cursor.execute("ALTER TABLE `posts` CHANGE COLUMN `body` `body` MEDIUMTEXT NULL DEFAULT NULL ,CHANGE COLUMN `body_html` `body_html` MEDIUMTEXT NULL DEFAULT NULL ;")
        db_mysql.commit()
        
        #roles
        #cursor.execute("truncate  table roles;")
        cursor.execute("select count(*)  from roles;")
        a = cursor.fetchone()
        flash("roles: " + str(a[0]))
        if a[0] == 0:
            roles = Role.query.filter(Role.id>0).all()
            for r in roles:
                if r.id == None:
                    id = "NULL"
                else:
                    id = str(r.id)
                if r.name==None:
                    name="NULL"
                else:
                    name=r.name
                if r.default==True:
                    default="TRUE"
                else:
                    default="FALSE"
                if r.permissions==None:
                    permissions="NULL"
                else:
                    permissions=str(r.permissions)
                sql = "insert into roles VALUES (" + id + ",'" + name +  "'," + default +  "," + permissions + ")"
                sql = sql.replace("'NULL'","NULL")
                try:
                    cursor.execute(sql)
                except Exception as e:
                    flash(str(e)+": "+sql)
                    continue
            db_mysql.commit()
            cursor.execute("select count(*)  from roles;")
            a = cursor.fetchone()
            flash("roles: " + str(a[0]))

        # users
        #cursor.execute("truncate table users;")
        cursor.execute("select count(*)  from users;")
        a = cursor.fetchone()
        flash("users: " + str(a[0]))
        if a[0] == 0:
            users = User.query.filter(User.id>0).order_by(User.id).all()
            for u in users:
                if u.id == None:
                    id = "NULL"
                else:
                    id = str(u.id)
                if u.email==None:
                    email="NULL"
                else:
                    email=u.email
                if u.username==None:
                    username="NULL"
                else:
                    username=u.username
                if u.role_id==None:
                    role_id="NULL"
                else:
                    role_id=str(u.role_id)
                if u.password_hash==None:
                    password_hash="NULL"
                else:
                    password_hash=u.password_hash            
                if u.confirmed == True:
                    confirmed = "TRUE"
                else:
                    confirmed = "FALSE"
                if u.teacher == True:
                    teacher = "TRUE"
                else:
                    teacher = "FALSE"
                if u.name==None:
                    name="NULL"
                else:
                    name=u.name
                if u.student_no==None:
                    student_no="NULL"
                else:
                    student_no=str(u.student_no)
                if u.tel==None:
                    tel="NULL"
                else:
                    tel=u.tel
                if u.location==None:
                    location="NULL"
                else:
                    location=u.location
                if u.about_me==None:
                    about_me="NULL"
                else:
                    about_me=(u.about_me).replace("'","''").replace('😊',':-)')
                if u.member_since==None:
                    member_since="NULL"
                else:
                    member_since = u.member_since.strftime("%Y-%m-%d %H:%M:%S.%f")
                if u.last_seen==None:
                    last_seen="NULL"
                else:
                    last_seen = u.last_seen.strftime("%Y-%m-%d %H:%M:%S.%f")
                if u.avatar_hash==None:
                    avatar_hash="NULL"
                else:
                    avatar_hash=u.avatar_hash
                if u.avatar_file==None:
                    avatar_file="NULL"
                else:
                    avatar_file=u.avatar_file
                sql = "insert into users VALUES (" + id + ",'"  + email +  "','" + username +  "','" + student_no + "'," + role_id +  ",'" + password_hash +  "'," + confirmed +  "," + teacher +  ",'" + name +  "','" + location +  "','" + tel +"','"+about_me+"','" + member_since+"','" + last_seen+"','"+avatar_hash+"','" +avatar_file + "');"
                sql = sql.replace("'NULL'","NULL")
                try:
                    cursor.execute(sql)
                except Exception as e:
                    flash(str(e)+": "+sql)
                    continue
            db_mysql.commit()
            cursor.execute("select count(*)  from users;")
            a = cursor.fetchone()
            flash("users: " + str(a[0]))

        # posts
        cursor.execute("select count(*)  from posts;")
        a = cursor.fetchone()
        flash("posts: " + str(a[0]))
        # if a[0] > 0:
        #     cursor.execute("truncate table posts;")
        if a[0] == 0:
            posts = Post.query.filter(Post.id>0).order_by(Post.id).all()
            for u in posts:
                if u.id == None:
                    id = "NULL"
                else:
                    id = str(u.id)
                if u.topic==None:
                    topic="NULL"
                else:
                    topic=(u.topic).replace("'","''")
                if u.pic==None:
                    pic="NULL"
                else:
                    pic=u.pic
                if u.pic1==None:
                    pic1="NULL"
                else:
                    pic=u.pic1
                if u.pic2==None:
                    pic2="NULL"
                else:
                    pic2=u.pic2
                if u.pic3==None:
                    pic3="NULL"
                else:
                    pic3=u.pic3
                if u.file1==None:
                    file1="NULL"
                else:
                    file1=u.file1
                if u.file2==None:
                    file2="NULL"
                else:
                    file2=u.file2
                if u.file3==None:
                    file3="NULL"
                else:
                    file3=u.file3
                if u.file4==None:
                    file4="NULL"
                else:
                    file4=u.file4
                if u.file5==None:
                    file5="NULL"
                else:
                    file5=u.file5
                if u.filename1==None:
                    filename1="NULL"
                else:
                    filename1=(u.filename1).replace("'","''")
                if u.filename2==None:
                    filename2="NULL"
                else:
                    filename2=(u.filename2).replace("'","''")
                if u.filename3==None:
                    filename3="NULL"
                else:
                    filename3=(u.filename3).replace("'","''")
                if u.filename4==None:
                    filename4="NULL"
                else:
                    filename4=(u.filename4).replace("'","''")
                if u.filename5==None:
                    filename5="NULL"
                else:
                    filename5=(u.filename5).replace("'","''")
                if u.body==None:
                    body="NULL"
                else:
                    body=(u.body).replace("'","''").replace('🦖','').replace('😷','').replace('⚡','').replace('🛒','').replace('⚠','').replace('📈','').replace('🚨','').replace('👑','').replace('🤖 ','').replace('🔑','').replace('😂','').replace('🤔','').replace('📢','').replace('🧢','').replace('👇','').replace('🏃‍♂️','').replace('🚀','').replace('💰','').replace('⛩','').replace('😀','').replace('🔑','').replace('👌','').replace('📊','').replace('🙏🏽','').replace('👻','').replace('😮','').replace('👻','').replace('👉','').replace('👯‍♂️','').replace('💸','').replace('🔶','').replace('🔐','').replace('🏦','').replace('🇦🇺','').replace('👨‍🔬','').replace('😊','').replace('🍇','').replace('🚔','').replace('😎','').replace('🔥','').replace('👉','').replace('🐻','').replace('💊','').replace('🍊','').replace('🎈','').replace('🍾','').replace('🎊','').replace('🌪','').replace('😏','').replace('🔞 ','').replace('🪐','').replace('🤝','').replace('🇬🇧','').replace('🐳','').replace('🤣','').replace('🌟','').replace('🌮','').replace('❤','').replace('🥕','').replace('💎','').replace('🐂','').replace('😄','').replace('👏','').replace('💪','').replace('🐼','').replace('👟','').replace('🤭','').replace('😶','').replace('👈','').replace('💵','').replace('🔔','').replace('🍿','').replace('🌕','').replace('📚','').replace('🙂','').replace('🏔','').replace('👍','').replace('🌏','').replace('🦄','').replace('💲','').replace('😆','').replace('🎂','').replace('😺','').replace('🔱','').replace('💙','').replace('📉','').replace('🎆','').replace('🏆','').replace('🤦‍♂️','').replace('👀','').replace('🇧🇷','').replace('🇻🇪','').replace('🇵🇪','').replace('🇨🇱','').replace('🇮🇷','').replace('🙏','').replace('🙇','').replace('🌍','').replace('🌍','').replace('😅','').replace('😢','').replace('🍍','').replace('🍕','').replace('💖','').replace('🥴','').replace('🗝','').replace('𝕵','J').replace('🛡','').replace('👩‍','').replace('😱','').replace('🙌','').replace('😉','').replace('🔴','').replace('🔓','').replace('🤖','').replace('🔒','').replace('💧','').replace('🗽','').replace('🌎','').replace('😌','').replace('🍮','').replace('🐋','').replace('🚩','').replace('🙋‍♀️','').replace('🇪🇬','').replace('🇨🇴','').replace('🇭🇰','').replace('🇦🇷','').replace('🃏','').replace('🌙','').replace('💡','').replace('💡','').replace('🦠🇨🇳☣️🌡🚜🚜🚜🏨☠️','').replace('🛳⛔️🛫🙈🙉🙊','').replace('🐟','').replace('🏽','').replace('','').replace('','')
                if u.body_html==None:
                    body_html="NULL"
                else:
                    body_html=(u.body_html).replace("'","''").replace('🦖','').replace('😷','').replace('⚡','').replace('🛒','').replace('⚠','').replace('📈','').replace('🚨','').replace('👑','').replace('🤖 ','').replace('🔑','').replace('😂','').replace('🤔','').replace('📢','').replace('🧢','').replace('👇','').replace('🏃‍♂️','').replace('🚀','').replace('💰','').replace('⛩','').replace('😀','').replace('🔑','').replace('👌','').replace('📊','').replace('🙏🏽','').replace('👻','').replace('😮','').replace('👻','').replace('👉','').replace('👯‍♂️','').replace('💸','').replace('🔶','').replace('🔐','').replace('🏦','').replace('🇦🇺','').replace('👨‍🔬','').replace('😊','').replace('🍇','').replace('🚔','').replace('😎','').replace('🔥','').replace('👉','').replace('🐻','').replace('💊','').replace('🍊','').replace('🎈','').replace('🍾','').replace('🎊','').replace('🌪','').replace('😏','').replace('🔞 ','').replace('🪐','').replace('🤝','').replace('🇬🇧','').replace('🐳','').replace('🤣','').replace('🌟','').replace('🌮','').replace('❤','').replace('🥕','').replace('💎','').replace('🐂','').replace('😄','').replace('👏','').replace('💪','').replace('🐼','').replace('👟','').replace('🤭','').replace('😶','').replace('👈','').replace('💵','').replace('🔔','').replace('🍿','').replace('🌕','').replace('📚','').replace('🙂','').replace('🏔','').replace('👍','').replace('🌏','').replace('🦄','').replace('💲','').replace('😆','').replace('🎂','').replace('😺','').replace('🔱','').replace('💙','').replace('📉','').replace('🎆','').replace('🏆','').replace('🤦‍♂️','').replace('👀','').replace('🇧🇷','').replace('🇻🇪','').replace('🇵🇪','').replace('🇨🇱','').replace('🇮🇷','').replace('🙏','').replace('🙇','').replace('🌍','').replace('🌍','').replace('😅','').replace('😢','').replace('🍍','').replace('🍕','').replace('💖','').replace('🥴','').replace('🗝','').replace('𝕵','J').replace('🛡','').replace('👩‍','').replace('😱','').replace('🙌','').replace('😉','').replace('🔴','').replace('🔓','').replace('🤖','').replace('🔒','').replace('💧','').replace('🗽','').replace('🌎','').replace('😌','').replace('🍮','').replace('🐋','').replace('🚩','').replace('🙋‍♀️','').replace('🇪🇬','').replace('🇨🇴','').replace('🇭🇰','').replace('🇦🇷','').replace('🃏','').replace('🌙','').replace('💡','').replace('💡','').replace('🦠🇨🇳☣️🌡🚜🚜🚜🏨☠️','').replace('🛳⛔️🛫🙈🙉🙊','').replace('🐟','').replace('🏽','').replace('','').replace('','')
                if u.private == True:
                    private = "TRUE"
                else:
                    private = "FALSE"
                if u.lang==None:
                    lang="NULL"
                else:
                    lang=u.lang
                if u.at_names==None:
                    at_names="NULL"
                else:
                    at_names=u.at_names
                if u.tag==None:
                    tag="NULL"
                else:
                    tag=u.tag
                if u.readers==None:
                    readers="NULL"
                else:
                    readers=str(u.readers)
                if u.time==None:
                    time="NULL"
                else:
                    time=u.time
                if u.timestamp==None:
                    timestamp="NULL"
                else:
                    timestamp = u.timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")
                if u.author_id==None:
                    author_id="NULL"
                else:
                    author_id=str(u.author_id)
                sql = "insert into posts VALUES (" + id + ",'"  + topic +  "','" + pic +  "','" + pic1 +  "','"  + pic2 +  "','"  + pic3 +  "','"  + file1 +  "','"  + filename1 +  "','"  + file2 +  "','"  + filename2 + "','" + file3 + "','" + filename3 + "','" + file4 + "','" + filename4 + "','" + file5 + "','"   + filename5 + "','"  + body + "','" + body_html + "','" + lang + "','"  + at_names + "'," + private + ",'" + tag +  "'," + readers + ",'" + time + "','" + timestamp +"'," + author_id +");"
                sql = sql.replace("'NULL'","NULL")
                try:
                    cursor.execute(sql)
                except Exception as e:
                    flash(str(e)+": "+sql)
                    continue
            db_mysql.commit()
            cursor.execute("select count(*)  from posts;")
            a = cursor.fetchone()
            flash("posts: " + str(a[0]))


        # atmes                
        # cursor.execute("truncate table atmes;")
        cursor.execute("select count(*)  from atmes;")
        a = cursor.fetchone()
        flash("atmes: " + str(a[0]))
        if a[0] == 0:
            atmes = AtMe.query.filter(AtMe.id>0).order_by(AtMe.id).all()
            for u in atmes:
                if u.id == None:
                    id = "NULL"
                else:
                    id = str(u.id)
                if u.timestamp==None:
                    timestamp="NULL"
                else:
                    timestamp = u.timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")
                if u.comment_id==None:
                    comment_id="NULL"
                else:
                    comment_id=str(u.comment_id)
                if u.username_whoatme == None:
                    username_whoatme="NULL"
                else:
                    username_whoatme = u.username_whoatme
                if u.username_ated == None:
                    username_ated = "NULL"
                else:
                    username_ated = u.username_ated
                sql = "insert into atmes VALUES (" + id + ",'"  + timestamp +  "'," + comment_id +  ",'" + username_ated + "','" + username_whoatme + "');"
                sql = sql.replace("'NULL'","NULL")
                try:
                    cursor.execute(sql)
                except Exception as e:
                    flash(str(e)+": "+sql)
                    continue
            db_mysql.commit()
            cursor.execute("select count(*)  from atmes;")
            a = cursor.fetchone()
            flash("atmes: " + str(a[0]))


        # collectposts        
        # cursor.execute("truncate table collectposts;")
        cursor.execute("select count(*)  from collectposts;")
        a = cursor.fetchone()
        flash("collectposts: " + str(a[0]))
        if a[0] == 0:
            collectposts = CollectPost.query.filter(CollectPost.user_id>0).order_by(CollectPost.timestamp).all()
            for u in collectposts:
                if u.id == None:
                    id = "NULL"
                else:
                    id = str(u.id)
                if u.user_id == None:
                    user_id = "NULL"
                else:
                    user_id = str(u.user_id)
                if u.post_id==None:
                    post_id="NULL"
                else:
                    post_id=str(u.post_id)
                if u.timestamp==None:
                    timestamp="NULL"
                else:
                    timestamp = u.timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")
                sql = "insert into collectposts VALUES (" + id + "," + user_id +  "," + post_id +  ",'" + timestamp + "');"
                sql = sql.replace("'NULL'","NULL")
                try:
                    cursor.execute(sql)
                except Exception as e:
                    flash(str(e)+": "+sql)
                    continue
            db_mysql.commit()
            cursor.execute("select count(*)  from collectposts;")
            a = cursor.fetchone()
            flash("collectposts: " + str(a[0]))

        # comments        
        # cursor.execute("truncate table comments;")
        cursor.execute("select count(*)  from comments;")
        a = cursor.fetchone()
        flash("comments: " + str(a[0]))
        if a[0] == 0:
            comments = Comment.query.filter(Comment.id>0).order_by(Comment.id).all()
            for u in comments:
                if u.id == None:
                    id = "NULL"
                else:
                    id = str(u.id)
                if u.body==None:
                    body="NULL"
                else:
                    body=u.body.replace("'","''")
                if u.body_html==None:
                    body_html="NULL"
                else:
                    body_html=u.body_html.replace("'","''")
                if u.disabled == True:
                    disabled = "TRUE"
                else:
                    disabled = "FALSE"
                if u.timestamp==None:
                    timestamp="NULL"
                else:
                    timestamp = u.timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")
                if u.author_id==None:
                    author_id="NULL"
                else:
                    author_id=str(u.author_id)
                if u.post_id==None:
                    post_id="NULL"
                else:
                    post_id=str(u.post_id)
                sql = "insert into comments VALUES (" + id + ",'" + body + "','" + body_html + "',"  + disabled + ",'"+ timestamp +  "'," + author_id + "," + post_id + ");"
                sql = sql.replace("'NULL'","NULL")
                try:
                    cursor.execute(sql)
                except Exception as e:
                    flash(str(e)+": "+sql)
                    continue
            db_mysql.commit()
            cursor.execute("select count(*)  from comments;")
            a = cursor.fetchone()
            flash("comments: " + str(a[0]))

        # follows        
        # cursor.execute("truncate table follows;")
        cursor.execute("select count(*)  from follows;")
        a = cursor.fetchone()
        flash("follows: " + str(a[0]))
        if a[0] == 0:
            follows = Follow.query.filter(Follow.follower_id>0).order_by(Follow.timestamp).all()
            for u in follows:
                if u.id == None:
                    id = "NULL"
                else:
                    id = str(u.id)
                if u.follower_id == None:
                    follower_id = "NULL"
                else:
                    follower_id = str(u.follower_id)
                if u.followed_id==None:
                    followed_id="NULL"
                else:
                    followed_id=str(u.followed_id)
                if u.timestamp==None:
                    timestamp="NULL"
                else:
                    timestamp = u.timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")
                sql = "insert into follows VALUES (" + id +"," + follower_id + ","  + followed_id+ ",'"  + timestamp + "');"
                sql = sql.replace("'NULL'","NULL")
                try:
                    cursor.execute(sql)
                except Exception as e:
                    flash(str(e)+": "+sql)
                    continue
            db_mysql.commit()
            cursor.execute("select count(*)  from follows;")
            a = cursor.fetchone()
            flash("follows: " + str(a[0]))

        # lessonfiles        
        # cursor.execute("truncate table lessonfiles;")
        cursor.execute("select count(*)  from lessonfiles;")
        a = cursor.fetchone()
        flash("lessonfiles: " + str(a[0]))
        if a[0] == 0:
            lessonfiles = LessonFile.query.filter(LessonFile.id>0).order_by(LessonFile.id).all()
            for u in lessonfiles:
                if u.id == None:
                    id = "NULL"
                else:
                    id = str(u.id)
                if u.filetype==None:
                    filetype="NULL"
                else:
                    filetype=u.filetype
                if u.visibility==None:
                    visibility="NULL"
                else:
                    visibility=u.visibility
                if u.file==None:
                    file="NULL"
                else:
                    file=u.file
                if u.filename==None:
                    filename="NULL"
                else:
                    filename=u.filename.replace("'","''")
                if u.about==None:
                    about="NULL"
                else:
                    about=u.about.replace("'","''")
                if u.timestamp==None:
                    timestamp="NULL"
                else:
                    timestamp = u.timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")
                if u.lesson_id==None:
                    lesson_id="NULL"
                else:
                    lesson_id=str(u.lesson_id)
                sql = "insert into lessonfiles VALUES (" + id + ",'" + filetype + "','" + visibility +  "','" + file + "','" + filename +  "','" + about + "','"  + timestamp  + "'," + lesson_id + ");"
                sql = sql.replace("'NULL'","NULL")
                try:
                    cursor.execute(sql)
                except Exception as e:
                    flash(str(e)+": "+sql)
                    continue
            db_mysql.commit()
            cursor.execute("select count(*)  from lessonfiles;")
            a = cursor.fetchone()
            flash("lessonfiles: " + str(a[0]))
        
        # lessons
        # cursor.execute("truncate table lessons;")
        cursor.execute("select count(*)  from lessons;")
        a = cursor.fetchone()
        flash("lessons: " + str(a[0]))
        if a[0] == 0:
            lessons = Lesson.query.filter(Lesson.id>0).order_by(Lesson.id).all()
            for u in lessons:
                if u.id == None:
                    id = "NULL"
                else:
                    id = str(u.id)
                if u.lesson_name==None:
                    lesson_name="NULL"
                else:
                    lesson_name=(u.lesson_name).replace("'","''")
                if u.about_lesson==None:
                    about_lesson="NULL"
                else:
                    about_lesson=(u.about_lesson).replace("'","''")
                if u.about_lesson_html==None:
                    about_lesson_html="NULL"
                else:
                    about_lesson_html=(u.about_lesson_html).replace("'","''")
                if u.pic==None:
                    pic="NULL"
                else:
                    pic=u.pic
                if u.file1==None:
                    file1="NULL"
                else:
                    file1=u.file1
                if u.file2==None:
                    file2="NULL"
                else:
                    file2=u.file2
                if u.file3==None:
                    file3="NULL"
                else:
                    file3=u.file3
                if u.file4==None:
                    file4="NULL"
                else:
                    file4=u.file4
                if u.file5==None:
                    file5="NULL"
                else:
                    file5=u.file5
                if u.file6==None:
                    file6="NULL"
                else:
                    file6=u.file6
                if u.file7==None:
                    file7="NULL"
                else:
                    file7=u.file7
                if u.file8==None:
                    file8="NULL"
                else:
                    file8=u.file8
                if u.filename1==None:
                    filename1="NULL"
                else:
                    filename1=(u.filename1).replace("'","''")
                if u.filename2==None:
                    filename2="NULL"
                else:
                    filename2=(u.filename2).replace("'","''")
                if u.filename3==None:
                    filename3="NULL"
                else:
                    filename3=(u.filename3).replace("'","''")
                if u.filename4==None:
                    filename4="NULL"
                else:
                    filename4=(u.filename4).replace("'","''")
                if u.filename5==None:
                    filename5="NULL"
                else:
                    filename5=(u.filename5).replace("'","''")
                if u.filename6==None:
                    filename6="NULL"
                else:
                    filename6=(u.filename6).replace("'","''")
                if u.filename7==None:
                    filename7="NULL"
                else:
                    filename7=(u.filename7).replace("'","''")
                if u.filename8==None:
                    filename8="NULL"
                else:
                    filename8=(u.filename8).replace("'","''")
                if u.timestamp==None:
                    timestamp="NULL"
                else:
                    timestamp = u.timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")
                if u.teacher_id==None:
                    teacher_id="NULL"
                else:
                    teacher_id=str(u.teacher_id)
                sql = "insert into lessons VALUES (" + id + ",'"  + lesson_name +  "','" + about_lesson +  "','" + about_lesson_html +  "','"  + pic +  "','"  + file1 +  "','"  + file2 +  "','" + file3 +  "','" + file4 +  "','" + file5 +  "','" + file6 +  "','" + file7 +  "','" + file8 +  "','" + filename1 +  "','"  + filename2 +  "','"  + filename3 + "','" + filename4 + "','" + filename5 + "','" + filename6 + "','" + filename7 + "','" + filename8 + "','" + timestamp +"'," + teacher_id +");"
                sql = sql.replace("'NULL'","NULL")
                try:
                    cursor.execute(sql)
                except Exception as e:
                    flash(str(e)+": "+sql)
                    continue
            db_mysql.commit()
            cursor.execute("select count(*)  from lessons;")
            a = cursor.fetchone()
            flash("lessons: " + str(a[0]))

        # newlessons        
        # cursor.execute("truncate table newlessons;")
        cursor.execute("select count(*)  from newlessons;")
        a = cursor.fetchone()
        flash("newlessons: " + str(a[0]))
        if a[0] == 0:
            newlessons = NewLesson.query.filter(NewLesson.id>0).order_by(NewLesson.id).all()
            for u in newlessons:
                if u.id == None:
                    id = "NULL"
                else:
                    id = str(u.id)
                if u.year==None:
                    year="NULL"
                else:
                    year=u.year
                if u.season==None:
                    season="NULL"
                else:
                    season=u.season
                if u.room_row==None:
                    room_row="NULL"
                else:
                    room_row=str(u.room_row)
                if u.room_column==None:
                    room_column="NULL"
                else:
                    room_column=str(u.room_column)
                if u.about==None:
                    about="NULL"
                else:
                    about=u.about.replace("'","''")
                if u.availability==None:
                    availability="NULL"
                else:
                    availability=u.availability.replace("'","''")
                if u.timestamp==None:
                    timestamp="NULL"
                else:
                    timestamp = u.timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")
                if u.lesson_id==None:
                    lesson_id="NULL"
                else:
                    lesson_id=str(u.lesson_id)
                sql = "insert into newlessons VALUES (" + id + ",'"  + year + "','"  + season +  "'," + room_row + ","  + room_column +  ",'" + about + "','" + availability + "','" + timestamp + "'," + lesson_id + ");"
                sql = sql.replace("'NULL'","NULL")
                try:
                    cursor.execute(sql)
                except Exception as e:
                    flash(str(e)+": "+sql)
                    continue
            db_mysql.commit()
            cursor.execute("select count(*)  from newlessons;")
            a = cursor.fetchone()
            flash("newlessons: " + str(a[0]))

        # students        
        # cursor.execute("truncate table students;")
        cursor.execute("select count(*)  from students;")
        a = cursor.fetchone()
        flash("students: " + str(a[0]))
        if a[0] == 0:
            students = Student.query.filter(Student.id>0).order_by(Student.id).all()
            for u in students:
                if u.id == None:
                    id = "NULL"
                else:
                    id = str(u.id)
                if u.seat==None:
                    seat="NULL"
                else:
                    seat=(u.seat)
                if u.absence == None:
                    absence = "NULL"
                else:
                    absence = str(u.absence)
                if u.confirm == True:
                    confirm = "TRUE"
                else:
                    confirm = "FALSE"
                if u.topic==None:
                    topic="NULL"
                else:
                    topic=(u.topic).replace("'","''")
                if u.body==None:
                    body="NULL"
                else:
                    body=(u.body).replace("'","''")
                if u.file1==None:
                    file1="NULL"
                else:
                    file1=u.file1
                if u.file2==None:
                    file2="NULL"
                else:
                    file2=u.file2
                if u.file3==None:
                    file3="NULL"
                else:
                    file3=u.file3
                if u.file4==None:
                    file4="NULL"
                else:
                    file4=u.file4
                if u.file5==None:
                    file5="NULL"
                else:
                    file5=u.file5
                if u.filename1==None:
                    filename1="NULL"
                else:
                    filename1=(u.filename1).replace("'","''")
                if u.filename2==None:
                    filename2="NULL"
                else:
                    filename2=(u.filename2).replace("'","''")
                if u.filename3==None:
                    filename3="NULL"
                else:
                    filename3=(u.filename3).replace("'","''")
                if u.filename4==None:
                    filename4="NULL"
                else:
                    filename4=(u.filename4).replace("'","''")
                if u.filename5==None:
                    filename5="NULL"
                else:
                    filename5=(u.filename5).replace("'","''")
                if u.criticism==None:
                    criticism="NULL"
                else:
                    criticism=(u.criticism).replace("'","''")
                if u.score==None:
                    score="NULL"
                else:
                    score=str(u.score)
                if u.score_answer==None:
                    score_answer="NULL"
                else:
                    score_answer=str(u.score_answer)
                if u.time==None:
                    time="NULL"
                else:
                    time=(u.time).replace("'","''")
                if u.timestamp==None:
                    timestamp="NULL"
                else:
                    timestamp = u.timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")
                if u.student_id==None:
                    student_id="NULL"
                else:
                    student_id=str(u.student_id)
                if u.newlesson_id==None:
                    newlesson_id="NULL"
                else:
                    newlesson_id=str(u.newlesson_id)
                sql = "insert into students VALUES (" + id + ",'"  + seat + "'," +absence + "," + confirm + ",'" + topic +  "','" + body +  "','"  + file1 +  "','"  + file2 +  "','" + file3 +  "','" + file4 +  "','" + file5 +  "','" + filename1 +  "','"  + filename2 +  "','"  + filename3 + "','" + filename4 + "','" + filename5 + "','" + criticism + "'," + score + "," + score_answer + ",'" + time + "','" + timestamp + "'," + student_id +"," + newlesson_id +");"
                sql = sql.replace("'NULL'","NULL")
                try:
                    cursor.execute(sql)
                except Exception as e:
                    flash(str(e)+": "+sql)
                    continue
            db_mysql.commit()
            cursor.execute("select count(*)  from students;")
            a = cursor.fetchone()
            flash("students: " + str(a[0]))

        # teachers        
        # cursor.execute("truncate table teachers;")
        cursor.execute("select count(*)  from teachers;")
        a = cursor.fetchone()
        flash("teachers: " + str(a[0]))
        if a[0] == 0:
            teachers = Teacher.query.filter(Teacher.id>0).order_by(Teacher.id).all()
            for u in teachers:
                if u.id == None:
                    id = "NULL"
                else:
                    id = str(u.id)
                if u.school==None:
                    school="NULL"
                else:
                    school=u.school.replace("'","''")
                if u.field==None:
                    field="NULL"
                else:
                    field=u.field.replace("'","''")
                if u.pic==None:
                    pic="NULL"
                else:
                    pic=u.pic
                if u.about_teacher==None:
                    about_teacher="NULL"
                else:
                    about_teacher=u.about_teacher.replace("'","'")
                if u.about_teacher_html==None:
                    about_teacher_html="NULL"
                else:
                    about_teacher_html=u.about_teacher_html.replace("'","'")
                if u.timestamp==None:
                    timestamp="NULL"
                else:
                    timestamp = u.timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")
                if u.teacher_id == None:
                    teacher_id = "NULL"
                else:
                    teacher_id = str(u.teacher_id)
                sql = "insert into teachers VALUES (" + id + ",'"  + school +  "','" + field +  "','" + pic +  "','" + about_teacher +  "','" + about_teacher_html +  "','" + timestamp +  "'," + teacher_id + ");"
                sql = sql.replace("'NULL'","NULL")
                try:
                    cursor.execute(sql)
                except Exception as e:
                    flash(str(e)+": "+sql)
                    continue
            db_mysql.commit()
            cursor.execute("select count(*)  from teachers;")
            a = cursor.fetchone()
            flash("teachers: " + str(a[0]))

        # 调整为原来的自增
        ai_tables = ['atmes','collectposts','comments','follows','lessonfiles','lessons','newlessons','posts','roles','students','teachers','users']
        for ai in ai_tables:
            try:
                sql = "ALTER TABLE " + ai + " CHANGE COLUMN `id` `id` INT NOT NULL AUTO_INCREMENT ;"
                # flash(sql)
                cursor.execute(sql)
                # flash(sql)
            except Exception as e:
                flash(str(e) + ": " + sql)

        # 调整为原来的外键        
        fk_tables = [['users','role_id','roles','id'],
                     ['teachers','teacher_id','users','id'],
                     ['students','student_id','users','id'],
                     ['students','newlesson_id','newlessons','id'],
                     ['posts','author_id','users','id'],
                     ['newlessons','lesson_id','lessons','id'],
                     ['lessons','teacher_id','users','id'],
                     ['lessonfiles','lesson_id','lessons','id'],
                     ['follows','follower_id','users','id'],
                     ['follows','followed_id','users','id'],
                     ['comments','author_id','users','id'],
                     ['comments','post_id','posts','id'],
                     ['collectposts','user_id','users','id'],
                     ['collectposts','post_id','posts','id'],
                     ['atmes','comment_id','comments','id'],
                     ['atmes','username_ated','users','username'],
                     ['atmes','username_whoatme','users','username']]
        for fk in fk_tables:
            try:
                sql = "alter table `" + fk[0] + "` add foreign key(`" + fk[1] + "`) references `" + fk[2] +"`(`" + fk[3] + "`) ON DELETE SET NULL;" # 使用:show create table book;命令可查看
                flash(sql)
                cursor.execute(sql)
                cursor.execute("SET GLOBAL FOREIGN_KEY_CHECKS=1;")
            except Exception as e:
                flash(str(e) + ": " + sql)
            
        # 数据提交并关闭mysql数据库
        db_mysql.commit()
        db_mysql.close()

    return render_template('user.html', user=user, users=users, atme_bodies=atme_bodies,\
                           posts=posts,posts_private=posts_private,openedlessons=openedlessons,\
                       pagination=pagination,pagination_private=pagination_private,pagination_atme=pagination_atme,\
                       show_my_private=show_my_private, mylessons=mylessons,english=english)
    

@main.route('/show-my-all/<username>')
def show_my_all(username):
    resp = make_response(redirect(url_for('.user',username=username)))
    resp.set_cookie('show_my_private', '0', max_age=30*24*60*60)
    return resp


@main.route('/show-my-private/<username>')
@login_required
def show_my_private(username):
    resp = make_response(redirect(url_for('.user',username=username)))
    resp.set_cookie('show_my_private', '1', max_age=30*24*60*60)
    return resp

@main.route('/show-my-selected-classes/<username>')
def show_my_selected_classes(username):
    resp = make_response(redirect(url_for('.user',username=username)))
    resp.set_cookie('show_my_private', '2', max_age=30*24*60*60)
    return resp

@main.route('/show-my-atme/<username>')
@login_required
def show_my_atme(username):
    resp = make_response(redirect(url_for('.user',username=username)))
    resp.set_cookie('show_my_private', '3', max_age=30*24*60*60)
    return resp

@main.route('/show-my-all-users-atme/<username>')
@login_required
def show_my_all_users(username):
    resp = make_response(redirect(url_for('.user',username=username)))
    resp.set_cookie('show_my_private', '4', max_age=30*24*60*60)
    return resp

@main.route('/show-my-received/<username>')
@login_required
def show_my_received(username):
    resp = make_response(redirect(url_for('.user',username=username)))
    resp.set_cookie('show_my_private', '5', max_age=30*24*60*60)
    return resp

#@main.route('/show-my-commented/<username>')
#@login_required
#def show_my_commented(username):
#    resp = make_response(redirect(url_for('.user',username=current_user.username)))
#    resp.set_cookie('show_my_commented', '', max_age=30*24*60*60)
#    return resp
#


@main.route('/user2/<username>')
def user2(username):
    english=request.cookies.get('english')
    page = request.args.get('page', 1, type=int)
    show_my_private = False
    users = User.query.filter(User.id > 0).order_by(User.member_since.desc()).all()
    user = User.query.filter_by(username=username).first_or_404()
    if current_user.is_authenticated and current_user.username==username:
        show_my_private = bool(request.cookies.get('show_my_private', ''))

    if not show_my_private:
        pagination = user.posts.filter(Post.private == False).order_by(Post.timestamp.desc()).paginate(
            page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
            error_out=False)
        posts = pagination.items
    if show_my_private:
        pagination = current_user.posts.filter(Post.private == True).order_by(Post.timestamp.desc()).paginate(
            page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
            error_out=False)
        posts = pagination.items
    if current_user.is_authenticated and current_user.username==username:
        students = Student.query.filter_by(student_id=current_user.id).all() 
        mylessons = []
        for s in students:
            newlesson = NewLesson.query.filter_by(id=s.newlesson_id).first()
            lesson = Lesson.query.filter_by(id=newlesson.lesson_id).first()
            mylessons.append([newlesson,lesson])
        return render_template('user.html', user=user, posts=posts,users=users, 
                           pagination=pagination,show_my_private=show_my_private,
                           mylessons=mylessons, english=english)
    return render_template('user.html', user=user, posts=posts,users=users, 
                           pagination=pagination,show_my_private=show_my_private, english=english)



@main.route('/user-posts/<username>')
def user_posts(username):
    english=request.cookies.get('english')
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    pagination = user.posts.filter(Post.private == False).order_by(Post.timestamp.desc()).paginate(
            page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
            error_out=False)
    posts = pagination.items
    return render_template('user_posts.html', user=user, posts=posts,
                           pagination=pagination, english=english)


@main.route('/comments-on-me/<int:user_id>')
@login_required
def comments_on_me(user_id):
    english=request.cookies.get('english')
#    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(id=user_id).first()
    posts = Post.query.filter_by(author_id=user.id).all()    
    post_comments = []
    post_comments2 = []
    timestamps = []
    for post in posts:
        comments = Comment.query.filter_by(post_id=post.id).all()
        if len(comments) != 0:
            for comment in comments:
                post_comments.append([post,comment])
                timestamps.append(comment.timestamp)
    if len(post_comments) != 0:
        timestamps2 = sorted(timestamps,reverse=True)
        for t in timestamps2:
            post_comments2.append(post_comments[timestamps.index(t)])
#    pagination = Comment
#    Post.query.join(Comment, Comment.post_id == user.id)\
#            .filter(Comment.author_id == user.id).order_by(Post.timestamp.desc()).paginate(
#            page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
#            error_out=False)
    return render_template('comments_on_me.html', post_comments2=post_comments2, english=english)
#                           pagination=pagination)

@main.route('/sent-comments/<int:user_id>')
@login_required
def sent_comments(user_id):
    english=request.cookies.get('english')
    page = request.args.get('page', 1, type=int)
    comments = Comment.query.filter_by(author_id=user_id).order_by(db.desc(Comment.timestamp)).all()    
    pagination = Comment.query.filter_by(author_id=user_id).paginate(page, \
                                        per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                                                           error_out=False)
    post_comments = []
    for comment in comments:
        post = Post.query.filter_by(id=comment.post_id).first()
        if post is not None:
            post_comments.append([post,comment])
        else:
            if english == "yes":
                post_comments.append(["The original blog has been deleted.",comment])
            else:
                post_comments.append(["原帖子已经删除",comment])
    return render_template('sent_comments.html', post_comments=post_comments,pagination=pagination, english=english)




@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    english=request.cookies.get('english')
    if current_user.is_authenticated:
        collect = CollectPost.query.filter_by(post_id=id).filter_by(user_id=current_user.id).first()
    else:
       collect = None 
    if collect == None:
        is_collect = 0
    else:
        is_collect = 1
    post = Post.query.get_or_404(id)
    names = None
    if post.at_names:
        names = (post.at_names).split()
    
    if post.readers == None:
        post.readers = 1
    else:
        post.readers = post.readers + 1
    db.session.commit()
    outdate=datetime.today() + timedelta(days=30)  
    resp = current_app.make_response(redirect(url_for('main.index')))
    if current_user.is_authenticated:
        if current_user.id != post.author_id and post.private == True:
            if post.at_names != None:
                if current_user.username not in post.at_names:
                    if english == "yes":
                        flash('The blog has been set as private.')
                    else:
                        flash('该帖子为私有。')
                    return redirect(url_for('.index'))
            else:
                if english == "yes":
                    flash('The blog has been set as private.')
                else:
                    flash('该帖子为私有。')
                return redirect(url_for('.index'))
                                     
    else:
        if post.private == True:
            if english == "yes":
                flash('The blog has been set as private.')
            else:
                flash('该帖子为私有。')
            return redirect(url_for('.index'))
            
    if english == "yes":
        form = CommentFormE()
    else:
        form = CommentForm()
    if form.validate_on_submit():
        if not current_user.is_anonymous:
            author = current_user._get_current_object()
            comment = Comment(body=form.body.data,
                              post=post,
                              author=author)
            db.session.add(comment)
            if english == "yes":
                flash('The comment has been uploaded.')
            else:
                flash('评论已经上传。')
        else:
            if english == "yes":
                flash('You can comment after logining in.')
            else:
                flash('登录后可以评论。')
            # author = User.query.filter_by(username='Anonymous').first()
        body = form.body.data
        # comment = Comment.query.filter_by(body=form.body.data).filter_by(post_id=post.id).first()
        ats = body.replace('@',' ').split()
        if len(ats) > 0:
            for username_ated in ats:
                user = User.query.filter_by(username=username_ated).first()
                if user is not None and not current_user.is_anonymous:
                    atme = AtMe(comment_id=comment.id,username_ated=username_ated, username_whoatme=current_user.username)
                    db.session.add(atme)
                if user is not None and current_user.is_anonymous:
                    atme = AtMe(comment_id=comment.id, username_ated=username_ated, username_whoatme='Anonymous')
                    db.session.add(atme)
        return redirect(url_for('.post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) // \
            current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    if post.tag != None:
        if ('newlessons' in post.tag or 'discussion' in post.tag) and post.tag != 'newlessons_' and post.tag != 'discussion_':
            flag = 1
            # flash(post.tag)
            # posts = Post.query.filter_by(tag='newlessons_').all()
            # for p in posts:
            #     student = Student.query.filter_by(topic=p.topic).first()
            #     if student==None:
            #         continue
            #     p.tag = 'newlessons_'+str(student.newlesson_id)
            #     flash(p.tag)
            #     db.session.commit()
            # posts = Post.query.filter_by(tag='discussion_').all()            
            # for p in posts:
            #     student = Student.query.filter_by(topic=p.topic).first()
            #     p.tag = 'discussion_'+str(student.newlesson_id)
            #     flash(p.tag)
            #     db.session.commit()
            # return redirect(url_for('.index'))
            newlesson_id = int(post.tag.split('_')[1])
            newlesson = NewLesson.query.filter_by(id=newlesson_id).first()
            lesson = Lesson.query.filter_by(id=newlesson.lesson_id).first()
            return render_template('post.html', post=post, form=form, is_collect=is_collect, comments=comments, pagination=pagination, lesson=lesson, names=names, newlesson=newlesson, flag=flag, english=english)
        else:
            flag = 0
    else:
        flag = 0
    return render_template('post.html', post=post, form=form, flag=flag, is_collect=is_collect, comments=comments, pagination=pagination, names=names, english=english)

@main.route('/new/<int:id>', methods=['GET', 'POST'])
def new(id):
    english=request.cookies.get('english')
    if current_user.is_authenticated:
        collect = CollectPost.query.filter_by(new_id=id).filter_by(user_id=current_user.id).first()
    else:
       collect = None 
    if collect == None:
        is_collect = 0
    else:
        is_collect = 1
    new = New.query.get_or_404(id)
    names = None
    if new.at_names:
        names = (new.at_names).split()
    if new.readers == None:
        new.readers = 1
    else:
        new.readers = new.readers + 1
    db.session.commit()
    outdate=datetime.today() + timedelta(days=30)  
    resp = current_app.make_response(redirect(url_for('main.index')))
    if current_user.is_authenticated:
        if current_user.id != new.author_id and new.private == True:
            if new.at_names != None:
                if current_user.username not in new.at_names:
                    if english == "yes":
                        flash('The blog has been set as private.')
                    else:
                        flash('该帖子为私有。')
                    return redirect(url_for('.index'))
            else:
                if english == "yes":
                    flash('The blog has been set as private.')
                else:
                    flash('该帖子为私有。')
                return redirect(url_for('.index'))
                                     
    else:
        if new.private == True:
            if english == "yes":
                flash('The blog has been set as private.')
            else:
                flash('该帖子为私有。')
            return redirect(url_for('.index'))
            
    if english == "yes":
        form = CommentFormE()
    else:
        form = CommentForm()
    if form.validate_on_submit():
        if not current_user.is_anonymous:
            author = current_user._get_current_object()
            comment = Comment(body=form.body.data,
                              author=author, new_id=id)
            db.session.add(comment)
            if english == "yes":
                flash('The comment has been uploaded.')
            else:
                flash('评论已经上传。')
        else:
            if english == "yes":
                flash('You can comment after logining in.')
            else:
                flash('登录后可以评论。')
            # author = User.query.filter_by(username='Anonymous').first()
        body = form.body.data
        comment = Comment.query.filter_by(body=form.body.data).filter_by(new_id=id).first()
        ats = body.replace('@',' ').split()
        if len(ats) > 0:
            for username_ated in ats:
                user = User.query.filter_by(username=username_ated).first()
                if user is not None and not current_user.is_anonymous:
                    atme = AtMe(comment_id=comment.id,username_ated=username_ated, username_whoatme=current_user.username)
                    db.session.add(atme)
                if user is not None and current_user.is_anonymous:
                    atme = AtMe(comment_id=comment.id, username_ated=username_ated, username_whoatme='Anonymous')
                    db.session.add(atme)
        return redirect(url_for('.new', id=new.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (new.comments.count() - 1) // \
            current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
    pagination = Comment.query.filter(Comment.new_id==id).order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('new.html', post=new, form=form, comments=comments,pagination=pagination,is_collect=is_collect,english=english)


@main.route('/oldnew/<int:id>', methods=['GET', 'POST'])
def oldnew(id):
    english=request.cookies.get('english')
    if current_user.is_authenticated:
        collect = CollectPost.query.filter_by(oldnew_id=id).filter_by(user_id=current_user.id).first()
    else:
       collect = None 
    if collect == None:
        is_collect = 0
    else:
        is_collect = 1
    oldnew = Oldnew.query.get_or_404(id)
    names = None
    if oldnew.at_names:
        names = (oldnew.at_names).split()
    if oldnew.readers == None:
        oldnew.readers = 1
    else:
        oldnew.readers = oldnew.readers + 1
    db.session.commit()
    outdate=datetime.today() + timedelta(days=30)  
    resp = current_app.make_response(redirect(url_for('main.index')))
    if current_user.is_authenticated:
        if current_user.id != oldnew.author_id and oldnew.private == True:
            if oldnew.at_names != None:
                if current_user.username not in oldnew.at_names:
                    if english == "yes":
                        flash('The blog has been set as private.')
                    else:
                        flash('该帖子为私有。')
                    return redirect(url_for('.index'))
            else:
                if english == "yes":
                    flash('The blog has been set as private.')
                else:
                    flash('该帖子为私有。')
                return redirect(url_for('.index'))
                                     
    else:
        if oldnew.private == True:
            if english == "yes":
                flash('The blog has been set as private.')
            else:
                flash('该帖子为私有。')
            return redirect(url_for('.index'))
            
    if english == "yes":
        form = CommentFormE()
    else:
        form = CommentForm()
    if form.validate_on_submit():
        if not current_user.is_anonymous:
            author = current_user._get_current_object()
            comment = Comment(body=form.body.data,
                              oldnew_id=id,
                              author=author)
            db.session.add(comment)
            if english == "yes":
                flash('The comment has been uploaded.')
            else:
                flash('评论已经上传。')
        else:
            if english == "yes":
                flash('You can comment after logining in.')
            else:
                flash('登录后可以评论。')
            # author = User.query.filter_by(username='Anonymous').first()
        body = form.body.data
        comment = Comment.query.filter_by(body=form.body.data).filter_by(oldnew_id=oldnew.id).first()
        ats = body.replace('@',' ').split()
        if len(ats) > 0:
            for username_ated in ats:
                user = User.query.filter_by(username=username_ated).first()
                if user is not None and not current_user.is_anonymous:
                    atme = AtMe(comment_id=comment.id,username_ated=username_ated, username_whoatme=current_user.username)
                    db.session.add(atme)
                if user is not None and current_user.is_anonymous:
                    atme = AtMe(comment_id=comment.id, username_ated=username_ated, username_whoatme='Anonymous')
                    db.session.add(atme)
        return redirect(url_for('.oldnew', id=oldnew.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (oldnew.comments.count() - 1) // \
            current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
    pagination = Comment.query.filter_by(oldnew_id=id).order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('oldnew.html', post=oldnew,form=form, pagination=pagination,comments=comments,is_collect=is_collect,english=english)


@main.route('/write', methods=['GET', 'POST'])
@login_required
def write():
    english=request.cookies.get('english')
    values = CombinedMultiDict([flask.request.files,flask.request.form])
    if english == "yes":
        form = PostFormE(values)
    else:
        form = PostForm(values)
    enctype="multipart/form-data"
    if form.private.data == None:
        private = False
    else:
        private = form.private.data
    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        names = (form.at_names.data).replace('@',' ')
        names_to_add = ""
        for n in names.split():
            user1 = User.query.filter_by(username=n).first()
            if user1:
                names_to_add = names_to_add + ' ' + n
                if english == 'yes':
                    flash('Already sent to: ' + n)
                else:
                    flash('已经抄送给：' + n)
            else:
                if english == 'yes':
                    flash(n + " is not a user's name. Please check again!")          
                else:
                    flash(n +'不是本站用户名，请通过编辑再次确认！' )
        post = Post(topic=form.topic.data,body=form.body.data,
                    private=private, tag="posts",at_names=names_to_add, time=datetime.today().isoformat()[:-7].replace("T"," "), author=current_user._get_current_object())
        if request.method == 'POST':
            pic = request.files['pic']
            size = (1024, 1024) 
            if pic and allowed_file(pic.filename):
                im = Image.open(pic)
                im.thumbnail(size)        
                filename = secure_filename(pic.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' + str(time.time()).replace('.','_') + '.' + filename.split('.')[-1]
                im.save(os.path.join('app/static', 'post', filename1))
                post.pic = url_for('static',filename='%s/%s' % ('post', filename1))
        if form.private.data == 1:
            if english == "yes":
                flash('The blog has uploaded and set as private, only you and friends being ated can see.')
            else:
                flash('帖子上传并设为私有，仅自己和被@的朋友可见。')
        else:
            if english == "yes":
                flash('The blog has been uploaded.')
            else:
                flash('帖子已经提交。')
        return redirect(url_for('.user',username=current_user.username))
    return render_template('write.html', form=form, enctype=enctype, english=english)


@main.route('/write2', methods=['GET', 'POST'])
@login_required
def write2():
    english=request.cookies.get('english')
    values = CombinedMultiDict([flask.request.files,flask.request.form])
    if english == "yes":
        form = PostFormE2(values)
    else:
        form = PostForm2(values)
    enctype="multipart/form-data"
    if form.private.data == None:
        private = False
    else:
        private = form.private.data
    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        names = (form.at_names.data).replace('@',' ')
        names_to_add = ""
        for n in names.split():
            user1 = User.query.filter_by(username=n).first()
            if user1:
                names_to_add = names_to_add + ' ' + n
                if english == 'yes':
                    flash('Already sent to: ' + n)
                else:
                    flash('已经抄送给：' + n)
            else:
                if english == 'yes':
                    flash(n + " is not a user's name. Please check again!")          
                else:
                    flash(n +'不是本站用户名，请通过编辑再次确认！' )

        post = Post(topic=form.topic.data,body=form.body.data,
                    private=private,tag="posts",at_names=names_to_add, time=datetime.today().isoformat()[:-7].replace("T"," "),
                    author=current_user._get_current_object())
        if request.method == 'POST':
            pic = request.files['pic']
            size = (1024, 1024) 
            if pic and allowed_file(pic.filename):
                im = Image.open(pic)
                im.thumbnail(size)        
                filename = secure_filename(pic.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' + str(time.time()).replace('.','_') + '.' + filename.split('.')[-1]
                im.save(os.path.join('app/static', 'post', filename1))
                post.pic = url_for('static',filename='%s/%s' % ('post', filename1))
    
            pic1 = request.files['pic1']
            if pic1 and allowed_file(pic1.filename):
                im = Image.open(pic1)
                im.thumbnail(size)        
                filename = secure_filename(pic1.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' + str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
                im.save(os.path.join('app/static', 'post', filename1))
                post.pic1 = url_for('static',filename='%s/%s' % ('post', filename1))
    
            pic2 = request.files['pic2']
            size = (1024, 1024) 
            if pic2 and allowed_file(pic2.filename):
                im = Image.open(pic2)
                im.thumbnail(size)        
                filename = secure_filename(pic2.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' + str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
                im.save(os.path.join('app/static', 'post', filename1))
                post.pic2 = url_for('static',filename='%s/%s' % ('post', filename1))
    
            pic3 = request.files['pic3']
            size = (1024, 1024) 
            if pic3 and allowed_file(pic3.filename):
                im = Image.open(pic3)
                im.thumbnail(size)        
                filename = secure_filename(pic3.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' + str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
                im.save(os.path.join('app/static', 'post', filename1))
                post.pic3 = url_for('static',filename='%s/%s' % ('post', filename1))
    
            file1 = request.files['file1']
            if file1 and allowed_file(file1.filename):
                filename = secure_filename(file1.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' +str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
                file1.save(os.path.join('app/static', 'file', filename1))
                post.file1 = url_for('static',filename='%s/%s' % ('file', filename1))
                post.filename1 = file1.filename        
    
            file2 = request.files['file2']
            if file2 and allowed_file(file2.filename):
                filename = secure_filename(file2.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' +str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
                file2.save(os.path.join('app/static', 'file', filename1))
                post.file2 = url_for('static',filename='%s/%s' % ('file', filename1))
                post.filename2 = file2.filename        
    
            file3 = request.files['file3']
            if file3 and allowed_file(file3.filename):
                filename = secure_filename(file3.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' +str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
                file3.save(os.path.join('app/static', 'audio', filename1))
                post.file3 = url_for('static',filename='%s/%s' % ('audio', filename1))
                post.filename3 = file3.filename        
    
            file4 = request.files['file4']
            if file4 and allowed_file(file4.filename):
                filename = secure_filename(file4.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' +str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
                file4.save(os.path.join('app/static', 'video', filename1))
                post.file4 = url_for('static',filename='%s/%s' % ('video', filename1))
                post.filename4 = file4.filename
    
            file5 = request.files['file5']
            if file5 and allowed_file(file5.filename):
                filename = secure_filename(file5.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' +str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
                file5.save(os.path.join('app/static', 'file', filename1))
                post.file5 = url_for('static',filename='%s/%s' % ('file', filename1))
                post.filename5 = file5.filename
        if form.private.data == 1:
            if english == "yes":
                flash('The blog has uploaded and set as private, only you and friends being ated can see.')
            else:
                flash('帖子上传并设为私有，仅自己和被@的朋友可见。')
        else:
            if english == "yes":
                flash('The blog has been uploaded.')
            else:
                flash('帖子已经提交。')
        return redirect(url_for('.user',username=current_user.username))
    return render_template('write2.html', form=form,enctype=enctype, english=english)



@main.route('/write_newlesson/<string:tag>', methods=['GET', 'POST'])
@login_required
def write_newlesson(tag):
    english=request.cookies.get('english')
    values = CombinedMultiDict([flask.request.files,flask.request.form])
    if english == "yes":
        form = PostFormNewlessonE(values)
    else:
        form = PostFormNewlesson(values)
    enctype="multipart/form-data"
    if form.private.data == None:
        private = False
    else:
        private = form.private.data
    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        names = (form.at_names.data).replace('@',' ')
        names_to_add = ""
        for n in names.split():
            user1 = User.query.filter_by(username=n).first()
            if user1:
                names_to_add = names_to_add + ' ' + n
                if english == 'yes':
                    flash('Already sent to: ' + n)
                else:
                    flash('已经抄送给：' + n)
            else:
                if english == 'yes':
                    flash(n + " is not a user's name. Please check again!")          
                else:
                    flash(n +'不是本站用户名，请通过编辑再次确认！' )
        post = Post(topic=form.topic.data,body=form.body.data,private=private, tag=tag, at_names=names_to_add, time=datetime.today().isoformat()[:-7].replace("T"," "), author=current_user._get_current_object())
        if request.method == 'POST':
            pic = request.files['pic']
            size = (1024, 1024) 
            if pic and allowed_file(pic.filename):
                im = Image.open(pic)
                im.thumbnail(size)        
                filename = secure_filename(pic.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') + '__' + str(time.time()).replace('.','_') + '.' + filename.split('.')[-1]
                im.save(os.path.join('app/static', 'post', filename1))
                post.pic = url_for('static',filename='%s/%s' % ('post', filename1))
        db.session.add(post)
        if english == "yes":
            flash('The post has been uploaded.')
        else:
            flash('帖子已经提交。')
        if 'discussion' in tag:
            return redirect(url_for('.current_lesson',newlesson_id=int(tag.split('_')[1]),tag=tag))
    return render_template('write_newlesson.html', form=form, enctype=enctype,tag=tag, english=english)



@main.route('/write_newlesson2/<string:tag>', methods=['GET', 'POST'])
@login_required
def write_newlesson2(tag):
    english=request.cookies.get('english')
    values = CombinedMultiDict([flask.request.files,flask.request.form])
    if english == "yes":
        form = PostFormE2(values)
    else:
        form = PostForm2(values)
    enctype="multipart/form-data"
    if form.private.data == None:
        private = False
    else:
        private = form.private.data
    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        names = (form.at_names.data).replace('@',' ')
        names_to_add = ""
        for n in names.split():
            user1 = User.query.filter_by(username=n).first()
            if user1:
                names_to_add = names_to_add + ' ' + n
                if english == 'yes':
                    flash('Already sent to: ' + n)
                else:
                    flash('已经抄送给：' + n)
            else:
                if english == 'yes':
                    flash(n + " is not a user's name. Please check again!")          
                else:
                    flash(n +'不是本站用户名，请通过编辑再次确认！' )
        post = Post(topic=form.topic.data,body=form.body.data,
                    private=private,tag=tag,at_names=names_to_add, time=datetime.today().isoformat()[:-7].replace("T"," "),
                    author=current_user._get_current_object())
        if request.method == 'POST':
            pic = request.files['pic']
            size = (1024, 1024) 
            if pic and allowed_file(pic.filename):
                im = Image.open(pic)
                im.thumbnail(size)        
                filename = secure_filename(pic.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' + str(time.time()).replace('.','_') + '.' + filename.split('.')[-1]
                im.save(os.path.join('app/static', 'post', filename1))
                post.pic = url_for('static',filename='%s/%s' % ('post', filename1))
    
            pic1 = request.files['pic1']
            if pic1 and allowed_file(pic1.filename):
                im = Image.open(pic1)
                im.thumbnail(size)        
                filename = secure_filename(pic1.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' + str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
                im.save(os.path.join('app/static', 'post', filename1))
                post.pic1 = url_for('static',filename='%s/%s' % ('post', filename1))
    
            pic2 = request.files['pic2']
            size = (1024, 1024) 
            if pic2 and allowed_file(pic2.filename):
                im = Image.open(pic2)
                im.thumbnail(size)        
                filename = secure_filename(pic2.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' + str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
                im.save(os.path.join('app/static', 'post', filename1))
                post.pic2 = url_for('static',filename='%s/%s' % ('post', filename1))
    
            pic3 = request.files['pic3']
            size = (1024, 1024) 
            if pic3 and allowed_file(pic3.filename):
                im = Image.open(pic3)
                im.thumbnail(size)        
                filename = secure_filename(pic3.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' + str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
                im.save(os.path.join('app/static', 'post', filename1))
                post.pic3 = url_for('static',filename='%s/%s' % ('post', filename1))
    
            file1 = request.files['file1']
            if file1 and allowed_file(file1.filename):
                filename = secure_filename(file1.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' +str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
                file1.save(os.path.join('app/static', 'file', filename1))
                post.file1 = url_for('static',filename='%s/%s' % ('file', filename1))
                post.filename1 = file1.filename        
    
            file2 = request.files['file2']
            if file2 and allowed_file(file2.filename):
                filename = secure_filename(file2.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' +str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
                file2.save(os.path.join('app/static', 'file', filename1))
                post.file2 = url_for('static',filename='%s/%s' % ('file', filename1))
                post.filename2 = file2.filename        
    
            file3 = request.files['file3']
            if file3 and allowed_file(file3.filename):
                filename = secure_filename(file3.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' +str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
                file3.save(os.path.join('app/static', 'audio', filename1))
                post.file3 = url_for('static',filename='%s/%s' % ('audio', filename1))
                post.filename3 = file3.filename        
    
            file4 = request.files['file4']
            if file4 and allowed_file(file4.filename):
                filename = secure_filename(file4.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' +str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
                file4.save(os.path.join('app/static', 'video', filename1))
                post.file4 = url_for('static',filename='%s/%s' % ('video', filename1))
                post.filename4 = file4.filename
    
            file5 = request.files['file5']
            if file5 and allowed_file(file5.filename):
                filename = secure_filename(file5.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' +str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
                file5.save(os.path.join('app/static', 'file', filename1))
                post.file5 = url_for('static',filename='%s/%s' % ('file', filename1))
                post.filename5 = file5.filename
        db.session.add(post)
        if english == "yes":
            flash('The blog has been uploaded.')
        else:
            flash('帖子已经提交。')
        if 'discussion' in tag:
            return redirect(url_for('.current_lesson',newlesson_id=int(tag.split('_')[1]),tag=tag))
        
    return render_template('write_newlesson2.html', form=form,enctype=enctype,tag=tag, english=english)

@main.route('/write_suggestion/<string:tag>', methods=['GET', 'POST'])
@login_required
def write_suggestion(tag):
    english=request.cookies.get('english')
    values = CombinedMultiDict([flask.request.files,flask.request.form])
    if english == "yes":
        form = PostFormE(values)
    else:
        form = PostForm(values)
    enctype="multipart/form-data"
    if form.private.data == None:
        private = False
    else:
        private = form.private.data
    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        names = (form.at_names.data).replace('@',' ')
        names_to_add = ""
        for n in names.split():
            user1 = User.query.filter_by(username=n).first()
            if user1:
                names_to_add = names_to_add + ' ' + n
                if english == 'yes':
                    flash('Already sent to: ' + n)
                else:
                    flash('已经抄送给：' + n)
            else:
                if english == 'yes':
                    flash(n + " is not a user's name. Please check again!")          
                else:
                    flash(n +'不是本站用户名，请通过编辑再次确认！' )
        post = Post(topic=form.topic.data,body=form.body.data,
                    private=private, tag=tag,at_names=names_to_add, time=datetime.today().isoformat()[:-7].replace("T"," "),
                    author=current_user._get_current_object())
        if request.method == 'POST':
            pic = request.files['pic']
            size = (1024, 1024) 
            if pic and allowed_file(pic.filename):
                im = Image.open(pic)
                im.thumbnail(size)        
                filename = secure_filename(pic.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' + str(time.time()).replace('.','_') + '.' + filename.split('.')[-1]
                im.save(os.path.join('app/static', 'post', filename1))
                post.pic = url_for('static',filename='%s/%s' % ('post', filename1))
        if form.private.data == 1:
            if english == "yes":
                flash('The blog has uploaded and set as private, only you and friends being ated can see.')
            else:
                flash('帖子上传并设为私有，仅自己和被@的朋友可见。')
        else:
            if english == "yes":
                flash('The blog has been uploaded.')
            else:
                flash('帖子已经提交。')
        return redirect(url_for('main.suggestion'))
    return render_template('write_suggestion.html', form=form,enctype=enctype,tag=tag, english=english)



@main.route('/write_conference/<string:tag>', methods=['GET', 'POST'])
@login_required
def write_conference(tag):
    english=request.cookies.get('english')
    values = CombinedMultiDict([flask.request.files,flask.request.form])
    if english == "yes":
        form = PostFormE(values)
    else:
        form = PostForm(values)
    enctype="multipart/form-data"
    if form.private.data == None:
        private = False
    else:
        private = form.private.data
    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        names = (form.at_names.data).replace('@',' ')
        names_to_add = ""
        for n in names.split():
            user1 = User.query.filter_by(username=n).first()
            if user1:
                names_to_add = names_to_add + ' ' + n
                if english == 'yes':
                    flash('Already sent to: ' + n)
                else:
                    flash('已经抄送给：' + n)
            else:
                if english == 'yes':
                    flash(n + " is not a user's name. Please check again!")          
                else:
                    flash(n +'不是本站用户名，请通过编辑再次确认！' )
        post = Post(topic=form.topic.data,body=form.body.data,
                    private=private, tag=tag, at_names=names_to_add, time=datetime.today().isoformat()[:-7].replace("T"," "),
                    author=current_user._get_current_object())
        if request.method == 'POST':
            pic = request.files['pic']
            size = (1024, 1024) 
            if pic and allowed_file(pic.filename):
                im = Image.open(pic)
                im.thumbnail(size)        
                filename = secure_filename(pic.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' + str(time.time()).replace('.','_') + '.' + filename.split('.')[-1]
                im.save(os.path.join('app/static', 'post', filename1))
                post.pic = url_for('static',filename='%s/%s' % ('post', filename1))
        if form.private.data == 1:
            if english == "yes":
                flash('The blog has uploaded and set as private, only you and friends being ated can see.')
            else:
                flash('帖子上传并设为私有，仅自己和被@的朋友可见。')
        else:
            if english == "yes":
                flash('The blog has been uploaded.')
            else:
                flash('帖子已经提交。')
        return redirect(url_for('main.conference'))
    return render_template('write_conference.html', form=form,enctype=enctype,tag=tag, english=english)



@main.route('/write0', methods=['GET', 'POST'])
@login_required
def write0():
    english=request.cookies.get('english')
    values = CombinedMultiDict([flask.request.files,flask.request.form])
    if english == "yes":
        form = PostForm0E(values)
    else:
        form = PostForm0(values)
    enctype="multipart/form-data"
    if form.private.data == None:
        private = False
    else:
        private = form.private.data
    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        names = (form.at_names.data).replace('@',' ')
        names_to_add = ""
        for n in names.split():
            user1 = User.query.filter_by(username=n).first()
            if user1:
                names_to_add = names_to_add + ' ' + n
                if english == 'yes':
                    flash('Already sent to: ' + n)
                else:
                    flash('已经抄送给：' + n)
            else:
                if english == 'yes':
                    flash(n + " is not a user's name. Please check again!")          
                else:
                    flash(n +'不是本站用户名，请通过编辑再次确认！' )
        post = Post(topic=form.topic.data,body=form.body.data,
                    private=private, tag=form.tag.data,at_names=names_to_add, time=datetime.today().isoformat()[:-7].replace("T"," "),
                    author=current_user._get_current_object())
        if request.method == 'POST':
            pic = request.files['pic']
            size = (1024, 1024) 
            if pic and allowed_file(pic.filename):
                im = Image.open(pic)
                im.thumbnail(size)        
                filename = secure_filename(pic.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' + str(time.time()).replace('.','_') + '.' + filename.split('.')[-1]
                im.save(os.path.join('app/static', 'post', filename1))
                post.pic = url_for('static',filename='%s/%s' % ('post', filename1))
        if form.private.data == 1:
            if english == "yes":
                flash('The blog has uploaded and set as private, only you and friends being ated can see.')
            else:
                flash('帖子上传并设为私有，仅自己和被@的朋友可见。')
        else:
            if english == "yes":
                flash('The blog has been uploaded.')
            else:
                flash('帖子已经提交。')
        return redirect(url_for('.index'))
    return render_template('write0.html', form=form,enctype=enctype,english=english)


@main.route('/write02', methods=['GET', 'POST'])
@login_required
def write02():
    english=request.cookies.get('english')
    values = CombinedMultiDict([flask.request.files,flask.request.form])
    if english == "yes":
        form = PostForm02E(values)
    else:
        form = PostForm02(values)
    enctype="multipart/form-data"
    if form.private.data == None:
        private = False
    else:
        private = form.private.data
    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        names = (form.at_names.data).replace('@',' ')
        names_to_add = ""
        for n in names.split():
            user1 = User.query.filter_by(username=n).first()
            if user1:
                names_to_add = names_to_add + ' ' + n
                if english == 'yes':
                    flash('Already sent to: ' + n)
                else:
                    flash('已经抄送给：' + n)
            else:
                if english == 'yes':
                    flash(n + " is not a user's name. Please check again!")          
                else:
                    flash(n +'不是本站用户名，请通过编辑再次确认！' )
        post = Post(topic=form.topic.data,body=form.body.data,
                    private=private,tag=form.tag.data,at_names=names_to_add, time=datetime.today().isoformat()[:-7].replace("T"," "),
                    author=current_user._get_current_object())
        if request.method == 'POST':
            pic = request.files['pic']
            size = (1024, 1024) 
            if pic and allowed_file(pic.filename):
                im = Image.open(pic)
                im.thumbnail(size)        
                filename = secure_filename(pic.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' + str(time.time()).replace('.','_') + '.' + filename.split('.')[-1]
                im.save(os.path.join('app/static', 'post', filename1))
                post.pic = url_for('static',filename='%s/%s' % ('post', filename1))
    
            pic1 = request.files['pic1']
            if pic1 and allowed_file(pic1.filename):
                im = Image.open(pic1)
                im.thumbnail(size)        
                filename = secure_filename(pic1.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' + str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
                im.save(os.path.join('app/static', 'post', filename1))
                post.pic1 = url_for('static',filename='%s/%s' % ('post', filename1))
    
            pic2 = request.files['pic2']
            size = (1024, 1024) 
            if pic2 and allowed_file(pic2.filename):
                im = Image.open(pic2)
                im.thumbnail(size)        
                filename = secure_filename(pic2.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' + str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
                im.save(os.path.join('app/static', 'post', filename1))
                post.pic2 = url_for('static',filename='%s/%s' % ('post', filename1))
    
            pic3 = request.files['pic3']
            size = (1024, 1024) 
            if pic3 and allowed_file(pic3.filename):
                im = Image.open(pic3)
                im.thumbnail(size)        
                filename = secure_filename(pic3.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' + str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
                im.save(os.path.join('app/static', 'post', filename1))
                post.pic3 = url_for('static',filename='%s/%s' % ('post', filename1))
    
            file1 = request.files['file1']
            if file1 and allowed_file(file1.filename):
                filename = secure_filename(file1.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' +str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
                file1.save(os.path.join('app/static', 'file', filename1))
                post.file1 = url_for('static',filename='%s/%s' % ('file', filename1))
                post.filename1 = file1.filename        
    
            file2 = request.files['file2']
            if file2 and allowed_file(file2.filename):
                filename = secure_filename(file2.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' +str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
                file2.save(os.path.join('app/static', 'file', filename1))
                post.file2 = url_for('static',filename='%s/%s' % ('file', filename1))
                post.filename2 = file2.filename        
    
            file3 = request.files['file3']
            if file3 and allowed_file(file3.filename):
                filename = secure_filename(file3.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' +str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
                file3.save(os.path.join('app/static', 'audio', filename1))
                post.file3 = url_for('static',filename='%s/%s' % ('audio', filename1))
                post.filename3 = file3.filename        
    
            file4 = request.files['file4']
            if file4 and allowed_file(file4.filename):
                filename = secure_filename(file4.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' +str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
                file4.save(os.path.join('app/static', 'video', filename1))
                post.file4 = url_for('static',filename='%s/%s' % ('video', filename1))
                post.filename4 = file4.filename
    
            file5 = request.files['file5']
            if file5 and allowed_file(file5.filename):
                filename = secure_filename(file5.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' +str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
                file5.save(os.path.join('app/static', 'file', filename1))
                post.file5 = url_for('static',filename='%s/%s' % ('file', filename1))
                post.filename5 = file5.filename
        if form.private.data == 1:
            if english == "yes":
                flash('The blog has uploaded and set as private, only you and friends being ated can see.')
            else:
                flash('帖子上传并设为私有，仅自己和被@的朋友可见。')
        else:
            if english == "yes":
                flash('The blog has been uploaded.')
            else:
                flash('帖子已经提交。')
        return redirect(url_for('.index'))
    return render_template('write02.html', form=form,enctype=enctype, english=english)



@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    english=request.cookies.get('english')
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
            not current_user.can(Permission.ADMINISTER):
        abort(403)
    if english == "yes":
        form = PostFormE()
    else:
        form = PostForm()
    if form.validate_on_submit():
        names = (form.at_names.data).replace('@',' ')
        names_to_add = ""
        for n in names.split():
            user1 = User.query.filter_by(username=n).first()
            if user1:
                names_to_add = names_to_add + ' ' + n
                if english == 'yes':
                    flash('Already sent to: ' + n)
                else:
                    flash('已经抄送给：' + n)
            else:
                if english == 'yes':
                    flash(n + " is not a user's name. Please check again!")          
                else:
                    flash(n +'不是本站用户名，请通过编辑再次确认！' )
        post.topic = form.topic.data
        post.body = form.body.data
        post.private = form.private.data
        post.at_names = names_to_add

        pic = request.files['pic']
        size = (1024, 1024) 
        if pic and allowed_file(pic.filename):
            im = Image.open(pic)
            im.thumbnail(size)        
            filename = secure_filename(pic.filename)
            filename1 = current_user.email.replace('@','__').replace('.','__') \
                        + '__' + str(time.time()).replace('.','_') + '.' + filename.split('.')[-1]
            im.save(os.path.join('app/static', 'post', filename1))
            try:
                os.remove("/root/cryptoepoch/app"+post.pic)
            except:
                pass
            post.pic = url_for('static',filename='%s/%s' % ('post', filename1))
      
        db.session.add(post)
        if form.private.data == 1:
            if english == "yes":
                flash('The blog has modified and set as private, only you and friends being ated can see.')
            else:
                flash('帖子修改并设为私有，仅自己和被@的朋友可见。')
        else:
            if english == "yes":
                flash('The blog has been modified.')
            else:
                flash('帖子已经修改。')
        if post.tag != None and 'suggestion' in post.tag:
            return redirect(url_for('.suggestion'))
        elif 'newlessons' in post.tag:
            return redirect(url_for('.current_lesson',newlesson_id=int(post.tag.split('_')[1]),tag=post.tag))
        else:
            return redirect(url_for('.post', id=post.id))
    form.topic.data = post.topic
    form.body.data = post.body
    form.private.data = post.private
    form.at_names.data = post.at_names
    
    return render_template('edit_post.html', form=form,id=id, tag=post.tag, english=english)


@main.route('/edit-news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    english=request.cookies.get('english')
    news = New.query.get_or_404(id)
    if current_user.id != news.author_id and \
            not current_user.can(Permission.ADMINISTER):
        abort(403)
    if english == "yes":
        form = NewsFormE()
    else:
        form = NewsForm()
    if form.validate_on_submit():
        names = (form.at_names.data).replace('@',' ')
        names_to_add = ""
        for n in names.split():
            user1 = User.query.filter_by(username=n).first()
            if user1:
                names_to_add = names_to_add + ' ' + n
                if english == 'yes':
                    flash('Already sent to: ' + n)
                else:
                    flash('已经抄送给：' + n)
            else:
                if english == 'yes':
                    flash(n + " is not a user's name. Please check again!")          
                else:
                    flash(n +'不是本站用户名，请通过编辑再次确认！' )
        news.topic = form.topic.data
        news.body = form.body.data
        news.private = form.private.data
        db.session.add(news)
        if form.private.data == 1:
            if english == "yes":
                flash('The blog has modified and set as private, only you and friends being ated can see.')
            else:
                flash('帖子修改并设为私有，仅自己和被@的朋友可见。')
        else:
            if english == "yes":
                flash('The blog has been modified.')
            else:
                flash('帖子已经修改。')
        return redirect(url_for('.new', id=news.id))
    form.topic.data = news.topic
    form.body.data = news.body
    form.private.data = news.private
    
    return render_template('edit_news.html', form=form, id=id, tag=news.tag, english=english)


@main.route('/edit2/<int:id>', methods=['GET', 'POST'])
@login_required
def edit2(id):
    english=request.cookies.get('english')
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
            not current_user.can(Permission.ADMINISTER):
        abort(403)
    if english == "yes":
        form = PostFormE2()
    else:
        form = PostForm2()
    if form.validate_on_submit():
        names = (form.at_names.data).replace('@',' ')
        names_to_add = ""
        for n in names.split():
            user1 = User.query.filter_by(username=n).first()
            if user1:
                names_to_add = names_to_add + ' ' + n
                if english == 'yes':
                    flash('Already sent to: ' + n)
                else:
                    flash('已经抄送给：' + n)
            else:
                if english == 'yes':
                    flash(n + " is not a user's name. Please check again!")          
                else:
                    flash(n +'不是本站用户名，请通过编辑再次确认！' )
        post.topic = form.topic.data
        post.body = form.body.data
        post.private = form.private.data
        post.at_names = names_to_add
        pic = request.files['pic']
        size = (1024, 1024) 
        if pic and allowed_file(pic.filename):
            im = Image.open(pic)
            im.thumbnail(size)        
            filename = secure_filename(pic.filename)
            filename1 = current_user.email.replace('@','__').replace('.','__') \
                        + '__' + str(time.time()).replace('.','_') + '.' + filename.split('.')[-1]
            im.save(os.path.join('app/static', 'post', filename1))
            try:
                os.remove("/root/cryptoepoch/app"+post.pic)
            except:
                pass    
                    
            post.pic = url_for('static',filename='%s/%s' % ('post', filename1))

        pic1 = request.files['pic1']
        size = (1024, 1024) 
        if pic1 and allowed_file(pic1.filename):
            im = Image.open(pic1)
            im.thumbnail(size)        
            filename = secure_filename(pic1.filename)
            filename1 = current_user.email.replace('@','__').replace('.','__') \
                        + '__' + str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
            im.save(os.path.join('app/static', 'post', filename1))
            try:
                os.remove("/root/cryptoepoch/app"+post.pic1)
            except:
                pass
            post.pic1 = url_for('static',filename='%s/%s' % ('post', filename1))

        pic2 = request.files['pic2']
        size = (1024, 1024) 
        if pic2 and allowed_file(pic2.filename):
            im = Image.open(pic2)
            im.thumbnail(size)        
            filename = secure_filename(pic2.filename)
            filename1 = current_user.email.replace('@','__').replace('.','__') \
                        + '__' + str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
            im.save(os.path.join('app/static', 'post', filename1))
            try:
                os.remove("/root/cryptoepoch/app"+post.pic2)
            except:
                pass
            post.pic2 = url_for('static',filename='%s/%s' % ('post', filename1))

        pic3 = request.files['pic3']
        size = (1024, 1024) 
        if pic3 and allowed_file(pic3.filename):
            im = Image.open(pic3)
            im.thumbnail(size)        
            filename = secure_filename(pic3.filename)
            filename1 = current_user.email.replace('@','__').replace('.','__') \
                        + '__' + str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
            im.save(os.path.join('app/static', 'post', filename1))
            try:
                os.remove("/root/cryptoepoch/app"+post.pic3)
            except:
                pass
            post.pic3 = url_for('static',filename='%s/%s' % ('post', filename1))

        file1 = request.files['file1']
        if file1 and allowed_file(file1.filename):
            filename = secure_filename(file1.filename)
            filename1 = current_user.email.replace('@','__').replace('.','__') \
                        + '__' +str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
            file1.save(os.path.join('app/static', 'file', filename1))
            try:
                os.remove("/root/cryptoepoch/app"+post.file1)
            except:
                pass
            post.file1 = url_for('static',filename='%s/%s' % ('file', filename1))
            post.filename1 = file1.filename        

        file2 = request.files['file2']
        if file2 and allowed_file(file2.filename):
            filename = secure_filename(file2.filename)
            filename1 = current_user.email.replace('@','__').replace('.','__') \
                        + '__' +str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
            file2.save(os.path.join('app/static', 'file', filename1))
            try:
                os.remove("/root/cryptoepoch/app"+post.file2)
            except:
                pass
            post.file2 = url_for('static',filename='%s/%s' % ('file', filename1))
            post.filename2 = file2.filename        

        file3 = request.files['file3']
        if file3 and allowed_file(file3.filename):
            filename = secure_filename(file3.filename)
            filename1 = current_user.email.replace('@','__').replace('.','__') \
                        + '__' +str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
            file3.save(os.path.join('app/static', 'audio', filename1))
            try:
                os.remove("/root/cryptoepoch/app"+post.file3)
            except:
                pass
            post.file3 = url_for('static',filename='%s/%s' % ('audio', filename1))
            post.filename3 = file3.filename        

        file4 = request.files['file4']
        if file4 and allowed_file(file4.filename):
            filename = secure_filename(file4.filename)
            filename1 = current_user.email.replace('@','__').replace('.','__') \
                        + '__' +str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
            file4.save(os.path.join('app/static', 'video', filename1))
            try:
                os.remove("/root/cryptoepoch/app"+post.file4)
            except:
                pass
            post.file4 = url_for('static',filename='%s/%s' % ('video', filename1))
            post.filename4 = file4.filename

        file5 = request.files['file5']
        if file5 and allowed_file(file5.filename):
            filename = secure_filename(file5.filename)
            filename1 = current_user.email.replace('@','__').replace('.','__') \
                        + '__' +str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
            file5.save(os.path.join('app/static', 'file', filename1))
            try:
                os.remove("/root/cryptoepoch/app"+post.file5)
            except:
                pass
            post.file5 = url_for('static',filename='%s/%s' % ('file', filename1))
            post.filename5 = file5.filename
            
        db.session.commit()
        if form.private.data == 1:
            if english == "yes":
                flash('The blog has modified and set as private, only you and friends being ated can see.')
            else:
                flash('帖子修改并设为私有，仅自己和被@的朋友可见。')
        else:
            if english == "yes":
                flash('The blog has been modified.')
            else:
                flash('帖子已经修改。')
        if post.tag != None and 'suggestion' in post.tag:
            return redirect(url_for('.suggestion'))
        elif post.tag != None and 'newlessons' in post.tag:
            return redirect(url_for('.current_lesson',newlesson_id=int(post.tag.split('_')[1]),tag=post.tag))
        else:
            return redirect(url_for('.post', id=post.id))
    form.topic.data = post.topic
    form.body.data = post.body
    form.private.data = post.private
    form.at_names.data = post.at_names
    
    return render_template('edit_post2.html', form=form, id=id, tag=post.tag, english=english)



@main.route('/edit0/<int:id>', methods=['GET', 'POST'])
@login_required
def edit0(id):
    english=request.cookies.get('english')
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
            not current_user.can(Permission.ADMINISTER):
        abort(403)
    if english == "yes":
        form = PostForm0E()
    else:
        form = PostForm0()
    if form.validate_on_submit():
        names = (form.at_names.data).replace('@',' ')
        names_to_add = ""
        for n in names.split():
            user1 = User.query.filter_by(username=n).first()
            if user1:
                names_to_add = names_to_add + ' ' + n
                if english == 'yes':
                    flash('Already sent to: ' + n)
                else:
                    flash('已经抄送给：' + n)
            else:
                if english == 'yes':
                    flash(n + " is not a user's name. Please check again!")          
                else:
                    flash(n +'不是本站用户名，请通过编辑再次确认！' )
        post.topic = form.topic.data
        post.body = form.body.data
        post.tag = form.tag.data
        post.private = form.private.data
        post.at_names = names_to_add

        pic = request.files['pic']
        size = (1024, 1024) 
        if pic and allowed_file(pic.filename):
            im = Image.open(pic)
            im.thumbnail(size)        
            filename = secure_filename(pic.filename)
            filename1 = current_user.email.replace('@','__').replace('.','__') \
                        + '__' + str(time.time()).replace('.','_') + '.' + filename.split('.')[-1]
            im.save(os.path.join('app/static', 'post', filename1))
            try:
                os.remove("/root/cryptoepoch/app"+post.pic)
            except:
                pass
            post.pic = url_for('static',filename='%s/%s' % ('post', filename1))
      
        db.session.add(post)
        if form.private.data == 1:
            if english == "yes":
                flash('The blog has modified and set as private, only you and friends being ated can see.')
            else:
                flash('帖子修改并设为私有，仅自己和被@的朋友可见。')
        else:
            if english == "yes":
                flash('The blog has been modified.')
            else:
                flash('帖子已经修改。')
        if post.tag != None and 'suggestion' in post.tag:
            return redirect(url_for('.suggestion'))
        elif post.tag != None and 'newlessons' in post.tag:
            return redirect(url_for('.current_lesson',newlesson_id=int(post.tag.split('_')[1]),tag=post.tag))
        else:
            return redirect(url_for('.post', id=post.id))
    form.topic.data = post.topic
    form.tag.data = post.tag
    form.body.data = post.body
    form.private.data = post.private
    form.at_names = post.at_names
    
    return render_template('edit_post0.html', form=form,id=id, tag=post.tag, english=english)


@main.route('/edit02/<int:id>', methods=['GET', 'POST'])
@login_required
def edit02(id):
    english=request.cookies.get('english')
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
            not current_user.can(Permission.ADMINISTER):
        abort(403)
    if english == "yes":
        form = PostForm02E()
    else:
        form = PostForm02()
    if form.validate_on_submit():
        names = (form.at_names.data).replace('@',' ')
        names_to_add = ""
        for n in names.split():
            user1 = User.query.filter_by(username=n).first()
            if user1:
                names_to_add = names_to_add + ' ' + n
                if english == 'yes':
                    flash('Already sent to: ' + n)
                else:
                    flash('已经抄送给：' + n)
            else:
                if english == 'yes':
                    flash(n + " is not a user's name. Please check again!")          
                else:
                    flash(n +'不是本站用户名，请通过编辑再次确认！' )
        post.topic = form.topic.data
        post.body = form.body.data
        post.private = form.private.data
        post.tag = form.tag.data
        post.at_names = names_to_add
        pic = request.files['pic']
        size = (1024, 1024) 
        if pic and allowed_file(pic.filename):
            im = Image.open(pic)
            im.thumbnail(size)        
            filename = secure_filename(pic.filename)
            filename1 = current_user.email.replace('@','__').replace('.','__') \
                        + '__' + str(time.time()).replace('.','_') + '.' + filename.split('.')[-1]
            im.save(os.path.join('app/static', 'post', filename1))
            try:
                os.remove("/root/cryptoepoch/app"+post.pic)
            except:
                pass    
                    
            post.pic = url_for('static',filename='%s/%s' % ('post', filename1))

        pic1 = request.files['pic1']
        size = (1024, 1024) 
        if pic1 and allowed_file(pic1.filename):
            im = Image.open(pic1)
            im.thumbnail(size)        
            filename = secure_filename(pic1.filename)
            filename1 = current_user.email.replace('@','__').replace('.','__') \
                        + '__' + str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
            im.save(os.path.join('app/static', 'post', filename1))
            try:
                os.remove("/root/cryptoepoch/app"+post.pic1)
            except:
                pass
            post.pic1 = url_for('static',filename='%s/%s' % ('post', filename1))

        pic2 = request.files['pic2']
        size = (1024, 1024) 
        if pic2 and allowed_file(pic2.filename):
            im = Image.open(pic2)
            im.thumbnail(size)        
            filename = secure_filename(pic2.filename)
            filename1 = current_user.email.replace('@','__').replace('.','__') \
                        + '__' + str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
            im.save(os.path.join('app/static', 'post', filename1))
            try:
                os.remove("/root/cryptoepoch/app"+post.pic2)
            except:
                pass
            post.pic2 = url_for('static',filename='%s/%s' % ('post', filename1))

        pic3 = request.files['pic3']
        size = (1024, 1024) 
        if pic3 and allowed_file(pic3.filename):
            im = Image.open(pic3)
            im.thumbnail(size)        
            filename = secure_filename(pic3.filename)
            filename1 = current_user.email.replace('@','__').replace('.','__') \
                        + '__' + str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
            im.save(os.path.join('app/static', 'post', filename1))
            try:
                os.remove("/root/cryptoepoch/app"+post.pic3)
            except:
                pass
            post.pic3 = url_for('static',filename='%s/%s' % ('post', filename1))

        file1 = request.files['file1']
        if file1 and allowed_file(file1.filename):
            filename = secure_filename(file1.filename)
            filename1 = current_user.email.replace('@','__').replace('.','__') \
                        + '__' +str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
            file1.save(os.path.join('app/static', 'file', filename1))
            try:
                os.remove("/root/cryptoepoch/app"+post.file1)
            except:
                pass
            post.file1 = url_for('static',filename='%s/%s' % ('file', filename1))
            post.filename1 = file1.filename        

        file2 = request.files['file2']
        if file2 and allowed_file(file2.filename):
            filename = secure_filename(file2.filename)
            filename1 = current_user.email.replace('@','__').replace('.','__') \
                        + '__' +str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
            file2.save(os.path.join('app/static', 'file', filename1))
            try:
                os.remove("/root/cryptoepoch/app"+post.file2)
            except:
                pass
            post.file2 = url_for('static',filename='%s/%s' % ('file', filename1))
            post.filename2 = file2.filename        

        file3 = request.files['file3']
        if file3 and allowed_file(file3.filename):
            filename = secure_filename(file3.filename)
            filename1 = current_user.email.replace('@','__').replace('.','__') \
                        + '__' +str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
            file3.save(os.path.join('app/static', 'audio', filename1))
            try:
                os.remove("/root/cryptoepoch/app"+post.file3)
            except:
                pass
            post.file3 = url_for('static',filename='%s/%s' % ('audio', filename1))
            post.filename3 = file3.filename        

        file4 = request.files['file4']
        if file4 and allowed_file(file4.filename):
            filename = secure_filename(file4.filename)
            filename1 = current_user.email.replace('@','__').replace('.','__') \
                        + '__' +str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
            file4.save(os.path.join('app/static', 'video', filename1))
            try:
                os.remove("/root/cryptoepoch/app"+post.file4)
            except:
                pass
            post.file4 = url_for('static',filename='%s/%s' % ('video', filename1))
            post.filename4 = file4.filename

        file5 = request.files['file5']
        if file5 and allowed_file(file5.filename):
            filename = secure_filename(file5.filename)
            filename1 = current_user.email.replace('@','__').replace('.','__') \
                        + '__' +str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
            file5.save(os.path.join('app/static', 'file', filename1))
            try:
                os.remove("/root/cryptoepoch/app"+post.file5)
            except:
                pass
            post.file5 = url_for('static',filename='%s/%s' % ('file', filename1))
            post.filename5 = file5.filename
            
        db.session.commit()
        if form.private.data == 1:
            if english == "yes":
                flash('The blog has modified and set as private, only you and friends being ated can see.')
            else:
                flash('帖子修改并设为私有，仅自己和被@的朋友可见。')
        else:
            if english == "yes":
                flash('The blog has been modified.')
            else:
                flash('帖子已经修改。')
        if post.tag != None and 'suggestion' in post.tag:
            return redirect(url_for('.suggestion'))
        elif post.tag != None and 'newlessons' in post.tag:
            return redirect(url_for('.current_lesson',newlesson_id=int(post.tag.split('_')[1]),tag=post.tag))
        else:
            return redirect(url_for('.post', id=post.id))
    form.topic.data = post.topic
    form.tag.data = post.tag
    form.body.data = post.body
    form.private.data = post.private
    
    return render_template('edit_post02.html', form=form, id=id, tag=post.tag, english=english)


@main.route('/edit_post_newlesson/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post_newlesson(id):
    english=request.cookies.get('english')
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
            not current_user.can(Permission.ADMINISTER):
        abort(403)
    if english == "yes":
        form = PostFormE()
    else:
        form = PostForm()
    if form.validate_on_submit():
        names = (form.at_names.data).replace('@',' ')
        names_to_add = ""
        for n in names.split():
            user1 = User.query.filter_by(username=n).first()
            if user1:
                names_to_add = names_to_add + ' ' + n
                if english == 'yes':
                    flash('Already sent to: ' + n)
                else:
                    flash('已经抄送给：' + n)
            else:
                if english == 'yes':
                    flash(n + " is not a user's name. Please check again!")          
                else:
                    flash(n +'不是本站用户名，请通过编辑再次确认！' )
        post.topic = form.topic.data
        post.body = form.body.data
        post.private = form.private.data
        post.at_names = names_to_add

        pic = request.files['pic']
        size = (1024, 1024) 
        if pic and allowed_file(pic.filename):
            im = Image.open(pic)
            im.thumbnail(size)        
            filename = secure_filename(pic.filename)
            filename1 = current_user.email.replace('@','__').replace('.','__') \
                        + '__' + str(time.time()).replace('.','_') + '.' + filename.split('.')[-1]
            im.save(os.path.join('app/static', 'post', filename1))
            try:
                os.remove("/root/cryptoepoch/app"+post.pic)
            except:
                pass
            post.pic = url_for('static',filename='%s/%s' % ('post', filename1))
      
        db.session.add(post)
        if form.private.data == 1:
            if english == "yes":
                flash('The blog has modified and set as private, only you and friends being ated can see.')
            else:
                flash('帖子修改并设为私有，仅自己和被@的朋友可见。')
        else:
            if english == "yes":
                flash('The blog has been modified.')
            else:
                flash('帖子已经修改。')
        if post.tag != None and 'suggestion' in post.tag:
            return redirect(url_for('.suggestion'))
        elif post.tag != None and 'newlessons' in post.tag:
            return redirect(url_for('.current_lesson',newlesson_id=int(post.tag.split('_')[1]),tag=post.tag))
        else:
            return redirect(url_for('.post', id=post.id))
    form.topic.data = post.topic
    form.body.data = post.body
    form.private.data = post.private
    form.at_names.data = post.at_names
    return render_template('edit_post_newlesson.html', form=form,id=id, tag=post.tag, english=english)


@main.route('/edit_post_newlesson2/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post_newlesson2(id):
    english=request.cookies.get('english')
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
            not current_user.can(Permission.ADMINISTER):
        abort(403)
    if english == "yes":
        form = PostFormE2()
    else:
        form = PostForm2()
    if form.validate_on_submit():
        names = (form.at_names.data).replace('@',' ')
        names_to_add = ""
        for n in names.split():
            user1 = User.query.filter_by(username=n).first()
            if user1:
                names_to_add = names_to_add + ' ' + n
                if english == 'yes':
                    flash('Already sent to: ' + n)
                else:
                    flash('已经抄送给：' + n)
            else:
                if english == 'yes':
                    flash(n + " is not a user's name. Please check again!")          
                else:
                    flash(n +'不是本站用户名，请通过编辑再次确认！' )
        post.topic = form.topic.data
        post.body = form.body.data
        post.private = form.private.data
        post.at_names = names_to_add

        pic = request.files['pic']
        size = (1024, 1024) 
        if pic and allowed_file(pic.filename):
            im = Image.open(pic)
            im.thumbnail(size)        
            filename = secure_filename(pic.filename)
            filename1 = current_user.email.replace('@','__').replace('.','__') \
                        + '__' + str(time.time()).replace('.','_') + '.' + filename.split('.')[-1]
            im.save(os.path.join('app/static', 'post', filename1))
            try:
                os.remove("/root/cryptoepoch/app"+post.pic)
            except:
                pass    
                    
            post.pic = url_for('static',filename='%s/%s' % ('post', filename1))

        pic1 = request.files['pic1']
        size = (1024, 1024) 
        if pic1 and allowed_file(pic1.filename):
            im = Image.open(pic1)
            im.thumbnail(size)        
            filename = secure_filename(pic1.filename)
            filename1 = current_user.email.replace('@','__').replace('.','__') \
                        + '__' + str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
            im.save(os.path.join('app/static', 'post', filename1))
            try:
                os.remove("/root/cryptoepoch/app"+post.pic1)
            except:
                pass
            post.pic1 = url_for('static',filename='%s/%s' % ('post', filename1))

        pic2 = request.files['pic2']
        size = (1024, 1024) 
        if pic2 and allowed_file(pic2.filename):
            im = Image.open(pic2)
            im.thumbnail(size)        
            filename = secure_filename(pic2.filename)
            filename1 = current_user.email.replace('@','__').replace('.','__') \
                        + '__' + str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
            im.save(os.path.join('app/static', 'post', filename1))
            try:
                os.remove("/root/cryptoepoch/app"+post.pic2)
            except:
                pass
            post.pic2 = url_for('static',filename='%s/%s' % ('post', filename1))

        pic3 = request.files['pic3']
        size = (1024, 1024) 
        if pic3 and allowed_file(pic3.filename):
            im = Image.open(pic3)
            im.thumbnail(size)        
            filename = secure_filename(pic3.filename)
            filename1 = current_user.email.replace('@','__').replace('.','__') \
                        + '__' + str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
            im.save(os.path.join('app/static', 'post', filename1))
            try:
                os.remove("/root/cryptoepoch/app"+post.pic3)
            except:
                pass
            post.pic3 = url_for('static',filename='%s/%s' % ('post', filename1))

        file1 = request.files['file1']
        if file1 and allowed_file(file1.filename):
            filename = secure_filename(file1.filename)
            filename1 = current_user.email.replace('@','__').replace('.','__') \
                        + '__' +str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
            file1.save(os.path.join('app/static', 'file', filename1))
            try:
                os.remove("/root/cryptoepoch/app"+post.file1)
            except:
                pass
            post.file1 = url_for('static',filename='%s/%s' % ('file', filename1))
            post.filename1 = file1.filename        

        file2 = request.files['file2']
        if file2 and allowed_file(file2.filename):
            filename = secure_filename(file2.filename)
            filename1 = current_user.email.replace('@','__').replace('.','__') \
                        + '__' +str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
            file2.save(os.path.join('app/static', 'file', filename1))
            try:
                os.remove("/root/cryptoepoch/app"+post.file2)
            except:
                pass
            post.file2 = url_for('static',filename='%s/%s' % ('file', filename1))
            post.filename2 = file2.filename        

        file3 = request.files['file3']
        if file3 and allowed_file(file3.filename):
            filename = secure_filename(file3.filename)
            filename1 = current_user.email.replace('@','__').replace('.','__') \
                        + '__' +str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
            file3.save(os.path.join('app/static', 'audio', filename1))
            try:
                os.remove("/root/cryptoepoch/app"+post.file3)
            except:
                pass
            post.file3 = url_for('static',filename='%s/%s' % ('audio', filename1))
            post.filename3 = file3.filename        

        file4 = request.files['file4']
        if file4 and allowed_file(file4.filename):
            filename = secure_filename(file4.filename)
            filename1 = current_user.email.replace('@','__').replace('.','__') \
                        + '__' +str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
            file4.save(os.path.join('app/static', 'video', filename1))
            try:
                os.remove("/root/cryptoepoch/app"+post.file4)
            except:
                pass
            post.file4 = url_for('static',filename='%s/%s' % ('video', filename1))
            post.filename4 = file4.filename

        file5 = request.files['file5']
        if file5 and allowed_file(file5.filename):
            filename = secure_filename(file5.filename)
            filename1 = current_user.email.replace('@','__').replace('.','__') \
                        + '__' +str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
            file5.save(os.path.join('app/static', 'file', filename1))
            try:
                os.remove("/root/cryptoepoch/app"+post.file5)
            except:
                pass
            post.file5 = url_for('static',filename='%s/%s' % ('file', filename1))
            post.filename5 = file5.filename
            
        db.session.commit()
        if form.private.data == 1:
            if english == "yes":
                flash('The blog has modified and set as private, only you and friends being ated can see.')
            else:
                flash('帖子修改并设为私有，仅自己和被@的朋友可见。')
        else:
            if english == "yes":
                flash('The blog has been modified.')
            else:
                flash('帖子已经修改。')
        if post.tag != None and 'suggestion' in post.tag:
            return redirect(url_for('.suggestion'))
        elif post.tag != None and 'newlessons' in post.tag:
            return redirect(url_for('.current_lesson',newlesson_id=int(post.tag.split('_')[1]),tag=post.tag))
        else:
            return redirect(url_for('.post', id=post.id))
    form.topic.data = post.topic
    form.body.data = post.body
    form.private.data = post.private
    form.at_names.data = post.at_names
    return render_template('edit_post_newlesson2.html', form=form, id=id, tag=post.tag, english=english)


@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    english=request.cookies.get('english')
    user = User.query.filter_by(username=username).first()
    if user is None:
        if english == "yes":
            flash('Invalid user.')
        else:
            flash('无效用户。')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        if english == "yes":
            flash('You have followed him/her.')
        else:
            flash('您已关注此人。')
        return redirect(url_for('.user', username=username))
    current_user.follow(user)
    if english == "yes":
        flash('You have followed ' % username)
    else:
        flash('您已关注了 %s。' % username)
    return redirect(url_for('.user', username=username))


@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    english=request.cookies.get('english')
    user = User.query.filter_by(username=username).first()
    if user is None:
        if english == "yes":
            flash('无效用户，')
        else:
            flash('Invalid user.')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        if english == "yes":
            flash("You haven't followed him/her.")
        else:
            flash('您没有关注此人。')
        return redirect(url_for('.user', username=username))
    current_user.unfollow(user)
    if english == "yes":
        flash('You do not follow %s any more。' % username)
    else:
        flash('您不再关注 %s 。' % username)
    return redirect(url_for('.user', username=username))


@main.route('/followers/<username>')
def followers(username):
    english=request.cookies.get('english')
    user = User.query.filter_by(username=username).first()
    if user is None:
        if english == "yes":
            flash('Invalid user.')
        else:
            flash('无效用户。')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, 
                           endpoint='.followers', pagination=pagination,
                           follows=follows, english=english)


@main.route('/followed-by/<username>')
def followed_by(username):
    english=request.cookies.get('english')
    user = User.query.filter_by(username=username).first()
    if user is None:
        if english == "yes":
            flash('Invalid user.')
        else:
            flash('无效用户。')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followered-by.html', user=user, 
                           endpoint='.followed_by', pagination=pagination,
                           follows=follows, english=english)


@main.route('/show-write')
@login_required
def show_write():
    resp = make_response(redirect(url_for('.write')))
    resp.set_cookie('show_write', '1', max_age=30*24*60*60)
    return resp


@main.route('/del-user/<int:id>')
@login_required
def del_user(id):
    User.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('.user',username=current_user.username))


@main.route('/del-teacher/<int:id>')
@login_required
def del_teacher(id):
    Teacher.query.filter_by(id=id).delete()
    current_user.teacher = 0
    db.session.commit()
    return redirect(url_for('.user',username=current_user.username))


@main.route('/del-post/<int:id>')
@login_required
def del_post(id):
    post = Post.query.filter_by(id=id).first()
    tag = post.tag
    if post.pic != None:
        try:
            os.remove("/root/cryptoepoch/app"+post.pic)
        except:
            pass    
    if post.pic1 != None:
        try:
            os.remove("/root/cryptoepoch/app"+post.pic1)
        except:
            pass    
    if post.pic2 != None:
        try:
            os.remove("/root/cryptoepoch/app"+post.pic2)
        except:
            pass    
    if post.pic3 != None:
        try:
            os.remove("/root/cryptoepoch/app"+post.pic3)
        except:
            pass    
    if post.file1 != None:
        try:
            os.remove("/root/cryptoepoch/app"+post.file1)
        except:
            pass    
    if post.file2 != None:
        try:
            os.remove("/root/cryptoepoch/app"+post.file2)
        except:
            pass    
    if post.file3 != None:
        try:
            os.remove("/root/cryptoepoch/app"+post.file3)
        except:
            pass    
    if post.file4 != None:
        try:
            os.remove("/root/cryptoepoch/app"+post.file4)
        except:
            pass    
    if post.file5 != None:
        try:
            os.remove("/root/cryptoepoch/app"+post.file5)
        except:
            pass     
    db.session.delete(Post.query.get_or_404(id))
    db.session.commit()
    if 'posts' in tag:
        return redirect(url_for('.user',username=current_user.username))
    if 'suggestion' in tag:
        return redirect(url_for('.suggestion'))
    if 'newlessons' in tag:
        return redirect(url_for('.current_lesson',newlesson_id=int(tag.split('_')[1]),tag=tag))
    if 'research' in tag:
        return redirect(url_for('.research'))
    if 'basic' in tag:
        return redirect(url_for('.basic'))
    else:
        return redirect(url_for('.index'))

@main.route('/del-news/<int:id>')
@login_required
def del_news(id):
    db.session.delete(New.query.get_or_404(id))
    db.session.commit()
    return redirect(url_for('.index'))


@main.route('/del-comment/<int:id>')
@login_required
def del_comment(id):
    AtMe.query.filter_by(comment_id=id).delete()
    id2 = Comment.query.get_or_404(id).post_id
    db.session.delete(Comment.query.get_or_404(id))
    db.session.commit()
    if id2 == None:
        return redirect(url_for('.index'))        
    return redirect(url_for('.post',id=id2))

@main.route('/del-news-comment/<int:id>')
@login_required
def del_news_comment(id):
    AtMe.query.filter_by(comment_id=id).delete()
    id2 = Comment.query.get_or_404(id).new_id
    db.session.delete(Comment.query.get_or_404(id))
    db.session.commit()
    if id2 == None:
        return redirect(url_for('.index'))        
    return redirect(url_for('.new',id=id2))


@main.route('/del-oldnews-comment/<int:id>')
@login_required
def del_oldnews_comment(id):
    AtMe.query.filter_by(comment_id=id).delete()
    id2 = Comment.query.get_or_404(id).oldnew_id
    db.session.delete(Comment.query.get_or_404(id))
    db.session.commit()
    if id2 == None:
        return redirect(url_for('.index'))        
    return redirect(url_for('.oldnew',id=id2))


@main.route('/del-comment2/<int:id>')
@login_required
def del_comment2(id):
    db.session.delete(Comment.query.get_or_404(id))
    db.session.commit()
    return redirect(url_for('.sent_comments',user_id=current_user.id))

@main.route('/open-lesson', methods=['GET', 'POST'])
@login_required
def open_lesson():
    english=request.cookies.get('english')
    values = CombinedMultiDict([flask.request.files,flask.request.form])
    if english == "yes":
        form = AddLessonFormE(values)
    else:
        form = AddLessonForm(values)
    if current_user.can(Permission.WRITE_ARTICLES) and \
            form.validate_on_submit():
        lesson = Lesson(lesson_name=form.lesson_name.data,\
                        about_lesson=form.about_lesson.data,teacher_id=current_user.id)
        if request.method == 'POST':
            pic = request.files['pic']
            size = (1024, 1024) 
            if pic and allowed_file(pic.filename):
                im = Image.open(pic)
                im.thumbnail(size)        
                filename = secure_filename(pic.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' + str(time.time()).replace('.','_') + '.' + filename.split('.')[-1]
                im.save(os.path.join('app/static', 'lesson', filename1))
                lesson.pic = url_for('static',filename='%s/%s' % ('lesson', filename1))      

            file1 = request.files['file1']
            if file1 and allowed_file(file1.filename):
                filename = secure_filename(file1.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' +str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
                file1.save(os.path.join('app/static', 'file', filename1))
                lesson.file1 = url_for('static',filename='%s/%s' % ('lessonfile', filename1))
                lesson.filename1 = file1.filename        
    
            file2 = request.files['file2']
            if file2 and allowed_file(file2.filename):
                filename = secure_filename(file2.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' +str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
                file2.save(os.path.join('app/static', 'file', filename1))
                lesson.file2 = url_for('static',filename='%s/%s' % ('lessonfile', filename1))
                lesson.filename2 = file2.filename        
    
            file3 = request.files['file3']
            if file3 and allowed_file(file3.filename):
                filename = secure_filename(file3.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' +str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
                file3.save(os.path.join('app/static', 'file', filename1))
                lesson.file3 = url_for('static',filename='%s/%s' % ('lessonfile', filename1))
                lesson.filename3 = file3.filename      
    
            file4 = request.files['file4']
            if file4 and allowed_file(file4.filename):
                filename = secure_filename(file4.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' +str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
                file4.save(os.path.join('app/static', 'file', filename1))
                lesson.file4 = url_for('static',filename='%s/%s' % ('lessonfile', filename1))
                lesson.filename4 = file4.filename

            file5 = request.files['file5']
            if file5 and allowed_file(file5.filename):
                filename = secure_filename(file5.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' +str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
                file5.save(os.path.join('app/static', 'lessonfile', filename1))
                lesson.file5 = url_for('static',filename='%s/%s' % ('lessonfile', filename1))
                lesson.filename5 = file5.filename
                
    
            file6 = request.files['file6']
            if file6 and allowed_file(file6.filename):
                filename = secure_filename(file6.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' +str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
                file6.save(os.path.join('app/static', 'lessonfile', filename1))
                lesson.file6 = url_for('static',filename='%s/%s' % ('lessonfile', filename1))
                lesson.filename6 = file6.filename
                
    
            file7 = request.files['file7']
            if file7 and allowed_file(file7.filename):
                filename = secure_filename(file7.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' +str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
                file7.save(os.path.join('app/static', 'lessonfile', filename1))
                lesson.file7 = url_for('static',filename='%s/%s' % ('lessonfile', filename1))
                lesson.filename7 = file7.filename
                
    
            file8 = request.files['file8']
            if file8 and allowed_file(file8.filename):
                filename = secure_filename(file8.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' +str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
                file8.save(os.path.join('app/static', 'lessonfile', filename1))
                lesson.file8 = url_for('static',filename='%s/%s' % ('lessonfile', filename1))
                lesson.filename8 = file8.filename
                                    
        db.session.add(lesson)
        lessons = Lesson.query.filter_by(teacher_id=current_user.id).all()
        return redirect(url_for('main.lesson',id=lessons[-1].id))
    return render_template('open_lesson.html', form=form, english=english)

@main.route('/edit-lesson/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_lesson(id):
    english=request.cookies.get('english')
    values = CombinedMultiDict([flask.request.files,flask.request.form])
    if english == "yes":
        form = AddLessonFormE(values)
    else:
        form = AddLessonForm(values)
    lesson = Lesson.query.filter_by(id=id).first()
    if current_user.can(Permission.WRITE_ARTICLES) and \
            form.validate_on_submit():
        lesson.lesson_name = form.lesson_name.data
        lesson.about_lesson = form.about_lesson.data
        lesson.teacher_id = current_user.id
        if request.method == 'POST':
            pic = request.files['pic']
            size = (1024, 1024) 
            if pic and allowed_file(pic.filename):
                im = Image.open(pic)
                im.thumbnail(size)        
                filename = secure_filename(pic.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' + str(time.time()).replace('.','_') + '.' + filename.split('.')[-1]
                im.save(os.path.join('app/static', 'lesson', filename1))
                try:
                    os.remove("/root/cryptoepoch/app"+post.pic)
                except:
                    pass
                lesson.pic = url_for('static',filename='%s/%s' % ('lesson', filename1))   

            file1 = request.files['file1']
            if file1 and allowed_file(file1.filename):
                filename = secure_filename(file1.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' +str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
                file1.save(os.path.join('app/static', 'lessonfile', filename1))
                try:
                    os.remove("/root/cryptoepoch/app"+post.file1)
                except:
                    pass
                lesson.file1 = url_for('static',filename='%s/%s' % ('lessonfile', filename1))
                lesson.filename1 = file1.filename        
    
            file2 = request.files['file2']
            if file2 and allowed_file(file2.filename):
                filename = secure_filename(file2.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' +str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
                file2.save(os.path.join('app/static', 'lessonfile', filename1))
                try:
                    os.remove("/root/cryptoepoch/app"+post.file2)
                except:
                    pass
                lesson.file2 = url_for('static',filename='%s/%s' % ('lessonfile', filename1))
                lesson.filename2 = file2.filename        
    
            file3 = request.files['file3']
            if file3 and allowed_file(file3.filename):
                filename = secure_filename(file3.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' +str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
                file3.save(os.path.join('app/static', 'lessonfile', filename1))
                try:
                    os.remove("/root/cryptoepoch/app"+post.file3)
                except:
                    pass
                lesson.file3 = url_for('static',filename='%s/%s' % ('lessonfile', filename1))
                lesson.filename3 = file3.filename      
 
            file4 = request.files['file4']
            if file4 and allowed_file(file4.filename):
                filename = secure_filename(file4.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' +str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
                file4.save(os.path.join('app/static', 'file', filename1))
                try:
                    os.remove("/root/cryptoepoch/app"+post.file4)
                except:
                    pass
                lesson.file4 = url_for('static',filename='%s/%s' % ('lessonfile', filename1))
                lesson.filename4 = file4.filename

            file5 = request.files['file5']
            if file5 and allowed_file(file5.filename):
                filename = secure_filename(file5.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' +str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
                file5.save(os.path.join('app/static', 'lessonfile', filename1))
                try:
                    os.remove("/root/cryptoepoch/app"+post.file5)
                except:
                    pass
                lesson.file5 = url_for('static',filename='%s/%s' % ('lessonfile', filename1))
                lesson.filename5 = file5.filename
                
    
            file6 = request.files['file6']
            if file6 and allowed_file(file6.filename):
                filename = secure_filename(file6.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' +str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
                file6.save(os.path.join('app/static', 'lessonfile', filename1))
                try:
                    os.remove("/root/cryptoepoch/app"+post.file6)
                except:
                    pass
                lesson.file6 = url_for('static',filename='%s/%s' % ('lessonfile', filename1))
                lesson.filename6 = file6.filename
                
    
            file7 = request.files['file7']
            if file7 and allowed_file(file7.filename):
                filename = secure_filename(file7.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' +str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
                file7.save(os.path.join('app/static', 'lessonfile', filename1))
                try:
                    os.remove("/root/cryptoepoch/app"+post.file7)
                except:
                    pass
                lesson.file7 = url_for('static',filename='%s/%s' % ('lessonfile', filename1))
                lesson.filename7 = file7.filename
                
    
            file8 = request.files['file8']
            if file8 and allowed_file(file8.filename):
                filename = secure_filename(file8.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' +str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
                file8.save(os.path.join('app/static', 'lessonfile', filename1))
                try:
                    os.remove("/root/cryptoepoch/app"+post.file8)
                except:
                    pass
                lesson.file8 = url_for('static',filename='%s/%s' % ('lessonfile', filename1))
                lesson.filename8 = file8.filename
                                    
        db.session.add(lesson)
        return redirect(url_for('.lesson',id=id))
    form.lesson_name.data=lesson.lesson_name
    form.about_lesson.data=lesson.about_lesson
    return render_template('edit_lesson.html', form=form,id=id,lesson=lesson, english=english)


@main.route('/del-lesson/<int:id>')
@login_required
def del_lesson(id):
    lesson = Lesson.query.filter_by(id=id).first()
    if lesson.file1 != None:
        try:
            os.remove("/root/cryptoepoch/app"+lesson.file1)
        except:
            pass    
    if lesson.file2 != None:
        try:
            os.remove("/root/cryptoepoch/app"+lesson.file2)
        except:
            pass    
    if lesson.file3 != None:
        try:
            os.remove("/root/cryptoepoch/app"+lesson.file3)
        except:
            pass    
    if lesson.file4 != None:
        try:
            os.remove("/root/cryptoepoch/app"+lesson.file4)
        except:
            pass    
    if lesson.file5 != None:
        try:
            os.remove("/root/cryptoepoch/app"+lesson.file5)
        except:
            pass     
    if lesson.file6 != None:
        try:
            os.remove("/root/cryptoepoch/app"+lesson.file6)
        except:
            pass    
    if lesson.file7 != None:
        try:
            os.remove("/root/cryptoepoch/app"+lesson.file7)
        except:
            pass    
    if lesson.file8 != None:
        try:
            os.remove("/root/cryptoepoch/app"+lesson.file8)
        except:
            pass             
    db.session.delete(Lesson.query.get_or_404(id))
    db.session.commit()
    teacher = Teacher.query.filter_by(teacher_id=current_user.id).first()
    return redirect(url_for('.teacher',id=teacher.teacher_id))

@main.route('/lesson-main', methods=['GET', 'POST'])
def lesson_main():
    english=request.cookies.get('english')
    page = request.args.get('page', 1, type=int)
    show_all_teacher = request.cookies.get('show_all_teacher')
    if show_all_teacher == None:
            show_all_teacher = "0"
    show_all_class = request.cookies.get('show_all_class', '')
    teachers = Teacher.query.filter(Teacher.id>0).all()
    teachers_all = []
    for teacher in teachers:
        user = User.query.filter_by(id=teacher.teacher_id).first()
        if user.teacher:
            lessons = Lesson.query.filter_by(teacher_id=teacher.teacher_id).all()
            teachers_all.append([teacher,user,lessons])
    pagination = Lesson.query.\
                          order_by(Lesson.timestamp.desc()).paginate(
                          page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                                                           error_out=False)
    lessons = pagination.items
    n = len(lessons)
    users = []
    for lesson in lessons:
        users.append(User.query.filter_by(id = lesson.teacher_id).first())
    return render_template('lesson_main.html', lessons=lessons,users=users,
                           show_all_teacher=show_all_teacher, n=n, show_all_class=show_all_class, pagination=pagination, teachers_all=teachers_all,english=english)

@main.route('/lesson/<int:id>')
def lesson(id):
    english = request.cookies.get('english')
    lesson = Lesson.query.filter_by(id=id).first()
    if lesson == None:
        if english == 'yes':
            flash("No such lesson!")
        else:
            flash("没有这个课。")
        return redirect(url_for('.lesson_main'))
    user_teacher = User.query.filter_by(id=lesson.teacher_id).first()   
    teacher = Teacher.query.filter_by(teacher_id=lesson.teacher_id).first()
    newlessons = NewLesson.query.filter_by(lesson_id=id).order_by(NewLesson.timestamp.desc()).all()
    newlessons_teacher = NewLesson.query.filter_by(lesson_id=id).order_by(NewLesson.timestamp.desc()).all()    
    show_all_class = request.cookies.get('show_all_class')
    if current_user.is_authenticated:
        if show_all_class == None: # or (teacher.id != current_user.id and show_all_class not in ["0","1","2"]):
            show_all_class = "0"
    students = []
    if current_user.is_authenticated:
        students = Student.query.filter_by(student_id=current_user.id).all()
    mylessons = []
    in_lesson = False
    if students:
        for s in students:
            nl = NewLesson.query.filter_by(id=s.newlesson_id).first()
            if nl:
                if nl.lesson_id == id:
                    in_lesson = True
                if nl in newlessons:
                    mylessons.append(nl)    
    lesson_files = []
    lessonfiles = LessonFile.query.filter_by(lesson_id=id).order_by(LessonFile.timestamp.desc()).all()
    for lf in lessonfiles:
        lesson_files.append([lesson,lf])
    lesson_discussions = []
    for newlesson in newlessons:
        posts = Post.query.filter(or_(Post.tag=="discussion_"+str(newlesson.id),Post.tag=="newlessons_"+str(newlesson.id))).order_by(Post.timestamp.desc()).all()
        for p in posts:
            user2 = User.query.filter_by(id=p.author_id).first()
            lesson_discussions.append([lesson,newlesson,p,user2])
    lesson_students = []
    for newlesson in newlessons:
        students = Student.query.filter_by(newlesson_id=newlesson.id).order_by(Student.timestamp.desc()).all()
        for student in students:
            user3 = User.query.filter_by(id=student.student_id).first()
            lesson_students.append([lesson,newlesson,user3,student])
    return render_template('lesson.html',lesson=lesson,user_teacher=user_teacher,lesson_files=lesson_files,lesson_discussions=lesson_discussions,lesson_students=lesson_students,in_lesson = in_lesson,newlessons=newlessons,newlessons_teacher=newlessons_teacher,mylessons=mylessons,teacher=teacher,show_all_class=show_all_class, english=english)


@main.route('/current-lesson/<int:newlesson_id>',methods=['GET', 'POST'])
@login_required
def current_lesson(newlesson_id):
    english=request.cookies.get('english')    
    newlesson = NewLesson.query.filter_by(id=newlesson_id).first()
    lesson = Lesson.query.filter_by(id=newlesson.lesson_id).first()
    teacher = User.query.filter_by(id=lesson.teacher_id).first()    
    students = Student.query.filter_by(newlesson_id=newlesson_id).all()
    # all_newlessons = NewLesson.query.filter_by(lesson_id=lesson.id).all()
    # lesson_confirmed = 0 # 用户是否选修任何该课程的新开课
    # user_students = Student.query.filter_by(student_id=current_user.id).all()
    # for n in all_newlessons:
    #     for s in user_students:
    #         if n.id == s.newlesson_id:
    #             lesson_confirmed = 1
    # # flash(lesson_confirmed)
    if len(students)>1:
        sn = []
        for s in students:
            sn.append((s,User.query.filter_by(id=s.student_id).first().student_no))
        sn.sort(key=lambda x:x[1])
        students = [i[0] for i in sn]
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.filter(or_(Post.tag == "newlessons_"+str(newlesson_id),Post.tag=="discussion_"+str(newlesson_id))).filter(Post.private==0).order_by(Post.timestamp.desc()).filter(not_(Post.author_id==teacher.id)).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False)
    posts = pagination.items
    pagination_teacher = Post.query.filter(or_(Post.tag == "discussion_"+str(newlesson_id),Post.tag == "newlessons_"+str(newlesson_id))).filter(Post.private==0).filter_by(author_id=teacher.id).order_by(Post.timestamp.desc()).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False)
    posts_teacher = pagination_teacher.items
    show_lesson_discussion = request.cookies.get('show_lesson_discussion')
    if show_lesson_discussion == None:    
        show_lesson_discussion = "0"    
    student = None
    if current_user.is_authenticated:
        ss  = Student.query.filter_by(student_id=current_user.id).all()
        if len(ss) != 0:
            for s in ss:
                if s in students:
                    student = s
                    if student.seat == None:
                        flash("请选择座位，之后可以进行其它操作！")
                        show_lesson_discussion = "2"
    users_confirmed_posts = []
    for s in students:
        if s.confirm:
            if Post.query.filter_by(topic=s.topic).filter_by(author_id=s.student_id).first():
                users_confirmed_posts.append([s,User.query.filter_by(id=s.student_id).first(),\
                                        Post.query.filter_by(author_id=s.student_id).filter_by(topic=s.topic).first().id])
    users_confirmed = []
    users_unconfirmed = []
    for s in students:
        if s.confirm:
            users_confirmed.append(User.query.filter_by(id=s.student_id).first())
        else:
            users_unconfirmed.append(User.query.filter_by(id=s.student_id).first())
    if len(users_confirmed)>=1:
        for i in range(len(users_confirmed)):
            n = random.randint(0,len(students)-1)
            replier = User.query.filter_by(id=students[n].student_id).first()
            student_replier = Student.query.filter_by(newlesson_id=newlesson_id).filter_by(student_id=replier.id).first()
            if student_replier.seat:
                break
        if student_replier.seat == None:
            replier_seat_name = "目前尚无人选位"
        else:
            replier_seat_name = student_replier.seat + " " + replier.name
    else:
        replier_seat_name = ""

    if request.method == 'POST':
        if current_user==teacher:
            seat = request.form['seat']
            student = Student.query.filter(Student.newlesson_id==newlesson_id).filter_by(seat=seat).first()
            student.absence = student.absence + 1
            db.session.commit()           
        else:
            student.seat = request.form['seat']
            db.session.commit()
    
    seats = []
    absences = []
    scores = []
    score_answers = []
    for i in range(newlesson.room_row):
        if i < 9:
            row = "0" + str(i+1)
        else:
            row = str(i+1)
        for j in range(newlesson.room_column):
            if j < 9:
                column = "0" + str(j+1)
            else:
                column = str(j+1)            
            flag = 0
            seat = row + column
            for s in students:
                if s.seat != None:
                    if i+1==int(s.seat[0:2]) and j+1==int(s.seat[2:4]):
                        seats.append(User.query.filter_by(id=s.student_id).first().name)
                        absences.append(s.absence)
                        scores.append(s.score)
                        score_answers.append(s.score_answer)
                        flag = 1
                        break
            if flag == 0:
                seats.append(seat)
                absences.append('')
                scores.append('')
                score_answers.append('')
    
    return render_template('current_lesson.html',teacher=teacher,lesson=lesson,\
                               student=student,posts=posts,posts_teacher=posts_teacher, users_confirmed=users_confirmed,users_unconfirmed=users_unconfirmed,users_confirmed_posts=users_confirmed_posts, replier_seat_name=replier_seat_name,  seats=seats,absences=absences, newlesson=newlesson, show_lesson_discussion=show_lesson_discussion, scores=scores, score_answers=score_answers, english=english)        
               
@main.route('/current-lesson-score/<int:newlesson_id>/<string:replier_seat_name>',methods=['GET', 'POST'])
@login_required
def current_lesson_score(newlesson_id,replier_seat_name):
    student1 = Student.query.filter_by(newlesson_id=newlesson_id).filter_by(seat=replier_seat_name[0:4]).first()
    # flash(student1.seat)
    # flash(student1.score_answer)
#    flash(newlesson_id)
    if student1.score_answer == None:
        student1.score_answer = 1
        flash(replier_seat_name[4:]+ ": 恭喜！实现了从0到1的突破！")
    else:
        student1.score_answer = student1.score_answer + 1
        flash(replier_seat_name[4:] + ": 恭喜！又得1分！")
    db.session.commit()
#    flash(student1.score_answer)
    return redirect(url_for('main.current_lesson',newlesson_id=newlesson_id))        

@main.route('/current-lesson-absence/<int:newlesson_id>/<string:replier_seat_name>',methods=['GET', 'POST'])
@login_required
def current_lesson_absence(newlesson_id,replier_seat_name):
    student1 = Student.query.filter_by(newlesson_id=newlesson_id).filter_by(seat=replier_seat_name[0:4]).first()
    if student1.absence == None:
        student1.absence = 1
        flash(replier_seat_name[4:]+ ": 第一次缺勤！")
    else:
        student1.absence = student1.absence + 1
        flash(replier_seat_name[4:]+ ": 又缺勤了！")
    db.session.commit()
#    flash(student1.absence)
    return redirect(url_for('main.current_lesson',newlesson_id=newlesson_id))        
                         

@main.route('/show-lesson-discussion/<int:newlesson_id>')
def show_lesson_discussion(newlesson_id):
    resp = make_response(redirect(url_for('main.current_lesson',newlesson_id=newlesson_id)))
    resp.set_cookie('show_lesson_discussion', '0', max_age=30*24*60*60)
    return resp

@main.route('/show-lesson-namelist/<int:newlesson_id>')
def show_lesson_namelist(newlesson_id):
    resp = make_response(redirect(url_for('main.current_lesson',newlesson_id=newlesson_id)))
    resp.set_cookie('show_lesson_discussion', '1', max_age=30*24*60*60)
    return resp


@main.route('/show-lesson-seat/<int:newlesson_id>')
def show_lesson_seat(newlesson_id):
    resp = make_response(redirect(url_for('main.current_lesson',newlesson_id=newlesson_id)))
    resp.set_cookie('show_lesson_discussion', '2', max_age=30*24*60*60)
    return resp


@main.route('/show-lesson-exercise/<int:newlesson_id>')
def show_lesson_exercise(newlesson_id):
    resp = make_response(redirect(url_for('main.current_lesson',newlesson_id=newlesson_id)))
    resp.set_cookie('show_lesson_discussion', '3', max_age=30*24*60*60)
    return resp

@main.route('/show-lesson-notice/<int:newlesson_id>')
def show_lesson_notice(newlesson_id):
    resp = make_response(redirect(url_for('main.current_lesson',newlesson_id=newlesson_id)))
    resp.set_cookie('show_lesson_discussion', '4', max_age=30*24*60*60)
    return resp

@main.route('/select-lesson/<int:newlesson_id>')
@login_required
def select_lesson(newlesson_id):
    english=request.cookies.get('english')
    newlesson = NewLesson.query.filter_by(id=newlesson_id).first()
    lesson = Lesson.query.filter_by(id=newlesson.lesson_id).first()
    if newlesson.availability == "close_selection" or newlesson.availability == "close_update" :
        if english == "yes":
            flash("The lesson's selection has been closed. For details, please contact the teacher.")
        else:
            flash("该课选修功能已被老师关闭。详情请联系该老师。")
        return redirect(url_for('main.current_lesson',newlesson_id=newlesson_id))
        
    if current_user.id == lesson.teacher_id:
        if english == "yes":
            flash('The teacher of the class cannot select the class.')
        else:
            flash("开课老师不能选修自己的课程。")
        return redirect(url_for('main.lesson',id=lesson.id))
    if current_user.name == None or current_user.tel == None or \
        current_user.location == None or current_user.about_me == None:
        if english == "yes":
            flash('Please update your profile.')
        else:
            flash("请先完善个人资料。")
        return redirect(url_for('main.lesson',id=lesson.id))
    students = Student.query.filter_by(student_id=current_user.id).all()
    for s in students:
        if s.newlesson_id == newlesson_id:
            if english == "yes":
                flash('You have selected the class.')
            else:
                flash('你已经选了该课程。')
            return redirect(url_for('main.lesson',id=newlesson.lesson_id))
    student = Student(student_id=current_user.id,newlesson_id=newlesson_id,confirm=0)
    db.session.add(student)
    return redirect(url_for('main.current_lesson',newlesson_id=newlesson_id))


@main.route('/update-topic/<int:newlesson_id>/<int:student_id>',methods=['GET', 'POST'])
@login_required
def update_topic(newlesson_id, student_id):
    english=request.cookies.get('english')
    if current_user.id != student_id and current_user.is_administrator == False:
        if english == "yes":
            flash("You are not supposed to modify it!")
        else:
            flash("您无权修改！")
        return redirect(url_for('main.current_lesson',newlesson_id=newlesson_id))
    newlesson = NewLesson.query.filter_by(id=newlesson_id).first()
    lesson = Lesson.query.filter_by(id=newlesson.lesson_id).first()   
    student = Student.query.filter_by(student_id=student_id).filter_by(newlesson_id=newlesson_id).first()
    if student == None:
        if english == "yes":
            flash("The blog's refered homework has been deleted!")
        else:
            flash("该帖子对应的作业已经删除！")
        return redirect(url_for('main.current_lesson',newlesson_id=newlesson_id))
        
    if newlesson.availability == 'close_update':
        if english == "yes":
            flash("The lesson's homeowork upload function has been close. Please contact the teacher!")
        else:
            flash("课程上传已经关闭。详情可联系老师。")
        return redirect(url_for('main.current_lesson',newlesson_id=newlesson_id))
    values = CombinedMultiDict([flask.request.files,flask.request.form])
    if english == "yes":
        form = UpdateTopicFormE(values)
    else:
        form = UpdateTopicForm(values)

    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        student.topic = request.form['topic']
        student.body = request.form['body']
        if request.method == 'POST':
            file1 = request.files['file1']
            if file1 and allowed_file(file1.filename):
                filename = secure_filename(file1.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' +str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
                file1.save(os.path.join('app/static', 'post', filename1))
                student.file1 = url_for('static',filename='%s/%s' % ('post', filename1))
                student.filename1 = file1.filename        

            file2 = request.files['file2']
            if file2 and allowed_file(file2.filename):
                filename = secure_filename(file2.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' +str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
                file2.save(os.path.join('app/static', 'post', filename1))
                student.file2 = url_for('static',filename='%s/%s' % ('post', filename1))
                student.filename2 = file2.filename        

            file3 = request.files['file3']
            if file3 and allowed_file(file3.filename):
                filename = secure_filename(file3.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' +str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
                file3.save(os.path.join('app/static', 'post', filename1))
                student.file3 = url_for('static',filename='%s/%s' % ('post', filename1))
                student.filename3 = file3.filename      

            file4 = request.files['file4']
            if file4 and allowed_file(file4.filename):
                filename = secure_filename(file4.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' +str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
                file4.save(os.path.join('app/static', 'post', filename1))
                student.file4 = url_for('static',filename='%s/%s' % ('post', filename1))
                student.filename4 = file4.filename

            file5 = request.files['file5']
            if file5 and allowed_file(file5.filename):
                filename = secure_filename(file5.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' +str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
                file5.save(os.path.join('app/static', 'post', filename1))
                student.file5 = url_for('static',filename='%s/%s' % ('post', filename1))
                student.filename5 = file5.filename
            student.time = datetime.today().isoformat()[:-7].replace("T"," ")
        db.session.add(student)
        if english == "yes":
            flash("The homework has been updated!")
        else:
            flash("作业已经更新！")
        post = Post.query.filter_by(author_id=student_id).filter_by(tag="newlessons_"+str(newlesson_id)).filter_by(topic=student.topic).first()
        if post != None:
            post.topic = student.topic
            post.body = student.body
            post.file1 = student.file1
            post.file2 = student.file2
            post.file3 = student.file3
            post.file4 = student.file4
            post.file5 = student.file5
            post.filename1 = student.filename1
            post.filename2 = student.filename2
            post.filename3 = student.filename3
            post.filename4 = student.filename4
            post.filename5 = student.filename5
            post.tag = "newlessons_" + str(newlesson_id)
            post.time = datetime.today().isoformat()[:-7].replace("T"," ")
            db.session.add(post)
            if english == "yes":
                flash("The homework has updated the referred blog!")
            else:
                flash("作业对应的帖子已经更新!")
        else:
            post = Post(topic=student.topic,body=student.body,
                        file1 = student.file1,
                        file2 = student.file2,                            
                        file3 = student.file3,                            
                        file4 = student.file4,                            
                        file5 = student.file5,                            
                        filename1 = student.filename1,
                        filename2 = student.filename2,
                        filename3 = student.filename3,
                        filename4 = student.filename4,
                        filename5 = student.filename5,
                        tag='newlessons_'+ str(newlesson_id),
                        time=datetime.today().isoformat()[:-7].replace("T"," "),
                        author=current_user._get_current_object())
            db.session.add(student)
            if english == "yes":
                flash("The homework has created the referred blog!")
            else:
                flash("作业对应的帖子已经生成!")
        return redirect(url_for('main.current_lesson', newlesson_id=newlesson_id))
    form.topic.data = student.topic
    form.body.data = student.body

    return render_template('update_topic.html',form=form,newlesson_id=newlesson_id, english=english)

    
@main.route('/del-topic/<int:newlesson_id>')
@login_required
def del_topic(newlesson_id):
    english=request.cookies.get('english')
    newlesson1 = NewLesson.query.filter_by(id=newlesson_id).first()
    if newlesson1.availability == 'close_update':
        if english == "yes":
            flash("The lesson's homeowork upload function has been close. Please contact the teacher!")
        else:
            flash("课程上传已经关闭。详情可联系老师。")
        return redirect(url_for('main.current_lesson',newlesson_id=newlesson_id))
    student = Student.query.filter_by(student_id=current_user.id).filter_by(newlesson_id=newlesson_id).first()
    if student==None:
        if english == "yes":
            flash("You are not the student of the lesson!")
        else:
            flash("您不是该班学生！")
        return redirect(url_for('main.current_lesson',newlesson_id=newlesson_id))
        
    post = Post.query.filter_by(author_id=current_user.id).filter_by(topic=student.topic).filter_by(tag="newlessons_" + str(newlesson_id)).first()
    if post != None:
        db.session.delete(Post.query.get_or_404(post.id))
        if english == "yes":
            flash("The homework's related post has been deleted!")
        else:
            flash("作业相关联的帖子已经删除！")
        
    student.topic = None
    student.body = None
    student.body_html = None
    if student.file1:
        try:
            os.remove("/root/cryptoepoch/app"+student.file1)
        except:
            pass    
    student.file1 = None
    if student.file2:
        try:
            os.remove("/root/cryptoepoch/app"+student.file2)
        except:
            pass    
    student.file2 = None
    if student.file3:
        try:
            os.remove("/root/cryptoepoch/app"+student.file3)
        except:
            pass    
    student.file3 = None
    if student.file4:
        try:
            os.remove("/root/cryptoepoch/app"+student.file4)
        except:
            pass    
    student.file4 = None
    if student.file5:
        try:
            os.remove("/root/cryptoepoch/app"+student.file5)
        except:
            pass    
    student.file5 = None
    student.filename1 = None
    student.filename2 = None
    student.filename3 = None
    student.filename4 = None
    student.filename5 = None
    db.session.add(student)
    if english == "yes":
        flash("Your homework has been deleted!")
    else:
        flash("您的作业已经删除！")
    return redirect(url_for('.current_lesson',newlesson_id=newlesson_id))    
    
    
@main.route('/open-new-lesson/<int:id>', methods=['GET', 'POST'])
@login_required
def open_new_lesson(id):
    english=request.cookies.get('english')
    values = CombinedMultiDict([flask.request.files,flask.request.form])
    if english == "yes":
        form = NewLessonFormE(values)
    else:
        form = NewLessonForm(values)
    if current_user.can(Permission.WRITE_ARTICLES) and \
            form.validate_on_submit():
        newlesson = NewLesson(year=form.year.data,season=form.season.data,\
                              room_row=form.room_row.data,\
                              room_column=form.room_column.data,\
                              about = form.about.data,availability=form.availability.data,lesson_id = id)
        db.session.add(newlesson)
        return redirect(url_for('main.lesson',id=id))
    return render_template('open_new_lesson.html', form=form, english=english)

    
@main.route('/upload-lesson-file/<int:id>', methods=['GET', 'POST'])
@login_required
def upload_lesson_file(id):
    english=request.cookies.get('english')
    values = CombinedMultiDict([flask.request.files,flask.request.form])
    if english == "yes":
        form = LessonFileFormE(values)
    else:
        form = LessonFileForm(values)
    if current_user.can(Permission.WRITE_ARTICLES) and \
            form.validate_on_submit():
        lessonfile = LessonFile(filetype=form.filetype.data,visibility=form.visibility.data,\
                              about = form.about.data,lesson_id = id)
        if request.method == 'POST':
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' +str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
                file.save(os.path.join('app/static', 'lesson', filename1))
                lessonfile.file = url_for('static',filename='%s/%s' % ('lesson', filename1))
                lessonfile.filename = file.filename               
        db.session.add(lessonfile)   
        return redirect(url_for('main.lesson',id=id))
    return render_template('upload_lesson_file.html', form=form, english=english)

@main.route('/edit-lesson-file/<int:file_id>/<int:lesson_id>', methods=['GET', 'POST'])
@login_required
def edit_lesson_file(file_id,lesson_id):
    english=request.cookies.get('english')
    values = CombinedMultiDict([flask.request.files,flask.request.form])
    lessonfile = LessonFile.query.filter_by(id=file_id).first()
    if english == "yes":
        form = LessonFileFormE(values)
    else:
        form = LessonFileForm(values)
    if current_user.can(Permission.WRITE_ARTICLES) and \
            form.validate_on_submit():
        lessonfile.filetype=form.filetype.data
        lessonfile.visibility=form.visibility.data
        lessonfile.about = form.about.data
        if request.method == 'POST':
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename1 = current_user.email.replace('@','__').replace('.','__') \
                            + '__' +str(time.time()).replace('.','') + '.' + filename.split('.')[-1]
                file.save(os.path.join('app/static', 'lesson', filename1))
                lessonfile.file = url_for('static',filename='%s/%s' % ('lesson', filename1))
                lessonfile.filename = file.filename               
        db.session.commit()   
        return redirect(url_for('main.lesson',id=lesson_id))
    form.about.data = lessonfile.about
    form.filetype.data = lessonfile.filetype
    form.visibility.data = lessonfile.visibility
    return render_template('edit_lesson_file.html', form=form, file_id=file_id, lesson_id=lesson_id,english=english)

@main.route('/del-lesson-file/<int:file_id>/<int:lesson_id>', methods=['GET', 'POST'])
@login_required
def del_lesson_file(file_id,lesson_id):
    LessonFile.query.filter_by(id=file_id).delete()
    return redirect(url_for('main.lesson',id=lesson_id))

    
@main.route('/edit-new-lesson/<int:newlesson_id>', methods=['GET', 'POST'])
@login_required
def edit_new_lesson(newlesson_id):
    english=request.cookies.get('english')
    values = CombinedMultiDict([flask.request.files,flask.request.form])
    if english == "yes":
        form = NewLessonFormE(values)
    else:
        form = NewLessonForm(values)
    newlesson = NewLesson.query.filter_by(id=newlesson_id).first()
    if current_user.can(Permission.WRITE_ARTICLES) and \
            form.validate_on_submit():
        newlesson.year=form.year.data
        newlesson.season=form.season.data
        newlesson.room_row=form.room_row.data
        newlesson.room_column=form.room_column.data
        newlesson.about = form.about.data
        newlesson.availability = form.availability.data
        db.session.commit()
        return redirect(url_for('main.current_lesson',newlesson_id=newlesson_id))
    form.year.data = newlesson.year
    form.season.data = newlesson.season
    form.room_row.data = newlesson.room_row
    form.room_column.data = newlesson.room_column
    form.about.data = newlesson.about
    form.availability.data = newlesson.availability
    return render_template('edit_new_lesson.html', form=form,newlesson_id=newlesson_id, english=english)


@main.route('/del-new-lesson/<int:newlesson_id>')
@login_required
def del_new_lesson(newlesson_id):
    db.session.delete(NewLesson.query.get_or_404(newlesson_id))
    db.session.commit()
    teacher = Teacher.query.filter_by(teacher_id=current_user.id).first()
    return redirect(url_for('.teacher',id=teacher.teacher_id))

@main.route('/del-student/<int:newlesson_id>/<int:student_id>')
@login_required
def del_student(newlesson_id,student_id,):
    students = Student.query.filter_by(newlesson_id=newlesson_id).all()
    student = None
    if current_user.is_authenticated:
        ss  = Student.query.filter_by(student_id=student_id).all()
        if len(ss) != 0:
            for s in ss:
                if s in students:
                    student = s
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('.current_lesson',newlesson_id=newlesson_id))

@main.route('/auth-student/<int:newlesson_id>/<int:student_id>')
@login_required
def auth_student(newlesson_id,student_id):
    students = Student.query.filter_by(newlesson_id=newlesson_id).all()
    student = None
    if current_user.is_authenticated:
        ss  = Student.query.filter_by(student_id=student_id).all()
        if len(ss) != 0:
            for s in ss:
                if s in students:
                    student = s
    student.confirm = 1
    db.session.commit()
    return redirect(url_for('.current_lesson',newlesson_id=newlesson_id))

@main.route('/del-student-from-teacher/<int:newlesson_id>/<int:student_id>')
@login_required
def del_student_from_teacher(newlesson_id,student_id,):
    students = Student.query.filter_by(newlesson_id=newlesson_id).all()
    student = None
    if current_user.is_authenticated:
        ss  = Student.query.filter_by(student_id=student_id).all()
        if len(ss) != 0:
            for s in ss:
                if s in students:
                    student = s
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('.teacher',id=current_user.id))

@main.route('/auth-student-from-teacher/<int:newlesson_id>/<int:student_id>')
@login_required
def auth_student_from_teacher(newlesson_id,student_id):
    students = Student.query.filter_by(newlesson_id=newlesson_id).all()
    student = None
    if current_user.is_authenticated:
        ss  = Student.query.filter_by(student_id=student_id).all()
        if len(ss) != 0:
            for s in ss:
                if s in students:
                    student = s
    student.confirm = 1
    db.session.commit()
    return redirect(url_for('.teacher',id=current_user.id))



@main.route('/lesson-comment')
@login_required
def lesson_comments():
    english=request.cookies.get('english')
    return render_template('lesson_comments.html', english=english)


@main.route('/show-all-lesson')
def show_all_lesson():
    resp = make_response(redirect(url_for('main.lesson_main')))
    resp.set_cookie('show_all_teacher', '0', max_age=30*24*60*60)
    return resp


@main.route('/show-all-teacher')
def show_all_teacher():
    resp = make_response(redirect(url_for('main.lesson_main')))
    resp.set_cookie('show_all_teacher', '1', max_age=30*24*60*60)
    return resp

@main.route('/show-about-lesson/<int:id>')
def show_about_lesson(id):
    resp = make_response(redirect(url_for('main.lesson',id=id)))
    resp.set_cookie('show_all_class', '0', max_age=30*24*60*60)
    return resp

@main.route('/show-all-class/<int:id>')
def show_all_class(id):
    resp = make_response(redirect(url_for('main.lesson',id=id)))
    resp.set_cookie('show_all_class', '1', max_age=30*24*60*60)
    return resp


@main.route('/show-all-file/<int:id>')
def show_all_file(id):
    resp = make_response(redirect(url_for('main.lesson',id=id)))
    resp.set_cookie('show_all_class', '2', max_age=30*24*60*60)
    return resp


@main.route('/show-all-discussion/<int:id>')
@login_required
def show_all_discussion(id):
    resp = make_response(redirect(url_for('main.lesson',id=id)))
    resp.set_cookie('show_all_class', '3', max_age=30*24*60*60)
    return resp


@main.route('/show-all-student/<int:id>')
@login_required
def show_all_student(id):
    resp = make_response(redirect(url_for('main.lesson',id=id)))
    resp.set_cookie('show_all_class', '4', max_age=30*24*60*60)
    return resp


@main.route('/teacher/<int:id>')
def teacher(id):
    english=request.cookies.get('english')
    show_opened_lesson = request.cookies.get('show_opened_lesson')
    if show_opened_lesson == None:
        show_opened_lesson = "0"
    teacher = Teacher.query.filter_by(id=id).first_or_404()
    user = User.query.filter_by(id=teacher.teacher_id).first_or_404()
    lessons = Lesson.query.filter_by(teacher_id=id).order_by(Lesson.timestamp.desc()).all()
    lesson_files = []
    if lessons is not None:
        for lesson in lessons:
            lessonfiles = LessonFile.query.filter_by(lesson_id=lesson.id).order_by(LessonFile.timestamp.desc()).all()
            for lf in lessonfiles:
                lesson_files.append([lesson,lf])
    lesson_discussions = []
    if lessons is not None:
        for lesson in lessons:
            newlessons = NewLesson.query.filter_by(lesson_id=lesson.id).order_by(NewLesson.timestamp.desc()).all()
            for newlesson in newlessons:
                posts = Post.query.filter_by(tag="newlessons_"+str(newlesson.id)).order_by(Post.timestamp.desc()).all()
                for p in posts:
                    user2 = User.query.filter_by(id=p.author_id).first()
                    lesson_discussions.append([lesson,newlesson,p,user2])
    lesson_students = []
    if lessons is not None:
        for lesson in lessons:
            newlessons = NewLesson.query.filter_by(lesson_id=lesson.id).order_by(NewLesson.timestamp.desc()).all()
            for newlesson in newlessons:
                students = Student.query.filter_by(newlesson_id=newlesson.id).order_by(Student.timestamp.desc()).all()
                for student in students:
                    user3 = User.query.filter_by(id=student.student_id).first()
                    lesson_students.append([lesson,newlesson,user3,student])
    return render_template('teacher.html', teacher=teacher,user=user,lessons=lessons,\
                           lesson_files=lesson_files,lesson_discussions=lesson_discussions,\
                           lesson_students=lesson_students,
                           show_opened_lesson=show_opened_lesson,english=english)


@main.route('/show-about-teacher/<int:id>')
def show_about_teacher(id):
    resp = make_response(redirect(url_for('main.teacher',id=id)))
    resp.set_cookie('show_opened_lesson', '0', max_age=30*24*60*60)
    return resp



@main.route('/show-opened-lesson/<int:id>')
def show_opened_lesson(id):
    resp = make_response(redirect(url_for('main.teacher',id=id)))
    resp.set_cookie('show_opened_lesson', '1', max_age=30*24*60*60)
    return resp


@main.route('/show-opened-lesson-file/<int:id>')
def show_opened_lesson_file(id):
    resp = make_response(redirect(url_for('main.teacher',id=id)))
    resp.set_cookie('show_opened_lesson', '2', max_age=30*24*60*60)
    return resp


@main.route('/show-opened-lesson-discussion/<int:id>')
def show_opened_lesson_discussion(id):
    resp = make_response(redirect(url_for('main.teacher',id=id)))
    resp.set_cookie('show_opened_lesson', '3', max_age=30*24*60*60)
    return resp


@main.route('/show-opened-lesson-student/<int:id>')
def show_opened_lesson_student(id):
    resp = make_response(redirect(url_for('main.teacher',id=id)))
    resp.set_cookie('show_opened_lesson', '4', max_age=30*24*60*60)
    return resp



@main.route('/show-chosen-lesson')
@login_required
def show_chosen_lesson(username):
    resp = make_response(redirect(url_for('.lesson')))
    resp.set_cookie('show_chosen_lesson', '1', max_age=30*24*60*60)
    return resp

@main.route('/show-my-teach')
@login_required
def show_my_teach(username):
    resp = make_response(redirect(url_for('.user')))
    resp.set_cookie('show_my_teach', '1', max_age=30*24*60*60)
    return resp


@main.route('/show-open-lesson')
@login_required
def show_open_lesson(username):
    resp = make_response(redirect(url_for('.user')))
    resp.set_cookie('show_open_lesson', '1', max_age=30*24*60*60)
    return resp

@main.route('/collect/<int:post_id>/<int:is_collect>')
@login_required
def collect(post_id,is_collect):
    if is_collect:
        collectpost = CollectPost.query.filter_by(user_id=current_user.id).filter_by(post_id=post_id).first()
        db.session.delete(collectpost)
        flash("已经取消收藏！")

    else:
        collectpost = CollectPost(user_id=current_user.id,post_id=post_id)
        db.session.add(collectpost)
        flash("已经成功收藏！")
    db.session.commit()
    return redirect(url_for('.post',id=post_id))

@main.route('/collect2/<int:post_id>/<int:is_collect>')
@login_required
def collect2(post_id,is_collect):
    if is_collect:
        collectpost = CollectPost.query.filter_by(user_id=current_user.id).filter_by(new_id=post_id).first()
        db.session.delete(collectpost)
        flash("已经取消收藏！")

    else:
        collectpost = CollectPost(user_id=current_user.id,new_id=post_id)
        db.session.add(collectpost)
        flash("已经成功收藏！")
    db.session.commit()
    return redirect(url_for('.new',id=post_id))

@main.route('/show-news/<int:user_id>')
def show_news(user_id):
    resp = make_response(redirect(url_for('.collection',user_id=user_id)))
    resp.set_cookie('show_collection', 'news', max_age=30*24*60*60)
    return resp

@main.route('/show-blog/<int:user_id>')
def show_blog(user_id):
    resp = make_response(redirect(url_for('.collection',user_id=user_id)))
    resp.set_cookie('show_collection', 'blog', max_age=30*24*60*60)
    return resp

@main.route('/collection/<int:user_id>')
@login_required
def collection(user_id):
    english=request.cookies.get('english')
    values = CombinedMultiDict([flask.request.files,flask.request.form])
    if english == "yes":
        form = PostFormE(values)
    else:
        form = PostForm(values)
    resp=request.cookies.get('show_collection')
    if resp == None:
        resp = 'news'
    page = request.args.get('page', 1, type=int)
    collectposts = CollectPost.query.filter_by(user_id=user_id).filter(CollectPost.post_id != None).all()
    posts = []
    timestamps = []
    for cp in collectposts:        
        p = Post.query.filter_by(id=cp.post_id).filter_by(private=False).first()
        if p is not None:
            posts.append(p)
            timestamps.append(cp.timestamp)
    pagination_blog = CollectPost.query.filter(CollectPost.user_id==current_user.id).filter(CollectPost.post_id != None).order_by(CollectPost.timestamp.desc()).paginate(
                          page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                                                           error_out=False)
    blogs = []
    if len(posts) != 0:
        timestamps2 = sorted(timestamps,reverse=True)
        for t in timestamps2:
            blogs.append(posts[timestamps.index(t)])
            
    collectposts_news = CollectPost.query.filter_by(user_id=user_id).filter(CollectPost.new_id != None).all()
    news = []
    timestamps_news = []
    for cp in collectposts_news:        
        p = New.query.filter_by(id=cp.new_id).filter_by(private=False).first()
        if p is not None:
            news.append(p)
            timestamps_news.append(cp.timestamp)
    pagination_news = CollectPost.query.filter(CollectPost.user_id==current_user.id).filter(CollectPost.new_id != None).order_by(CollectPost.timestamp.desc()).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False)
    news2 = []
    if len(news) != 0:
        timestamps2_news = sorted(timestamps_news,reverse=True)
        for t in timestamps2_news:
            news2.append(news[timestamps_news.index(t)])
    return render_template('collection.html', form=form, posts=blogs, user_id=user_id,resp=resp, news = news2, pagination_blog=pagination_blog,pagination_news=pagination_news, english=english)

@main.route('/white-board')
def white_board():
    english=request.cookies.get('english')
    return render_template('white_board.html', english=english)

@main.route('/clock')
def clock():
    english=request.cookies.get('english')
    return render_template('clock.html', english=english)

@main.route('/countdown')
def countdown():
    english=request.cookies.get('english')
    return render_template('countdown.html', english=english)

@main.route('/tools')
def tools():
    english=request.cookies.get('english')
    return render_template('tools.html', english=english)

@main.route('/claculator')
def calculator():
    english=request.cookies.get('english')
    return render_template('calculator.html', english=english)


@main.route('/claculator-science')
def calculator_science():
    english=request.cookies.get('english')
    return render_template('calculator_science.html', english=english)


@main.route('/claculator-date')
def calculator_date():
    english=request.cookies.get('english')
    return render_template('calculator_date.html', english=english)

@main.route('/criticism/<int:newlesson_id>/<int:student_id>', methods=['GET', 'POST'])
@login_required
def criticism(newlesson_id,student_id):
    english=request.cookies.get('english')
    student = Student.query.filter_by(id=student_id).first()
    user = User.query.filter_by(id=student.student_id).first()
    if english == "yes":
        form = CriticismFormE()
    else:
        form = CriticismForm()
    if current_user.can(Permission.WRITE_ARTICLES) and \
            form.validate_on_submit():
        student.criticism = form.criticism.data
        student.score = form.score.data
        db.session.commit()
        return redirect(url_for('.current_lesson',id=current_user.id,newlesson_id=newlesson_id,english=english))   
    return render_template('criticism.html', form=form,user=user,newlesson_id=newlesson_id,english=english)


@main.route('/edit-criticism/<int:newlesson_id>/<int:student_id>', methods=['GET', 'POST'])
@login_required
def edit_criticism(newlesson_id,student_id):
    english=request.cookies.get('english')
    student = Student.query.filter_by(id=student_id).first()
    user = User.query.filter_by(id=student.student_id).first()
    if english == "yes":
        form = CriticismFormE()
    else:
        form = CriticismForm()
    if current_user.can(Permission.WRITE_ARTICLES) and \
            form.validate_on_submit():
        student.criticism = form.criticism.data
        student.score = form.score.data
        db.session.commit()
        return redirect(url_for('.current_lesson',id=current_user.id,newlesson_id=newlesson_id,english=english))   
    form.criticism.data = student.criticism
    form.score.data = student.score
    return render_template('criticism.html', form=form,user=user,newlesson_id=newlesson_id,english=english)

#
#@main.route('/vote/<int:post_id>/<int:user_id>')
#@login_required
#def vote(post_id,user_id):
#    english=request.cookies.get('english')
#    vote = Vote.query.filter_by(post_id=post_id).filter_by(user_id=user_id).first()
#    if vote == None:
#        vote = Vote(post_id=post_id,user_id=user_id)
#        db.session.add(vote)
#        if english == "yes":
#            flash('已经点赞！')
#        else:
#            flash('You have voted successfully!')
#    else:
#        if english == "yes":
#            flash('已经点过赞了！')
#        else:
#            flash('You have ever already voted!')
#    return redirect(url_for(s=post_id))
#
#        

# @main.route('/baidu_verify_QD9sSrJMXW.html')
# def baidu_verify_QD9sSrJMXW():
#     render_template('baidu_verify_QD9sSrJMXW.html')




@main.route('/get-toutaio')
@login_required
def get_toutiao():
    english=request.cookies.get('english')
    resp = request.cookies.get('show')  
    if resp == None:
            resp = "all"  
    page = request.args.get('page', 1, type=int)    
    lastpost = None
    try:
        lastpost = Post.query.filter(tag=="toutiao",tag=='newsflash')[-1]
        lasttime = lastpost.time
    except:
        lasttime = ""
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) ... Chrome/61.0.3163.100 Safari/537.36"
    cookie="mediav=%7B%22eid%22%3A%22387123...b3574ef2-21b9-11e8-b39c-1bc4029c43b8"
    headers={"User-Agent":user_agent,"Cookie":cookie}
    a = []

    # 金色财经
    u1 = "https://www.jinse.com/news/blockchain/"
    try:
        s1 = BeautifulSoup(requests.get(u1).text,'lxml')
        items = s1.find_all(class_="col right")
        socket.setdefaulttimeout(30)
        for item in items:
            topic = item.a.string
            url = item.a['href']
            s = requests.get(url,headers=headers).text
            t = hour2date(s.split('class="time">')[1].split('</div>')[0])
            body = s.split('js-article-detail">')[1].split('</div>')[0].lstrip() + '\n（<a href="' + url + '">' + '转自金色财经，' + t + '</a>）\n'
            a.append([date2sec(t),topic,url,t, body,'toutiao'])
    except:
        pass

    # 巴比特
    try:
        u1 = "https://www.8btc.com/news"
        s1 = BeautifulSoup(requests.get(u1, headers=headers).text,'lxml')
        for item in s1.find_all(class_="article-item-warp"):
            topic = item.img['alt']
            url = "https://www.8btc.com" + item.a['href']
            s2 = requests.get(url,headers=headers).text
            t = hour2date(s2.split('datatime')[1].split('>')[1].split('<')[0])
            body = s2.split('class="bbt-html" data-v-76ec936b>')[1].split('</div>')[0].lstrip() + '\n（<a href="' + url + '">'  + '转自巴比特，' + t + '</a>）\n'
            a.append([date2sec(t),topic,url,t, body, 'toutiao'])
    except:
        pass

    # 链得得新闻
    try:
        u1 = "https://www.chaindd.com/"
        items = BeautifulSoup(requests.get(u1, headers=headers).text,'lxml').find_all(class_="post_part clearfix")
        for item in items:
            url = "https://www.chaindd.com" + item.a.get('href')
            s2 = requests.get(url,headers=headers).text
            topic = s2.split('</title>')[0].split('<title>')[1]
            if '涨跌榜' in topic or '交易榜' in topic:
                continue
            t1 = s2.split('前<')[0].split('>')[-1] + '前'
            t = hour2date(t1)
            body = s2.split('<div class="inner">')[1].split('</div>')[0].lstrip() + '\n（<a href="' + url + '">' + '转自链得得，' + t + '</a>）\n'
            a.append([date2sec(t),topic,url,t, body, 'toutiao'])
    except:
        pass

    # 币世界新闻
    try:
        u1 = "https://www.bishijie.com/shendu.html"
        s1 = BeautifulSoup(requests.get(u1, headers=headers).text,'lxml')
        s = '''</div>
					<section class="contentContainer" id="contentLazyload">
						<div class="content">'''
        for item in s1.find_all(class_="container"):
            topic = item.img['alt']
            url = "https://www.bishijie.com" + item.a['href']
            s2 = requests.get(url,headers=headers).text
            t = hour2date(s2.split('<span class="time">')[1].split('<')[0])
            body = s2.split('<div class="abstract">')[1].split('<div class="authorcontainer">')[0].replace(s,'').replace('					<p>','').lstrip() + '\n（<a href="' + url + '">'  + '转自币世界，' + t + '</a>）\n'
            a.append([date2sec(t),topic,url,t, body, 'toutiao'])
    except:
        pass

    # 币快报
    try:
        u1 = "http://www.beekuaibao.com"
        s1 = requests.get(u1, headers=headers).text.split('<div class="title" data-v-5b0403f0>')
        for i in range(1,len(s1)-1):
            topic = s1[i].split('</div>')[0]
            url = "http://www.beekuaibao.com" + s1[i-1].split('href="')[-1].split('"')[0]
            s2 = requests.get(url, headers=headers).text.split('<div class="content">')
            t = hour2date(s2[0].split('前</span>')[0].split('>')[-1] + '前')
            body = s2[1].split('声明：')[0].lstrip() + '\n（<a href="' + url + '">'  + '转自币快报，' + t + '</a>）\n'
            a.append([date2sec(t),topic,url,t, body, 'toutiao'])
    except:
        pass

    # 按时间排序
    swapped = True
    while swapped:
        swapped = False
        for i in range(len(a)-1):
            if a[i][0] > a[i+1][0]:
                a[i], a[i+1] = a[i+1], a[i]
                swapped = True

    # 数据上传
    for item in a:
        item[4] = item[4].replace('<s>','').replace('</s>','').replace('<div>','').replace('</div>','').replace('<article','').replace('</article>','').replace('<section>','').replace('</section','').replace('<em>','').replace('</em>','').replace('<!-- 增加 二维码图片 -->','').replace('&ldquo;','').replace('&rdquo;','')
        # if '<img' in item[4]:
        #     item[4] = item[4].split('<img')[0] + item[4].split('<img')[1].split('>')[1].replace('<p></p>','').replace('<p></p','')
        if (lasttime=="" or date2sec(lasttime) < item[0]) and "行情" not in item[1]:
            post = Post(topic=item[1], body=item[4].replace('<p></p>',''), lang="cn", tag=item[5], time=item[3], author=current_user._get_current_object())
            db.session.add(post)
        
    return redirect(url_for('.show_toutiao'))



@main.route('/get-newsflash')
@login_required
def get_newsflash():
    english=request.cookies.get('english')
    resp = request.cookies.get('show')  
    if resp == None:
            resp = "all"  
    page = request.args.get('page', 1, type=int)    
    lastpost = None
    try:
        lastpost = Post.query.filter(tag=="toutiao",tag=='newsflash')[-1]
        lasttime = lastpost.time
    except:
        lasttime = ""
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) ... Chrome/61.0.3163.100 Safari/537.36"
    cookie="mediav=%7B%22eid%22%3A%22387123...b3574ef2-21b9-11e8-b39c-1bc4029c43b8"
    headers={"User-Agent":user_agent,"Cookie":cookie}
    a = []
    # 链得得快讯
    try:
        u1 = "https://www.chaindd.com/nictation"
        s1 = BeautifulSoup(requests.get(u1,headers=headers).text,'lxml')
        for item in s1.find_all(class_="w_tit"):
            topic = '快讯：' + item.a.string
            url = item.a['href']
            s2 = requests.get(url,headers=headers).text
            t = hour2date(s2.split('<span class="color-unclickable">')[1].split('</span>')[0])
            try:
                body = s2.split('ChainDD）')[1].split('/>')[0].lstrip() + '\n（<a href="' + url + '">' + '转自链得得，' + t + '</a>）\n'
            except:
                body = s2.split('【链得得播报】')[1].split('</p>')[0].lstrip() + '\n（<a href="' + url + '">' + '转自链得得，' + t + '</a>）\n'        
            a.append([date2sec(t),topic,url,t, body,'newsflash'])
    except:
        pass

    # 币世界
    try:
        u1 = "https://www.bishijie.com/kuaixun/"
        s1 = requests.get(u1,headers=headers).text.split('<ul data-id=')[1:-1]
        date = requests.get(u1,headers=headers).text.split('<div class="live livetop ')[1].split('">')[0]
        for item in s1:
            topic = '快讯：' + item.split('title="')[1].split('">')[0]
            url = "https://www.bishijie.com" + item.split('href="')[1].split('" ')[0]
            t = date + ' ' + item.split('</span>')[0].split('>')[-1]
            body = item.split('title="')[2].split('">\n')[1].split('</a>')[0].replace(' ','').lstrip() + '\n（<a href="' + url + '">' + '转自币世界，' + t + '</a>）\n'
            a.append([date2sec(t),topic,url,t, body,'newsflash'])
    except:
        pass

    # 币快报
    u1 = "http://www.beekuaibao.com/newsflashes"
    s1 = requests.get(u1,headers=headers).text.split('<div class="title" data-v-5b0403f0>')
    for i in range(1,len(s1)):
        topic = '快讯：' + s1[i].split('</div>')[0]
        url = "http://www.beekuaibao.com" + s1[i-1].split('href="')[-1].split('" ')[0]
        t = hour2date(s1[i].split('前</span>')[0].split('>')[-1] + '前')
        body = s1[i].split('<div class="desc-container" data-v-5b0403f0>')[1].split('</div>')[0].lstrip() + '\n（<a href="' + url + '">' + '转自币世界，' + t + '</a>）\n'
        a.append([date2sec(t),topic,url,t, body,'newsflash'])

    # 按时间排序
    swapped = True
    while swapped:
        swapped = False
        for i in range(len(a)-1):
            if a[i][0] > a[i+1][0]:
                a[i], a[i+1] = a[i+1], a[i]
                swapped = True

    # 数据上传
    for item in a:
        item[4] = item[4].replace('<s>','').replace('</s>','').replace('<div>','').replace('</div>','').replace('<article','').replace('</article>','').replace('<section>','').replace('</section','').replace('<em>','').replace('</em>','').replace('<!-- 增加 二维码图片 -->','').replace('&ldquo;','').replace('&rdquo;','')
        if '<img' in item[4]:
            item[4] = item[4].split('<img')[0] + item[4].split('<img')[1].split('/>')[1].replace('<p></p>','').replace('<p></p','')
        if (lasttime=="" or date2sec(lasttime) < item[0]) and "行情" not in item[1]:
            post = Post(topic=item[1], body=item[4].replace('<p></p>',''), lang="cn", tag=item[5], time=item[3], author=current_user._get_current_object())
            db.session.add(post)
        
    return redirect(url_for('.show_newsflash'))



@main.route('/check', methods=['GET', 'POST'])
def check():
    english=request.cookies.get('english')
    values = CombinedMultiDict([flask.request.files,flask.request.form])
    form = CheckForm(konghus="201 401 502 702 1201 1401 1801")
    if form.validate_on_submit():
        apartments = [
            '101',	'102',
            '201',	'202',
            '301',	'302',
            '401',	'402',
            '501',	'502',
            '601',	'602',
            '701',	'702',
            '801',	'802',
            '901',	'902',
            '1001',	'1002',
            '1101',	'1102',
            '1201',	'1202',
            '1301',	'1302',
            '1401',	'1402',
            '1501',	'1502',
            '1601',	'1602',
            '1701',	'1702',
            '1801',	'1802',
            '1901',	'1902',
            '2001',	'2002',
            '2101',	'2102',
            '2201',	'2202',
            '2301',	'2302',
            '2401',	'2402',
            '2501',	'2502'
        ]

        txt = form.body.data

        konghus = form.konghus.data.split(" ")

        jielongs = []
        chongfus = []
        for t in txt.split(". "):
            j = t.split(' ')[0].replace('5-','').replace('6-','').replace('4-','')
            if "-" in j:
                j = j.split('-')[0]
            if len(j) > 4:
                j = j[0:4]
                if j[-1] != "1" and j[-1] != "2":
                    j = j[0:3]
            if j in apartments:
                if j in jielongs:
                    chongfus.append(j)
                else:
                    jielongs.append(j)
        chayi = set(apartments)-set(jielongs)-set(konghus)
        flash("空户为：" + '，'.join((x for x in konghus)))
        if len(chongfus) != 0:
            flash("重复接龙的有："+','.join((x for x in chongfus)))
        if len(chayi) != 0:
            flash("未接龙的有：" +'，'.join((x for x in chayi)))
        else:
            flash("全部已经完成接龙！")
                    
    return render_template('check.html', form=form)

@main.route('/update-news')
@login_required
def update_news():
    if current_user.id != 1:
        return redirect(url_for('main.index'))
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) ... Chrome/61.0.3163.100 Safari/537.36"
    cookie="mediav=%7B%22eid%22%3A%22387123...b3574ef2-21b9-11e8-b39c-1bc4029c43b8"
    headers={"User-Agent":user_agent,"Cookie":cookie}
    socket.setdefaulttimeout(30)
    
    try:
        tag = 'jinse_news'
        u1 = "https://www.jinse.com/blockchain/"
        s1 = BeautifulSoup(requests.get(u1,headers=headers).text,'lxml')
        items = []
        items = s1.find_all(class_="font20")
        for item in items:
            url = item.a['href']            
            s = BeautifulSoup(requests.get(url,headers=headers).text,'lxml')
            try:
                topic = item.a['title']
                if Post.query.filter_by(topic=topic).first() == None:
                    continue
            except:
                continue
            con = 0
            for keyword in ['币','BTC','周报','后市分析','空头','早盘','震荡','行情','实时']:
                if keyword in topic:
                    con = 1
            if con == 1:
                continue
            try:
                t = s.find(class_="js-liveDetail__date").text.replace('\n','').replace(' ','').split('，')[0]
                if "前" in t:
                    t = hour2date(t)
                if '月' not in t:                        
                    t = parse(t)
                    t = time.strftime("%Y-%m-%d %H:%M")                    
            except Exception as e:
                t = time.strftime("%Y-%m-%d %H:%M:%S")
            flash('jinse_news--' + time.strftime("%Y-%m-%d %H:%M") + '--' + "%s--%s" % (t,topic))
            try:
                s1 = requests.get(url,headers=headers).text                
                body = s1.split('<div class="js-article" data-v-64e3d832>')[1].split('</div>')[0] + '\n（<a href="' + url + '">' + '转自金色财经，' + t + '</a>）\n'
            except:
                continue
            a.append([date2sec(t),topic,url,t,body.replace("'",'"'),tag,body2html(body.replace("'",'"')),437,'cn'])
            insert(a)
            a = []
    except Exception as e:
        flash("金色财经新闻下载时出现错误--" + str(e))
    
    try:
        tag = 'babite_news'
        u1 = "https://www.8btc.com/news"    
        a = []
        s1 = BeautifulSoup(requests.get(u1, headers=headers).text,'lxml')
        for item in s1.find_all(class_="article-info"):
            try:
                topic = item.h3.text.replace("\n",'').strip()
                if Post.query.filter_by(topic=topic).first() == None:
                    continue
            except Exception as e:
                flash("topic class is not find: " + str(e))
            url = "https://www.8btc.com" + item.a['href']
            s2 = requests.get(url,headers=headers).text
            try:
                t = s2.find(class_="time").text
                if "前" in t:
                    t = hour2date(t)                        
                t = parse(t.replace('@',''))
                t = time.strftime("%Y-%m-%d %H:%M")
            except Exception as e:
                t = time.strftime("%Y-%m-%d %H:%M:%S")
            flash('bikuaibao--' + time.strftime("%Y-%m-%d %H:%M") + '--' + "%s--%s" % (t,topic))
            body = s2.split('<div class="bbt-html" data-v-7f057cc4>')[1] + '\n（<a href="' + url + '">'  + '转自巴比特新闻，' + t + '</a>）\n'
            a.append([date2sec(t),topic,url,t,body.replace("'",'"'),tag,body2html(body.replace("'",'"')),433,'cn'])
            insert(a)
            a = []
    except Exception as e:
        flash("8比特新闻下载时出现问题--" + str(e))

    try:
        tag = 'bikuaibao_news'
        u1 = "http://www.beekuaibao.com"
        a = []
        s1 = requests.get(u1, headers=headers).text.split('<div class="title" data-v-5b0403f0>')
        for i in range(1,len(s1)-1):
            topic = s1[i].split('</div>')[0]
            if Post.query.filter_by(topic=topic).first() == None:
                continue
            url = "http://www.beekuaibao.com" + s1[i-1].split('href="')[-1].split('"')[0]
            s2 = requests.get(url, headers=headers).text.split('<article class="content">')
            try:
                t = hour2date(s2[0].split('前</span>')[0].split('>')[-1] + '前')
            except Exception as e:
                t = time.strftime("%Y-%m-%d %H:%M:%S")
            flash('bikuaibao--' + time.strftime("%Y-%m-%d %H:%M") + '--' + "%s--%s" % (t,topic))
            body = s2[1].split('</article>')[0].lstrip() + '\n（<a href="' + url + '">'  + '转自币快报，' + t + '</a>）\n'
            a.append([date2sec(t),topic,url,t, body, tag, body2html(body),436,'cn'])
            insert(a)
            a = []
    except Exception as e:
        flash("币快报下载时出现问题--" + str(e))


    return redirect(url_for('main.index'))


@main.route('/update-flash-news')
@login_required
def update_flash_news():
    if current_user.id != 1:
        return redirect(url_for('main.index'))
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) ... Chrome/61.0.3163.100 Safari/537.36"
    cookie="mediav=%7B%22eid%22%3A%22387123...b3574ef2-21b9-11e8-b39c-1bc4029c43b8"
    headers={"User-Agent":user_agent,"Cookie":cookie}
    socket.setdefaulttimeout(30)
    try:
        tag  = 'bikuaibao_newsflash'
        u1 = "http://www.beekuaibao.com/newsflashes"
        s1 = requests.get(u1,headers=headers).text.split('<div class="title" data-v-5b0403f0>')
        a = []
        for i in range(1,len(s1)):
            topic = s1[i].split('</div>')[0]
            if Post.query.filter_by(topic=topic).first() == None:
                continue
            url = "http://www.beekuaibao.com" + s1[i-1].split('href="')[-1].split('" ')[0]
            try:
                t = hour2date(s1[i].split('前</span>')[0].split('>')[-1] + '前')
            except Exception as e:
                t = time.strftime("%Y-%m-%d %H:%M:%S")
            flash('bikuaibao--' + time.strftime("%Y-%m-%d %H:%M") + '--' + "%s--%s" % (t,topic))
            body = s1[i].split('<div class="desc-container" data-v-5b0403f0>')[1].split('</div>')[0].lstrip() + '\n（<a href="' + url + '">' + '转自币快报，' + t + '</a>）\n'
            a.append([date2sec(t), topic, url, t, body, tag, body2html(body),436,'cn'])
            insert(a)
            a = []
    except Exception as e:
        flash("币快报快讯，下载出出问题--" + str(e))
    
    
    try:
        tag = 'jinse_newsflash'
        u1 = "https://www.jinse.com/lives"
        a = []    
        s1 = BeautifulSoup(requests.get(u1).text,'lxml')
        items = s1.find_all(class_="tit font20 font-w")
        for item in items:
            topic = item.a['title']
            if Post.query.filter_by(topic=topic).first() == None:
                continue
            url = item.a['href']
            s2 = requests.get(url,headers=headers).text
            t = time.strftime("%Y-%m-%d %H:%M:%S")
            flash('jinse_newsflash--' + time.strftime("%Y-%m-%d %H:%M") + '--' + "%s--%s" % (t,topic))
            body = s2.split('<div class="js-article" data-v-')[1][9:].split('</div>')[0] + '\n（<a href="' + url + '">' + '转自金色财经，' + t + '</a>）\n'
            a.append([date2sec(t),topic,url,t,body.replace("'",'"'),tag,body2html(body.replace("'",'"')),437,'cn'])
            insert(a)
            a = []
    except Exception as e:
        flash("金色财经快讯下载时出现问题--" + str(e))

    try:
        tag = 'chaindd_newsflash'
        u1 = "http://www-test.liandede.com/nictation?t1654657347983"
        a = []
        s1 = BeautifulSoup(requests.get(u1,headers=headers).text,'lxml')
        for item in s1.find_all(class_="w_tit"):
            topic = item.a.string
            if Post.query.filter_by(topic=topic).first() == None:
                continue
            url = item.a['href']
            s2 = requests.get(url,headers=headers).text
            try:
                t = s2.split('<span class="color-unclickable">')[1].split('</span>')[0]
                if "前" in t:
                    t = hour2date(t)                        
                t = parse(t)
                t = time.strftime("%Y-%m-%d %H:%M")                    
            except Exception as e:
                t = time.strftime("%Y-%m-%d %H:%M:%S")
            flash('链得得--' + time.strftime("%Y-%m-%d %H:%M") + '--' + "%s--%s" % (t,topic))
            try:
                body = s2.split('ChainDD）')[1].split('/>')[0].lstrip() + '\n（<a href="' + url + '">' + '转自链得得快讯，' + t + '</a>）\n'
            except Exception as e:
                flash("8. " + str(e))
                body = s2.split('【链得得播报】')[1].split('</p>')[0].lstrip() + '\n（<a href="' + url + '">' + '转自链得得快讯，' + t + '</a>）\n'        
            a.append([date2sec(t),topic,url,t, body,tag, body2html(body),435,'cn'])
            insert(a)
            a = []
    except Exception as e:
        flash("链得得下载出错--" + str(e))

    try:
        tag = 'babite_newsflash'
        u1 = "https://www.8btc.com/news"    
        a = []
        s1 = BeautifulSoup(requests.get(u1, headers=headers).text,'lxml')
        for item in s1.find_all(class_="flash-item"):
            try:
                topic = item.find(class_='flash-item__title link-dark-major').text.replace("\n",'').strip()
                if Post.query.filter_by(topic=topic).first() == None:
                    continue
            except Exception as e:
                flash("topic class is not find: " + str(e))
            url = "https://www.8btc.com" + item.a['href']
            s2 = requests.get(url,headers=headers).text
            try:
                t = hour2date(s2.find(class_="time").text)
                if "前" in t:
                    t = hour2date(t)                        
                t = parse(t)
                t = time.strftime("%Y-%m-%d %H:%M")  
            except Exception as e:
                t = time.strftime("%Y-%m-%d %H:%M:%S")
            flash('bikuaibao--' + time.strftime("%Y-%m-%d %H:%M") + '--' + "%s--%s" % (t,topic))
            body = s2.split('<div class="bbt-html" data-v-7f057cc4>')[1] + '\n（<a href="' + url + '">'  + '转自巴比特快讯，' + t + '</a>）\n'
            a.append([date2sec(t),topic,url,t,body.replace("'",'"'),tag,body2html(body.replace("'",'"')),433,'cn'])
            insert(a)
            a = []
    except Exception as e:
        flash("8比特快讯下载时出现问题--" + str(e))

    return redirect(url_for('main.index'))


@main.route('/update-english-news')
@login_required
def update_english_news():
    if current_user.id != 1:
        return redirect(url_for('main.index'))
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) ... Chrome/61.0.3163.100 Safari/537.36"
    cookie="mediav=%7B%22eid%22%3A%22387123...b3574ef2-21b9-11e8-b39c-1bc4029c43b8"
    headers={"User-Agent":user_agent,"Cookie":cookie}
    socket.setdefaulttimeout(30)
    
    try:
        tag = 'coindesk_news'
        u1 = "https://www.coindesk.com/tech/"    
        s1 = BeautifulSoup(requests.get(u1,headers=headers).text,'lxml')
        a = []
        items = []
        items = s1.find_all(class_='typography__StyledTypography-owin6q-0 jASKws')
        items1 = s1.find_all(class_='typography__StyledTypography-owin6q-0 cyUtww')
        items.extend(items1)
        for item in items:
            url =[]
            url = 'https://coindesk.com' + item.find('a').get('href')
            topic = item.find('a').text
            if Post.query.filter_by(topic=topic).first() == None:
                continue
            try:
                t = (item.find('a').get('href')).replace('/layer2/','').replace('/tech/','')[:10]
                if "前" in t:
                    t = hour2date(t)                        
                t = parse(t)
                t = time.strftime("%Y-%m-%d %H:%M")                    
            except Exception as e:
                t = time.strftime("%Y-%m-%d %H:%M:%S")
            s = requests.get(url,headers=headers).text
            flash('coindesk--' + time.strftime("%Y-%m-%d %H:%M") + '--' + "%s--%s" % (t,topic))
            body = s.split('<div class="contentstyle__StyledWrapper-g5cdrh-0 gCDWPA">')[1].split('div class="Box-sc-1hpkeeg-0">')[0] + '\n（<a href="' + url + '">' + 'From: coindesk.com，' + t + '</a>）\n'
            a.append([date2sec(t),topic,url,t, body.replace("&#8820;",'”'),tag, body2html(body),441,'en'])
            insert(a)
            a = []
    except Exception as e:
        flash("coindex download error--" + str(e))    
        
    try:
        tag = 'cointelegraph_news'
        u1 = "https://cointelegraph.com/press-releases"    
        s1 = BeautifulSoup(requests.get(u1,headers=headers).text,'lxml')
        a = []    
        items = s1.find_all(class_="post-card-inline__header")
        for item in items:   
            url = 'https://cointelegraph.com' + item.find('a').get('href')
            topic = item.find(class_="post-card-inline__title").text
            if Post.query.filter_by(topic=topic).first() == None:
                continue
            s = requests.get(url,headers=headers).text
            try:
                t = s.split('<time datetime="')[1].split('"')[0]
                t = parse(t)
                t = time.strftime("%Y-%m-%d %H:%M")                    
            except Exception as e:
                t = time.strftime("%Y-%m-%d %H:%M:%S")
            flash('cointelegraph--' + time.strftime("%Y-%m-%d %H:%M") + '--' + "%s--%s" % (t,topic))
            body = s.split('<div class="post-content" data-v-2a0745c6>')[1].split("</div>")[0] + '\n（<a href="' + url + '">' + 'From: cointelegraph.com，' + t + '</a>）\n'
            a.append([date2sec(t),topic,url,t, body,tag, body2html(body),440,'en'])
            insert(a)
            a = []
    except Exception as e:
        flash('cointelegraph dowload error--' + str(e))
    
    try:    
        tag = 'cryptopotato_news'
        u1 = "https://cryptopotato.com/"    
        s1 = BeautifulSoup(requests.get(u1,headers=headers).text,'lxml')
        a = []    
        items = s1.find_all(class_="media-heading entry-title")
        for item in items:   
            url = item.find('a').get('href')
            topic = item.find('a').text
            if Post.query.filter_by(topic=topic).first() == None:
                continue
            s = requests.get(url,headers=headers).text.split('<span class="breadcrumb_last" aria-current="page">')[1].split('<div class="rp4wp-related-posts rp4wp-related-post">')[0]
            try:
                t = s.split('<span class="last-modified-timestamp">')[1].split('</span>')[0]
                t = parse(t.replace('@',''))
                t = time.strftime("%Y-%m-%d %H:%M")
            except Exception as e:
                t = time.strftime("%Y-%m-%d %H:%M:%S")
            flash('bikuaibao--' + time.strftime("%Y-%m-%d %H:%M") + '--' + "%s--%s" % (t,topic))
            body = s.split('<div class="coincodex-content">')[1].split('<div class="rp4wp-related-posts rp4wp-related-post">')[0].lstrip().replace("&#8217;","") + '\n（<a href="' + url + '">' + 'From: cryptopotato.com，' + t + '</a>）\n'
            a.append([date2sec(t),topic,url,t, body,tag, body2html(body),439,'en'])
            insert(a)
            a = []
    except Exception as e:
        flash('cryptopotato download error--' + str(e))

    try:    
        tag = 'thebitcoinnews_news'
        u1 = "https://thebitcoinnews.com/category/bitcoin-news/"    
        s1 = BeautifulSoup(requests.get(u1,headers=headers).text,'lxml')
        a = []    
        items = s1.find_all(class_="td-module-thumb")
        for item in items:   
            url = item.find('a').get('href')
            topic = item.find('a').get('title') #s.split('<title>')[1].split('</title>')[0].replace('&#039;','').replace('&amp;','&').replace('&quot;',"'")
            if Post.query.filter_by(topic=topic).first() == None:
                continue
            s = requests.get(url,headers=headers).text
            try:
                t = s.split('<time class="entry-date updated td-module-date" datetime="')[1].split('">')[0]
                t = parse(t.replace('@',''))
                t = time.strftime("%Y-%m-%d %H:%M")
            except Exception as e:
                t = time.strftime("%Y-%m-%d %H:%M:%S")
            flash('bikuaibao--' + time.strftime("%Y-%m-%d %H:%M") + '--' + "%s--%s" % (t,topic))
            if len(s.split('td-adspot-title')[1].replace('<div></div>','').split('</div>')[1])<500:
                body = s.split('td-adspot-title')[1].replace('<div></div>','').split('</div>')[2].split('</div>')[0].lstrip() + '\n（<a href="' + url + '">' + 'From: thebitcoinnews.com，' + t + '</a>）\n'
            else:
                body = s.split('td-adspot-title')[1].replace('<div></div>','').split('</div>')[1].split('</div>')[0].lstrip() + '\n（<a href="' + url + '">' + 'From: thebitcoinnews.com，' + t + '</a>）\n'
            a.append([date2sec(t),topic,url,t, body,tag, body2html(body),438,'en'])
            insert(a)
            a = []
    except Exception as e:
        flash('thebitcoinnews dowload error--' + str(e))

    return redirect(url_for('main.index'))

@main.route('/go', methods=['GET', 'POST'])
@login_required
def go():
    english=request.cookies.get('english')
    filename = 'app/templates/go/' + current_user.username + '.html'
    try:
        f = open(filename, 'r+')
    except:
        with open(filename, 'w') as f:
            f.write('这里显示网页')
            f.close()    
    if english == "yes":
        form = UrlFormE()
    else:
        form = UrlForm()
    if form.validate_on_submit():
        url = form.search.data
        return redirect(url_for('main.get', url=url))
    return render_template('go.html', form=form, english=english)

@main.route('/google', methods=['GET', 'POST'])
@login_required
def google():
    english=request.cookies.get('english')
    filename = 'app/templates/go/' + current_user.username + '.html'
    try:
        f = open(filename, 'r+')
    except:
        with open(filename, 'w') as f:
            f.write('这里显示网页')
            f.close()    
    if english == "yes":
        form = GoogleFormE()
    else:
        form = GoogleForm()
    if form.validate_on_submit():
        key = form.search.data.replace(' ','+')
        return redirect(url_for('main.get', key=key))
    return render_template('google.html', form=form, english=english)


@main.route('/get', methods=['GET', 'POST'])
@login_required
def get():
    english=request.cookies.get('english')
    url = request.args.get('url')
    if '.' not in url:
        google = 1
        url = 'https://www.google.com/search?q=' + url
    else:
        google = 0
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) ... Chrome/61.0.3163.100 Safari/537.36"
    cookie="mediav=%7B%22eid%22%3A%22387123...b3574ef2-21b9-11e8-b39c-1bc4029c43b8"
    headers={"User-Agent":user_agent,"Cookie":cookie}
    # flash(url)
    if url == '' or url == None:
        if english == "yes":
            flash("Please input key words!")
        else:
            flash("请输入关键字！")
        return redirect(url_for('main.go'))
    else:
        if 'http://' in url or 'https://' in url:
            html = requests.get(url,headers=headers).text
        else:
            url = 'https://' + url
            html = requests.get(url,headers=headers).text
        filename = current_user.username + '.html'
        with open('app/templates/go/'+filename, 'w') as f:
            if google == 1:
                f.write(html.replace('href="','tartget="_blank" href="'))
            else:
                f.write(html.replace('href="http','target="_blank" href="https://wujiangang.space/url?q=http'))
            f.close()
            # flash(len(html))
        return redirect(url_for('main.go'))
    
@main.route('/url', methods=['GET', 'POST'])
@login_required
def url():
    english=request.cookies.get('english')
    url = request.args.get('q')
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) ... Chrome/61.0.3163.100 Safari/537.36"
    cookie="mediav=%7B%22eid%22%3A%22387123...b3574ef2-21b9-11e8-b39c-1bc4029c43b8"
    headers={"User-Agent":user_agent,"Cookie":cookie}
    # flash(url)
    if url == '' or url == None:
        if english == "yes":
            flash("Please input key words!")
        else:
            flash("请输入关键字！")
        return redirect(url_for('main.go'))
    else:
        if 'http://' in url or 'https://' in url:
            html = requests.get(url,headers=headers).text
        else:
            url = 'https://' + url
            html = requests.get(url,headers=headers).text
        filename = current_user.username + '.html'
        with open('app/templates/go/'+filename, 'w') as f:
            f.write(html.replace('href="http','target="_blank" href="https://wujiangang.space/url?q=http').replace('href="/','target="_blank" href="'+url+'/'))
            f.close()
            # flash(len(html))
        return redirect(url_for('main.output'))            

@main.route('/output', methods=['GET', 'POST'])
@login_required
def output():
    return render_template('go/' + current_user.username + '.html')

# @main.route('/all_index', methods=['GET', 'POST'])
# def all_index():
#     return render_template('index/all_index.html')

# @main.route('/bank_index', methods=['GET', 'POST'])
# def bank_index():
#     return render_template('index/bank_index.html')

# @main.route('/car_index', methods=['GET', 'POST'])
# def car_index():
#     return render_template('index/car_index.html')

# @main.route('/commerce_index', methods=['GET', 'POST'])
# def commerce_index():
#     return render_template('index/commerce_index.html')

# @main.route('/edu_index', methods=['GET', 'POST'])
# def edu_index():
#     return render_template('index/edu_index.html')

# @main.route('/energy_index', methods=['GET', 'POST'])
# def energy_index():
#     return render_template('index/energy_index.html')

# @main.route('/estate_index', methods=['GET', 'POST'])
# def estate_index():
#     return render_template('index/estate_index.html')

# @main.route('/exchange_index', methods=['GET', 'POST'])
# def exchange_index():
#     return render_template('index/exchange_index.html')

# @main.route('/futures_index', methods=['GET', 'POST'])
# def futures_index():
#     return render_template('index/futures_index.html')

# @main.route('/gold_index', methods=['GET', 'POST'])
# def gold_index():
#     return render_template('index/gold_index.html')

# @main.route('/industry_index', methods=['GET', 'POST'])
# def industry_index():
#     return render_template('index/industry_index.html')

# @main.route('/info_index', methods=['GET', 'POST'])
# def info_index():
#     return render_template('index/info_index.html')

# @main.route('/invest_index', methods=['GET', 'POST'])
# def invest_index():
#     return render_template('index/invest_index.html')

# @main.route('/IT_index', methods=['GET', 'POST'])
# def IT_index():
#     return render_template('index/IT_index.html')

# @main.route('/journey_index', methods=['GET', 'POST'])
# def journey_index():
#     return render_template('index/journey_index.html')

# @main.route('/licai_index', methods=['GET', 'POST'])
# def licai_index():
#     return render_template('index/licai_index.html')

# @main.route('/life_index', methods=['GET', 'POST'])
# def life_index():
#     return render_template('index/life_index.html')

# @main.route('/mall_index', methods=['GET', 'POST'])
# def mall_index():
#     return render_template('index/mall_index.html')

# @main.route('/niublog_index', methods=['GET', 'POST'])
# def niublog_index():
#     return render_template('index/niublog_index.html')

# @main.route('/securities_index', methods=['GET', 'POST'])
# def securities_index():
#     return render_template('index/securities_index.html')

# @main.route('/shiyong_index', methods=['GET', 'POST'])
# def shiyong_index():
#     return render_template('index/shiyong_index.html')

# @main.route('/shuju_index', methods=['GET', 'POST'])
# def shuju_index():
#     return render_template('index/shuju_index.html')

# @main.route('/software_index', methods=['GET', 'POST'])
# def software_index():
#     return render_template('index/software_index.html')

# @main.route('/tool_index', methods=['GET', 'POST'])
# def tool_index():
#     return render_template('index/tool_index.html')

# @main.route('/trade_index', methods=['GET', 'POST'])
# def trade_index():
#     return render_template('index/trade_index.html')

# @main.route('/trust_index', methods=['GET', 'POST'])
# def trust_index():
#     return render_template('index/trust_index.html')

# @main.route('/first_index', methods=['GET', 'POST'])
# def first_index():
#     return render_template('index/first_index.html')

# @main.route('/fund_index', methods=['GET', 'POST'])
# def fund_index():
#     return render_template('index/fund_index.html')

# @main.route('/jigou_index', methods=['GET', 'POST'])
# def jigou_index():
#     return render_template('index/jigou_index.html')

@main.route('/webguide', methods=['GET', 'POST'])
def webguide():
    return render_template('webguide.html')

@main.route('/baidu_verify_code-RTu0ZniTY6.html')
def baidu_verify_code():
    return render_template('baidu_verify_code-RTu0ZniTY6.html')

@main.route('/sogousiteverification.txt')
def sogousiteverification():
    return render_template('sogousiteverification.txt')
