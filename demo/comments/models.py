# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import dbsettings

class DuplicateRestriction(dbsettings.Group):
    max_duplicates = dbsettings.PositiveIntegerValue(help_text = "The maximum number of duplicate comments allowed during a given time period.",
                                                     default = 0)
    window_hours = dbsettings.PositiveIntegerValue(help_text = "The historic period (in hours) checked for duplicate comments.",
                                                   default = 24)
    duplicate_lockout_minutes = dbsettings.PositiveIntegerValue(help_text = "How long (in minutes) the ip address will be locked out if it violates this restriction.",
                                                      default = 1)
    duplicate_lockout_reason = dbsettings.StringValue(help_text = "Message sent with error indicating why lockout occurred.",
                                            default = "Duplicate comment")
    
class FrequencyRestriction(dbsettings.Group):
    max_postings = dbsettings.PositiveIntegerValue(help_text = "The maximum number of comments allowed during a given time period.",
                                                     default = 2)
    window_minutes = dbsettings.PositiveIntegerValue(help_text = "The historic period (in minutes) used for counting the number of comments posted by a given ip address.",
                                                   default = 1)
    frequency_lockout_minutes = dbsettings.PositiveIntegerValue(help_text = "How long (in minutes) the ip address will be locked out if it violates this restriction.",
                                                      default = 5)
    frequency_lockout_reason = dbsettings.StringValue(help_text = "Message sent with error indicating why lockout occurred.",
                                            default = "Too many comments posted")
    
class UrlSettings(dbsettings.Group):
    valid_urls = dbsettings.StringValue(help_text="**REQUIRES RESTART** Comma separated string of urls which can accept comments.",
                                        default="/low-altitude-launch,/planetary-motion,/pop-quiz")

class Comment(models.Model):
    # Model settings
    duplicate_restrictions = DuplicateRestriction("Duplicate Restrictions")
    frequency_restrictions = FrequencyRestriction("Frequency Restrictions")
    url_settings = UrlSettings("URL Settings")
    
    comment = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    posting_ip = models.CharField(max_length=64)
    url = models.CharField(max_length=256)
    username = models.CharField(max_length=256)
    
class IPLockout(models.Model):
    ip_address = models.CharField(max_length=64)
    locked_until = models.DateTimeField()
    reason = models.CharField(max_length=256)
