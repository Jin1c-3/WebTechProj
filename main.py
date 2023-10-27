import math

from flask import Flask, flash, render_template, request, url_for, redirect, session

from DBFactory import *

app = Flask(__name__)
app.secret_key = "abcdefgh!@#$%"
dbf = DBFactory()


def CheckLogin():
    if "userid" not in session:
        return False
    else:
        return True


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if dbf.validate_username_password(
            request.form["username"], request.form["password"]
    ):
        session["userid"] = request.form["username"]
        flash("登录成功", category="success")
        return redirect(url_for("index"))
    # 开始注册
    username = request.form["username"]
    password = request.form["password"]
    if len(dbf.do("select * from users where username=?", username)) > 0:
        flash("用户名已存在", category="danger")
        return render_template("login.html")
    dbf.register(username, password)
    flash("注册成功！请点击登录", category="success")
    return render_template("login.html", username=username)
    # flash("登陆失败！请检查用户名和密码", category="danger")
    # return render_template("login.html")


# @app.post("/register")
# def register():
#     username=request.form["username"]
#     password=request.form["password"]
#     if(len(dbf.do('select * from users where username=?',username))>0):
#         flash("注册失败！用户名已存在", category="danger")
#         return render_template("login.html")
#     dbf.register(username,password)
#     flash("注册成功！请点击登录", category="success")
#     return render_template("login.html")


@app.get("/")
def index():
    """
    # order_flag     1的时候表示正在排序。下面的值1表示正排，-1表示负排
    # search_flag    1的时候表示搜索。
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

    if not CheckLogin():
        return redirect(url_for("login"))

    tablename = "student_info"
    where_str = []
    # order_str = []
    sql = (
        "SELECT s.stu_id,s.stu_name,s.stu_sex,s.stu_age,s.stu_origin,p.stu_profession FROM student_info s INNER JOIN stu_profession p "
        "on s.stu_profession_id=p.stu_profession_id"
    )
    for key in request.args:
        print(key, request.args[key])
    for key in request.form:
        print(key, request.form[key])
    # 默认值
    page_size = 10
    current_page = 1
    if "page_size" in request.args:
        if not (request.args["page_size"] == "" or request.args["page_size"] is None or request.args[
            "page_size"] == " "):
            page_size = request.args["page_size"]
            page_size = int(page_size)
            print(f'page_size真实值{page_size}')
    if "current_page" in request.args:
        if not (request.args["current_page"] == "" or request.args["current_page"] is None or request.args[
            "current_page"] == " "):
            current_page = request.args["current_page"]
            print(f'-----current_page {current_page}')
            current_page = int(current_page)

    # print(f'current_page{current_page}')
    # if "order_flag" in request.args:
    #     order_flag = request.args["order_flag"]
    #     if order_flag == "1" or order_flag == 1 or order_flag == True:
    #         for key in request.args:
    #             # 跳过搜索flag
    #             if key == "search_flag":
    #                 continue
    #             if request.args[key] == 1 or request.args[key] == "1":
    #                 order_str.append(f"{key} asc")
    #                 continue
    #             if request.args[key] == -1 or request.args[key] == "-1":
    #                 order_str.append(f"{key} desc")
    #                 continue

    # if "search_flag" in request.args:
    #     search_flag = request.args["search_flag"]
    #     if search_flag == "1" or search_flag == 1 or search_flag == True:
    #         for key in request.args:
    #             # 跳过排序flag
    #             if key == "order_flag":
    #                 continue
    #             if request.args[key] != None and request.args[key] != "":
    #                 where_str.append(f"{key} like %{request.args[key]}%")
    #                 continue
    for key in request.args:
        if key == 'page_size' or key == 'current_page':
            continue
        if request.args[key] != None and request.args[key] != "":
            where_str.append(f"{key} like '%{request.args[key]}%'")

    # if "name" in request.args:
    #     name = request.args["name"]
    #     if name != "":
    #         where_str.append("stu_name like '%%%s%%'" % name)
    # if "stuno" in request.args:
    #     stuno = request.args["stuno"]
    #     if stuno != "":
    #         where_str.append("stu_id = '%s'" % stuno)
    if len(where_str) > 0:
        sql = sql + " where " + " and ".join(where_str)
        # print(sql)
    # if len(order_str) > 0:
    #     sql = sql + " order by " + ",".join(order_str)
    #     print(sql)
    result = dbf.do(sql)
    total_size = len(result)
    # print(f'current_page{current_page}类型{type(current_page)}')
    current_page = int(current_page)
    if total_size > page_size:
        print(f'(current_page - 1) * page_size{(current_page - 1) * page_size}')
        print(f'current_page * page_size{current_page * page_size}')
        result = result[(current_page - 1) * page_size: current_page * page_size]

    print(f'page_size {page_size}')
    print(f'current_page {current_page}')

    for r in result[(current_page - 1) * page_size: current_page * page_size]:
        print(r)

    fields = dbf.get_fields(tablename)
    fields = fields[: len(fields) - 1]
    fields.append("专业")
    # if total_size % page_size:
    #     total_page = total_size / page_size + 1
    # else:
    #     total_page = total_size / page_size
    return render_template(
        "show1.html", datas=result, fields=fields, total_page=math.ceil(total_size / page_size), page_size=page_size,
        current_page=current_page
    )


@app.route("/add", methods=["GET", "post"])
def add():
    if not CheckLogin():
        return redirect(url_for("login"))

    if request.method == "GET":
        datas = dbf.all("stu_profession")
        return render_template("add.html", datas=datas)

    else:
        data = dict(
            stu_id=request.form["stu_id"],
            stu_name=request.form["stu_name"],
            stu_sex=request.form["stu_sex"],
            stu_age=request.form["stu_age"],
            stu_origin=request.form["stu_origin"],
            stu_profession_id=request.form["stu_profession"],
        )
        if (
                len(dbf.do("select * from student_info where stu_id='%s'" % data["stu_id"]))
                > 0
        ):
            flash("添加失败！学号已存在", category="danger")
            return redirect(url_for("add"))
        dbf.insert(data, "student_info")
        flash("添加成功！", category="success")
        return redirect(url_for("index"))


@app.post("/multidel")
def multidel():
    if not CheckLogin():
        return redirect(url_for("login"))
    ids = request.form.getlist("ids")
    print(ids)
    try:
        for id in ids:
            dbf.delete_by_id("stu_id", id, "student_info")
        flash("删除成功！", category="success")
        return redirect(url_for("index"))
    except:
        flash("删除失败！", category="danger")
        return redirect(url_for("index"))


@app.route("/del", methods=["GET"])
def delete():
    if not CheckLogin():
        return redirect(url_for("login"))
    id = request.args["stuid"]
    try:
        dbf.delete_by_id("stu_id", id, "student_info")
        flash("删除成功！", category="success")
        return redirect(url_for("index"))
    except:
        flash("删除失败！", category="danger")
        return redirect(url_for("index"))


@app.route("/del2/<id>", methods=["GET"])
def delete2(id):
    if not CheckLogin():
        return redirect(url_for("login"))
    try:
        dbf.delete_by_id("stu_id", id, "student_info")
        flash("删除成功！", category="success")
        return redirect(url_for("index"))
    except:
        flash("删除失败！", category="danger")
        return redirect(url_for("index"))


@app.route("/update", methods=["GET", "post"])
def upadte():
    if not CheckLogin():
        return redirect(url_for("login"))

    if request.method == "GET":
        id = request.args["id"]
        result = dbf.do("select * from student_info where stu_id='%s'" % id)
        # result, _ = GetSql2("SELECT s.*,  p.stu_profession FROM student_info s INNER JOIN stu_profession p " \
        #                     "on s.stu_profession_id=p.stu_profession_id where stu_id='%s'" % id)
        print(result[0])
        print(type(result[0]))
        datas = dbf.all("stu_profession")
        # for p in pro:
        #     print(p)+
        return render_template("update.html", data=result[0], datas=datas)
    else:
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
        return redirect(url_for("index"))


if __name__ == "__main__":
    # app.run("0.0.0.0",debug=True)
    app.run(debug=True)
    # app.run()
