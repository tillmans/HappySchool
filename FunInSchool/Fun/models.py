from __future__ import unicode_literals

from django.db.models import *
from django.db.models.fields.files import ImageField,ImageFieldFile

# Create your models here.

class Teacher(Model):
    user_name = CharField(max_length=20)
    real_name = CharField(max_length=20)
    address = CharField(max_length = 250)
    kindergarten_id = ForeignKey(Kindergarten)
    teacher_kid_list = ManyToManyField(Kid,through = 'Teacher_Kid')
    email = CharField(max_length = 250)
    telephone = CharField(max_length=20)

    class Meta:
        ordering=['user_name']
        db_table='teacher'

    def __unicode__(self):
        return self.user_name

class Teacher_Kid(Model):
    teacher = ForeignKey(Teacher) 
    kid = ForeignKey(Kid)

    class Meta:
        db_table = 'Teacher_Kid'
    

class Kindergarten(Model):
    name = CharField(max_length=20)
    address = TextField()

    class Meta:
        db_table = 'kindergarten'
        ordering=['name']

    def __unicode__(self):
        return self.name

class Parents(Model):
    user_name= CharField(max_length=20)  
    real_name= CharField(max_length=20)  
    address = CharField(max_length = 250)
    kidList = ManyToManyField(Kid,through='Parents_Kid')
    email = CharField(max_length = 250)
    telephone = CharField(max_length=20)

    class Meta:
        db_table = 'parents'
        ordering = ['user_name']

    def __unicode__(self):
        return self.user_name

class Parents_Kid(Model):
    parents = ForeignKey(Teacher) 
    kid = ForeignKey(Kid)

    class Meta:
        db_table = 'Parents_Kid'

GENDER_CHOICES=(
    (u'B','boy'), #0
    (u'G','girl'), #1
)
 
class Kid(Model):
    name= CharField(max_length=20)  
    age = IntegerField(3)
    gender = IntegerField(2)
    head_shot = ImageField(upload_to='photos')
    teacherlist = ManyToManyField(Teacher,through = 'Teacher_Kid')
    parentslist = ManyToManyField(Parents,through = 'Parents_Kid')
    photolist = ManyToManyField(Photo,through = 'Photo_Kid')

    class Meta:
        db_table = 'Kid'
        ordering = ['name']

    def __unicode__(self):
        return self.name

class Photo(Model):
    title = CharField(max_length = 250)
    description = TextField()
    kidlist = ManyToManyField(Kid,through = 'Photo_Kid')
    image = ImageField(upload_to='photos') 

    class Meta:
        db_table = 'photo'
        ordering = ['title']
    def __unicode__(self):
        return self.title

    def _get_path(self):
        self._require_file()
        return self.storage.path(self.name)

    path = property(_get_path)

