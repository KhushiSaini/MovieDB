from django.contrib import admin
from .models import Movies, Collection
# Register your models here.
@admin.register(Movies)
class MoviesAdmin(admin.ModelAdmin):
	list_display = ['uuid', 'title', 'description', 'genres','cuuid']
	#readonly_fields=['cuuid']


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
	list_display = ['uuid', 'title', 'description', 'muuid', 'mtitle', 'mdescription', 'mgenres']
	#'fav_genres'