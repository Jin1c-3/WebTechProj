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
    username=request.form["username"]
    password=request.form["password"]
    if(len(dbf.do('select * from users where username=?',username))>0):
        flash("用户名已存在", category="danger")
        return render_template("login.html")
    dbf.register(username,password)
    flash("注册成功！请点击登录", category="success")
    return render_template("login.html")
    # flash("登陆失败！请检查用户名和密码", category="danger")
    # return render_template("login.html")
    
@app.post("/register")
def register():
    username=request.form["username"]
    password=request.form["password"]
    if(len(dbf.do('select * from users where username=?',username))>0):
        flash("注册失败！用户名已存在", category="danger")
        return render_template("login.html")
    dbf.register(username,password)
    flash("注册成功！请点击登录", category="success")
    return render_template("login.html")

@app.route("/", methods=["GET"])
def index():
    if not CheckLogin():
        return redirect(url_for("login"))
    tablename = "student_info"
    sql = (
        "SELECT s.stu_id,s.stu_name,s.stu_sex,s.stu_age,s.stu_origin,p.stu_profession FROM student_info s INNER JOIN stu_profession p "
        "on s.stu_profession_id=p.stu_profession_id"
    )
    strWhere = []
    if "name" in request.args:
        name = request.args["name"]
        if name != "":
            strWhere.append("stu_name like '%%%s%%'" % name)
    if "stuno" in request.args:
        stuno = request.args["stuno"]
        if stuno != "":
            strWhere.append("stu_id = '%s'" % stuno)
    if len(strWhere) > 0:
        sql = sql + " where " + " and ".join(strWhere)
        print(sql)
    result = dbf.do(sql)
    # result=result[:len(result)-2]
    fields = dbf.get_fields(tablename)
    fields = fields[: len(fields) - 1]
    fields.append("专业")
    return render_template("show1.html", datas=result, fields=fields)


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
