from flask import Blueprint, render_template, flash, redirect
from flask_login.utils import login_required
from flask_login import current_user
from models import get_db, Assignment, Task
from flask.globals import request
from flask.helpers import send_file, url_for
from io import BytesIO

module003 = Blueprint("module003", __name__,static_folder="static",template_folder="templates")
db = get_db()


@module003.route('/<task_id>/<alum_id>', methods=['GET'])
@login_required
def module003_index(task_id, alum_id):
    if current_user.profile == 'student' and current_user.id == alum_id:
        assignment = Assignment.query.filter_by(user=current_user.id, task=int(task_id)).first()
        task = Task.query.filter_by(id=int(task_id)).first()
        return render_template("module003_index.html",module='module003', assignment=assignment, task=task, alum_id=current_user.id, task_id=task_id, professor=False)
    elif current_user.profile == 'professor':
        assignment = Assignment.query.filter_by(user=int(alum_id), task=int(task_id)).first()
        task = Task.query.filter_by(id=int(task_id)).first()
        return render_template("module003_index.html", module='module003', assignment=assignment, task=task, alum_id=alum_id, task_id=task_id, professor=True)
    else:
        flash("ERROR")
        return redirect(url_for("index"))


@module003.route('/upload', methods=['POST'])
@login_required
def module003_upload():
    if current_user.profile == 'student' and request.method == 'POST':
        if request.form['del'] == "1":
            db.session.delete(Assignment.query.filter_by(user=current_user.id, task=int(request.form['task'])).first())
            db.session.commit()
            flash('Erased file')
            return redirect(url_for('assignment', task_id = int(request.form['task'], alum_id = current_user.id)))
        else:
            file_contents = request.files['file']
            newfile = Assignment(name=file_contents.filename, file=file_contents.read(), user=current_user.id, task=int(request.form['task']))
            db.session.add(newfile)
            db.session.commit()
            flash(f'Uploaded file {file_contents.filename}')
            return redirect(url_for('assignment', task_id = int(request.form['task'], alum_id = current_user.id)))
    flash("ERROR")
    return redirect(url_for('index'))


@module003.route('/download/<task_id>/<alum_id>', methods = ['GET'])
@login_required
def module003_download(task_id, alum_id):
    if current_user.profile == 'professor' or current_user.profile == 'student' and current_user.id == int(alum_id):
        file_contents = Assignment.query.filter_by(user=current_user.id, task=int(task_id)).first()
        return send_file(BytesIO(file_contents.file), attachment_filename=file_contents.name)


@module003.route('/mark', methods=['POST'])
@login_required
def module003_nota():
    if current_user.profile == 'professor' and request.method == 'POST':
        assignment = Assignment.query.filter_by(user=int(request.form['alumno']), task=int(request.form['task'])).first()
        assignment.nota = float(request.form['nota'])
        db.session.commit()
        flash('Mark updated correctly')
        return redirect(url_for('assignment', task_id = int(request.form['task'], alum_id = int(request.form['alumno']))))
    flash("ERROR")
    return redirect(url_for('index'))


@module003.route('/test')
def module003_test():
    return 'OK'