from django.utils.timezone import is_naive, make_aware
from dateutil.parser import parse
import datetime

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO
import json
import six

if six.PY3:
    unicode = str

__author__ = 'jpalanca'


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, datetime.timedelta):
            return (datetime.datetime.min + obj).time().isoformat()
        else:
            return super(DateTimeEncoder, self).default(obj)


def geojson_to_str(geojson_dict):
    if geojson_dict is None:
        return geojson_dict
    result = {}
    for k, v in geojson_dict.items():
        if isinstance(v, str) or isinstance(v, unicode):
            result[str(k)] = str(v)
        else:
            result[str(k)] = v
    return str(result)


def parse_date(dt):
    dt = parse(dt)
    if is_naive(dt):
        return make_aware(dt).isoformat()
    else:
        return dt.isoformat()


def parse_place(tweet):
    if tweet["place"] is None:
        return None
    place = tweet["place"]
    bb = place["bounding_box"]["coordinates"][0]
    # close polygon
    if bb[0] is not bb[-1]:
        bb.append(bb[0])
    place["bounding_box"] = geojson_to_str(place["bounding_box"])
    if not place["contained_within"]:
        del place["contained_within"]
    pre = [{
        "pk": place["id"],
        "model": "tweet.Place",
        "fields": place
    }]
    data = StringIO.StringIO()
    data.write(json.dumps(pre))
    data.seek(0)
    from django.core import serializers
    for deserialized_object in serializers.deserialize("json", data):
        data.close()
        return deserialized_object


def parse_user(tweet):
    user = tweet["user"]
    user["created_at"] = parse_date(user["created_at"])
    del user["id_str"]
    del user["entities"]
    if "profile_location" in user:
        del user["profile_location"]
    pre = [{
        "pk": user["id"],
        "model": "tweet.User",
        "fields": user
    }]

    data = StringIO.StringIO()
    data.write(json.dumps(pre))
    data.seek(0)
    from django.core import serializers
    for deserialized_object in serializers.deserialize("json", data):
        data.close()
        return deserialized_object


def parse_tweet(tweet):
    elements = []
    tweet["author"] = tweet["user"]["id"]
    elements.append(parse_user(tweet))
    tweet["created_at"] = parse_date(tweet["created_at"])
    del tweet["user"]
    del tweet["entities"]
    for skip in ["scopes", "withheld_in_countries", "withheld_scope"]:
        if skip in tweet:
            del tweet[skip]
    try:
        tweet["place"] = tweet["place"]["id"]
        elements.append(parse_place(tweet))
    except TypeError:
        tweet["place"] = None
    del tweet["id_str"]
    del tweet["metadata"]
    # set in_reply_to_user
    tweet["in_reply_to_user"] = tweet['in_reply_to_user_id']
    del tweet['in_reply_to_user_id']
    del tweet['in_reply_to_user_id_str']
    del tweet['in_reply_to_screen_name']
    # set in_reply_to_status
    tweet["in_reply_to_status"] = tweet['in_reply_to_status_id']
    del tweet['in_reply_to_status_id']
    del tweet['in_reply_to_status_id_str']
    # is retweet
    try:
        retweet = parse_tweet(tweet["retweeted_status"])
        elements += retweet
        tweet["retweeted_status"] = tweet["retweeted_status"]["id"]
    except KeyError:
        tweet["retweeted_status"] = None
    # is quoted tweet
    try:
        quoted = parse_tweet(tweet["quoted_status"])
        elements += quoted
        tweet["quoted_status"] = tweet["quoted_status"]["id"]
    except KeyError:
        tweet["quoted_status"] = None
    if "quoted_status_id_str" in tweet:
        del tweet["quoted_status_id_str"]
    if "quoted_status_id" in tweet:
        del tweet["quoted_status_id"]
    # prepare coordinates
    tweet["geo"] = geojson_to_str(tweet["geo"])
    tweet["coordinates"] = geojson_to_str(tweet["coordinates"])
    pre = [{
        "pk": tweet["id"],
        "model": "tweet.Tweet",
        "fields": tweet
    }]

    data = StringIO.StringIO()
    data.write(json.dumps(pre))
    data.seek(0)
    from django.core import serializers
    for deserialized_object in serializers.deserialize("json", data):
        data.close()
        elements.append(deserialized_object)
        return elements
