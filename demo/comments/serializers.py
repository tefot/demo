from .models import Comment, IPLockout
from rest_framework import serializers
from datetime import datetime, timedelta


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.ChoiceField(choices=[(value, value) for value in Comment.url_settings.valid_urls.split(',')])
    
    class Meta:
        model = Comment
        fields = ('username', 'comment', 'url', 'posting_ip', 'date_created')
        
    def validate(self, data):
        """
        Checks restrictions and creates lock out objects as necessary.
        """
        posting_ip = data.get('posting_ip')
        lock_outs = []
        # Check if the same comment has been posted within given time period
        if Comment.objects.filter(comment=data['comment'], 
                                  date_created__gt=datetime.now() - timedelta(hours=Comment.duplicate_restrictions.window_hours)).count() > Comment.duplicate_restrictions.max_duplicates:
            lock_outs.append((Comment.duplicate_restrictions.duplicate_lockout_minutes, Comment.duplicate_restrictions.duplicate_lockout_reason))
        # Check if the same user is posting too often
        if Comment.objects.filter(posting_ip=posting_ip, 
                                  date_created__gt=datetime.now() - timedelta(minutes=Comment.frequency_restrictions.window_minutes)).count() > Comment.frequency_restrictions.max_postings:
            lock_outs.append((Comment.frequency_restrictions.frequency_lockout_minutes, Comment.frequency_restrictions.frequency_lockout_reason))
            
        if lock_outs:
            reasons = []
            for minutes, reason in lock_outs:
                reasons.append(reason)
                IPLockout.objects.create(ip_address=posting_ip, 
                                         locked_until=datetime.now() + timedelta(minutes=minutes), 
                                         reason=reason)
            raise serializers.ValidationError("Unable to post comment: " + ', '.join(reasons))
        return data