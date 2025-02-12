from ieddit import *
import json

ubp = Blueprint('user', 'user', url_prefix='/user')

@ubp.route('/delete/post',  methods=['POST'])
def user_delete_post():
	if 'username' not in session:
		flash('not logged in', 'error')
		return redirect(url_for('login'))
	pid = request.form.get('post_id')
	post = db.session.query(Post).filter_by(id=pid).first()
	sub_url = config.URL + '/r/' + post.sub

	if post.author == session['username']:
		post.deleted = True
		db.session.commit()
		cache.delete_memoized(get_subi)
		flash('post deleted', category='success')
		return redirect(sub_url)
	else:
		return '403'

@ubp.route('/delete/comment',  methods=['POST'])
def user_delete_comment():
	if 'username' not in session:
		flash('not logged in', 'error')
		return redirect(url_for('login'))
	cid = request.form.get('comment_id')
	comment = db.session.query(Comment).filter_by(id=cid).first()
	post = db.session.query(Post).filter_by(id=comment.post_id).first()

	if comment.author == session['username']:
		comment.deleted = True
		db.session.commit()
		cache.delete_memoized(get_subi)
		flash('post deleted', category='success')
		return redirect(post.permalink)
	else:
		return '403'


@ubp.route('/edit/<itype>/<iid>/', methods=['GET'])
def user_get_edit(itype, iid):
	if 'username' not in session:
		flash('not logged in', 'error')
		return redirect(url_for('login'))
	if itype == 'post':
		obj = db.session.query(Post).filter_by(id=iid).first()
		if hasattr(obj, 'self_text'):
			etext = obj.self_text
		else:
			return '403'
	elif itype == 'comment':
		obj = db.session.query(Comment).filter_by(id=iid).first()
		etext = obj.text
	else:
		return 'bad itype'
	return render_template('edit.html', itype=itype, iid=iid, etext=etext)

@ubp.route('/edit',  methods=['POST'])
def user_edit_post():
	if 'username' not in session:
		flash('not logged in', 'error')
		return redirect(url_for('login'))
	itype = request.form.get('itype')
	iid = request.form.get('iid')
	etext = request.form.get('etext')

	if len(etext) < 1 or len(etext) > 20000:
		return 'invalid edit length'

	if config.CAPTCHA_ENABLE:
		if captcha.validate() == False:
			flash('invalid captcha', 'danger')
			return redirect('/user/edit/%s/%s/' % (itype, iid))
		if 'rate_limit' in session and config.RATE_LIMIT == True:
			rl = session['rate_limit'] - time.time()
			if rl > 0:
				flash('rate limited, try again in %s seconds' % str(rl))
				return redirect('/user/edit/%s/%s/' % (itype, iid))

	if itype == 'post':
		obj = db.session.query(Post).filter_by(id=iid).first()
	elif itype == 'comment':
		obj = db.session.query(Comment).filter_by(id=iid).first()
	else:
		return 'bad itype'

	if obj.author != session['username']:
		return '403'

	if hasattr(obj, 'self_text'):
		obj.self_text = etext
		obj.edited = True
		db.session.commit()
		cache.clear()
		flash('post edited', category='succes')
		return redirect(obj.permalink)
	elif hasattr(obj, 'text'):
		obj.edited = True
		obj.text = etext
		db.session.commit()
		cache.delete_memoized(c_get_comments)
		flash('comment edited', category='succes')
		return redirect(obj.permalink)
	else:
		return '403'

@ubp.route('/nsfw',  methods=['POST'])
def user_marknsfw(pid=None):
	if 'username' not in session:
		flash('not logged in', 'danger')
		return redirect(url_for('login'))

	post_id = request.form.get('post_id')
	post = db.session.query(Post).filter_by(id=post_id).first()

	if session['username'] != post.author:
		return '403'

	post.nsfw = True
	flash('marked as nsfw')
	db.session.commit()
	cache.clear()
	return redirect(post.permalink)


@ubp.route('/darkmode', methods=['POST'])
def user_darkmode(username=None):
	if 'username' not in session:
		flash('not logged in', 'danger')
		return redirect(url_for('login'))

	if username is None:
		user = db.session.query(Iuser).filter_by(username=session['username']).first()

	action = request.form.get('action')

	if action == 'disable':	
		user.darkmode = False
		mode = 'light'
		session['darkmode'] = False
	elif action == 'enable':
		user.darkmode = True
		mode = 'dark'
		session['darkmode'] = True
	else:
		return 'bad action'

	flash('switched to %s mode' % mode, 'success')
	db.session.add(user)
	db.session.commit()
	cache.clear()
	return redirect('/u/' + user.username)

@ubp.route('/anonymous', methods=['POST'])
def user_uanonymous(username=None):
	if 'username' not in session:
		flash('not logged in', 'danger')
		return redirect(url_for('login'))

	if username is None:
		user = db.session.query(Iuser).filter_by(username=session['username']).first()

	action = request.form.get('action')

	if action == 'disable':	
		user.anonymous = False
		session['anonymous'] = False
	elif action == 'enable':
		user.anonymous = True
		session['anonymous'] = True
	else:
		return 'bad action'

	flash('toggled anonymous', 'success')
	db.session.add(user)
	db.session.commit()
	cache.clear()
	return redirect('/u/' + user.username)

