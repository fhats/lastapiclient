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
import logging
import simplejson as json
import os
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util
from lastfmapi import getLastFmJson


class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write('Hello world!')

class TrackHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write( render_template('track_info.html', {}) )
        
    def post(self):
        track_name = cgi.escape(self.request.get('track'))
        artist_name = cgi.escape(self.request.get('artist'))
        
        lastfm_args = {
            'method': 'track.getInfo',
            'artist': artist_name,
            'track': track_name
        }
        lastfm_response = getLastFmJson(lastfm_args)
        
        self.response.out.write( render_template('track_info.html', lastfm_response) )
        
class ArtistHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write( render_template('artist_info.html', {}) )
        
    def post(self):
        artist_name = cgi.escape(self.request.get('artist'))
        
        lastfm_args = {
            'method': 'artist.getInfo',
            'artist': artist_name
        }
        lastfm_response = getLastFmJson(lastfm_args)
        
        logging.info(json.dumps(lastfm_response, sort_keys=True, indent=4))
        
        #Just pick one of the available images!
        if 'artist' in lastfm_response:
            lastfm_response['artist']['image'] = lastfm_response['artist']['image'][3]['#text']
        
        self.response.out.write( render_template('artist_info.html', lastfm_response) )

def render_template(file, args):
    path = os.path.join(os.path.dirname(__file__), 'templates', file)
    return template.render(path, args)
        
def main():
    application = webapp.WSGIApplication([('/', MainHandler),
                                          ('/track/info', TrackHandler),
                                          ('/artist/info', ArtistHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
