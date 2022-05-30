from flask import Flask, render_template, redirect, request, session
from flask_session import Session
from utils.Model import Model

links = ['home', 'register', 'search', 'login', 'profile', 'logout']


app = Flask(__name__)

# setting up session 😎
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# ------------------- 😁 routes 🏀 ----------------------


@app.route('/')
def index():
    return render_template('index.html', links=links, currentPage='home')


@app.route('/home')
def home():
    return render_template('index.html', links=links, currentPage='home')


@app.route('/profiles',  methods=["GET"])
def profiles():
    if not 'user' in session or session['user'] == None:
        return redirect('/login')
    profileType = request.args.get("type")
    profileId = request.args.get("id")
    print(profileType, profileId)
    data = Model(profileType).load(condition={'ID': profileId})
    if data:
        # count visit
        model = Model('visits')
        previously_visited = model.load(
            condition={'email': session['user'], 'type': profileType, 'profileId': profileId})
        if not previously_visited:
            model.email = session['user']
            model.type = profileType
            model.profileId = profileId
            model.save()
        print(data)
        return render_template('profiles.html', links=links, currentPage='profiles', type=profileType, profile=data[0])
    return redirect('/')


@app.route('/worker',  methods=["POST", "GET"])
def worker():
    # if form is submitted
    if request.method == "POST":
        model = Model('worker')
        model.firstName = request.form.get("fname")
        model.lastName = request.form.get("lname")
        model.age = request.form.get("age")
        model.phoneNumber = request.form.get("number")
        model.skill = request.form.get("skills")
        model.range = request.form.get("range_pref")
        if model.save():
            print("data saved ⭐")
            return render_template('worker.html', links=links, currentPage='worker', msg='worker registered successfully ⭐')
        return render_template('worker.html', links=links, currentPage='worker', msg='some error occured ⭕')
    return render_template('worker.html', links=links, currentPage='worker')


@app.route('/material',  methods=["POST", "GET"])
def material():
    # if form is submitted
    if request.method == "POST":
        model = Model('material')
        model.shopName = request.form.get("name")
        model.shopAddress = request.form.get("address")
        model.phoneNumber = request.form.get("mobile")
        model.product = request.form.get("product")
        if model.save():
            print("data saved ⭐")
            return render_template('material.html', links=links, currentPage='material', msg='material provider registered successfully ⭐')
        return render_template('material.html', links=links, currentPage='material', msg='some error occured ⭕')
    return render_template('material.html', links=links, currentPage='material')


@app.route('/event',  methods=["POST", "GET"])
def event():
    # if form is submitted
    if request.method == "POST":
        model = Model('event')
        model.firstName = request.form.get("fname")
        model.lastName = request.form.get("lname")
        model.venue = request.form.get("venue")
        model.event = request.form.get("event")
        if model.save():
            print("data saved ⭐")
            return render_template('event.html', links=links, currentPage='event', msg='event Manager registered successfully ⭐')
        return render_template('event.html', links=links, currentPage='event', msg='some error occured ⭕')
    return render_template('event.html', links=links, currentPage='event')


@app.route('/search',  methods=["POST", "GET"])
def search():
    # if form is submitted
    if request.method == "POST":
        form = request.form.to_dict(flat=True)
        options = [(k) for k in form.keys() if k != 'search']
        print(options)
        if request.form.get("search").strip() != '':
            model = Model('worker')
            tmp = {}
            for i in options:
                if i == 'material':
                    tmp[i] = Model(i).load(
                        condition={'shopName': request.form.get("search")})
                if i == 'event':
                    tmp[i] = Model(i).load(
                        condition={'firstName': request.form.get("search")})
                if i == 'worker':
                    tmp[i] = Model(i).load(
                        condition={'firstName': request.form.get("search")})
            print(tmp)
            return render_template('search.html', links=links, currentPage='search', data=tmp)
        tmp = {}
        for i in options:
            tmp[i] = Model(i).load()
            print(tmp)
        return render_template('search.html', links=links, currentPage='search', data=tmp)
    return render_template('search.html', links=links, currentPage='search')


@app.route('/register',  methods=["POST", "GET"])
def register():
    # if form is submitted
    if request.method == "POST":
        user = Model('users')
        user.name = request.form.get("name")
        user.phoneNumber = request.form.get("no")
        user.email = request.form.get("email")
        user.password = request.form.get("password")
        if(user.save()):
            return render_template('register.html', links=links, msg='success', currentPage='register')
        else:
            return render_template('register.html', links=links, msg='some error occured', currentPage='register')
    return render_template('register.html', links=links, currentPage='register')


@app.route('/login',  methods=["POST", "GET"])
def login():
    if 'user' in session and session['user'] != None:
        return redirect('/')
    # if form is submitted
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        print(email, password)
        user = Model('users')
        x = user.load({'email': email, 'password': password})
        print(x)
        print(user.load())
        if not x:
            return render_template('login.html', links=links, msg='email or password are incorrect', currentPage='login')
        # save user into session 🏀
        session['user'] = x[0][3]
        return redirect('/profile')
    return render_template('login.html', links=links, currentPage='login')


@app.route('/profile')
def profile():
    if not 'user' in session or session['user'] == None:
        return redirect('/')
    # fetch profile
    user = Model('users')
    print(Model('visits').load(condition={'email': session["user"]}))
    return render_template('profile.html', links=links, profile=user.load(condition={'email': session['user']})[0], visits=Model('visits').load(condition={'email': session["user"]}), currentPage='profile')


@app.route('/logout')
def logout():
    # destroy the session 🔻
    session['user'] = None
    print(session)
    return redirect('/')


class Run:
    def __init__(self):
        app.run(debug=True)


# if __name__ == '__main__':
#     app.run(debug=True)
