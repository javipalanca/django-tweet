# -*- coding: utf-8 -*-
from django.contrib.gis.db import models
from django.contrib.postgres.fields import HStoreField


class Tweet(models.Model):

    id = models.BigIntegerField(primary_key=True)
    author = models.ForeignKey('User', related_name='tweets')

    created_at = models.DateTimeField()

    text = models.TextField()

    favorited = models.BooleanField(default=False)
    retweeted = models.BooleanField(default=False)
    truncated = models.BooleanField(default=False)

    source = models.CharField(max_length=100)
    source_url = models.URLField(null=True)

    lang = models.CharField(max_length=10)

    favorite_count = models.PositiveIntegerField()
    retweet_count = models.PositiveIntegerField()
    replies_count = models.PositiveIntegerField(null=True)

    in_reply_to_status = models.BigIntegerField('Replies', null=True)
    in_reply_to_user = models.BigIntegerField('Replies', null=True)

    favorites_users = models.ManyToManyField('User', related_name='favorites')
    retweeted_status = models.BigIntegerField('Retweets', null=True)

    possibly_sensitive = models.NullBooleanField()
    is_quote_status = models.BooleanField(default=False)
    quoted_status_id = models.BigIntegerField('Quoted', null=True)

    contributors = HStoreField(null=True)

    place = models.ForeignKey("Place", null=True)

    coordinates = models.PointField(null=True)
    geo = models.PointField(null=True)

    entities = HStoreField(null=True)

    objects = models.GeoManager()

    def __unicode__(self):
        return u'%s: %s' % (self.author, self.text)

    class Meta:
        ordering = ["-created_at"]
        index_together = ["created_at", "coordinates"]


class Place(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    full_name = models.CharField(max_length=200)
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=100)
    country_code = models.CharField(max_length=4)
    bounding_box = models.PolygonField()
    place_type = models.CharField(max_length=50)
    url = models.URLField()
    contained_within = HStoreField(null=True)
    attributes = HStoreField(null=True)

    objects = models.GeoManager()

    def __unicode__(self):
        return u'%s' % self.name


class User(models.Model):

    id = models.BigIntegerField(primary_key=True)
    screen_name = models.CharField(u'Screen name', max_length=50, unique=True)

    name = models.CharField(u'Name', max_length=100)
    description = models.TextField(u'Description')
    location = models.CharField(u'Location', max_length=100)
    time_zone = models.CharField(u'Time zone', max_length=100, null=True)
    lang = models.CharField(max_length=10)

    created_at = models.DateTimeField()

    contributors_enabled = models.NullBooleanField(u'Contributors enabled', default=False)
    default_profile = models.NullBooleanField(u'Default profile', default=False)
    default_profile_image = models.NullBooleanField(u'Default profile image', default=False)
    follow_request_sent = models.NullBooleanField(u'Follow request sent', default=False)
    following = models.NullBooleanField(u'Following', default=False)
    geo_enabled = models.NullBooleanField(u'Geo enabled', default=False)
    is_translator = models.NullBooleanField(u'Is translator', default=False)
    is_translation_enabled = models.NullBooleanField(u'Is translation enable', default=False)
    has_extended_profile = models.NullBooleanField(u'Has extended profile', default=False)
    notifications = models.NullBooleanField(u'Notifications', default=False)
    profile_use_background_image = models.NullBooleanField(u'Profile use background image', default=False)
    protected = models.NullBooleanField(u'Protected', default=False)
    verified = models.NullBooleanField(u'Verified', default=False)

    profile_background_image_url = models.URLField(max_length=300)
    profile_background_image_url_https = models.URLField(max_length=300)
    profile_background_tile = models.NullBooleanField(default=False)
    profile_background_color = models.CharField(max_length=6)
    profile_banner_url = models.URLField(max_length=300)
    profile_image_url = models.URLField(max_length=300)
    profile_image_url_https = models.URLField(max_length=300)
    url = models.URLField(max_length=300, null=True)

    profile_link_color = models.CharField(max_length=6)
    profile_sidebar_border_color = models.CharField(max_length=6)
    profile_sidebar_fill_color = models.CharField(max_length=6)
    profile_text_color = models.CharField(max_length=6)

    favourites_count = models.PositiveIntegerField()
    followers_count = models.PositiveIntegerField()
    friends_count = models.PositiveIntegerField()
    listed_count = models.PositiveIntegerField()
    statuses_count = models.PositiveIntegerField()
    utc_offset = models.IntegerField(null=True)

    entities = HStoreField(null=True)

    followers = models.ManyToManyField('User')

    objects = models.GeoManager()

    def __unicode__(self):
        return self.name