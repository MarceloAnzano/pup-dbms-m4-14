import cgi
from google.appengine.ext import ndb
from google.appengine.api import users
import os
import webapp2
import jinja2
import json
import logging


jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class ThesisDB(ndb.Model):
    year = ndb.IntegerProperty(required=True)
    title = ndb.StringProperty(required=True)
    abstract = ndb.TextProperty(required=True)
    adviser = ndb.StringProperty(required=True)
    section = ndb.IntegerProperty(required=True)
    datecreated = ndb.DateTimeProperty(auto_now_add=True)
    created_by = ndb.TextProperty(required=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user is not None:
            logout_url = users.create_logout_url(self.request.uri)
            template = jinja_env.get_template('index.html')
            content = {
                'user' : user.nickname(),
                'logout_url': logout_url,
            }
            self.response.write(template.render(content))
        else:
            login_url = users.create_login_url(self.request.uri)
            self.redirect(login_url)
    
    def post(self):
        user = users.get_current_user()
        thesis = ThesisDB(
            year=int(self.request.get('year')),
            title=cgi.escape(self.request.get('title')),
            abstract=cgi.escape(self.request.get('abstract')),
            adviser=cgi.escape(self.request.get('adviser')),
            section=int(self.request.get('section')),
            created_by = user.user_id(),
            )
        thesis.put()
        self.redirect('/api/student')

class APIThesis(webapp2.RequestHandler):
    def get(self):
        thesis = ThesisDB.query().order(-ThesisDB.datecreated).fetch()
        thesis_list = []

        for paper in thesis:
            thesis_list.append({
                'id': paper.key.urlsafe(),
                'year': paper.year,
                'title': paper.title,
                'abstract': paper.abstract,
                'adviser' : paper.adviser,
                'section' : paper.section
            })

        response = {
            'result': 'OK',
            'data': thesis_list
        }

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(response))

    def post(self):
        user = users.get_current_user()
        thesis = ThesisDB(
            year=int(self.request.get('year')),
            title=cgi.escape(self.request.get('title')),
            abstract=cgi.escape(self.request.get('abstract')),
            adviser=cgi.escape(self.request.get('adviser')),
            section=int(self.request.get('section')),
            created_by = user.user_id(),
            )
        thesis.put()

        self.response.headers['Content-Type'] = 'application/json'
        response = {
            'result': 'OK',
            'data': {
                'id': thesis.key.urlsafe(),
                'year': thesis.year,
                'title': thesis.title,
                'abstract': thesis.abstract,
                'adviser' : thesis.adviser,
                'section' : thesis.section,
            }
        }
        self.response.out.write(json.dumps(response))


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/api/thesis', APIThesis),
], debug=True)