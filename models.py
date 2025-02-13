from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import geocoder
from urllib.request import urljoin, urlopen
import json

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    pwdhash = db.Column(db.String(54))

    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname.title()
        self.lastname = lastname.title()
        self.email = email.lower()
        self.set_password(password)

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)


class Place(object):
    def meters_to_walking_time(self, meters):
        # 80 meters is one minute walking time
        return int(meters / 80)

    def wiki_path(self, slug):
        return urljoin("http://en.wikipedia.org/wiki/", slug.replace(' ', '_'))

    def address_to_latlng(self, address):
        g = geocoder.google(address, key='AIzaSyCl4YBnQYTfAiiBzRGKUT1w-FHJDDOdWPc')

        # g.status == 'OVER_QUERY_LIMIT'
        if g.latlng:
            return g.latlng
        else:
            return (32.641856, 74.1647665)

    def query(self, address):
        lat, lng = self.address_to_latlng(address)

        query_url = f'https://en.wikipedia.org/w/api.php?action=query&list=geosearch&gsradius=5000&gscoord={lat}%7C{lng}&gslimit=20&format=json'
        g = urlopen(query_url)
        results = g.read()
        g.close()

        data = json.loads(results)

        places = []
        for place in data['query']['geosearch']:
            name = place['title']
            meters = place['dist']
            lat = place['lat']
            lng = place['lon']

            wiki_url = self.wiki_path(name)
            walking_time = self.meters_to_walking_time(meters)

            d = {
                'name': name,
                'url': wiki_url,
                'time': walking_time,
                'lat': lat,
                'lng': lng
            }

            places.append(d)

        return places