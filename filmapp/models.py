from django.db import models



class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    genre = models.CharField(max_length=50)
    director = models.CharField(max_length=255)  # Field for the movie's director
    cast = models.TextField()  # Field for the movie's cast
    language = models.CharField(max_length=50,null=True,default='none')
    image = models.ImageField(upload_to='movies/', null=True, blank=True)
    is_active = models.BooleanField(default=True) 

    def __str__(self):
        return self.title



