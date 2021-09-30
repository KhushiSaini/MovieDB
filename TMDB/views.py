from django.shortcuts import render, redirect
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Movies, Collection

from rest_framework_jwt.utils import jwt_payload_handler
from rest_framework_jwt.utils import jwt_encode_handler
from rest_framework_jwt.utils import jwt_response_payload_handler

from .serializers import MovieSerializer, CollectionSerializer, Edit_CollectionSerializer, Insert_MovieSerializer
#from rest_framework.permissions import IsAuthenticated
#from rest_framework.authentication import TokenAuthentication

from rest_framework.pagination import PageNumberPagination
from rest_framework import pagination
from .mypaginations import MyCursorPagination
from django.core.paginator import Paginator
from rest_framework import status

#from TMDB.customauth import CustomAuthentication
from rest_framework.generics import ListAPIView



# Create your views here.
class ResponsePagination(PageNumberPagination):
	page_query_param = 'p'
	page_size = 5
	page_size_query_param = 'page_size'
	max_page_size =3

class MovieApiView(ListAPIView):
	queryset = Movies.objects.all()
	serializer_class=MovieSerializer
	#authentication_classes=[CustomAuthentication]
	#permission_classes=[IsAuthenticated]
	#pagination_class=MyCursorPagination
	
	def get(self,request):

		"""allMovies=Movie.objects.all().values()
								return Response({"Message":"List of Movies","Count":Movie.objects.count(), "Movie List":allMovies})
						"""
		response=requests.get('https://api.themoviedb.org/3/movie/top_rated?api_key=e02e4c9c4a5c80784abee76fcc5ab326').json()
		#print(response)
		results=response['results']
		data=[{"title":res['original_title'], "description":res['overview'], "genres":res['genre_ids'], "uuid":res['id']} for res in results]

		#For Pagination
		paginator = ResponsePagination()
		resultss = paginator.paginate_queryset(data, request)
		serializer = MovieSerializer(resultss, many=True, context={'request':request}) 
		return paginator.get_paginated_response(serializer.data)


		"""allMovies=Movie.objects.all().values()
								return Response({"Message":"List of Movies","Count":Movie.objects.count(), "Data":data})
						"""

	"""def post(self,request):
					print('Request data is :',request.data)
					serializer_obj=MovieSerializer(data=request.data)
					if(serializer_obj.is_valid()):
			
			
			
						Movie.objects.create(uuid=serializer_obj.data.get("uuid"),
										 	title=serializer_obj.data.get("title"),
										 	description=serializer_obj.data.get("description"),
										 	genres=serializer_obj.data.get("genres")
										 	)
					
					movie=Movie.objects.all().filter(uuid=request.data["uuid"]).values()
					return Response({"Message":"New Movie Added!!!", "Movie":movie})"""


def Main(request):
	response=requests.get('https://api.themoviedb.org/3/movie/top_rated?api_key=e02e4c9c4a5c80784abee76fcc5ab326').json()
	#print(response)
	results=response['results']

	original_title=[i['original_title'] for i in results]
	overview=[j['overview'] for j in results]


	print(results)	
	return render(request, 'TMDB/home.html',{'response':response, 
		'results':results, 'original_title':original_title, 'overview' :overview })


class CollectionApiView(ListAPIView):
	queryset = Collection.objects.all()
	serializer_class=CollectionSerializer

	def get(self,request):
		allCollections=Collection.objects.all().values()
		data=[{ "uuid":res['uuid'], "title":res['title'], "description":res['description']} for res in allCollections]

		return Response({"Message":"List of Collection", "Collections":data, "Favourite_Genres": "Action, Drama, Science Fiction"})

	def post(self,request):
		#print('Request data is :',request.data)
		serializer_obj=CollectionSerializer(data=request.data)
		if(serializer_obj.is_valid()):	
			Collection.objects.create(uuid=serializer_obj.data.get("uuid"),
						 	title=serializer_obj.data.get("title"),
						 	description=serializer_obj.data.get("description"),
						 	#fav_genres=serializer_obj.data.get("genres")
						 	muuid=serializer_obj.data.get("muuid"),
						 	mtitle=serializer_obj.data.get("mtitle"),
						 	mdescription=serializer_obj.data.get("mdescription"),
						 	mgenres=serializer_obj.data.get("mgenres"),
						 	)

		collection=Collection.objects.all().filter(uuid=request.data["uuid"]).values()
		movies=[{"muuid":d['muuid'], "mtitle":d['mtitle'], "mdescription":d['mdescription'], "mgenres":d['mgenres']} for d in collection]
		data=[{ "uuid":d['uuid'], "title":d['title'], "description":d['description'], "movies":movies} for d in collection]
		return Response({"Message":"New Collection Added!!!", "Collection":data})

class Edit_Collection(ListAPIView):
	queryset = Collection.objects.all()
	serializer_class=Edit_CollectionSerializer

	def get_object(self,pk):
		try:
			return Collection.objects.get(pk=pk)
		except Collection.DoesNotExist:
			return Response(status=status.HTTP_400_BAD_REQUEST)

	def get(self,request,pk):
		coll_obj=self.get_object(pk)
		serializer_objj=Edit_CollectionSerializer(coll_obj)
		return Response(serializer_objj.data)


	def put(self,request,pk):
		coll_obj=self.get_object(pk)
		coll_serial=Edit_CollectionSerializer(coll_obj,data=request.data)
		if coll_serial.is_valid():
			coll_serial.save()
			return Response(coll_serial.data,status=status.HTTP_200_OK)
		return Response(coll_serial.errors,status=status.HTTP_400_BAD_REQUEST)


	def delete(self,request,pk):
		coll_obj=self.get_object(pk)
		coll_obj.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)


class Insert_Movies(ListAPIView):
	queryset = Movies.objects.all()
	serializer_class=Insert_MovieSerializer

	def get_object(self,cuuid):
		try:
			return Movies.objects.all().filter(cuuid=cuuid)
		except Movies.DoesNotExist:
			return Response(status=status.HTTP_400_BAD_REQUEST)

	def get(self,request,cuuid):
		mov_obj=self.get_object(cuuid)
		serializer_objj=Insert_MovieSerializer(mov_obj, many=True)
		movie=serializer_objj.data
		#data=[{"cuuid":res['cuuid'],"uuid":res['uuid'],"title":res['title'],"description":res['description'],"genres":res['genres']} for res in movie]
		collection=Collection.objects.all().filter(uuid=cuuid).values()
		coll_name=[{"title":d['title'],"description":d['description']} for d in collection]
		return Response({"Message":"List of Movies in Collection","Collection":coll_name,"Movies":movie})
		#return Response(serializer_objj.data)
		
	
	def post(self,request,cuuid):
		#print('Request data is :',request.data)
		serializer_obj=Insert_MovieSerializer(data=request.data)
		if(serializer_obj.is_valid()):	
			Movies.objects.create(uuid=serializer_obj.data.get("uuid"),
						 	title=serializer_obj.data.get("title"),
						 	description=serializer_obj.data.get("description"),
						 	genres=serializer_obj.data.get("genres"),
						 	cuuid=Collection.objects.get(uuid="uuid")
						 	)

		#movies=Movies.objects.all().filter(cuuid=request.data["cuuid"]).values()
		#data=[{"cuuid":d['cuuid'],"uuid":d['uuid'], "title":d['title'], "description":d['description'], "movies":movies} for d in movies]
		return Response({"Message":"New Movie Added to Collection!!!"})
		#, "Movies":data



"""
API Key: e02e4c9c4a5c80784abee76fcc5ab326

An example request looks like:

https://api.themoviedb.org/3/movie/550?api_key=e02e4c9c4a5c80784abee76fcc5ab326"""


