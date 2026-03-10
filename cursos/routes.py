from . import cursos
from flask import render_template, request, redirect, url_for
import forms
from models import db, Curso, Alumnos, Maestros 
from sqlalchemy.exc import IntegrityError 

@cursos.route("/Cursos")
def lista_cursos():
    # ORM select * from cursos
    todos_los_cursos = Curso.query.all()
    return render_template("/cursos/Cursos.html", cursos=todos_los_cursos)

@cursos.route("/Cursos/registrar", methods=["GET","POST"])
def registrar():
    create_form = forms.CursoForm(request.form)    
    create_form.maestro_id.choices = [(m.matricula, f"{m.nombre} {m.apellidos}") for m in Maestros.query.all()]
    
    if request.method == 'POST':
        nuevo_curso = Curso(
            nombre=create_form.nombre.data,
            descripcion=create_form.descripcion.data,
            maestro_id=create_form.maestro_id.data
        )
        db.session.add(nuevo_curso)
        db.session.commit()
        return redirect(url_for('cursos.lista_cursos'))
    maestros_lista = Maestros.query.all() 
    return render_template("/cursos/registrar.html", form=create_form, maestros=maestros_lista)


@cursos.route("/Cursos/inscribir", methods=["GET", "POST"])
def inscribir_alumno():
    create_form = forms.InscripcionForm(request.form)
    
    create_form.alumno_id.choices = [(a.id, f"{a.nombre} {a.apellidos}") for a in Alumnos.query.all()]
    create_form.curso_id.choices = [(c.id, f"{c.nombre}") for c in Curso.query.all()]
    
    error_duplicado = False

    if request.method == "POST":
        curso_id = create_form.curso_id.data
        alumno_id = create_form.alumno_id.data
        
        curso = Curso.query.get(curso_id)
        alumno = Alumnos.query.get(alumno_id)
        
        if curso and alumno:
            try:
                curso.alumnos.append(alumno)
                db.session.commit()
                return redirect(url_for('cursos.lista_cursos'))
            except IntegrityError:
                db.session.rollback()
                error_duplicado = True

    seleccionado = request.args.get('curso_id')
    
    return render_template("/cursos/inscribir.html", form=create_form, alumnos=Alumnos.query.all(), cursos=Curso.query.all(), 
                           seleccionado=seleccionado, error_duplicado=error_duplicado)


@cursos.route("/Cursos/detalles", methods=["GET"])
def detalles_curso():
    id = request.args.get('id')    
    curso_obj = db.session.query(Curso).filter(Curso.id == id).first()
    
    if curso_obj:
        nombre = curso_obj.nombre
        descripcion = curso_obj.descripcion
        maestro = f"{curso_obj.maestro.nombre} {curso_obj.maestro.apellidos}"
        
        return render_template("/cursos/detalles.html", 
                               id=id, 
                               nombre=nombre, 
                               descripcion=descripcion, 
                               maestro=maestro,
                               curso_obj=curso_obj) 
    
    return redirect(url_for('cursos.lista_cursos'))

@cursos.route("/Cursos/modificar", methods=["GET", "POST"])
def modificar():
    create_form = forms.CursoForm(request.form)
    maestros_lista = Maestros.query.all()    
    create_form.maestro_id.choices = [(m.matricula, f"{m.nombre} {m.apellidos}") for m in maestros_lista]

    if request.method == "GET":
        id = request.args.get("id")
        curso = db.session.query(Curso).filter(Curso.id == id).first()
        
        if curso:
            create_form.id.data = curso.id
            create_form.nombre.data = curso.nombre
            create_form.descripcion.data = curso.descripcion
            create_form.maestro_id.data = curso.maestro_id
        else:
            return redirect(url_for('cursos.lista_cursos'))

    if request.method == "POST":
        id = request.form.get("id") 
        curso = db.session.query(Curso).filter(Curso.id == id).first()
        
        if curso:
            curso.nombre = create_form.nombre.data
            curso.descripcion = create_form.descripcion.data
            curso.maestro_id = create_form.maestro_id.data
            
            db.session.add(curso)
            db.session.commit()
            return redirect(url_for("cursos.lista_cursos"))

    return render_template("/cursos/modificar.html", form=create_form, maestros=maestros_lista)

@cursos.route("/Cursos/eliminar", methods=["GET", "POST"])
def eliminar():
    create_form = forms.CursoForm(request.form)
    maestros_lista = Maestros.query.all() 
    
    if request.method == "GET":
        id = request.args.get("id")
        curso = db.session.query(Curso).filter(Curso.id == id).first()
        
        if curso:
            create_form.id.data = curso.id
            create_form.nombre.data = curso.nombre
            create_form.descripcion.data = curso.descripcion
            create_form.maestro_id.data = curso.maestro_id
            return render_template("/cursos/eliminar.html", form=create_form, maestros=maestros_lista)
        else:
            return redirect(url_for('cursos.lista_cursos'))

    if request.method == "POST":
        id = request.form.get("id")
        curso = db.session.query(Curso).filter(Curso.id == id).first()
        if curso:
            db.session.delete(curso)
            db.session.commit()
        return redirect(url_for("cursos.lista_cursos"))

    return render_template("/cursos/eliminar.html", form=create_form, maestros=maestros_lista)