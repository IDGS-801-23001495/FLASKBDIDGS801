from . import maestros

from flask import render_template, request, redirect, url_for

import forms
from models import db,Maestros

@maestros.route('/perfil/<nombre>')
def perfil(nombre):
    return f"Perfil de {nombre}"

@maestros.route("/Maestros")
def maestro():
	create_from=forms.UserForm2(request.form)
	#ORM select * from maestros
	maestro=Maestros.query.all()
	return render_template("/maestros/Maestros.html", form=create_from,maestro=maestro)


@maestros.route("/Maestros/registrar", methods=["GET","POST"])
def registar():
	create_form=forms.UserForm3(request.form)
	if request.method=='POST':
		maes=Maestros(nombre=create_form.nombre.data,
			     apellidos=create_form.apellidos.data,
				 especialidad=create_form.especialidad.data,
				 email=create_form.correo.data)
		db.session.add(maes)
		db.session.commit()
		return redirect(url_for('maestros.maestro'))
	return render_template("/maestros/registrar.html")

@maestros.route("/Maestros/detalles", methods=["GET", "POST"])
def detalles():
	create_form=forms.UserForm3(request.form)
	if request.method=='GET':
		matricula=request.args.get('matricula')
		#select * from maestros where id == id
		maestro1 = db.session.query(Maestros).filter(Maestros.matricula==matricula).first()
		matricula=request.args.get('matricula')
		nombre=maestro1.nombre
		apellidos=maestro1.apellidos
		especialidad=maestro1.especialidad
		email=maestro1.email
	return render_template("/maestros/detalles.html", matricula=matricula, nombre=nombre, apellidos=apellidos, email=email, especialidad=especialidad, maestro_obj=maestro1)

@maestros.route("/Maestros/modificar", methods=["GET", "POST"])
def nodificar():
	create_form=forms.UserForm3(request.form)
	if request.method=="GET":
		matricula=request.args.get("matricula")
		#select * from maestros where id == id 
		maestro1 = db.session.query(Maestros).filter(Maestros.matricula==matricula).first()
		create_form.matricula.data=request.args.get("matricula")
		create_form.nombre.data=str.rstrip(maestro1.nombre)
		create_form.apellidos.data=maestro1.apellidos
		create_form.especialidad.data=maestro1.especialidad
		create_form.correo.data=maestro1.email
	if request.method=="POST":
		matricula=create_form.matricula.data
		maestro1 = db.session.query(Maestros).filter(Maestros.matricula==matricula).first()
		maestro1.matricula=matricula
		maestro1.nombre=str.rstrip(create_form.nombre.data)
		maestro1.apellidos=create_form.apellidos.data
		maestro1.especialidad=create_form.especialidad.data
		maestro1.email=create_form.correo.data
		db.session.add(maestro1)
		db.session.commit()
		return redirect(url_for("maestros.maestro"))
	return render_template("/maestros/modificar.html", form=create_form)

@maestros.route("/Maestros/eliminar", methods=["GET", "POST"])
def eliminar():
	create_form=forms.UserForm3(request.form)
	if request.method == "GET":
		matricula=request.args.get("matricula")
		maestro1=db.session.query(Maestros).filter(Maestros.matricula==matricula).first()
		if maestro1:
			create_form.matricula.data=maestro1.matricula
			create_form.nombre.data=maestro1.nombre
			create_form.apellidos.data=maestro1.apellidos
			create_form.especialidad.data=maestro1.especialidad
			create_form.correo.data=maestro1.email
			return render_template("/maestros/eliminar.html", form=create_form)
	if request.method == "POST":
		matricula=create_form.matricula.data
		maes=db.session.query(Maestros).filter(Maestros.matricula==matricula).first()
		if maes:
			db.session.delete(maes)
			db.session.commit()
		return redirect(url_for("maestros.maestro"))

	return render_template("/maestros/eliminar.html", form=create_form)	