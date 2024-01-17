from collections.abc import Mapping, Sequence
from typing import Any
from flask import Flask, request, render_template, redirect, url_for, session
from flask_login import LoginManager, login_required, UserMixin, login_user, logout_user
from flask_wtf import FlaskForm
from wtforms.validators import ValidationError
from wtforms import StringField, IntegerField, SubmitField, PasswordField
from functions_Mysql import Functions_MySQL
from get_UsersData import Get_UsersData
from datetime import timedelta
from dotenv import load_dotenv
import os
import secrets


# self.user_id = FM.read_query(connection, "SELECT user_id FROM normal_users;")
# self.user_name = FM.read_query(connection, "SELECT user_name FROM normal_users;")
# self.user_pass = FM.read_query(connection, "SELECT user_pass FROM normal_users;")
# self.user_age = FM.read_query(connection, "SELECT user_age FROM normal_users;")


#初期化
app = Flask(__name__)
app.permanent_session_lifetime = timedelta(minutes=30) #セッションタイムアウトについて
login_manager = LoginManager()
login_manager.init_app(app)
app.config["SECRET_KEY"] = secrets.token_hex() #cookieで使用

#MySQLに接続するためのパスワードを環境変数として.envに保存して使用する．
load_dotenv()
PASS = os.getenv("MYSQL_PASS") 
FM = Functions_MySQL()
connection_users = FM.create_db_connection("localhost", "root", PASS, "users")
connection_research = FM.create_db_connection("localhost", "root", PASS, "prior_research")

#Controller(最終的にはモジュール分ける)
class User(UserMixin):
  def __init__(self,user_id):
    self.id = user_id

class LoginForm(FlaskForm):
    user_name = StringField("Name")
    user_pass = PasswordField("Password")
    submit = SubmitField("Login")

    def validate_user_name(self, user_name): #ユーザーネームの存在確認
        users = Get_UsersData().get_data() #usersにDBにあるnameとpassを保存
        if user_name.data not in users:
            print(users)
            raise ValidationError("Not Exist This Name.")
    
    def validate_user_pass(self, user_pass): #パスワードがあっているかの確認
        users = Get_UsersData().get_data()
        if self.user_name.data in users and user_pass.data != users[self.user_name.data]:
            raise ValidationError("Invalid Password.")

class RegisterForm(FlaskForm):
    user_name = StringField("Name")
    user_pass = PasswordField("Password")
    user_age = IntegerField("Age")
    submit = SubmitField("Register")

    def validate_user_name(self, user_name): #ユーザーネームが使われているかの確認, 長さ確認
        users = Get_UsersData().get_data()
        if user_name.data in users:
            raise ValidationError("This name has been used.")
        if len(user_name.data) >= 40:
            raise ValidationError("Please enter your name less than 40 characters.") 
        
    def validate_user_pass(self, user_pass): #パスワードの長さ確認
        if len(user_pass.data) >= 40:
            raise ValidationError("Please enter the password less than 40 characters.")

class SearchForm(FlaskForm):
    query = StringField("Query")
    submit = SubmitField("Search")

    def validate_query(self, query):
        if query == None:
            raise ValidationError("query is none")

class AddForm(FlaskForm):
    title = StringField("Title")
    author = StringField("Author")
    conference = StringField("Conference")
    date = StringField("Date")
    submit = SubmitField("Add")

    def validate_title(self, title):
        if title == None:
            raise ValidationError("")
        elif len(title.data) == 0 or len(title.data) > 100:
            raise ValidationError("title length : 0 < title < 100")

    def validate_author(self, author):
        if author == None:
            raise ValidationError("")
        elif len(author.data) == 0 or len(author.data) > 100:
            raise ValidationError("author length : 0 < title < 100")
        
    def validate_conference(self, conference):
        if conference == None:
            raise ValidationError("")
        elif len(conference.data) == 0 or len(conference.data) > 100:
            raise ValidationError("title length : 0 < title < 100")
        
    def validate_date(self, date):
        if date == None:
            raise ValidationError("")
        elif len(date.data) == 0 or len(date.data) > 4:
            raise ValidationError("date length : 0 < title < 100")


#実際の処理(Model)
@login_manager.user_loader
def load_user(user_id):
  return User(user_id)


@app.route("/")
def main_page():
    return render_template("main_page.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    users = Get_UsersData().get_data()
    if form.validate_on_submit(): #制約に引っかからなかったとき
        if form.user_name.data in users and form.user_pass.data == users[form.user_name.data]:
            user = User(form.user_name.data)
            login_user(user)
            return redirect(url_for("mypage", user=form.user_name.data))
        else:
            print("error")
    return render_template("login.html", form = form)


@app.route("/mypage/<user>", methods=["GET", "POST"])
@login_required
def mypage(user):
    sform = SearchForm()
    aform = AddForm()
    change_q=f"""
            SELECT *
            FROM {user};
            """

    if sform.query.data != None:
        change_q=f"""
            SELECT *
            FROM {user}
            WHERE PR_title LIKE "%{sform.query.data}%";
            """

    if aform.title.data != None and aform.author.data != None and aform.conference.data != None and aform.date.data != None:
        if aform.validate_on_submit():
            #データをリスト化
            alist = []
            alist.append((aform.title.data, aform.author.data, aform.conference.data, aform.date.data))

            #リスト化したデータをDBに追加
            add_q = f'''
            INSERT INTO {user} (PR_title, PR_author, PR_conference, PR_date) 
            VALUES (%s, %s, %s, %s)
            '''
            FM.execute_list_query(connection_research, add_q, alist)
            print("redirect")
            return redirect(url_for("mypage", user=user))

    return render_template("mypage.html", sform=sform, aform=aform, user=user, data=FM.read_query(connection_research, change_q))
    

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit(): #制約に引っかからなかったとき
        userList = [(form.user_name.data, form.user_pass.data, form.user_age.data)]
        insert_q = f'''
        INSERT INTO normal_users (user_name, user_pass, user_age) 
        VALUES (%s, %s, %s)
        '''
        create_q = f'''
        CREATE TABLE {form.user_name.data} (
        research_id INT AUTO_INCREMENT,
        PR_title VARCHAR(100) NOT NULL,
        PR_author VARCHAR(100) NOT NULL,
        PR_conference VARCHAR(100) NOT NULL,
        PR_date VARCHAR(4),
        PRIMARY KEY (research_id)
        );
        '''
        #ユーザーをuserに追加
        FM.execute_list_query(connection_users, insert_q, userList)
        #ユーザー名のテーブルを別のdbに作成
        FM.execute_query(connection_research, create_q)
        return redirect("/")
    return render_template("register.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")

if __name__ == "__main__":
    app.run(port=12345, debug=False)