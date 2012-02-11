from ajax_select import LookupChannel
from django.utils.html import escape
from django.db.models import Q
from vinyl.models import *

class GenreLookup(LookupChannel):
    model = Genre

    def get_query(self,q,request):
        return Genre.objects.filter(Q(genre_name__icontains=q)).order_by('genre_name')

    def get_result(self,obj):
        u""" result is the simple text that is the completion of what the person typed """
        return obj.genre_name

    def format_match(self,obj):
        """ (HTML) formatted item for display in the dropdown """
        return self.format_item_display(obj)

    def format_item_display(self,obj):
        """ (HTML) formatted item for displaying item in the selected deck area """
        return u"<div><i>%s</i></div>" % (escape(obj.genre_name))
    def check_auth(self, request):
        return True

class ArtistLookup(LookupChannel):
    model = Artist

    def get_query(self,q,request):
        return Artist.objects.filter(Q(name__icontains=q)).order_by('name')

    def get_result(self,obj):
        u""" result is the simple text that is the completion of what the person typed """
        return obj.name

    def format_match(self,obj):
        """ (HTML) formatted item for display in the dropdown """
        return self.format_item_display(obj)

    def format_item_display(self,obj):
        """ (HTML) formatted item for displaying item in the selected deck area """
        return u"<div><i>%s</i></div>" % (escape(obj.name))
    def check_auth(self, request):
        return True

class SoundtrackTitleLookup(LookupChannel):
    model = Soundtrack
    def get_query(self,q,request):
        return Soundtrack.objects.filter(Q(title__icontains=q)).order_by('title')
    def get_result(self,obj):
        u""" result is the simple text that is the completion of what the person typed """
        return obj.title
    def format_match(self,obj):
        """ (HTML) formatted item for display in the dropdown """
        return self.format_item_display(obj)
    def format_item_display(self,obj):
        """ (HTML) formatted item for displaying item in the selected deck area """
        return u"<div><i>%s</i></div>" % (escape(obj.title))
    def check_auth(self, request):
        return True

class MusicplayerLookup(LookupChannel):
    model = Musicplayer
    def get_query(self,q,request):
        return Musicplayer.objects.filter(Q(player_name__icontains=q)).order_by('player_name')
    def get_result(self,obj):
        u""" result is the simple text that is the completion of what the person typed """
        return obj.player_name
    def format_match(self,obj):
        """ (HTML) formatted item for display in the dropdown """
        return self.format_item_display(obj)
    def format_item_display(self,obj):
        """ (HTML) formatted item for displaying item in the selected deck area """
        return u"<div><i>%s</i></div>" % (escape(obj.player_name))
    def check_auth(self, request):
        return True