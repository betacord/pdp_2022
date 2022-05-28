from flask import request, redirect, abort, Blueprint

from models.comment import CommentModel


def add_comment():
    if request.method == 'POST':
        form_data = request.form

        new_comment = CommentModel(
            author=form_data['author'],
            content=form_data['content'],
            clip_id=form_data['clip_id']
        )
        new_comment.save()

        return redirect(request.referrer)

    abort(405)


def remove_comment():
    if request.method == 'POST':
        form_data = request.form
        comment_id = form_data['id']

        comment = CommentModel.find_by_id(comment_id)
        comment.remove()

        return redirect(request.referrer)

    abort(405)


comment_bp = Blueprint('comment_bp', __name__)

comment_bp.route('/add', methods=['POST'])(add_comment)
comment_bp.route('/remove', methods=['POST'])(remove_comment)
