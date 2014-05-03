#############################################
# Author: Glen Kidwell
#
# Description: This program will find events with free food by hitting the meetup.com API
# 
# You will need to have a config.json in the project directory for this to work. It should contain your meetup.com api key
# You can obtain this key here, if you are logged in to meetup.com:
# https://secure.meetup.com/meetup_api/key/
# Copy and paste this code into config_temp.json as the value for the "key" field, and rename the file to config.json
#
# python find_food.py -z 02110
# 
# -z is optional and defaults to 02110 (Boston):
# 
#############################################

import json, csv, urllib2, simplejson, time
from optparse import OptionParser

def main():
    parser = OptionParser()
    parser.add_option("-z", "--zipcode", dest="zipcode", default="02110",
                      help="desired zip code to search")
    # parser.add_option("-q", "--quiet",
    #                   action="store_false", dest="verbose", default=True,
    #                   help="don't print status messages to stdout")

    (options, args) = parser.parse_args()
    zipcode = options.zipcode

    meetup_key = get_key()

    groups = gather_groups(zipcode, meetup_key)
    group_ids = []

    for each in groups:
        group_ids.append(str(each["id"]))

    # intentionally decrease set size for testing purposes
    group_ids = group_ids[:10]

    # Compile events
    # Start with the open_events (not tied to a particular Meetup Group)
    # Then add in the group_events (which would require membership in a group to 'attend' on Meetup)
    events = get_open_events(zipcode, meetup_key)
    for each in group_ids:
        events += get_group_events(each, meetup_key)
    print "Total events: " + str(len(events))

    # Determine keywords to search for
    # This will be expanded and refined later, to attempt to ascertain if the desired food and events are, indeed, free
    keywords = ["refreshments", "pizza", "food"]
    free_events = []

    # Step throught the descriptions of the accumulated events, looking for the desired keywords
    for each in events:
        try:
            desc = each["description"].encode('ascii', 'ignore')
            for word in keywords:
                if word in desc:
                    free_events.append(each)
        except:
            pass
    print "Events with keywords: " + str(len(free_events))

    # Export events with keywords to .csv file
    export_food_events(free_events)

    print "Done."

def get_key():
    # Get key from config.json file
    # If you don't have this file, see the comment at the top of this program
    f = open('config.json')
    key = json.load(f)["key"]
    f.close()
    return key

def hit_meetup(url):
    # Hit meetup.com with given url
    # Sleep for two seconds after each request, otherwise Meetup.com will get angry
    req = urllib2.Request(url)
    res = simplejson.loads(urllib2.urlopen(req).read())
    time.sleep(2.0)
    return res["results"]

def get_open_events(zipcode, meetup_key):
    print "Retrieving open events..."
    open_events_url = "http://api.meetup.com/2/open_events.json/?text_format=plain" + "&zip=" + zipcode + "&key=" + meetup_key
    return hit_meetup(open_events_url)

def gather_groups(zipcode, meetup_key):
    print "Gathering groups."
    groups_url = "http://api.meetup.com/2/groups.json/?" + "zip=" + zipcode + "&key=" + meetup_key
    return hit_meetup(groups_url)

def get_group_events(group_id, meetup_key):
    print "Retrieving group events for " + group_id + "..."
    group_events_url = "http://api.meetup.com/2/events.json/?text_format=plain" + "&group_id=" + group_id + "&key=" + meetup_key
    return hit_meetup(group_events_url)

def export_food_events(events):
    print "Exporting to csv..."
    f = csv.writer(open('food-events.csv', 'wb+'))

    f.writerow(["id", "name", "event_url", "description", "time", "status"])

    for each in events:
        f.writerow([
            each["id"],
            each["name"],
            each["event_url"],
            each["description"].encode('ascii', 'ignore'),
            each["status"].encode('ascii', 'ignore')
            ])

if __name__ == "__main__":
    main()