from __future__ import unicode_literals

from django.db.models import *
from django.db.models.fields.files import ImageField,ImageFieldFile

# Create your models here.

class Teacher(Model):
    user_name = CharField(max_length=20)
    real_name = CharField(max_length=20)
    address = CharField(max_length = 250)
    school = ForeignKey(School)
    kid = ManyToManyField(Kid)
    email = CharField(max_length = 250)
    telephone = CharField(max_length=20)
    gender = IntegerField(2)
    age = IntegerField(3)
    head_portrait = ImageField(upload_to='portrait')
    gmt_create = DateTimeField(auto_now_add = True)
    gmt_modify = DateTimeField(auto_now_add = True)

    class Meta:
        ordering=['user_name']
        db_table='teacher'
	order_with_respect_to = 'school'

    def __unicode__(self):
        return self.user_name


class School(Model):
    name = CharField(max_length=20,unique = True)
    address = TextField(unique = True)
    #description_txt = TextField()
    principal_telephone = CharField(max_length = 20)
    principal_email = CharField(max_length = 250)
    gmt_create = DateTimeField(auto_now_add = True)
    gmt_modify = DateTimeField(auto_now_add = True)

    class Meta:
        db_table = 'school'
        ordering=['name']

    def __unicode__(self):
        return self.name

GENDER_CHOICES_PARENT=(
    (u'M','male'),
    (u'F','feimale')
)

class Parents(Model):
    user_name= CharField(max_length=20)  
    real_name= CharField(max_length=20)  
    address = CharField(max_length = 250)
    kid = ManyToManyField(Kid)
    email = CharField(max_length = 250)
    telephone = CharField(max_length=20)
    gender = CharField(max_length=1,choices=GENDER_CHOICES_PARENT)
    age = IntegerField(3)
    head_portrait = ImageField(upload_to='portrait')
    gmt_create = DateTimeField(auto_now_add = True)
    gmt_modify = DateTimeField(auto_now_add = True)

    class Meta:
        db_table = 'parents'
        ordering = ['user_name']

    def __unicode__(self):
        return self.user_name


GENDER_CHOICES=(
    (u'B','boy'), #0
    (u'G','girl'), #1
)
 
class Kid(Model):
    name= CharField(max_length=20)  
    age = IntegerField(3)
    gender = CharField(max_length=1,choices = GENDER_CHOICES)
    head_portrait = ImageField(upload_to='portrait')
    moment = ManyToManyField(Moment)
    gmt_create = DateTimeField(auto_now_add = True)
    gmt_modify = DateTimeField(auto_now_add = True)

    class Meta:
        db_table = 'Kid'
        ordering = ['name']

    def __unicode__(self):
        return self.name

class Moment(Model):
    title = CharField(max_length = 250)
    description = TextField()
    kid = ManyToManyField(Kid)
    image = ImageField(upload_to='moments') 
    gmt_create = DateTimeField(auto_now_add = True)
    gmt_modify = DateTimeField(auto_now_add = True)

    class Meta:
        db_table = 'moment'
        ordering = ['title']

    def __unicode__(self):
        return self.title

    def _get_path(self):
        self._require_file()
        return self.storage.path(self.name)

    path = property(_get_path)

