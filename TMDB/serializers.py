from rest_framework import serializers
from .models import Movies, Collection

# Create your models here.
class MovieSerializer(serializers.Serializer):
	uuid=serializers.IntegerField(label="Movie uuid")
	title=serializers.CharField(label="Movie Title")
	description=serializers.CharField(label="Overview")
	#genres=serializers.ArrayRefrenceField(label="Genres")
	genres=serializers.ListField(child = serializers.IntegerField())

	def __str__(self):
		return str(self.uuid)+"|"+self.title+"|"+self.description+"|"+self.genres

class CollectionSerializer(serializers.Serializer):
		uuid=serializers.IntegerField(label="Collection uuid")
		title=serializers.CharField(label="Collection Title", style={'placeholder': 'Name Of Collection'})
		description=serializers.CharField(label="Description of Collection")
		#fav_genres=serializers.CharField(label="Fav Genres")

		muuid=serializers.IntegerField(label="Movie uuid")
		mtitle=serializers.CharField(label="Movie Title")
		mdescription=serializers.CharField(label="Movie Overview")
		mgenres=serializers.CharField(label="Genres")

		def __str__(self):
			return str(self.uuid+"|"+self.title+"|"+self.description+"|"+self.muuid+"|"+self.mtitle+"|"+self.mdescription+"|"+self.mgenres)	

class Edit_CollectionSerializer(serializers.ModelSerializer):
	class Meta:
		model=Collection
		fields='__all__'
	
	
class Insert_MovieSerializer(serializers.ModelSerializer):
	class Meta:
		model=Movies
		fields=('uuid','title','description','genres','cuuid')
	