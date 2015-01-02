#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2, jinja2, os, logging, urllib2, urllib, json, time

from settings import *

from google.appengine.api import urlfetch
from datetime import datetime

jinja_environment = jinja2.Environment(loader=
    jinja2.FileSystemLoader(os.path.dirname(__file__)))

YO_URL = "http://api.justyo.co/yo/"

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        template = jinja_environment.get_template('main.html')
        self.response.out.write(template.render(template_values))

class TimezoneHandler(webapp2.RequestHandler):
    def get(self):
        # *FOR LIVE DEPLOYMENT*
        # location = self.request.get("location")
        # username = self.request.get("username")
 
        # *FOR USE ON LOCAL MACHINE*
        location = "51.5033630;-0.1276250"
        username = YO_USERNAME

        temp = list(location)
        index = location.index(';')
        temp[index] = ","
        location = "".join(temp)
 
        timestamp = str(time.time())
       
        timezone_url = "https://maps.googleapis.com/maps/api/timezone/json?location="+location+"&timestamp="+timestamp
        response = urlfetch.fetch(url=timezone_url)
        json_data = json.loads(response.content)
        current_time = int(json_data["dstOffset"]) + int(json_data["rawOffset"]) + time.time()
        
        self.redirect("/yo?location="+location+"&currenttime="+str(current_time)+"&username="+username)

class YoHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")
        location = self.request.get("location")
        current_time = self.request.get("currenttime")
        link = "http://newyearyoapp.appspot.com/link?location="+location+"&currenttime="+str(current_time)
        values = {'api_token':YO_API_TOKEN, 'username':username, 'link':link}
        data = urllib.urlencode(values)
        req = urllib2.Request(YO_URL,data)
        response = urllib2.urlopen(req)

class LinkHandler(webapp2.RequestHandler):
    def get(self):
        location = self.request.get("location")
        current_time = self.request.get("currenttime")
        template_values = {
            "location":location,
            "currenttime":current_time
        }
        template = jinja_environment.get_template('user.html')
        self.response.out.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/timezone', TimezoneHandler),
    ('/yo', YoHandler),
    ('/link', LinkHandler),
], debug=True)
