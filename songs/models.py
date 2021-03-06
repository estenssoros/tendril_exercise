from __future__ import unicode_literals

from django.db import models


class Song(models.Model):
    track_id = models.CharField(primary_key=True, max_length=18)
    title = models.CharField(max_length=256, blank=True, null=True)
    song_id = models.CharField(max_length=18, blank=True, null=True)
    release = models.CharField(max_length=256, blank=True, null=True)
    artist_id = models.CharField(max_length=18, blank=True, null=True)
    artist_mbid = models.CharField(max_length=36, blank=True, null=True)
    artist_name = models.CharField(max_length=256, blank=True, null=True)
    duration = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    artist_familiarity = models.DecimalField(max_digits=7, decimal_places=6, blank=True, null=True)
    artist_hotttnesss = models.DecimalField(max_digits=7, decimal_places=6, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    sha256 = models.CharField(max_length=64, blank=True, null=True)
    u_artist_name = models.CharField(max_length=256, blank=True, null=True)
    my_songs = models.IntegerField(blank=True, null=True, default=0)

    class Meta:
        db_table = 'songs'
        verbose_name = 'song'
        verbose_name_plural = 'songs'
