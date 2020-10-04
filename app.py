from flask import Flask, jsonify, session, request, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from bson.objectid import ObjectId
import static.forms as forms
import static.validations as val
import static.json as json_handler
import static.CaptureOrder
import pymongo
import time
import secrets
import hashlib
import requests
import json
import os

mb_user = "Vinicius"
pwd = "sYlrvbXJUtKyvwBZ"

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config["SECRET_KEY"] = "STRINGHARDTOGUESS"

client = pymongo.MongoClient("mongodb+srv://"+mb_user+":"+pwd+"@recdb.smlnb.mongodb.net/RecDB?retryWrites=true&w=majority")
db = client.RecDB

@app.route('/',methods=["GET","POST"])
def index():
	form = forms.userLogin()
	if form.validate_on_submit():
		email = form.email.data
		data = db["Users"].find_one({"user_email":email})
		userdata = User(username=data["name"],email=data["user_email"])
		client.close()
		return str(userdata.username)
	return render_template("base.html",form=form, name=session.get("name"),user=session.get("user"))
		
@app.route('/user',methods=["GET","POST"])
def user():
	form = forms.userSignUp()
	form2 = forms.userLogin()
	
	return render_template("index.html",form=form,form2=form2,signUp = "userSignUp", signIn = "userSignIn", name=session.get("name"),user=session.get("user"))

@app.route('/userSignUp', methods=["GET","POST"])
def userSignUp():
	form = forms.userSignUp()
	form2 = forms.userLogin()

	name = request.form["name"]
	email = request.form["email"]
	pswd = hashlib.sha256(request.form["pswd"].encode()).hexdigest()

	query = db["Users"].find_one({"user_email":email})
	if(query):
		flash(str(query["_id"]))
	else:
		db["Users"].insert_one({"name":name,"user_email":email,"user_pswd":pswd})
		flash("Registered sucessfully!")

	return render_template("index.html",form=form,form2=form2,signUp = "userSignUp", signIn = "userSignIn", name=session.get("name"),user=session.get("user"))

@app.route('/userSignIn', methods=["GET","POST"])
def userSignIn():
	form = forms.userSignUp()
	form2 = forms.userLogin()

	email = request.form["login_email"]
	pswd = hashlib.sha256(request.form["login_pswd"].encode()).hexdigest()
	
	query = db["Users"].find_one({"user_email":email,"user_pswd":pswd})
	if(query):
		session["_id"] = str(query["_id"])
		session["name"] = str(query["name"])
		session["user"] = "user"
		return redirect(url_for("userInfo"))
	else:
		flash("Incorrect E-mail or Password.")

	return render_template("index.html",form=form,form2=form2,signUp = "userSignUp", signIn = "userSignIn", name=session.get("name"),user=session.get("user"))

@app.route('/userInfo')
def userInfo():
	form = forms.searchColab()
	form2 = forms.getScore()
	return render_template("user_info.html",form=form, form2 = form2, name=session.get("name"),user=session.get("user"), _id=session.get("_id"), info=None, status=None)

@app.route('/userInfo/Evaluations',methods=["GET","POST"])
def userInfoEvaluation():
	form = forms.searchColab()
	form2 = forms.getScore()

	info = {}
	info_aux = {}
	apps = db["Avaliacoes"].distinct("app_id",{"user_id":ObjectId(session.get("_id"))})
	if apps:
		for i in apps:
			query = db["Applications"].find_one({"_id":i},{"name":1,"questions":1})
			app_name = query["name"]
			app_questions = query["questions"]
			body = {"user_id":session.get("_id"),"app_id":str(i)}

			res= list(db["Avaliacoes"].find({"user_id":ObjectId(session.get("_id")),"app_id":ObjectId(i)},{"evaluation":1,"evaluation_time":1,"questions":1,"comment":1,"_id":0}))
			
			for j in res:
				j["evaluation_time"] = str(time.strftime('%d-%m-%Y %H:%M:%S', time.localtime(j["evaluation_time"])))
			
			info[app_name] = res
			info_aux[app_name+"_questions"] = app_questions

	else:
		flash("You don't have any evaluation yet.")

	return render_template("user_info.html",form=form, form2 = form2, name=session.get("name"),user=session.get("user"), _id=session.get("_id"), info=info, info2=info_aux)

@app.route('/colaborator',methods=["GET","POST"])
def colaborator():
	form = forms.colaboratorSignUp()
	form2 = forms.userLogin()
	
	return render_template("index.html",form=form,form2=form2,signUp = "colaboratorSignUp", signIn="colaboratorSignIn", name=session.get("name"),user=session.get("user"))

@app.route('/colaboratorSignUp', methods=["GET","POST"])
def colaboratorSignUp():
	form = forms.colaboratorSignUp()
	form2 = forms.userLogin()

	name = request.form["name"]
	email = request.form["email"]
	psw = hashlib.sha256(request.form["pswd"].encode()).hexdigest()

	query = db["Colaborators"].find_one({"user_email":email})
	if(query):
		flash("User already exists.")
	else:
		db["Colaborators"].insert_one({"name":name,"user_email":email,"user_pswd":psw})
		flash("Registered sucessfully!")
	return render_template("index.html",form=form,form2=form2,signUp = "colaboratorSignUp", signIn="colaboratorSignIn", name=session.get("name"),user=session.get("user"))

@app.route('/colaboratorSignIn', methods=["GET","POST"])
def colaboratorSignIn():
	form = forms.userSignUp()
	form2 = forms.userLogin()

	email = request.form["login_email"]
	pswd = hashlib.sha256(request.form["login_pswd"].encode()).hexdigest()
	
	query = db["Colaborators"].find_one({"user_email":email,"user_pswd":pswd})
	if(query):
		session["_id"] = str(query["_id"])
		session["name"] = str(query["name"])
		session["user"] = "colab"
		return redirect(url_for("colaboratorInfo"))
	else:
		flash("Incorrect E-mail or Password.")

	return render_template("index.html",form=form,form2=form2,signUp = "colaboratorSignUp", signIn="colaboratorSignIn", name=session.get("name"),user=session.get("user"))

@app.route('/colaboratorInfo')
def colaboratorInfo():
	form = forms.searchColab()
	form2 = forms.getScore()
	return render_template("colab_info.html",form=form, form2 = form2, name=session.get("name"),user=session.get("user"), _id=session.get("_id"), info=None, status=None)

@app.route('/colaboratorInfo/Score',methods=["GET","POST"])
def colaboratorInfoScore():
	form = forms.searchColab()
	form2 = forms.getScore()

	info = {}
	info_aux = {}
	apps = db["Avaliacoes"].distinct("app_id",{"colaborator_id":ObjectId(session.get("_id"))})
	if apps:
		for i in apps:
			query = db["Applications"].find_one({"_id":i},{"name":1,"questions":1})
			app_name = query["name"]
			app_questions = query["questions"]
			body = {"colaborator_id":session.get("_id"),"app_id":str(i)}
			res= requests.get("https://recomendation-api-cefet.herokuapp.com/evaluationByApp",data=json.dumps(body),headers={"content-type":"application/json"}).json()
			for j in res["Evaluations"]:
				j["evaluation_time"] = str(time.strftime('%d-%m-%Y %H:%M:%S', time.localtime(j["evaluation_time"])))

			info[app_name] = res["Evaluations"]
			info_aux[app_name+"_mean"] = res["Mean"]
			info_aux[app_name+"_questions"] = app_questions
	else:
		flash("You don't have any evaluation yet.")

	return render_template("colab_info.html",form=form, form2 = form2, name=session.get("name"),user=session.get("user"), _id=session.get("_id"), info=info, info2=info_aux)

@app.route('/application',methods=["GET","POST"])
def application():
	form = forms.applicationSignUp()
	form2 = forms.userLogin()

	return render_template("index.html",form=form,form2=form2,signUp = "appSignUp", signIn="appSignIn", name=session.get("name"),user=session.get("user"))

@app.route('/appSignUp',methods=["GET","POST"])
def appSignUp():
	name = request.form["name"]
	email = request.form["email"]
	psw = hashlib.sha256(frequest.form["pswd"].encode()).hexdigest()
	question = request.form["question"].split(",")
	
	query = db["Applications"].find_one({"name":name})
	if(query):
		flash("Application already exists, please check if the key entered is correct and try again.")

	else:
		db["Applications"].insert_one({"name":name,
									  "user_email":email,
									  "user_psw":psw,
									  "key":None,
									  "key_status":False,
									  "limit":0,
									  "requisitions":0,
									  "questions":question})
		flash("Registered sucessfully!")
	return render_template("index.html",form=form,form2=form2,signUp = "appSignUp", signIn="appSignIn",name=session.get("name"),user=session.get("user"))

@app.route('/appSignIn', methods=["GET","POST"])
def appSignIn():
	form = forms.userSignUp()
	form2 = forms.userLogin()

	email = request.form["login_email"]
	pswd = hashlib.sha256(request.form["login_pswd"].encode()).hexdigest()
	
	query = db["Applications"].find_one({"user_email":email,"user_pswd":pswd})
	if(query):
		session["_id"] = str(query["_id"])
		session["name"] = str(query["name"])
		session["user"] = "app"
		session["key"] = str(query["key"])
		return redirect(url_for("appInfo"))
	else:
		flash("Incorrect E-mail or Password.")

	return redirect(url_for("application"))
	
@app.route('/appInfo',methods=["GET","POST"])
def appInfo():
	form = forms.searchColab()
	form2 = forms.manageColab()
	return render_template("app_info.html",form=form, form2 = form2, name=session.get("name"),user=session.get("user"), info=None, status=None)

@app.route('/appInfo/Procurar',methods=["GET","POST"])
def appInfoBuscar():
	form = forms.searchColab()
	form2 = forms.manageColab()
	
	colaborator_list = request.form["cid"].split(',')
	status_list = []

	body = {"key":session.get("key"),"colaborator_list":colaborator_list,"status_list":status_list}

	res= requests.get("https://recomendation-api-cefet.herokuapp.com/ManageColaborators",data=json.dumps(body),headers={"content-type":"application/json"}).json()
	res["Questions"] = db["Applications"].find_one({"_id":ObjectId(session.get("_id"))},{"questions":1,"_id":0})["questions"]
	return render_template("app_info.html",form=form, form2 = form2, name=session.get("name"),user=session.get("user"), info=res)

@app.route('/appInfo/Cadastrar',methods=["GET","POST"])
def appInfoCadastrar():
	form = forms.searchColab()
	form2 = forms.manageColab()
	
	colaborator_list = request.form["cid"].split(',')
	status_list = request.form["status"].split(',')

	body = {"key":session.get("key"),"colaborator_list":colaborator_list,"status_list":status_list}

	res= requests.post("https://recomendation-api-cefet.herokuapp.com/ManageColaborators",data=json.dumps(body),headers={"content-type":"application/json"})

	flash(res.text)
	return render_template("app_info.html",form=form, form2 = form2, name=session.get("name"),user=session.get("user"), info=None, status=res.status_code)

@app.route('/appInfo/Atualizar', methods=["GET","POST"])
def appInfoAtualizar():
	form = forms.searchColab()
	form2 = forms.manageColab()
	
	colaborator_list = request.form["cid"].split(',')
	status_list = request.form["status"].split(',')

	body = {"key":session.get("key"),"colaborator_list":colaborator_list,"status_list":status_list}

	res= requests.post("https://recomendation-api-cefet.herokuapp.com/ManageColaborators",data=json.dumps(body),headers={"content-type":"application/json"})

	flash(res.text)
	return render_template("app_info.html",form=form, form2 = form2, name=session.get("name"),user=session.get("user"), info=None, status=res.status_code)

@app.route('/appInfo/Remover',methods=["GET","POST","DELETE"])
def appInfoRemover():
	form = forms.searchColab()
	form2 = forms.manageColab()
	
	colaborator_list = request.form["cid"].split(',')
	status_list = []

	body = {"key":session.get("key"),"colaborator_list":colaborator_list,"status_list":status_list}

	requests.delete("https://recomendation-api-cefet.herokuapp.com/ManageColaborators",data=json.dumps(body),headers={"content-type":"application/json"})

	flash("Colaborator removed sucessfully")
	return render_template("app_info.html",form=form, form2 = form2, name=session.get("name"),user=session.get("user"), info=None, status=res.status_code)

@app.route('/logout',methods=["GET","POST"])
def logout():
	session.clear()
	return redirect(url_for("application"))
	
@app.route('/buy',methods=["GET","POST"])
def buy():
	if session.get("_id"):
		form = forms.payment()
		if form.validate_on_submit():
			data = db["Applications"].find_one({"_id":ObjectId(session.get("_id"))})
			if data:
				session["key_type"] = form.key_type.data
				return redirect(url_for("payment"))

			else:
				flash("Application don't exists")
				return redirect(url_for("application",
										form=forms.applicationSignUp(), form2=forms.userLogin()), 
										name=session.get("name"),user=session.get("user"))

		return render_template("base.html",form=form,  name=session.get("name"),user=session.get("user"))
	else:
		flash("Você não está logado!")
		return redirect(url_for("application",
										form=forms.applicationSignUp(), form2=forms.userLogin()), 
										name=session.get("name"),user=session.get("user"))

@app.route('/payment',methods=["GET","POST"])
def payment():
	key_type = int(session.get("key_type"))
	if key_type == 1:
		value = 100.00
	elif key_type == 2:
		value = 195.00
	elif key_type == 3:
		value = 250.00
	return render_template('payment.html',value=value, name=session.get("name"),user=session.get("user"))

@app.route('/confirmPayment',methods=["GET","POST"])
def confirm():
	data = request.get_json()
	response = CaptureOrder().capture_order(data["orderID"],
											client.OrdersDB,
											db,
											session.get("_id"),
											int(session.get("key_type")),
											debug=True)
	return "Sucess",201


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
