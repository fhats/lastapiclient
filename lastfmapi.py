import logging
import simplejson as json
import urllib
import urllib2

from google.appengine.api import memcache

lastfm_api_key = "295e485894bdf30203b53607f1d94e34"
lastfm_api_root = "http://ws.audioscrobbler.com/2.0/"
result_limit = 15

def getLastFmJson(args):
    arguments = {}
    
    for key in args:
        arguments[key] = args[key]
        
    cache_key = "%s" % json.dumps(arguments)
    
    arguments["format"] = "json"
    arguments["api_key"] = lastfm_api_key
    arguments["limit"] = result_limit
    
    #Check the cache for stored results
    api_result = ""
    cached_data = memcache.get(cache_key)
    if cached_data is not None:
        api_result = cached_data
        logging.info("Cache hit for key %s" % cache_key)
    else:
        values = urllib.urlencode(arguments)
        api_string = lastfm_api_root + "?" + values
        api_request = urllib2.Request(api_string)
        response = urllib2.urlopen(api_request)
        api_result = response.read()
        memcache.add(cache_key, api_result, 60 * 60 * 24 * 7) #cache results for up to a week
        logging.info("Cache miss for key %s; adding data %s" % (cache_key, api_result))
    return json.loads(api_result)