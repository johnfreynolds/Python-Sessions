import os, sys, cgi, json, urlparse
sys.path.append("lib")
import webapp2, jinja2, urllib, urllib2

from google.appengine.api import users, oauth, urlfetch
from webapp2_extras import sessions

### Jinja2 Configurations ###
template_dir = os.path.join(os.path.dirname(__file__))
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

### Configuration ###
config = {}
config['webapp2_extras.sessions'] = {'secret_key': 'my-super-secret-key',}

class BaseHandler(webapp2.RequestHandler):
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        # Here is where the problem was - the `return` was missing
        return self.session_store.get_session()

class CheckVar(BaseHandler):
    def get(self):
        self.session['foo'] = 'bar'
        foo = self.session.get('foo')

        context = { 'foo' : foo }

        # Template Settings
        template = jinja_env.get_template('index.html')
        self.response.write(template.render(context))

app = webapp2.WSGIApplication([
    ('/', CheckVar),
], debug=True, config=config)
