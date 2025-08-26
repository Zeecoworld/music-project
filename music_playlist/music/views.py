from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from .models import MusicList
from .forms import MusicForm, SearchForm

def music_list_view(request):
    """List View: Show all songs with search functionality"""
    songs = MusicList.objects.all()
    search_form = SearchForm(request.GET)
    
    # Handle search
    if search_form.is_valid():
        search_query = search_form.cleaned_data.get('search_query')
        if search_query:
            songs = songs.filter(
                Q(artist__icontains=search_query) | 
                Q(song_title__icontains=search_query)
            )
    
    context = {
        'songs': songs,
        'search_form': search_form,
        'total_songs': songs.count()
    }
    return render(request, 'music_list.html', context)

def add_music_view(request):
    """Add Music View: Form to add a new song"""
    if request.method == 'POST':
        form = MusicForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                song = form.save()
                messages.success(request, f'"{song.song_title}" by {song.artist} has been added successfully!')
                return redirect('music_list')
            except Exception as e:
                messages.error(request, f'Error saving song: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = MusicForm()
    
    context = {
        'form': form
    }
    return render(request, 'add_song.html', context)