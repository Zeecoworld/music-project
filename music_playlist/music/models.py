from django.db import models
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

class MusicList(models.Model):
    song_title = models.CharField(max_length=200, help_text="Enter the song title")
    artist = models.CharField(max_length=200, help_text="Enter the artist name")
    album_cover = models.ImageField(upload_to='album_covers/', blank=True, null=True, help_text="Upload album cover image")
    album_cover_url = models.URLField(blank=True, null=True, help_text="Or provide URL for album cover")
    spotify_youtube_url = models.URLField(help_text="Spotify or YouTube embed link")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Music"
        verbose_name_plural = "Music List"
    
    def __str__(self):
        return f"{self.song_title} by {self.artist}"
    
    def clean(self):
        if not self.song_title.strip():
            raise ValidationError({'song_title': 'Song title cannot be empty.'})
        if not self.artist.strip():
            raise ValidationError({'artist': 'Artist name cannot be empty.'})
        
        if self.spotify_youtube_url:
            if not any(domain in self.spotify_youtube_url.lower() for domain in ['spotify.com', 'youtube.com', 'youtu.be']):
                raise ValidationError({'spotify_youtube_url': 'Please provide a valid Spotify or YouTube URL.'})
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    @property
    def get_album_cover(self):
        """Return album cover URL (uploaded file or external URL)"""
        if self.album_cover:
            return self.album_cover.url
        elif self.album_cover_url:
            return self.album_cover_url
        return None