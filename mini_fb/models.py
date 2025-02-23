# mini_fb/models.py
# these are our data objects n such
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.models import User
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    city = models.TextField(blank=False)
    email = models.TextField(blank=False)
    image_url = models.URLField(blank=True)
    firstname = models.TextField(blank=False)
    lastname = models.TextField(blank=False)
    def __str__(self):
        '''
        string of main obj profy
        '''
        return f'{self.firstname} {self.lastname}'
    def get_status_messages(self):
        return self.statusmessage_set.all().order_by('-timestamp')
    def get_absolute_url(self):
        return reverse('show_profile', kwargs={'pk': self.pk})
    def get_friends(self):
        friendships = Friend.objects.filter(Q(profile1=self) | Q(profile2=self))
        friends = []
        for friendship in friendships:
            if friendship.profile1 == self:
                friends.append(friendship.profile2)
            else:
                friends.append(friendship.profile1)
        return friends
    def add_friend(self, other):
        if self == other:
            print("cant friend ourself you lonely guy")
            return
        friendship_exists = Friend.objects.filter(
            (Q(profile1=self) & Q(profile2=other)) | (Q(profile1=other) & Q(profile2=self))
        ).exists()
        if not friendship_exists:
            friendship = Friend(profile1=self, profile2=other)
            friendship.save()
            print(f"Friendship created {self} {other}.")
        else:
            print(f"Friendship already have {self}  {other}.")
    def get_friend_suggestions(self):
        all_profiles = Profile.objects.exclude(pk=self.pk)
        friends = self.get_friends()
        suggestions = all_profiles.exclude(pk__in=[friend.pk for friend in friends])
        return suggestions
    def get_news_feed(self):
        friends = self.get_friends()
        profiles = [self] + friends
        news_feed = StatusMessage.objects.filter(profile__in=profiles).order_by('-timestamp')
        return news_feed
class StatusMessage(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    message = models.TextField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    def get_images(self):
        '''
        all images of this obj
        '''
        return self.image_set.all()
    
    def __str__(self):
        '''
        string of statusmsg
        '''
        return f"StatusMessage({self.profile.firstname} {self.profile.lastname} at {self.timestamp})"

class Image(models.Model):
    image_file = models.ImageField(upload_to='images/')
    status_message = models.ForeignKey('StatusMessage', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    def __str__(self):
        '''
        string of image instance
        '''
        return f"Image for StatusMessage {self.status_message.id} at {self.timestamp}"

class Friend(models.Model):
    profile1 = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='friend_set1'
    )
    profile2 = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='friend_set2'
    )
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.profile1.firstname} {self.profile1.lastname} & {self.profile2.firstname} {self.profile2.lastname}"