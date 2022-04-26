from django.db import models

# Create your models here.
class Dataset_info(models.Model):
    dname = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    date_time = models.CharField(max_length=100)
    link = models.CharField(max_length=255)
    access_type = models.CharField(max_length=100)
    need_UA = models.CharField(max_length=45)
    UA = models.CharField(max_length=1000)

class Approved_req(models.Model):
    dname = models.CharField(max_length=100)
    cname = models.CharField(max_length=100)

class Pending_req(models.Model):
    dname = models.CharField(max_length=100)
    cname = models.CharField(max_length=100)

class Rejected_req(models.Model):
    dname = models.CharField(max_length=100)
    cname = models.CharField(max_length=100)

class user_details(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)