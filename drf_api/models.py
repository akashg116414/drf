from django.db import models

class Person(models.Model):            
    userid = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.CharField(unique=True, max_length=150)
    userdob = models.DateField()
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    flag = models.IntegerField(default=1)

    class Meta:
        db_table = "person"
