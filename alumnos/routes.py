from . import alumnos

from flask import render_template, request, redirect, url_for

import forms
from models import db,Alumnos


@alumnos.route('/aa/<nombre>')
def perfil(nombre):
    return f"Perfil de {nombre}"

@alumnos.route("/Alumnos")
def alumno():
	create_from=forms.UserForm2(request.form)
	#ORM select * from alumnos
	alumno=Alumnos.query.all()
	return render_template("/alumnos/Alumnos.html", form=create_from,alumno=alumno)

@alumnos.route("/Alumnos/registrar", methods=["GET","POST"])
def registrar():
	create_form=forms.UserForm2(request.form)
	if request.method=='POST':
		alum=Alumnos(nombre=create_form.nombre.data,
			     apellidos=create_form.apellidos.data,
				 email=create_form.correo.data,
				 telefono=create_form.telefono.data)
		db.session.add(alum)
		db.session.commit()
		return redirect(url_for('alumnos.alumno'))
	return render_template("/alumnos/registrar.html")

@alumnos.route("/Alumnos/detalles", methods=["GET", "POST"])
def detalles():
	create_form=forms.UserForm2(request.form)
	if request.method=='GET':
		id=request.args.get('id')
		#select * from alumnos where id == id
		alumn1 = db.session.query(Alumnos).filter(Alumnos.id==id).first()
		id=request.args.get('id')
		nombre=alumn1.nombre
		apellidos=alumn1.apellidos
		email=alumn1.email
		telefono=alumn1.telefono
	return render_template("/alumnos/detalles.html", id=id, nombre=nombre, apellidos=apellidos, email=email, telefono=telefono, alumno_obj=alumn1)

@alumnos.route("/Alumnos/modificar", methods=["GET", "POST"])
def nodificar():
	create_form=forms.UserForm2(request.form)
	if request.method=="GET":
		id=request.args.get("id")
		#select * from alumnos where id == id 
		alum1 = db.session.query(Alumnos).filter(Alumnos.id==id).first()
		create_form.id.data=request.args.get("id")
		create_form.nombre.data=str.rstrip(alum1.nombre)
		create_form.apellidos.data=alum1.apellidos
		create_form.correo.data=alum1.email
		create_form.telefono.data=alum1.telefono
	if request.method=="POST":
		id=create_form.id.data
		alum1 = db.session.query(Alumnos).filter(Alumnos.id==id).first()
		alum1.id=id
		alum1.nombre=str.rstrip(create_form.nombre.data)
		alum1.apellidos=create_form.apellidos.data
		alum1.email=create_form.correo.data
		alum1.telefono=create_form.telefono.data
		db.session.add(alum1)
		db.session.commit()
		return redirect(url_for("alumnos.alumno"))
	return render_template("/alumnos/modificar.html", form=create_form)

@alumnos.route("/Alumnos/eliminar", methods=["GET", "POST"])
def eliminar():
	create_form=forms.UserForm2(request.form)
	if request.method == "GET":
		id=request.args.get("id")
		alum1=db.session.query(Alumnos).filter(Alumnos.id==id).first()
		if alum1:
			create_form.id.data=alum1.id
			create_form.nombre.data=alum1.nombre
			create_form.apellidos.data=alum1.apellidos
			create_form.correo.data=alum1.email
			create_form.telefono.data=alum1.telefono
			return render_template("/alumnos/eliminar.html", form=create_form)
	if request.method == "POST":
		id=create_form.id.data
		alum=db.session.query(Alumnos).filter(Alumnos.id==id).first()
		if alum:
			db.session.delete(alum)
			db.session.commit()
		return redirect(url_for("alumnos.alumno"))

	return render_template("/alumnos/eliminar.html", form=create_form)	