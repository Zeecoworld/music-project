from django import forms
from .models import MusicList

class MusicForm(forms.ModelForm):
    class Meta:
        model = MusicList
        fields = ['song_title', 'artist', 'album_cover', 'album_cover_url', 'spotify_youtube_url']
        widgets = {
            'song_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter song title',
                'required': True
            }),
            'artist': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter artist name',
                'required': True
            }),
            'album_cover': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'album_cover_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com/album-cover.jpg'
            }),
            'spotify_youtube_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://open.spotify.com/... or https://youtube.com/...',
                'required': True
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        song_title = cleaned_data.get('song_title', '').strip()
        artist = cleaned_data.get('artist', '').strip()
        
        if not song_title:
            self.add_error('song_title', 'Song title cannot be empty.')
        
        if not artist:
            self.add_error('artist', 'Artist name cannot be empty.')
        
        return cleaned_data
    

class SearchForm(forms.Form):
    search_query = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by artist or song title...',
        })
    )