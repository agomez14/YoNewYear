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
import webapp2, jinja2, os, logging, urllib2, urllib, json

from settings import *

from google.appengine.api import urlfetch

jinja_environment = jinja2.Environment(loader=
	jinja2.FileSystemLoader(os.path.dirname(__file__)))

YO_TOKEN = YO_API_TOKEN
TIMEZONE_KEY = TIMEZONE_API_KEY

YO_URL = "http://dev.justyo.co"

timestamp = "1420009914"

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        template = jinja_environment.get_template('main.html')
        self.response.out.write(template.render(template_values))

class YoHandler(webapp2.RequestHandler):
	def get(self):
		username = "CHIVAS604"
		location = "42.360091;-71.094159"
		url = "https://maps.googleapis.com/maps/api/timezone/json?"
		temp = list(location)
		index = location.index(';')
		temp[index] = ","
		location = "".join(temp)
		parameters = [
			("location",location),
			("timestamp",timestamp)
		]
		form_data = urllib.urlencode(parameters)
		response = urlfetch.fetch(url=url,
			payload=form_data,
			method=urlfetch.POST
		).content
		logging.info(response)
		json_data = json.loads(response)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/yo', YoHandler),
], debug=True)
