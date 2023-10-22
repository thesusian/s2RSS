from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import xml.etree.ElementTree as ET
import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    feeds = db.relationship('Feed', backref='owner', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Feed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    item_search_pattern = db.Column(db.Text)
    title = db.Column(db.Text)
    link = db.Column(db.Text)
    desc = db.Column(db.Text)

    def gen_xml(self):
        root = ET.Element("rss", version="2.0")
        channel = ET.SubElement(root, "channel")
        # Add the feed information to the channel.
        ET.SubElement(channel, "title").text = self.title
        ET.SubElement(channel, "link").text = self.link
        ET.SubElement(channel, "description").text = self.desc 
        channel.set("pubDate", datetime.datetime.utcnow().isoformat())
        return ET.tostring(root, encoding="utf-8").decode()

@login.user_loader
def load_user(id):
    return User.query.get(int(id))