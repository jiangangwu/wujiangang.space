from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
                    TextAreaField, SelectField, IntegerField, DateField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User,Role
from flask_pagedown.fields import PageDownField
from flask_wtf.file import FileField,FileAllowed


class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[Required(), Length(1, 64), Email()])
    password = PasswordField('密码', validators=[Required()])
    remember_me = BooleanField('保持登入状态')
    submit = SubmitField('登入')

class LoginFormE(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me log in')
    submit = SubmitField('Log in')

class RegistrationForm(FlaskForm):
    email = StringField('邮箱', validators=[Required(), Length(1, 64),
                                           Email()])
    password = PasswordField('密码', validators=[
        Required(), EqualTo('password2', message='两次输入的密码不一致')])
    password2 = PasswordField('再次输入密码', validators=[Required()])
    username = StringField('昵称（注册后不可修改）', validators=[
        Required(), Length(1, 64), Regexp('^[\u4e00-\u9fa5A-Za-z0-9_.]*$', 0,
                                          '名字只能是中文、英文、数字、下划线或点组成！')])
    submit = SubmitField('注册')

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user:
 #           if user.confirmed:
            raise ValidationError('邮箱已经被人注册')
            # else:
            #     raise ValidationError('该邮箱被人注册过，但尚未通过邮件确认，您依然可以使用。')

    def validate_username(self, field):
        user = User.query.filter_by(username=field.data).first()
        if user:
#            if user.confirmed:            
            raise ValidationError('用户名已经被人注册')
            # else:
            #     raise ValidationError('该用户名被人使用过，但尚未通过邮件确认，您依然可以使用。')

class RegistrationFormE(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                           Email()])
    username = StringField('Username', validators=[
        Required(), Length(1, 64), Regexp('^[\u4e00-\u9fa5A-Za-z0-9_.]*$', 0,
                                          'Name can be in compositon of Chinese, English, numbers, underline.')])
    password = PasswordField('Password', validators=[
        Required(), EqualTo('password2', message='The two inputs are differenct!')])
    password2 = PasswordField('Password again', validators=[Required()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            if User.query.filter_by(email=field.data).first().confirmed:
                raise ValidationError('邮箱已经被人注册')
            else:
                raise ValidationError('该邮箱被人注册过，但尚未通过邮件确认，您依然可以使用。')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            if User.query.filter_by(username=field.data).first().confirmed:
                raise ValidationError('用户名已经被人注册')
            else:
                raise ValidationError('该用户名被人使用过，但尚未通过邮件确认，您依然可以使用。')
                
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('The Email has been occupied!')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('The username has been occupied!')



class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('旧密码', validators=[Required()])
    password = PasswordField('新密码', validators=[
        Required(), EqualTo('password2', message='两次输入的密码必须一致')])
    password2 = PasswordField('再次输入密码', validators=[Required()])
    submit = SubmitField('更新密码')

class ChangePasswordFormE(FlaskForm):
    old_password = PasswordField('Old password', validators=[Required()])
    password = PasswordField('New password', validators=[
        Required(), EqualTo('password2', message='The two inputs are different!')])
    password2 = PasswordField('Password again', validators=[Required()])
    submit = SubmitField('Update password')



class PasswordResetRequestForm(FlaskForm):
    email = StringField('邮箱', validators=[Required(), Length(1, 64),
                                             Email()])
    submit = SubmitField('重设密码')

class PasswordResetRequestFormE(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    submit = SubmitField('Reset password')


class PasswordResetForm(FlaskForm):
    email = StringField('邮箱', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField('新密码', validators=[
        Required(), EqualTo('password2', message='两次输入的密码必须一致')])
    password2 = PasswordField('再次输入密码', validators=[Required()])
    submit = SubmitField('重设密码')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('未知邮箱')


class PasswordResetFormE(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField('New password', validators=[
        Required(), EqualTo('password2', message='The two inputs are different!')])
    password2 = PasswordField('Password again', validators=[Required()])
    submit = SubmitField('Reset password')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Unknown Email')


class ChangeEmailForm(FlaskForm):
    email = StringField('新邮箱', validators=[Required(), Length(1, 64),
                                                 Email()])
    password = PasswordField('密码', validators=[Required()])
    submit = SubmitField('更新邮箱地址')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已被注册')

class ChangeEmailFormE(FlaskForm):
    email = StringField('New Email', validators=[Required(), Length(1, 64),
                                                 Email()])
    password = PasswordField('password', validators=[Required()])
    submit = SubmitField('Reset Email')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('The Email has been occupied!')

class EditProfileForm(FlaskForm):
    name = StringField('真实姓名', validators=[Required(),Length(0, 64)])
    student_no = StringField('学号或工号', validators=[Required(),Length(0, 64)])
    tel = StringField('手机', validators=[Required(),Length(0, 64)])
    location = StringField('地址', validators=[Required(),Length(0, 64)])
    about_me = PageDownField('关于我（必填）', validators=[Required(),Length(0, 64)])
    submit = SubmitField('提交')



class EditProfileFormE(FlaskForm):
    name = StringField('Real name', validators=[Required(),Length(0, 64)])
    student_no = StringField('Student number or work number', validators=[Required(),Length(0, 64)])
    tel = StringField('Telephone', validators=[Required(),Length(0, 64)])
    location = StringField('Address', validators=[Required(),Length(0, 64)])
    about_me = PageDownField('About me', validators=[Required(),Length(0, 64)])
    submit = SubmitField('Submit')


class EditProfileAdminForm(FlaskForm):
    email = StringField('电邮', validators=[Required(), Length(1, 64),
                                             Email()])
    username = StringField('用户名', validators=[
        Required(), Length(1, 64), Regexp('^[\u4e00-\u9fa5A-Za-z0-9_.]*$', 0,
                                          '名字只能是中文、英文、数字、下划线或点组成！')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('工作', coerce=int)
    name = StringField('真实姓名', validators=[Length(0, 64)])
    location = StringField('地区', validators=[Length(0, 64)])
    about_me = TextAreaField('关于我')
    submit = SubmitField('提交')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经存在了。')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经存在了。')


class EditProfileAdminFormE(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[
        Required(), Length(1, 64), Regexp('^[\u4e00-\u9fa5A-Za-z0-9_.]*$', 0,
                                          'Name can be in compositon of Chinese, English, numbers, underline.')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('The Email has been occupied!')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('The username has been occupied!')



class AddTeacherForm(FlaskForm):
    school = StringField('单位', validators=[Required(), Length(1, 64)])
    field = StringField('研究领域',validators=[Required(), Length(1, 64)])
    about_teacher = PageDownField('申请老师描述', validators=[Required()])
    submit = SubmitField('提交')

class AddTeacherFormE(FlaskForm):
    school = StringField('Firm', validators=[Required(), Length(1, 64)])
    field = StringField('Research areas',validators=[Required(), Length(1, 64)])
    about_teacher = PageDownField('About teacher', validators=[Required()])
    submit = SubmitField('Submit')
    
    
class NameForm(FlaskForm):
    name = StringField('你的名字是什么？', validators=[Required()])
    submit = SubmitField('提交')

class NameFormE(FlaskForm):
    name = StringField('Your name?', validators=[Required()])
    submit = SubmitField('Submit')

class PostForm(FlaskForm):
    topic = StringField("标题",validators=[Required(),Length(0, 256)])
    pic = FileField(label='文首图片',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png'],message='可以上传bmp/jpg/jpeg/png/bmp/jif，上传失败可能是因为类型不对或文件太大，可点浏览器上一步，继续编辑。')])
    body = PageDownField("内容")
    at_names =  StringField("@给朋友",validators=[Length(0, 256)])
    private = BooleanField("私信")
    submit = SubmitField('提交')

class PostFormE(FlaskForm):
    topic = StringField("Topic",validators=[Required(),Length(0, 256)])
    pic = FileField(label='Picture before article',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png'],message="can upload bmp/jpg/jpeg/png/bmp/jif, if failed, may caused by too big file or wrong file type, please click browser's last page to edit again.")])
    body = PageDownField("Content")
    at_names =  StringField("@friends",validators=[Length(0, 256)])
    private = BooleanField("Private")
    submit = SubmitField('Submit')

class NewsForm(FlaskForm):
    topic = StringField("标题",validators=[Required(),Length(0, 256)])
    body = PageDownField("内容")
    private = BooleanField("私信")
    submit = SubmitField('提交')

class NewsFormE(FlaskForm):
    topic = StringField("Topic",validators=[Required(),Length(0, 256)])
    body = PageDownField("Content")
    private = BooleanField("Private")
    submit = SubmitField('Submit')
        
class PostForm2(FlaskForm):
    topic = StringField("标题",validators=[Required(),Length(0, 256)])
    pic = FileField(label='文首图片',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png'],message='可以上传bmp/jpg/jpeg/png/bmp/jif')])
    body = PageDownField("内容")
    pic1 = FileField(label='文末图片1',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png'],message='可以上传bmp/jpg/jpeg/png/bmp/jif')])
    pic2 = FileField(label='文末图片2',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png'],message='可以上传bmp/jpg/jpeg/png/bmp/jif')])
    pic3 = FileField(label='文末图片3',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png'],message='可以上传bmp/jpg/jpeg/png/bmp/jif')])
    file1 = FileField(label='文件1',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png','txt','TXT','pdf','PDF','xls','XLS','xlsx','XLSX','ppt','PPT','pptx','PPTX','doc','DOC','docx','DOCX', 'zip', 'ZIP', 'rar', 'RAR'],message="可以上传txt\pdf\word\excel\ppt\zip\rar或图片，如果上传失败可能是因为文件太大或类型不对，请返回上一页继续编辑。")])
    file2 = FileField(label='文件2',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png','txt','TXT','pdf','PDF','xls','XLS','xlsx','XLSX','ppt','PPT','pptx','PPTX','doc','DOC','docx','DOCX', 'zip', 'ZIP', 'rar', 'RAR'],message="可以上传txt\pdf\word\excel\ppt\zip\rar或图片，如果上传失败可能是因为文件太大或类型不对，请返回上一页继续编辑。")])
    file5 = FileField(label='文件3',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png','txt','TXT','pdf','PDF','xls','XLS','xlsx','XLSX','ppt','PPT','pptx','PPTX','doc','DOC','docx','DOCX', 'zip', 'ZIP', 'rar', 'RAR'],message="可以上传txt\pdf\word\excel\ppt\zip\rar或图片，如果上传失败可能是因为文件太大或类型不对，请返回上一页继续编辑。")])
    file3 = FileField(label='音频',validators=[
        FileAllowed(['wav','mp4','mp3','ogg','Wav','Mp3','Mp4','Ogg','WAV','MP3','MP4','OGG'],message='可以上传小于50M的mp3/mp4/ogg/wav等音频。')])            
    file4 = FileField(label='视频',validators=[
        FileAllowed(['Mp4','Ogg','Mpeg4','WebM','mp4','ogg','mpeg4','webm','MP4','OGG','MPEG4','WEBM'],message='可以上传小于50M的ogg/MPEG4/WebM等视频。')])
    at_names =  StringField("@给朋友（对方用户名用空间隔开）",validators=[Length(0, 256)])
    private = BooleanField("私有")
    submit = SubmitField('提交')


    
    
class PostFormE2(FlaskForm):
    topic = StringField("Topic",validators=[Required(),Length(0, 256)])
    pic = FileField(label='Picture before article',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png'],message="You can upload bmp/jpg/jpeg/png/bmp/jif, if failed, may caused by too big file or wrong file type, please click browser's last page to edit again.")])
    body = PageDownField("Content")
    pic1 = FileField(label='Picture after article: 1',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png'],message="You can upload bmp/jpg/jpeg/png/bmp/jif, if failed, may caused by too big file or wrong file type, please click browser's last page to edit again.")])
    pic2 = FileField(label='Picture after article: 2',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png'],message="You can upload bmp/jpg/jpeg/png/bmp/jif, if failed, may caused by too big file or wrong file type, please click browser's last page to edit again.")])
    pic3 = FileField(label='Picture after article: 3',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png'],message="You can upload bmp/jpg/jpeg/png/bmp/jif, if failed, may caused by too big file or wrong file type, please click browser's last page to edit again.")])
    file1 = FileField(label='File 1',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png','txt','TXT','pdf','PDF','xls','XLS','xlsx','XLSX','ppt','PPT','pptx','PPTX','doc','DOC','docx','DOCX', 'zip', 'ZIP', 'rar', 'RAR'],message='You can upload txt\pdf\word\excel\ppt\zip\rar or pictures')])
    file2 = FileField(label='File 2',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png','txt','TXT','pdf','PDF','xls','XLS','xlsx','XLSX','ppt','PPT','pptx','PPTX','doc','DOC','docx','DOCX', 'zip', 'ZIP', 'rar', 'RAR'],message='You can upload txt\pdf\word\excel\ppt\zip\rar or pictures')])
    file5 = FileField(label='File 3',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png','txt','TXT','pdf','PDF','xls','XLS','xlsx','XLSX','ppt','PPT','pptx','PPTX','doc','DOC','docx','DOCX', 'zip', 'ZIP', 'rar', 'RAR'],message='You can upload txt\pdf\word\excel\ppt\zip\rar or pictures')])
    file3 = FileField(label='Audio',validators=[
        FileAllowed(['wav','mp3','ogg','Wav','Mp3','Ogg','WAV','MP3','OGG'],message='You can upload audio files less than 50M such as mp3/ogg/wav.')])            
    file4 = FileField(label='Video',validators=[
        FileAllowed(['Mp4','Ogg','Mpeg4','WebM','mp4','ogg','mpeg4','webm','MP4','OGG','MPEG4','WEBM','mov','MOV','Mov','avi','AVI','Avi','mpg','MPG','Mpg'],message='You can upload video files less than 50M such as mp4/mov/ogg/mpe4/webm.')])
    at_names =  StringField("@friends（names should be seperated by a space.）",validators=[Length(0, 256)])
    private = BooleanField("Private")
    submit = SubmitField('Submit')


class PostForm0(FlaskForm):
    topic = StringField("标题",validators=[Required(),Length(0, 256)])
    tag = SelectField('类型',choices=[('posts','博客'), ('news','新闻'), ('research','研究'),  ('rating','评级'), ('guide','导航'), ('document','资料'), ('basic','入门'),('about','关于')],validators=[Required()])
    pic = FileField(label='文首图片',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png'],message='可以上传bmp/jpg/jpeg/png/bmp/jif')])
    body = PageDownField("内容")
    at_names =  StringField("@给朋友（对方用户名用空间隔开）",validators=[Length(0, 256)])
    private = BooleanField("私有")
    submit = SubmitField('提交')

class PostForm0E(FlaskForm):
    topic = StringField("Topic",validators=[Required(),Length(0, 256)])
    tag = SelectField('Type',choices=[('posts','blog'), ('news','news'), ('research','research'),  ('rating','rating'),('guide','guide'),('document','document'),  ('basic','basic'),('about','about')],validators=[Required()])
    pic = FileField(label='Picture before article',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png'],message='可以上传bmp/jpg/jpeg/png/bmp/jif')])
    body = PageDownField("Content")
    at_names =  StringField("@friends（names should be seperated by a space.）",validators=[Length(0, 256)])
    private = BooleanField("Private")
    submit = SubmitField('Submit')

    
class PostForm02(FlaskForm):
    topic = StringField("标题",validators=[Required(),Length(0, 256)])
    tag = SelectField('类型',choices=[('posts','博客'), ('news','新闻'), ('research','研究'),  ('rating','评级'), ('guide','导航'), ('document','资料'), ('basic','入门'),('about','关于')],validators=[Required()])
    pic = FileField(label='文首图片',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png'],message='可以上传bmp/jpg/jpeg/png/bmp/jif')])
    body = PageDownField("内容")
    pic1 = FileField(label='文末图片1',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png'],message='可以上传bmp/jpg/jpeg/png/bmp/jif')])
    pic2 = FileField(label='文末图片2',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png'],message='可以上传bmp/jpg/jpeg/png/bmp/jif')])
    pic3 = FileField(label='文末图片3',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png'],message='可以上传bmp/jpg/jpeg/png/bmp/jif')])
    file1 = FileField(label='文件1',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png','txt','TXT','pdf','PDF','xls','XLS','xlsx','XLSX','ppt','PPT','pptx','PPTX','doc','DOC','docx','DOCX', 'zip', 'ZIP', 'rar', 'RAR'],message="可以上传txt\pdf\word\excel\ppt\zip\rar或图片，如果上传失败可能是因为文件太大或类型不对，请返回上一页继续编辑。")])
    file2 = FileField(label='文件2',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png','txt','TXT','pdf','PDF','xls','XLS','xlsx','XLSX','ppt','PPT','pptx','PPTX','doc','DOC','docx','DOCX', 'zip', 'ZIP', 'rar', 'RAR'],message="可以上传txt\pdf\word\excel\ppt\zip\rar或图片，如果上传失败可能是因为文件太大或类型不对，请返回上一页继续编辑。")])
    file5 = FileField(label='文件3',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png','txt','TXT','pdf','PDF','xls','XLS','xlsx','XLSX','ppt','PPT','pptx','PPTX','doc','DOC','docx','DOCX', 'zip', 'ZIP', 'rar', 'RAR'],message="可以上传txt\pdf\word\excel\ppt\zip\rar或图片，如果上传失败可能是因为文件太大或类型不对，请返回上一页继续编辑。")])
    file3 = FileField(label='音频',validators=[
        FileAllowed(['wav','mp4','mp3','ogg','Wav','Mp3','Mp4','Ogg','WAV','MP3','MP4','OGG'],message='可以上传小于50M的mp3/mp4/ogg/wav等音频。')])            
    file4 = FileField(label='视频',validators=[
        FileAllowed(['Mp4','Ogg','Mpeg4','WebM','mp4','ogg','mpeg4','webm','MP4','OGG','MPEG4','WEBM'],message='可以上传小于50M的ogg/MPEG4/WebM等视频。')])
    at_names =  StringField("@给朋友（对方用户名用空间隔开）",validators=[Length(0, 256)])
    private = BooleanField("私有")
    submit = SubmitField('提交')


    
    
class PostForm02E(FlaskForm):
    topic = StringField("Topic",validators=[Required(),Length(0, 256)])
    tag = SelectField('Type',choices=[('posts','blog'), ('news','news'), ('research','research'), ('rating','rating'), ('guide','guide'), ('document','document'), ('basic','basic'),('about','about')],validators=[Required()])
    pic = FileField(label='Picture before artile',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png'],message="You can upload bmp/jpg/jpeg/png/bmp/jif, if failed, may caused by too big file or wrong file type, please click browser's last page to edit again.")])
    body = PageDownField("Content")
    pic1 = FileField(label='Picture after article: 1',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png'],message="You can upload bmp/jpg/jpeg/png/bmp/jif, if failed, may caused by too big file or wrong file type, please click browser's last page to edit again.")])
    pic2 = FileField(label='Picture after article: 2',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png'],message="You can upload bmp/jpg/jpeg/png/bmp/jif, if failed, may caused by too big file or wrong file type, please click browser's last page to edit again.")])
    pic3 = FileField(label='Picture after article: 3',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png'],message="You can upload bmp/jpg/jpeg/png/bmp/jif, if failed, may caused by too big file or wrong file type, please click browser's last page to edit again.")])
    file1 = FileField(label='File 1',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png','txt','TXT','pdf','PDF','xls','XLS','xlsx','XLSX','ppt','PPT','pptx','PPTX','doc','DOC','docx','DOCX', 'zip', 'ZIP', 'rar', 'RAR'],message='You can upload txt\pdf\word\excel\ppt\zip\rar or pictures')])
    file2 = FileField(label='File 2',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png','txt','TXT','pdf','PDF','xls','XLS','xlsx','XLSX','ppt','PPT','pptx','PPTX','doc','DOC','docx','DOCX', 'zip', 'ZIP', 'rar', 'RAR'],message='You can upload txt\pdf\word\excel\ppt\zip\rar or pictures')])
    file5 = FileField(label='File 3',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png','txt','TXT','pdf','PDF','xls','XLS','xlsx','XLSX','ppt','PPT','pptx','PPTX','doc','DOC','docx','DOCX', 'zip', 'ZIP', 'rar', 'RAR'],message='You can upload txt\pdf\word\excel\ppt\zip\rar or pictures')])
    file3 = FileField(label='Audio',validators=[
        FileAllowed(['wav','mp3','ogg','Wav','Mp3','Ogg','WAV','MP3','OGG'],message='You can upload audio files less than 50M such as mp3/ogg/wav.')])            
    file4 = FileField(label='Video',validators=[
        FileAllowed(['Mp4','Ogg','Mpeg4','WebM','mp4','ogg','mpeg4','webm','MP4','OGG','MPEG4','WEBM','mov','MOV','Mov','avi','AVI','Avi','mpg','MPG','Mpg'],message='You can upload video files less than 50M such as mp4/mov/ogg/mpe4/webm.')])
    at_names =  StringField("@friends（names should be seperated by a space.）",validators=[Length(0, 256)])
    private = BooleanField("Private")
    submit = SubmitField('Submit')



class PostFormNewlesson(FlaskForm):
    topic = StringField("标题",validators=[Required(),Length(0, 256)])
    pic = FileField(label='文首图片',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png'],message='可以上传bmp/jpg/jpeg/png/bmp/jif')])
    body = PageDownField("内容")
    at_names =  StringField("@朋友",validators=[Length(0, 256)])
    private = BooleanField("Private")
    submit = SubmitField('提交')

class PostFormNewlessonE(FlaskForm):
    topic = StringField("Topic",validators=[Required(),Length(0, 256)])
    pic = FileField(label='Picture before the article',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png'],message='you can upload: bmp/jpg/jpeg/png/bmp/jif')])
    body = PageDownField("Content")
    at_names =  StringField("@friends（names should be seperated by a space.）",validators=[Length(0, 256)])
    private = BooleanField("Private")
    submit = SubmitField('Submit')


    
class PostFormNewlesson2(FlaskForm):
    topic = StringField("标题",validators=[Required(),Length(0, 256)])
    pic = FileField(label='文首图片',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png'],message='可以上传bmp/jpg/jpeg/png/bmp/jif')])
    body = PageDownField("内容")
    pic1 = FileField(label='文末图片1',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png'],message='可以上传bmp/jpg/jpeg/png/bmp/jif')])
    pic2 = FileField(label='文末图片2',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png'],message='可以上传bmp/jpg/jpeg/png/bmp/jif')])
    pic3 = FileField(label='文末图片3',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png'],message='可以上传bmp/jpg/jpeg/png/bmp/jif')])
    file1 = FileField(label='文末文件1',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png','txt','TXT','pdf','PDF','xls','XLS','xlsx','XLSX','ppt','PPT','pptx','PPTX','doc','DOC','docx','DOCX', 'zip', 'ZIP', 'rar', 'RAR'],message="可以上传txt\pdf\word\excel\ppt\zip\rar或图片，如果上传失败可能是因为文件太大或类型不对，请返回上一页继续编辑。")])
    file2 = FileField(label='文末文件2',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png','txt','TXT','pdf','PDF','xls','XLS','xlsx','XLSX','ppt','PPT','pptx','PPTX','doc','DOC','docx','DOCX', 'zip', 'ZIP', 'rar', 'RAR'],message="可以上传txt\pdf\word\excel\ppt\zip\rar或图片，如果上传失败可能是因为文件太大或类型不对，请返回上一页继续编辑。")])
    file5 = FileField(label='文末文件3',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png','txt','TXT','pdf','PDF','xls','XLS','xlsx','XLSX','ppt','PPT','pptx','PPTX','doc','DOC','docx','DOCX', 'zip', 'ZIP', 'rar', 'RAR'],message="可以上传txt\pdf\word\excel\ppt\zip\rar或图片，如果上传失败可能是因为文件太大或类型不对，请返回上一页继续编辑。")])
    file3 = FileField(label='文末音频',validators=[
        FileAllowed(['wav','mp4','mp3','ogg','Wav','Mp3','Mp4','Ogg','WAV','MP3','MP4','OGG'],message='可以上传小于50M的mp3/mp4/ogg/wav等音频。')])            
    file4 = FileField(label='文末视频',validators=[
        FileAllowed(['Mp4','Ogg','Mpeg4','WebM','mp4','ogg','mpeg4','webm','MP4','OGG','MPEG4','WEBM'],message='可以上传小于50M的ogg/MPEG4/WebM等视频。')])
    at_names =  StringField("@朋友",validators=[Length(0, 256)])
    private = BooleanField("Private")
    submit = SubmitField('提交')


class PostFormNewlesson2E(FlaskForm):
    topic = StringField("Topic",validators=[Required(),Length(0, 256)])
    pic = FileField(label='Picture before article',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png'],message="You can upload bmp/jpg/jpeg/png/bmp/jif, if failed, may caused by too big file or wrong file type, please click browser's last page to edit again.")])
    body = PageDownField("Content")
    pic1 = FileField(label='Picture after article: 1',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png'],message="You can upload bmp/jpg/jpeg/png/bmp/jif, if failed, may caused by too big file or wrong file type, please click browser's last page to edit again.")])
    pic2 = FileField(label='Picture after article: 2',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png'],message="You can upload bmp/jpg/jpeg/png/bmp/jif, if failed, may caused by too big file or wrong file type, please click browser's last page to edit again.")])
    pic3 = FileField(label='Picture after article: 3',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png'],message="You can upload bmp/jpg/jpeg/png/bmp/jif, if failed, may caused by too big file or wrong file type, please click browser's last page to edit again.")])
    file1 = FileField(label='File 1',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png','txt','TXT','pdf','PDF','xls','XLS','xlsx','XLSX','ppt','PPT','pptx','PPTX','doc','DOC','docx','DOCX', 'zip', 'ZIP', 'rar', 'RAR'],message='You can upload txt\pdf\word\excel\ppt\zip\rar or pictures')])
    file2 = FileField(label='File 2',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png','txt','TXT','pdf','PDF','xls','XLS','xlsx','XLSX','ppt','PPT','pptx','PPTX','doc','DOC','docx','DOCX', 'zip', 'ZIP', 'rar', 'RAR'],message='You can upload txt\pdf\word\excel\ppt\zip\rar or pictures')])
    file5 = FileField(label='File 3',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png','txt','TXT','pdf','PDF','xls','XLS','xlsx','XLSX','ppt','PPT','pptx','PPTX','doc','DOC','docx','DOCX', 'zip', 'ZIP', 'rar', 'RAR'],message='You can upload txt\pdf\word\excel\ppt\zip\rar or pictures')])    
    file3 = FileField(label='Audio',validators=[
        FileAllowed(['wav','mp3','ogg','Wav','Mp3','Ogg','WAV','MP3','OGG'],message='You can upload audio files less than 50M such as mp3/ogg/wav.')])            
    file4 = FileField(label='Video',validators=[
        FileAllowed(['Mp4','Ogg','Mpeg4','WebM','mp4','ogg','mpeg4','webm','MP4','OGG','MPEG4','WEBM','mov','MOV','Mov','avi','AVI','Avi','mpg','MPG','Mpg'],message='You can upload video files less than 50M such as mp4/mov/ogg/mpe4/webm.')])
    at_names =  StringField("@friends（names should be seperated by a space.）",validators=[Length(0, 256)])
    private = BooleanField("Private")
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    body = PageDownField('输入评论', validators=[Required()])
    submit = SubmitField('提交')

class CommentFormE(FlaskForm):
    body = PageDownField('Comment', validators=[Required()])
    submit = SubmitField('Submit')


class AddLessonForm(FlaskForm):
    lesson_name = StringField("课程名",validators=[Required(),Length(0, 64)])
    pic = FileField(label='课程封面',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png'],message='可以上传bmp/jpg/jpeg/png/bmp/jif')])
    about_lesson = PageDownField("课程简介", validators=[Required()])

    file1 = FileField(label='参考资料1',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png','txt','TXT','pdf','PDF','xls','XLS','xlsx','XLSX','ppt','PPT','pptx','PPTX','doc','DOC','docx','DOCX', 'zip', 'ZIP', 'rar', 'RAR'],message="可以上传txt\pdf\word\excel\ppt\zip\rar或图片，如果上传失败可能是因为文件太大或类型不对，请返回上一页继续编辑。")])            
    file2 = FileField(label='参考资料2',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png','txt','TXT','pdf','PDF','xls','XLS','xlsx','XLSX','ppt','PPT','pptx','PPTX','doc','DOC','docx','DOCX', 'zip', 'ZIP', 'rar', 'RAR'],message="可以上传txt\pdf\word\excel\ppt\zip\rar或图片，如果上传失败可能是因为文件太大或类型不对，请返回上一页继续编辑。")])
    file3 = FileField(label='参考资料3',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png','txt','TXT','pdf','PDF','xls','XLS','xlsx','XLSX','ppt','PPT','pptx','PPTX','doc','DOC','docx','DOCX', 'zip', 'ZIP', 'rar', 'RAR'],message="可以上传txt\pdf\word\excel\ppt\zip\rar或图片，如果上传失败可能是因为文件太大或类型不对，请返回上一页继续编辑。")])
    file4 = FileField(label='参考资料4',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png','txt','TXT','pdf','PDF','xls','XLS','xlsx','XLSX','ppt','PPT','pptx','PPTX','doc','DOC','docx','DOCX', 'zip', 'ZIP', 'rar', 'RAR'],message="可以上传txt\pdf\word\excel\ppt\zip\rar或图片，如果上传失败可能是因为文件太大或类型不对，请返回上一页继续编辑。")])
    file5 = FileField(label='参考资料5',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png','txt','TXT','pdf','PDF','xls','XLS','xlsx','XLSX','ppt','PPT','pptx','PPTX','doc','DOC','docx','DOCX', 'zip', 'ZIP', 'rar', 'RAR'],message="可以上传txt\pdf\word\excel\ppt\zip\rar或图片，如果上传失败可能是因为文件太大或类型不对，请返回上一页继续编辑。")])
    file6 = FileField(label='参考资料6',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png','txt','TXT','pdf','PDF','xls','XLS','xlsx','XLSX','ppt','PPT','pptx','PPTX','doc','DOC','docx','DOCX', 'zip', 'ZIP', 'rar', 'RAR'],message="可以上传txt\pdf\word\excel\ppt\zip\rar或图片，如果上传失败可能是因为文件太大或类型不对，请返回上一页继续编辑。")])
    file7 = FileField(label='参考资料7',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png','txt','TXT','pdf','PDF','xls','XLS','xlsx','XLSX','ppt','PPT','pptx','PPTX','doc','DOC','docx','DOCX', 'zip', 'ZIP', 'rar', 'RAR'],message="可以上传txt\pdf\word\excel\ppt\zip\rar或图片，如果上传失败可能是因为文件太大或类型不对，请返回上一页继续编辑。")])
    file8 = FileField(label='参考资料8',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png','txt','TXT','pdf','PDF','xls','XLS','xlsx','XLSX','ppt','PPT','pptx','PPTX','doc','DOC','docx','DOCX', 'zip', 'ZIP', 'rar', 'RAR'],message="可以上传txt\pdf\word\excel\ppt\zip\rar或图片，如果上传失败可能是因为文件太大或类型不对，请返回上一页继续编辑。")])
    submit = SubmitField('提交课程')

class AddLessonFormE(FlaskForm):
    lesson_name = StringField("Name of the lesson",validators=[Required(),Length(0, 64)])
    pic = FileField(label='Picture',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png'],message='可以上传bmp/jpg/jpeg/png/bmp/jif')])
    about_lesson = PageDownField("Syllabus", validators=[Required()])

    file1 = FileField(label='Related file 1',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png','txt','TXT','pdf','PDF','xls','XLS','xlsx','XLSX','ppt','PPT','pptx','PPTX','doc','DOC','docx','DOCX', 'zip', 'ZIP', 'rar', 'RAR'],message="可以上传txt\pdf\word\excel\ppt\zip\rar或图片，如果上传失败可能是因为文件太大或类型不对，请返回上一页继续编辑。")])            
    file2 = FileField(label='Related file 2',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png','txt','TXT','pdf','PDF','xls','XLS','xlsx','XLSX','ppt','PPT','pptx','PPTX','doc','DOC','docx','DOCX', 'zip', 'ZIP', 'rar', 'RAR'],message="可以上传txt\pdf\word\excel\ppt\zip\rar或图片，如果上传失败可能是因为文件太大或类型不对，请返回上一页继续编辑。")])
    file3 = FileField(label='Related file 3',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png','txt','TXT','pdf','PDF','xls','XLS','xlsx','XLSX','ppt','PPT','pptx','PPTX','doc','DOC','docx','DOCX', 'zip', 'ZIP', 'rar', 'RAR'],message="可以上传txt\pdf\word\excel\ppt\zip\rar或图片，如果上传失败可能是因为文件太大或类型不对，请返回上一页继续编辑。")])
    file4 = FileField(label='Related file 4',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png','txt','TXT','pdf','PDF','xls','XLS','xlsx','XLSX','ppt','PPT','pptx','PPTX','doc','DOC','docx','DOCX', 'zip', 'ZIP', 'rar', 'RAR'],message="可以上传txt\pdf\word\excel\ppt\zip\rar或图片，如果上传失败可能是因为文件太大或类型不对，请返回上一页继续编辑。")])
    file5 = FileField(label='Related file 5',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png','txt','TXT','pdf','PDF','xls','XLS','xlsx','XLSX','ppt','PPT','pptx','PPTX','doc','DOC','docx','DOCX', 'zip', 'ZIP', 'rar', 'RAR'],message="可以上传txt\pdf\word\excel\ppt\zip\rar或图片，如果上传失败可能是因为文件太大或类型不对，请返回上一页继续编辑。")])
    file6 = FileField(label='Related file 6',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png','txt','TXT','pdf','PDF','xls','XLS','xlsx','XLSX','ppt','PPT','pptx','PPTX','doc','DOC','docx','DOCX', 'zip', 'ZIP', 'rar', 'RAR'],message="可以上传txt\pdf\word\excel\ppt\zip\rar或图片，如果上传失败可能是因为文件太大或类型不对，请返回上一页继续编辑。")])
    file7 = FileField(label='Related file 7',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png','txt','TXT','pdf','PDF','xls','XLS','xlsx','XLSX','ppt','PPT','pptx','PPTX','doc','DOC','docx','DOCX', 'zip', 'ZIP', 'rar', 'RAR'],message="可以上传txt\pdf\word\excel\ppt\zip\rar或图片，如果上传失败可能是因为文件太大或类型不对，请返回上一页继续编辑。")])
    file8 = FileField(label='Related file 8',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png','txt','TXT','pdf','PDF','xls','XLS','xlsx','XLSX','ppt','PPT','pptx','PPTX','doc','DOC','docx','DOCX', 'zip', 'ZIP', 'rar', 'RAR'],message="可以上传txt\pdf\word\excel\ppt\zip\rar或图片，如果上传失败可能是因为文件太大或类型不对，请返回上一页继续编辑。")])
    submit = SubmitField('Submit')


class NewLessonForm(FlaskForm):
    year = SelectField('学年',choices=[('2022','2022'),('2023','2023'),('2024','2024'),('2025','2025'),('2026','2026')],validators=[Required()])
    season = SelectField('学期',choices=[('春','春'), ('夏','夏'), ('秋','秋'), ('冬','冬')],validators=[Required()])
    room_row = IntegerField('教室座位行数')
    room_column = IntegerField('教室座位列数')
    about = StringField("简短说明",validators=[Required(),Length(0, 64)])
    availability = SelectField('课程可用性',choices=[('open_selection','开放选课'),('close_selection','关闭选课'),('close_update','关闭上传作业')],validators=[Required()])
    submit = SubmitField('提交')

class NewLessonFormE(FlaskForm):
    year = SelectField('Year',choices=[('2022','2022'),('2023','2023'),('2024','2024'),('2025','2025'),('2026','2026')],validators=[Required()])
    season = SelectField('Season',choices=[('春','Spring'), ('夏','Summer'), ('秋','Autumn'), ('冬','Winter')],validators=[Required()])
    room_row = IntegerField('Rows of the classroom')
    room_column = IntegerField('Columns of the classroom')
    about = StringField("About the class",validators=[Required(),Length(0, 64)])
    availability = SelectField('课程可用性',choices=[('open_selection','Open for Slection'),('close_selection','Close for Selection'),('close_update','Close for update homeowrk')],validators=[Required()])
    submit = SubmitField('提交')    

class UpdateTopicForm(FlaskForm):
    topic = StringField("选题",validators=[Required(),Length(0, 64)])
    body = PageDownField("简短说明",validators=[Required()])

    file1 = FileField(label='汇报幻灯片',validators=[
        FileAllowed(['ppt','PPT','pptx','PPTX','pdf','PDF','key','KEY'],message='可以上传ppt/pptx/pdf/key，上传失败请点浏览器上一页继续编辑。')])            
    file2 = FileField(label='期末论文',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png','txt','TXT','pdf','PDF','xls','XLS','xlsx','XLSX','ppt','PPT','pptx','PPTX','doc','DOC','docx','DOCX', 'zip', 'ZIP', 'rar', 'RAR','key','KEY'],message='可以上传txt\pdf\word\excel\ppt\zip\rar\key或图片，上传失败请点浏览器上一页继续编辑。')])
    file3 = FileField(label='相关资料1',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png','txt','TXT','pdf','PDF','xls','XLS','xlsx','XLSX','ppt','PPT','pptx','PPTX','doc','DOC','docx','DOCX', 'zip', 'ZIP', 'rar', 'RAR','key','KEY'],message='可以上传txt\pdf\word\excel\ppt\zip\rar\key或图片，上传失败请点浏览器上一页继续编辑。')])
    file4 = FileField(label='相关资料2',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png','txt','TXT','pdf','PDF','xls','XLS','xlsx','XLSX','ppt','PPT','pptx','PPTX','doc','DOC','docx','DOCX', 'zip', 'ZIP', 'rar', 'RAR','key','KEY'],message='可以上传txt\pdf\word\excel\ppt\zip\rar\key或图片，上传失败请点浏览器上一页继续编辑。')])
    file5 = FileField(label='相关资料3',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png','txt','TXT','pdf','PDF','xls','XLS','xlsx','XLSX','ppt','PPT','pptx','PPTX','doc','DOC','docx','DOCX', 'zip', 'ZIP', 'rar', 'RAR','key','KEY'],message='可以上传txt\pdf\word\excel\ppt\zip\rar\key或图片，上传失败请点浏览器上一页继续编辑。')])
    submit = SubmitField('提交')
    
    
class UpdateTopicFormE(FlaskForm):
    topic = StringField("Topic",validators=[Required(),Length(0, 64)])
    body = PageDownField("Remark",validators=[Required()])

    file1 = FileField(label='PPT',validators=[
        FileAllowed(['ppt','PPT','pptx','PPTX','pdf','PDF','key','KEY'],message='可以上传ppt/pptx/pdf/key')])            
    file2 = FileField(label='Paper',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png','txt','TXT','pdf','PDF','xls','XLS','xlsx','XLSX','ppt','PPT','pptx','PPTX','doc','DOC','docx','DOCX', 'zip', 'ZIP', 'rar', 'RAR','key','KEY'],message='可以上传txt\pdf\word\excel\ppt\zip\rar\key或图片')])
    file3 = FileField(label='Related file 1',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png','txt','TXT','pdf','PDF','xls','XLS','xlsx','XLSX','ppt','PPT','pptx','PPTX','doc','DOC','docx','DOCX', 'zip', 'ZIP', 'rar', 'RAR','key','KEY'],message='可以上传txt\pdf\word\excel\ppt\zip\rar\key或图片')])
    file4 = FileField(label='Related file 2',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png','txt','TXT','pdf','PDF','xls','XLS','xlsx','XLSX','ppt','PPT','pptx','PPTX','doc','DOC','docx','DOCX', 'zip', 'ZIP', 'rar', 'RAR','key','KEY'],message='可以上传txt\pdf\word\excel\ppt\zip\rar\key或图片')])
    file5 = FileField(label='Related file 3',validators=[
        FileAllowed(['bmp','BMP','jif','JIF','JPG','jpg','JPEG','jpeg','PNG','png','txt','TXT','pdf','PDF','xls','XLS','xlsx','XLSX','ppt','PPT','pptx','PPTX','doc','DOC','docx','DOCX', 'zip', 'ZIP', 'rar', 'RAR','key','KEY'],message='可以上传txt\pdf\word\excel\ppt\zip\rar\key或图片')])
    submit = SubmitField('Submit')    

class LessonFileForm(FlaskForm):
    filetype = SelectField('文件类型',choices=[('document','文档'),('audio','音频'),('video','视频'),('picture','图片')],validators=[Required()])
    visibility = SelectField('可见范围',choices=[('public','全网公开'),('student','选修学生可见'),('private','个人')],validators=[Required()])
    file = FileField(label='上传文件')               
    about = StringField("简短描述",validators=[Length(0, 128)])   
    submit = SubmitField('提交')

class LessonFileFormE(FlaskForm):
    filetype = SelectField('Type of the file',choices=[('document','Ducument'),('audio','Audio'),('video','Video'),('picture','Picture')],validators=[Required()])
    visibility = SelectField('Who can see',choices=[('public','Public'),('student','All student'),('private','Private')],validators=[Required()])
    file = FileField(label='Update a file')            
    about = StringField("Brief description",validators=[Length(0, 128)])
    submit = SubmitField('Submit')

class CriticismForm(FlaskForm):
    score = IntegerField("得分",validators=[Required()])
    criticism = TextAreaField("评语",validators=[Required(),Length(0, 1024)])
    submit = SubmitField('提交')


class CriticismFormE(FlaskForm):
    score = IntegerField("Score",validators=[Required()])
    criticism = TextAreaField("Criticism",validators=[Required(),Length(0, 1024)])
    submit = SubmitField('Submit')

class SearchForm(FlaskForm):
    search = StringField('', validators=[Required(), Length(1, 256)])
    submit = SubmitField('      搜    索     ')

class SearchFormE(FlaskForm):
    search = StringField('', validators=[Required(), Length(1, 256)])
    submit = SubmitField('  Search  ')
    
class CheckForm(FlaskForm):
    konghus = StringField("空户")
    body = StringField("接龙内容")
    submit = SubmitField('提交')

class UrlForm(FlaskForm):
    search = StringField('', validators=[Required(), Length(1, 256)])
    submit = SubmitField('      去到网址或谷歌搜索     ')

class UrlFormE(FlaskForm):
    search = StringField('', validators=[Required(), Length(1, 256)])
    submit = SubmitField('  Go to Website or Google Search  ')
    
class GoogleForm(FlaskForm):
    search = StringField('', validators=[Required(), Length(1, 256)])
    submit = SubmitField('      谷歌搜索     ')

class GoogleFormE(FlaskForm):
    search = StringField('', validators=[Required(), Length(1, 256)])
    submit = SubmitField('  Google  ')
