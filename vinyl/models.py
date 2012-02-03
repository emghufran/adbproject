from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

class UserProfile(models.Model):
	mid_name = models.CharField(max_length=128, null=True)
	phone = models.CharField(max_length= 32, null=True)
	address = models.CharField(max_length=256, null=True)
	profile_pic = models.CharField(max_length=1024, null=True)
	language = models.CharField(max_length=8, null=True)
	user = models.ForeignKey(User)

admin.site.register(UserProfile)
#class User(models.Model):
#    username = models.CharField(max_length=128, unique=True)
#    password = models.CharField(max_length=128)
#    first_name = models.CharField(max_length=128)
#    mid_name = models.CharField(max_length=128, null=True)
#    last_name = models.CharField(max_length=128)
#    email = models.CharField(max_length=256)
#    phone = models.CharField(max_length= 32, null=True)
#    address = models.CharField(max_length=256, null=True)
#    profile_pic = models.CharField(max_length=1024, null=True)
    
class Category(models.Model):
    category_name = models.CharField(max_length=128, unique=True)
    category_desc = models.CharField(max_length=256, null=True)
    no_of_disc = models.IntegerField(null=True)

admin.site.register(Category)
    
class Genre(models.Model):
    genre_name = models.CharField(max_length=32, unique=True)

admin.site.register(Genre)

class Artist(models.Model):
    name = models.CharField(max_length=128)
    artisttype = models.CharField(max_length=32, null=True)

admin.site.register(Artist)
    
class Musicplayer(models.Model):
    player_name = models.CharField(max_length=128, unique=True)

admin.site.register(Musicplayer)

class Playlist(models.Model):
    list_name = models.CharField(max_length=128)
    created_on = models.DateTimeField()
    is_published = models.BooleanField()
    published_on = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User)
    
    class Meta:
		unique_together = ('list_name', 'created_by',)
    
admin.site.register(Playlist)

class RecordLibrary(models.Model):
    library_type = models.CharField(max_length=32, null=True)
    is_published = models.NullBooleanField()
    userid = models.ForeignKey(User)

class SoundtrackAbstract(models.Model):
    title = models.CharField(max_length=256, null=True)
    release_date = models.DateTimeField(null=True)
    playing_time = models.TimeField(null=True)
    style = models.CharField(max_length=16, null=True)
    audio_engineer = models.CharField(max_length=128, null=True)
    lyricist = models.CharField(max_length=128, null=True)
    music_writer = models.CharField(max_length=256, null=True)
    rythm = models.CharField(max_length=32, null=True)
    label = models.CharField(max_length=128, null=True)
    
    class Meta:
        abstract = True

class Soundtrack(SoundtrackAbstract):
    genre = models.ForeignKey(Genre, null=True)
    original_version = models.ForeignKey("Soundtrack", null=True) 
    player = models.ManyToManyField(Musicplayer, null=True)

admin.site.register(Soundtrack)
    
class RecordAbstract(models.Model):
    title = models.CharField(max_length=256)
    disk_size = models.CharField(max_length=32, null=True)
    matrix_nubmer = models.CharField(max_length=64, null=True)
    press_info = models.CharField(max_length=128, null=True)
    producer = models.CharField(max_length=128, null=True)
    
    class Meta:
        abstract = True
    
class Record(RecordAbstract):
    genre = models.ForeignKey(Genre)
    category = models.ForeignKey(Category, null=True)
    artist = models.ForeignKey(Artist, null=True)
    
admin.site.register(Record)

class Trackartist(models.Model):
    track = models.ForeignKey(Soundtrack)
    artist = models.ForeignKey(Artist)
    artisttype = models.CharField(max_length=1)
    
admin.site.register(Trackartist)

class Recordtrack(models.Model):
    track = models.ForeignKey(Soundtrack)
    record = models.ForeignKey(Record)
    order = models.IntegerField()
    disc_number = models.IntegerField()

admin.site.register(Recordtrack)
    
class Rating(models.Model):
    record = models.ForeignKey(Record)
    count = models.IntegerField()
    avg_rating = models.FloatField()

class Userrating(models.Model):
    rated_by = models.ForeignKey(User)
    rated_for = models.ForeignKey(Record)
    rated_on = models.DateTimeField()

class Comment(models.Model):
    commentor = models.ForeignKey(User)
    record = models.ForeignKey(Record)
    comment = models.TextField()
    commented_on = models.DateTimeField()

class RecordLibraryItem(models.Model):
    record = models.ForeignKey(Record)
    record_type = models.CharField(max_length=32, null=True)
    condition = models.CharField(max_length=32, null=True)
    user = models.force_unicode(User)
    library = models.ForeignKey(RecordLibrary) 

admin.site.register(RecordLibraryItem)

class PlaylistShare(models.Model):
    shared_to = models.ForeignKey(User, related_name='shared_user')
    playlist = models.ForeignKey(Playlist)
    shared_on = models.DateTimeField()
    created_by = models.ForeignKey(User, related_name='owner')

class CustomAttribute(models.Model):
    created_by = models.ForeignKey(User)
    field_name = models.CharField(max_length=128)
    field_desc = models.CharField(max_length=256)
    record = models.ForeignKey(Record)
    field_value = models.CharField(max_length=256)
    
    class Meta:
    	unique_together = ('created_by','field_name',)

class Revision(models.Model):
    revision_type = models.CharField(max_length=32)
    created_on = models.DateTimeField(null=True)
    user = models.ForeignKey(User)

class RecordArchive(RecordAbstract):
    category_id = models.IntegerField(null=True)
    genre_id = models.IntegerField(null=True)
    revision = models.ForeignKey(Revision)

class RecordtrackArchive(Recordtrack):
    revision = models.ForeignKey(Revision)
    
class SoundtrackArchive(Soundtrack):
    genre_id = models.IntegerField(null=True)
    revision = models.ForeignKey(Revision)

class TrackplayerArchive(models.Model):
    musicplayer = models.ForeignKey(Musicplayer)
    track = models.ForeignKey(SoundtrackArchive)
    revision = models.ForeignKey(Revision)

class TrackartistArchive(models.Model):
    track = models.ForeignKey(SoundtrackArchive)
    artist = models.ForeignKey(Artist)
    type = models.CharField(max_length=1)
    revision = models.ForeignKey(Revision)
        