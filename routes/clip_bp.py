import datetime

from flask import render_template, request, redirect, Blueprint, abort

from models.clip import ClipModel


def index():
    newest_clips = ClipModel.newest(3)
    highest_rated = ClipModel.highest_rated(3)

    return render_template(
        'index.html',
        newest_clips_list=newest_clips,
        highest_rated_list=highest_rated
    )


def add_clip():
    if request.method == 'POST':
        form_values = request.form

        new_clip = ClipModel(
            title=form_values['title'],
            description=form_values['description'],
            link_yt=form_values['link_yt'],
            link_img=form_values['link_img'],
            added=datetime.datetime.now().timestamp(),
            score=0
        )
        new_clip.save()

        return redirect(request.url)

    return render_template('add.html')


def watch_clip(clip_id):
    if clip_details := ClipModel.find_by_id(clip_id):
        clip_details.added = datetime.datetime.fromtimestamp(clip_details.added)
        comments = clip_details.comments.all()

        return render_template('watch.html', clip=clip_details, comments=comments)

    abort(404)


def like_clip(clip_id):
    if clip := ClipModel.find_by_id(clip_id):
        clip.score += 1
        clip.save()

        return redirect(request.referrer)

    abort(404)


def unlike_clip(clip_id):
    if clip := ClipModel.find_by_id(clip_id):
        clip.score -= 1
        clip.save()

        return redirect(request.referrer)

    abort(404)


clip_bp = Blueprint('clip_bp', __name__)

clip_bp.route('/', methods=['GET'])(index)
clip_bp.route('/add', methods=['GET', 'POST'])(add_clip)
clip_bp.route('/clip/<clip_id>', methods=['GET'])(watch_clip)  # localhost:5000/clip/2
clip_bp.route('/like_clip/<clip_id>', methods=['GET'])(like_clip)
clip_bp.route('/unlike_clip/<clip_id>', methods=['GET'])(unlike_clip)
