from django.db import models

# Create your models here.
class Dataset_info(models.Model):
    dname = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    date_time = models.CharField(max_length=100)
    link = models.CharField(max_length=255)

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