from django.db import models

class UserActivityTracker(models.Model):
    user_id = models.BigIntegerField()
    button_id = models.IntegerField()
    username = models.CharField(max_length = 250,null=True,blank=True,default=None)
    click_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_activity_tracker'