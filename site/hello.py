from flask import Flask
from flask.ext.openid import OpenID
from flask import g, session, redirect, url_for

app = Flask(__name__)
app.debug=True


oid = OpenID(app, '/path/to/store', safe_roots=[])

@app.before_request
def lookup_current_user():
    g.user = None
    if 'openid' in session:
        openid = session['openid']
        g.user = User.query.filter_by(openid=openid).first()

@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None:
        return redirect(oid.get_next_url())
    if request.method == 'POST':
        openid = request.form.get('openid')
        if openid:
            return oid.try_login(openid, ask_for=['email', 'nickname'],
                                         ask_for_optional=['fullname'])
    return render_template('login.html', next=oid.get_next_url(),
                           error=oid.fetch_error())

@app.route('/')
def index():
	return redirect(url_for('hello'))

@app.route('/hello')
def hello_world():
    return 'hey'


if __name__ == '__main__':
    app.run()