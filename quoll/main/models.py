from django.db import models


class Venue(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Artist(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=150, default='')
    url = models.URLField(max_length=2083, default='')
    image = models.URLField(max_length=2083, default='')
    body = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    price = models.CharField(max_length=50, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    # relationship
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    artists = models.ManyToManyField(Artist)

    def __str__(self):
        return self.title
