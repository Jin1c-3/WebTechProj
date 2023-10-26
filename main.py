from flask import Flask, render_template, request, url_for, redirect, session

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
    if 1 == 1:
        if dbf.validate_username_password(
                request.form["username"], request.form["password"]
        ):
            session["userid"] = request.form["username"]
            return redirect(url_for("index"))
        else:
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
    fields=fields[:len(fields)-1]
    fields.append("专业")
    return render_template("show1.html", datas=result, fields=fields)


@app.route("/add", methods=["GET", "post"])
def add():
    if not CheckLogin():
        return redirect(url_for("login"))

    if request.method == "GET":
        datas = dbf.do("select * from stu_profession")
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
        dbf.insert(data, "student_info")
        return redirect(url_for("index"))


@app.route("/del", methods=["GET"])
def delete():
    if not CheckLogin():
        return redirect(url_for("login"))
    id = request.args["stuid"]
    dbf.delete_by_id("stu_id", id, "student_info")
    return redirect(url_for("index"))


@app.route("/del2/<id>", methods=["GET"])
def delete2(id):
    if not CheckLogin():
        return redirect(url_for("login"))
    dbf.delete_by_id("stu_id", id, "student_info")
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

        return redirect(url_for("index"))


if __name__ == "__main__":
    # app.run("0.0.0.0",debug=True)
    app.run(debug=True)
    # app.run()
