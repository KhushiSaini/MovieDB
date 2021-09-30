from django.db import models
from django.db.models import CharField, Model
from django_mysql.models import ListCharField


# Create your models here.


class Collection(models.Model):
	uuid=models.IntegerField(primary_key=True)
	title=models.CharField(max_length=100)
	description=models.CharField(max_length=200)
	muuid=models.IntegerField()
	mtitle=models.CharField(max_length=100)
	mdescription=models.CharField(max_length=500)
	mgenres=ListCharField(base_field=CharField(max_length=20), size=3, max_length=(6 * 11))

	"""def __str__(self):
					return str(self.uuid+"|"+self.title+"|"+self.description+"|"+self.muuid+"|"+self.mtitle+"|"+self.mdescription+"|"+self.mgenres)
			"""

class Movies(models.Model):
	uuid=models.IntegerField(primary_key=True)
	title=models.CharField(max_length=100)
	description=models.CharField(max_length=200)
	genres=models.CharField(max_length=40)
	cuuid=models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='display')

	"""def __str__(self):
					return str(self.uuid)+"|"+self.title+"|"+self.description+"|"+self.genre
					"""