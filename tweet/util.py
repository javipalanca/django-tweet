try:
    import cStringIO as StringIO
except ImportError:
    import StringIO
import json
from django.utils.timezone import make_aware

import six

if six.PY3:
    unicode = str

__author__ = 'jpalanca'


def geojson_to_str(geojson_dict):
    result = {}
    for k, v in geojson_dict.items():
        if isinstance(v, str) or isinstance(v, unicode):
            result[str(k)] = str(v)
        else:
            result[str(k)] = v
    return str(result)


def parse_place(tweet):
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
    del user["id_str"]
    user["created_at"] = make_aware(user["created_at"]).isoformat()
    del user["entities"]
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
    tweet["author"] = tweet["user"]["id"]
    del tweet["user"]
    del tweet["entities"]
    tweet["place"] = tweet["place"]["id"]
    tweet["created_at"] = make_aware(tweet["created_at"]).isoformat()
    del tweet["id_str"]
    del tweet["metadata"]
    if "quoted_status" in tweet:
        del tweet["quoted_status"]
        del tweet["quoted_status_id_str"]
    # set in_reply_to_user
    tweet["in_reply_to_user"] = tweet['in_reply_to_user_id']
    del tweet['in_reply_to_user_id']
    del tweet['in_reply_to_user_id_str']
    del tweet['in_reply_to_screen_name']
    # set in_reply_to_status
    tweet["in_reply_to_status"] = tweet['in_reply_to_status_id']
    del tweet['in_reply_to_status_id']
    del tweet['in_reply_to_status_id_str']
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
        return deserialized_object
