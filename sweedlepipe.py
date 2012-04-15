from gevent.wsgi import WSGIServer
from gevent import monkey
monkey.patch_all()
import bottle
from bottle import route, run, static_file, view, template, request, response
import logging
import requests
import time
from twitlist import twitlist, atrest
import config

########################
# Routes
@route('/static/<filename:path>')
def static(filename):
    return static_file(filename, root='static')

@route('/')
@view('hello')
def hello():
    return dict()

@route('/login_landing')
@view('login')
def login_landing():
    session = request.environ.get('beaker.session')
    verified = False
    screen_name = session.get("screen_name")
    if screen_name:
        verified = True
    return {'verified':verified, 'screen_name':screen_name}

@route('/login')
def login():
    session = request.environ.get('beaker.session')
    token, secret, redirect_url = twitlist.TwitterOAuthHandler.get_request_token(config.CALLBACK_URL)
    session["oauth_token"] = token
    session["oauth_secret"] = secret
    session.save()
    bottle.redirect(redirect_url)

@route('/verified')
@view('login')
def login():
    session = request.environ.get('beaker.session')
    oauth_secret = session.get("oauth_secret")
    oauth_token = request.query.oauth_token or None
    oauth_verifier = request.query.oauth_verifier or None
    user_token, user_secret, user_id, screen_name = twitlist.TwitterOAuthHandler.get_access_token(oauth_token, oauth_secret, oauth_verifier)
    session["user_oauth_token"] = user_token
    session["user_oauth_secret"] = user_secret
    session["user_id"] = user_id
    session["screen_name"] = screen_name
    session.save()
    bottle.redirect('/login_landing')

@route('/generate')
@view('generate')
def generate():
    session = request.environ.get('beaker.session')
    #TODO: remove when done testing
    session["groups"] = None
    session.persist()
    groups = session.get("groups")
    if groups is not None:
        bottle.redirect('/groups')
    return {}

@route('/generategroups')
def generate():
    session = request.environ.get('beaker.session')
    user_oauth_token = session.get("user_oauth_token")
    user_oauth_secret = session.get("user_oauth_secret")
    screen_name = session.get("screen_name")
    groups = session.get("groups")
    if groups is None:
        session["progress"] = None
        session.persist()
        groups = run_grouper(user_oauth_token, user_oauth_secret, screen_name)
        session["groups"] = groups
        session.save()
    return {}

@route('/progress')
def progress():
    session = request.environ.get('beaker.session')
    progress = session.get('progress', 0)
    return {'progress': progress}

@route('/groups')
@view('groups')
def groups():
    session = request.environ.get('beaker.session')
    groups = session.get("groups")
    if not groups:
        user_oauth_token = session.get("user_oauth_token")
        user_oauth_secret = session.get("user_oauth_secret")
        screen_name = session.get("screen_name")
        try:
            groups = run_grouper(user_oauth_token, user_oauth_secret, screen_name)
        except:
            logging.exception("run_grouper failed.")
            raise
        session["groups"] = groups
        session.save()
    return {'groups': groups}

@route('/groupdetails/<group_id:int>')
@view('groupdetails')
def groupdetails(group_id):
    session = request.environ.get('beaker.session')
    groups = session.get("groups")
    if groups is None:
        return {"user_details": (), "similarities": ()}
    group = groups.get(group_id)
    if group is None:
        return {"user_details": (), "similarities": ()}
    user_oauth_token = session.get("user_oauth_token")
    user_oauth_secret = session.get("user_oauth_secret")
    screen_name = session.get("screen_name")
    api = twitlist.TwitterRestAPI(oauth_token=user_oauth_token, oauth_secret=user_oauth_secret, cache=CACHE)
    similarities = api.userdetails(group["similarities"])
    user_details = group["user_details"]
    return {"user_details": user_details, "similarities": similarities}

@route('/makelist/<group_id:int>')
def makelist(group_id):
    session = request.environ.get('beaker.session')
    groups = session.get("groups")
    if groups is None:
        return
    group = groups.get(group_id)
    name = group["description"]
    userids = list(user["id"] for user in group["user_details"])
    user_oauth_token = session.get("user_oauth_token")
    user_oauth_secret = session.get("user_oauth_secret")
    screen_name = session.get("screen_name")
    api = twitlist.TwitterRestAPI(oauth_token=user_oauth_token, oauth_secret=user_oauth_secret, cache=CACHE)
    response = api.makelist(name, "Made by sweedlepipe.", userids)
    url = "http://www.twitter.com%s" % (response["uri"])
    bottle.redirect(url)


############################
# Utilities
def run_grouper(user_oauth_token, user_oauth_secret, screen_name):
    if user_oauth_token is None or user_oauth_secret is None:
        return list(tuple())
    api = twitlist.TwitterRestAPI(oauth_token=user_oauth_token, oauth_secret=user_oauth_secret, cache=CACHE)
    grouper = twitlist.Grouper(api)
    groups = grouper.generate_groups(user_name=screen_name, notification_hook=ProgressNotifier())
    if not groups:
        groups = list(tuple())
    return groups


class ProgressNotifier(object):
    def __init__(self):
        self.session = request.environ.get('beaker.session')
        self.step_count = 0

    def setup(self, step_count):
        self.step_count = step_count
        self.count = 0
        self.save(self.count)

    def step(self):
        step_value = 100.0 / self.step_count
        self.count += step_value 
        self.save(int(self.count))
        
    def finish(self):
        self.count = 100
        self.save(int(self.count))

    def save(self, value):
        self.session["progress"] = value
        self.session.persist()
    

############################
# Configuration
# logging config
logging.basicConfig(format='%(asctime)s %(message)s',level=logging.DEBUG)
# session configuration
from beaker.middleware import SessionMiddleware
session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 3000,
    'session.data_dir': './data',
    'session.auto': True
}
# cache backend configuration
CACHE = atrest.Cache(atrest.FileBackend('/tmp/atrest_cache'), 3600)
# oauth configuration
twitlist.TwitterOAuthHandler.config_oauth_handler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
application = SessionMiddleware(bottle.app(), session_opts)
if __name__ == '__main__':
    run(app=application, host='localhost', port=3000, reloader=True, server='gevent')
