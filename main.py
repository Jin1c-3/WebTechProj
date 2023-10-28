import json
import logging
import math
import re

from flask import Flask, flash, render_template, request, redirect, session

from DBFactory import *

app = Flask(__name__)

# 设置日志格式
formatter = logging.Formatter(
    "[%(levelname)s][%(asctime)s] %(filename)s-%(funcName)s:%(lineno)d - %(message)s"
)

# 设置日志处理器为流处理器,并指定格式化器
file_handler = logging.StreamHandler()
file_handler.setFormatter(formatter)

# 获取日志记录器,并添加处理器
log = logging.getLogger(__name__)
log.addHandler(file_handler)

# 设置日志级别
log.setLevel(logging.DEBUG)

app.secret_key = "abcdefgh!@#$%"
dbf = DBFactory()

stu_table_fieldname = [
    "stu_id",
    "stu_name",
    "stu_sex",
    "stu_age",
    "stu_origin",
    "stu_profession",
]


def validate_login():
    return "userid" in session


def dict_str(dict):
    return "{" + ", ".join(f"{k}={dict[k]}" for k in dict) + "}"


@app.get("/login")
def login_get():
    return render_template("login.html")


@app.post("/login")
def login():
    username = request.form["username"]
    password = request.form["password"]
    log.debug("request.form: %s", dict_str(request.form))
    if dbf.validate_username_password(username, password):
        session["userid"] = username
        flash("登录成功", category="success")
        return redirect("/")
    log.info("登录失败，开始自动注册")
    if len(dbf.do("select * from users where username=?", username)) > 0:
        flash("密码错误", category="danger")
        return render_template("login.html")
    dbf.register(username, password)
    flash("注册成功！请再次输入密码后点击登录", category="success")
    return render_template("login.html", username=username)


@app.get("/")
def index():
    """
    page_size      每一页最多多少内容
    current_page   当前页码
    total_size     总共多少条数据，用于页面计算有几页
    stu_id
    stu_name
    stu_sex
    stu_age
    stu_origin
    stu_profession
    """
    if not validate_login():
        flash("请先登录", category="danger")
        return render_template("login.html")
    tablename = "student_info"
    where_str = []
    sql = (
        "SELECT s.stu_id,s.stu_name,s.stu_sex,s.stu_age,s.stu_origin,p.stu_profession FROM student_info s INNER JOIN stu_profession p "
        "on s.stu_profession_id=p.stu_profession_id"
    )
    log.debug("request.args: %s", dict_str(request.args))
    # 默认值
    page_size = 10
    current_page = 1
    if "page_size" in request.args and not (
        request.args["page_size"] == ""
        or request.args["page_size"] is None
        or request.args["page_size"] == " "
    ):
        page_size = request.args["page_size"]
        page_size = int(page_size)
        log.debug(f"page_size被改为非默认值 {page_size}")
    if "current_page" in request.args and not (
        request.args["current_page"] == ""
        or request.args["current_page"] is None
        or request.args["current_page"] == " "
    ):
        current_page = request.args["current_page"]
        current_page = int(current_page)
        log.debug(f"current_page被改为非默认值 {current_page}")
    for key in request.args:
        if (
            key in stu_table_fieldname
            and request.args[key] != None
            and request.args[key] != ""
        ):
            where_str.append(f"{key} like '%{request.args[key]}%'")
    if len(where_str) > 0:
        sql = sql + " where " + " and ".join(where_str)
    log.debug(f"将要执行sql: {sql}")
    result = dbf.do(sql)
    total_size = len(result)
    if total_size > page_size:
        result = result[(current_page - 1) * page_size : current_page * page_size]
    fields = dbf.get_fields(tablename)
    fields = fields[: len(fields) - 1]
    fields.append("专业")
    return render_template(
        "show1.html",
        datas=result,
        fields=fields,
        total_page=math.ceil(total_size / page_size),
        page_size=page_size,
        current_page=current_page,
        stu_name=request.args.get("stu_name", ""),
        stu_id=request.args.get("stu_id", ""),
        all_radios_value=request.args.get("all-radios-value", ""),
    )


@app.route("/add", methods=["GET", "post"])
def add():
    if not validate_login():
        flash("请先登录", category="danger")
        return redirect("login")
    if request.method == "GET":
        datas = dbf.all("stu_profession")
        return render_template("add.html", datas=datas)
    log.debug("request.form: %s", dict_str(request.form))
    data = dict(
        stu_id=request.form["stu_id"],
        stu_name=request.form["stu_name"],
        stu_sex=request.form["stu_sex"],
        stu_age=request.form["stu_age"],
        stu_origin=request.form["stu_origin"],
        stu_profession_id=request.form["stu_profession"],
    )
    if len(dbf.do("select * from student_info where stu_id='%s'" % data["stu_id"])) > 0:
        flash("添加失败！学号已存在", category="danger")
        return redirect("/")
    dbf.insert(data, "student_info")
    flash("添加成功！", category="success")
    return redirect("/")


@app.get("/multidel")
def multidel():
    if not validate_login():
        flash("请先登录", category="danger")
        return redirect("login")
    log.debug("request.args: %s", dict_str(request.args))
    ids = json.loads(request.args["all-radios-value"])
    try:
        for id in ids:
            dbf.delete_by_id("stu_id", id, "student_info")
        log.debug("id将被删除: %s", " ; ".join(id for id in ids))
        flash("删除成功！", category="success")
        return redirect("/")
    except:
        flash("删除失败！", category="danger")
        return redirect("/")


@app.route("/del2/<id>", methods=["GET"])
def delete_by_id(id):
    if not validate_login():
        flash("请先登录", category="danger")
        return redirect("login")
    log.debug("request.args: %s", dict_str(request.args))
    try:
        dbf.delete_by_id("stu_id", id, "student_info")
        log.debug("id将被删除: %s", id)
        flash("删除成功！", category="success")
        return redirect("/")
    except:
        flash("删除失败！", category="danger")
        return redirect("/")


@app.route("/update", methods=["GET", "post"])
def upadte():
    if not validate_login():
        flash("请先登录", category="danger")
        return redirect("login")
    if request.method == "GET":
        id = request.args["id"]
        result = dbf.do(f"select * from student_info where stu_id={id}")
        datas = dbf.all("stu_profession")
        return render_template("update.html", data=result[0], datas=datas)
    log.debug("request.form: %s", dict_str(request.form))
    data = dict(
        stu_id=request.form["stu_id"],
        stu_name=request.form["stu_name"],
        stu_sex=request.form["stu_sex"],
        stu_age=request.form["stu_age"],
        stu_origin=request.form["stu_origin"],
        stu_profession_id=request.form["stu_profession"],
    )
    dbf.update(data, "student_info")
    flash("修改成功！", category="success")
    return redirect("/")


@app.get("/multupdate")
def multiupdate():
    if not validate_login():
        flash("请先登录", category="danger")
        return redirect("login")
    log.debug("request.args: %s", dict_str(request.args))
    students = json.loads(request.args["all-updates-data"])
    for s in students:
        stu_dict = {
            "stu_id": s[0],
            "stu_name": s[1],
            "stu_sex": s[2],
            "stu_age": s[3],
            "stu_origin": s[4],
            "stu_profession_id": 0,
        }
        # 检查名字是否合法
        if not re.match(r"^[\u4e00-\u9fa5]{2,4}$", stu_dict["stu_name"]):
            flash("修改失败！名字不合法", category="danger")
            return redirect("/")
        # 检查性别是否合法
        if stu_dict['stu_sex'] not in ['男','女']:
            flash("修改失败！性别不合法", category="danger")
            return redirect("/")
        # 检查年龄是否合法
        if not re.match(r"^[0-9]{1,2}$", stu_dict["stu_age"]):
            flash("修改失败！年龄不合法", category="danger")
            return redirect("/")
        # 检查籍贯是否合法
        if not re.match(r"^[\u4e00-\u9fa5]{2,4}$", stu_dict["stu_origin"]):
            flash("修改失败！籍贯不合法", category="danger")
            return redirect("/")
        # 检查专业是否合法
        stu_profession = s[5]
        for profession in dbf.all("stu_profession"):
            if stu_profession == profession[1]:
                stu_dict["stu_profession_id"] = profession[0]
                break
        if stu_dict["stu_profession_id"] == 0:
            flash("修改失败！专业不存在", category="danger")
            return redirect("/")
        dbf.update(stu_dict, "student_info")
    flash("修改成功！", category="success")
    return redirect("/")


if __name__ == "__main__":
    app.debug = True
    app.run()
