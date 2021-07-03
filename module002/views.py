from flask import Blueprint, render_template, abort, flash, redirect, url_for, request, redirect
from flask_login import login_required, current_user
from models import User, get_db, Course, Follow, Comment
from module002.forms import *

module002 = Blueprint("module002", __name__,static_folder="static",template_folder="templates")
db = get_db()


@module002.route('/')
@login_required
def module002_index():
    #user = User.filter_by(id=current_user.id)
    if current_user.profile in ('admin','staff','student'):
        cursos = Follow.query.filter_by(user_id=current_user.id)
        return render_template("module002_index.html",module="module002", rows=cursos)
    else:
        flash("Access denied!")
#        abort(404,description="Access denied!")
        return redirect(url_for('index'))







@module002.route('/forum/<course_id>', methods=['GET', 'POST'])
@login_required
def module002_forum(course_id):
    form = CommentForm()

    if request.method == 'GET':

        follows = Follow.query.filter_by(user_id=current_user.id)
        msgs = Comment.query.filter_by(course_id=course_id).all()

        msg_user_ids = tuple(msg.user_id for msg in msgs)
        users = User.query.filter(User.id.in_(msg_user_ids)).all()
        users = {user.id: user for user in users}

        return render_template("module002_forum.html", module='module002', course_id=course_id,
                           form=form, followed=follows, msgs=msgs, user=current_user, users=users)

    elif request.method == 'POST':

        form = CommentForm()
        if current_user.is_authenticated and form.validate_on_submit():
            print(request.form)
            comment = Comment(user_id=current_user.id,course_id=course_id,comment=form.comment.data)
            db.session.add(comment)
            db.session.commit()
            flash("Comentario añadido")
        else:
            flash("Error añadiendo comentario")
        return redirect(url_for('module002.module002_forum', course_id=course_id))



@module002.route('/test')
def module002_test():
    return 'OK'
