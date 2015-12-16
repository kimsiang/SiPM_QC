import urllib2
import simplejson
#import mysql

def getTemperature (location) :
    url = 'http://api.wunderground.com/api/{API_KEY}/conditions/q/' + location + '.json'
    response = simplejson.load(urllib2.urlopen(url) )
    temperature = response["current_observation"]["temp_f"]
    return temperature

locations = ['99354', '55403', '80482', '46953']
for location in locations :
    temperature = str(getTemperature(location))
