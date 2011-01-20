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
import cgi
import os
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util
from lastfmapi import getLastFmJson


class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write('Hello world!')

# ArtistHandler is responsible for providing an interface to the Last.FM API method artist.getInfo
# It handles two HTTP methods: GET and POST        
class ArtistHandler(webapp.RequestHandler):
    # Just provide a form to interact with ArtistHandler
    def get(self):
        self.response.out.write( render_template('artist_info.html', {}) )
        
    # Do the actual interaction with the Last.FM API based on form data
    def post(self):
        # Parse arguments from the form
        artist_name = cgi.escape(self.request.get('artist'))
        
        # Arguments to the Last.FM API, passed using a map
        lastfm_args = {
            'method': 'artist.getInfo',
            'artist': artist_name
        }
        lastfm_response = getLastFmJson(lastfm_args)
        
        #Just pick one of the available images!
        #This is a workaround for not being able to refer to variables with special letters i.e. the hash in #text
        if 'artist' in lastfm_response:
            lastfm_response['artist']['image'] = lastfm_response['artist']['image'][3]['#text']
        
        self.response.out.write( render_template('artist_info.html', lastfm_response) )

def render_template(file, args):
    path = os.path.join(os.path.dirname(__file__), 'templates', file)
    return template.render(path, args)
        
def main():
    application = webapp.WSGIApplication([('/', MainHandler),
                                          ('/artist/info', ArtistHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
