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
            return redirect("/mypage")
        else:
            print("error")
    return render_template("login.html", form = form)

    # 一応残してある
    # if request.method == "POST":
    #     print(request.form["user_name"])
    #     print(request.form["Name"])
    #     username = request.form["username"]
    #     userpass = request.form["userpass"]

    #     if username in users and users[username] == userpass:
    #         session["username"] = username
    #         return redirect(url_for("logined"))
    #     else:
    #         return render_template("main_page.html", error="Invalid credentials")
        
    # return render_template("main_page.html")

@app.route("/mypage")
@login_required
def logined():
    return render_template("mypage.html")
    
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

    # #処理を見るためにいったん残しておく
    # userList = [request.form["username"], request.form["userpass"], request.form["userage"]]

    # #MySQLに接続するためのパスワードを環境変数として.envに保存して使用する．
    # load_dotenv()
    # PASS = os.getenv("MYSQL_PASS") 

    # #MySQLへのコネクションの確立．
    # FM = Functions_MySQL()
    # connection = FM.create_db_connection("localhost", "root", PASS, "users")

    # q1 = f'''
    #     INSERT INTO normal_users (user_name, user_pass, user_age) 
    #     VALUES (%s, %s, %s)
    #     '''
    # #ユーザデータの追加
    # FM.execute_list_query(connection, q1, userList)

    # return render_template("main_page.html")


if __name__ == "__main__":
    app.run(port=12345, debug=False)