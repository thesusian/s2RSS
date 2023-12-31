from flask import render_template, flash, redirect, url_for, request, Response, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.models import User, Feed
from app.forms import LoginForm, RegistrationForm, CreateFeedForm
import app.helpers as helpers
from werkzeug.urls import url_parse


@app.route("/")
@app.route("/index")
@login_required
def index():
    feeds = Feed.query.filter_by(owner=current_user).all()
    print(type(feeds))
    return render_template("index.html", title="Home", feeds=feeds)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        # check password
        user = User.query.filter_by(username=form.username.data.lower()).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user)
        # redirect user to the page they were on, but first check if the redirect
        # is to a url, if not it can proceed
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)
    return render_template("login.html", title="Log In", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("index")


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        # lower-case username, for consistency
        user = User(username=form.username.data.lower())
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/create-feed", methods=["GET", "POST"])
@login_required
def create_feed():
    form = CreateFeedForm()
    if form.validate_on_submit():
        if form.desc.data == "":
            desc = "An RSS feed of " + form.link.data
        else:
            desc = form.desc.data
        feed = Feed(
            owner=current_user,
            address=form.address.data,
            pattern=form.pattern.data,
            item_title_template=form.item_title_template.data,
            item_link_template=form.item_link_template.data,
            item_content_template=form.item_content_template.data,
            title=form.title.data,
            link=form.link.data,
            desc=desc,
        )
        db.session.add(feed)
        db.session.commit()
        flash("Congratulations, you have created a feed, check it on your homepage!")
        return redirect(url_for("index"))
    return render_template("create-feed.html", title="Create Feed", form=form)


@app.route("/edit-feed/<id>", methods=["GET", "POST"])
@login_required
def edit_feed(id):
    feed = Feed.query.get(id)
    if feed is None or feed.owner != current_user:
        flash("You don't have permessions to delete this feed")
        return redirect(url_for("index"))

    form = CreateFeedForm()
    if form.validate_on_submit():
        if form.desc.data == "":
            desc = "An RSS feed of " + form.link.data
        else:
            desc = form.desc.data

        feed.address=form.address.data
        feed.pattern=form.pattern.data
        feed. item_title_template=form.item_title_template.data
        feed.item_link_template=form.item_link_template.data
        feed.item_content_template=form.item_content_template.data
        feed.title=form.title.data
        feed.link=form.link.data
        feed.desc=desc
        db.session.commit()
        flash("Your changes have been saved.")
        return redirect(url_for("index"))
    elif request.method == "GET":
        form.address.data=feed.address
        form.pattern.data=feed.pattern
        form.item_title_template.data=feed.item_title_template
        form.item_link_template.data=feed.item_link_template
        form.item_content_template.data=feed.item_content_template
        form.title.data=feed.title
        form.link.data=feed.link
        form.desc.data=feed.desc
    return render_template("edit-feed.html", title="Edit Feed", form=form)


@app.route("/delete-feed/<id>", methods=["GET"])
@login_required
def delete_feed(id):
    feed = Feed.query.get(id)
    if feed is None or feed.owner != current_user:
        flash("You don't have permessions to delete this feed")
        return redirect(url_for("index"))
    else:
        db.session.delete(feed)
        db.session.commit()
        flash("feed delted successfully")
        return redirect(url_for("index"))


@app.route("/feed/<id>.xml")
def get_feed(id):
    feed = Feed.query.filter_by(id=id).first_or_404()
    return Response(feed.gen_xml(), mimetype="text/xml")


#!! Internal APIs Under this point !!#
@app.route("/fetch-source", methods=["POST"])
@login_required
def fetch_source():
    source_code = helpers.get_address_source(request.json["address"])
    return jsonify({"source_code": source_code})


@app.route("/fetch-pattern-result", methods=["POST"])
@login_required
def fetch_pattern_result():
    pattern = request.json["pattern"]
    source_code = request.json["source_code"]
    pattern_result = helpers.get_foramtted_list(source_code, pattern)
    return jsonify({"pattern_result": pattern_result})


@app.route("/fetch-template-result", methods=["POST"])
@login_required
def fetch_template_result():
    pattern = request.json["pattern"]
    source_code = request.json["source_code"]

    title_template = request.json["title_item_template"]
    link_template = request.json["link_item_template"]
    desc_template = request.json["desc_item_template"]

    items = helpers.get_json_list(source_code, pattern).json

    template_result = ""

    for item in items:
        title, link, desc = title_template, link_template, desc_template
        for info in items[item]:
            # First check if item template has an element in it
            if info in title:
                title = title.replace(info, items[item][info])
            if info in link:
                link = link.replace(info, items[item][info])
            if info in desc:
                desc = desc.replace(info, items[item][info])
        template_result += (
            "Title: " + title + "\nLink: " + link + "\nContent: " + desc + "\n"
        )
        template_result += "\n"

    return jsonify({"template_result": template_result})
