from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=100)
    close_at = models.DateField(null=True)

class devices(models.Model):
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    type = models.TextField()
    osType = models.CharField(max_length=50,null=True)
    version = models.CharField(max_length=50,null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    keeper = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    status = models.CharField(max_length=30)
    bookedFrom = models.DateTimeField(null=True)
    bookedTo = models.DateTimeField(null=True)

class order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    device = models.ForeignKey(devices, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=30, default='Requesting')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    orderFrom = models.DateTimeField()
    orderTo = models.DateTimeField()

class supplement(models.Model):
    name = models.CharField(max_length=100)
    type = models.TextField()
    osType = models.CharField(max_length=50, null=True)
    version = models.CharField(max_length=50, null=True)
    quantity = models.IntegerField(default=1)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=30, default='Requesting')
    createdAt = models.DateTimeField(null=True)

