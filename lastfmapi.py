import logging
import simplejson as json
import urllib
import urllib2

from google.appengine.api import memcache

# Last.FM authentication details
lastfm_api_key = "295e485894bdf30203b53607f1d94e34"
lastfm_api_root = "http://ws.audioscrobbler.com/2.0/"
result_limit = 15

def getLastFmJson(args):
    arguments = {}
    
    for key in args:
        arguments[key] = args[key]
    
    arguments["format"] = "json"
    arguments["api_key"] = lastfm_api_key
    arguments["limit"] = result_limit
    

    api_result = ""
    
    # Call the Last.FM API using the standard Python urllib2
    # Note that even though we are using the urllib2 interface, App Engine
    # will use its own URLFetch service to get the data and count it against
    # our quota.
    values = urllib.urlencode(arguments)
    api_string = lastfm_api_root + "?" + values
    api_request = urllib2.Request(api_string)
    response = urllib2.urlopen(api_request)
    api_result = response.read()
    
    return json.loads(api_result)