from flask_login import UserMixin
from app import db, login
import app.helpers as helpers
from werkzeug.security import generate_password_hash, check_password_hash
import xml.etree.ElementTree as ET
import datetime


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    feeds = db.relationship("Feed", backref="owner", lazy="dynamic")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User {}>".format(self.username)


class Feed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    address = db.Column(db.Text)
    pattern = db.Column(db.Text)
    item_search_pattern = db.Column(db.Text)
    title = db.Column(db.Text)
    link = db.Column(db.Text)
    desc = db.Column(db.Text)
    item_title_template = db.Column(db.Text)
    item_link_template = db.Column(db.Text)
    item_content_template = db.Column(db.Text)

    def gen_xml(self):
        address_source = helpers.get_address_source(self.address)
        items = helpers.get_json_list(address_source, self.pattern).json

        root = ET.Element("rss", version="2.0")
        channel = ET.SubElement(root, "channel")

        # Add the feed information to the channel.
        ET.SubElement(channel, "title").text = self.title
        ET.SubElement(channel, "link").text = self.link
        ET.SubElement(channel, "description").text = self.desc
        channel.set("pubDate", datetime.datetime.utcnow().isoformat())

        # Add the items to the feed!
        for item in items:
            item_element = ET.SubElement(channel, "item")
            title, link, content = self.item_title_template, self.item_link_template, self.item_content_template
            for info in items[item]:
                # First check if item template has an element in it
                if info in title:
                    title = title.replace(info, items[item][info])
                if info in link:
                    link = link.replace(info, items[item][info])
                if info in content:
                    content = content.replace(info, items[item][info])
            ET.SubElement(item_element, "title").text = title
            ET.SubElement(item_element, "link").text = link
            ET.SubElement(item_element, "description").text = content

        return ET.tostring(root, encoding="utf-8").decode()


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
