from flask import render_template,request,redirect,url_for,abort,flash
from . import main
from .forms import PitchForm,CommentForm,UpvoteForm,DownvoteForm,UpdateProfile
from flask_login import login_required,current_user
from flask.views import View, MethodView
from ..model import User,Pitch,Comment,Downvote,Upvote
from ..import db,photos
import markdown2

@main.route('/', methods=['GET','POST'])
def index():
    pitch=Pitch.query.filter_by().first()

    title='Pitch Zone'

    investorpitch=Pitch.query.filter_by(category="investorpitch")
    productpitch=Pitch.query.filter_by(category="productpitch")
    interviewpitch=Pitch.query.filter_by(category="interviewpitch")
    marketpitch=Pitch.query.filter_by(category="marketpitch")

    upvotes=Upvote.get_all_upvotes(pitch_id=Pitch.id)

    return render_template('root.html',title=title,investorpitch=investorpitch,productpitch=productpitch,interviewpitch=interviewpitch,marketpitch=marketpitch,upvotes=upvotes)


@main.route('/pitch/new', methods=['GET','POST'])
@login_required
def make_pitch():

    form =PitchForm()
    available_upvotes=Upvote.query.filter_by(pitch_id = Pitch.id)
    if form.validate_on_submit(): 

        owner_id = current_user
        category = form.category.data
        description = form.description.data
        title = form.title.data
        print(current_user._get_current_object().id)
        make_pitch = Pitch(owner_id =current_user._get_current_object().id, title = title,description=description,category=category)
        db.session.add(make_pitch)
        db.session.commit()
        
        
        return redirect(url_for('main.index'))
    return render_template('pitch.html',form=form)


@main.route('/comment/new/<int:pitch_id>', methods = ['GET','POST'])
@login_required
def make_comment(pitch_id):
    form = CommentForm()
    pitch=Pitch.query.get(pitch_id)
    if form.validate_on_submit():
        description = form.description.data

        make_comment = Comment(description = description, user_id = current_user._get_current_object().id, pitch_id = pitch_id)
        db.session.add(make_comment)
        db.session.commit()


        return redirect(url_for('.make_comment', pitch_id= pitch_id))

    all_comments = Comment.query.filter_by(pitch_id = pitch_id).all()
    return render_template('comment.html', form = form, comment = all_comments, pitch = pitch )


@main.route('/pitch/upvote/<int:pitch_id>/upvote', methods = ['GET', 'POST'])
@login_required
def make_upvote(pitch_id):
    pitch = Pitch.query.get(pitch_id)
    user = current_user
    pitch_upvotes = Upvote.query.filter_by(pitch_id= pitch_id)
    
    if Upvote.query.filter(Upvote.user_id==user.id,Upvote.pitch_id==pitch_id).first():
        return  redirect(url_for('main.index'))
    
    made_upvote = Upvote(pitch_id=pitch_id, user = current_user)
    made_upvote.save_upvotes()
    return redirect(url_for('main.index'))

@main.route('/pitch/downvote/<int:pitch_id>/downvote', methods = ['GET', 'POST'])
@login_required
def make_downvote(pitch_id):
    pitch = Pitch.query.get(pitch_id)
    user = current_user
    pitch_downvotes = Downvote.query.filter_by(pitch_id= pitch_id)
    
    if Downvote.query.filter(Downvote.user_id==user.id,Downvote.pitch_id==pitch_id).first():
        return  redirect(url_for('main.index'))

    made_downvote = Downvote(pitch_id=pitch_id, user = current_user)
    made_downvote.save_downvotes()
    return redirect(url_for('main.index'))


@main.route('/user/<uname>')
def profile(uname):
    user=User.query.filter_by(username=uname).first()
    pitcheslist=Pitch.get_pitches(current_user.id)

    if user is None:
        abort (404)

    return render_template("profile/profile.html",user=user,pitcheslist=pitcheslist)

@main.route('/user/<uname>/update', methods=['GET','POST'])
@login_required

def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort (404)

    form=UpdateProfile()

    if form.validate_on_submit():
        user.bio=form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form=form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))


