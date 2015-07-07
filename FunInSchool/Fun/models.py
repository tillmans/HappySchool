#encoding:utf-8
from __future__ import unicode_literals

from django.db.models import *
from django.db.models.fields.files import ImageField,ImageFieldFile

# Create your models here.

class Province(Model):
    name = CharField(max_length = 20)
    class Meta:
	db_table = 'province'
	ordering = ['name']

    def __unicode__(self):
	return self.name

class City(Model):
    name = CharField(max_length = 20)
    province = ForeignKey(Province)
    class Meta:
	db_table = 'city'
	ordering = ['name']

    def __unicode__(self):
	return self.name

class District(Model):
    name = CharField(max_length = 20)
    city = ForeignKey(City)
    class Meta:
	db_table = 'district'
	ordering = ['name']

    def __unicode__(self):
	return self.name

class SchoolAdministator(Model):
    name = CharField(max_length = 20)
    telephone = CharField(max_length = 20,unique = True)
    email = CharField(max_length = 250)
    gmt_create = DateTimeField(auto_now_add = True)
    gmt_modify = DateTimeField(auto_now_add = True)
    passwd =  CharField(max_length = 250)
    #school = ForeignKey(School)

    class Meta:
        db_table = 'schooladministator'
        ordering=['name']

    def __unicode__(self):
        return self.name


class School(Model):
    address = CharField(max_length = 250,unique = True)
    #province = CharField(max_length = 20)
    #city = CharField(max_length = 20)
    #district = CharField(max_length = 20)
    school_admin = OneToOneField(SchoolAdministator)
    district = ForeignKey(District)
    name = CharField(max_length = 50)

    gmt_create = DateTimeField(auto_now_add = True)
    gmt_modify = DateTimeField(auto_now_add = True)

    class Meta:
        db_table = 'school'
        ordering=['name']
	order_with_respect_to = 'district'

    def __unicode__(self):
        return self.name



class Class(Model):
    name = CharField(max_length = 50)
    school = ForeignKey(School)
    gmt_create = DateTimeField(auto_now_add = True)
    gmt_modify = DateTimeField(auto_now_add = True)

    class Meta:
	db_table = 'class'
	ordering = ['name']
	order_with_respect_to = 'school'

    def __unicode__(self):
        return self.name


ADULT_GENDER=(
    (u'm','男'),
    (u'f','女')
)

TEACHER_STATUS=(
    (u'EP','审核通过'),
    (u'EF','审核未通过'),
    (u'EI','审核中'),
    (u'NE','未审核')
)

class Teacher(Model):
    name = CharField(max_length=20)
    class_id = ForeignKey(Class)
    email = CharField(max_length = 250)
    telephone = CharField(max_length=20,unique = True)
    gender = IntegerField(1,choices = ADULT_GENDER)
    age = IntegerField(3)
    head_portrait = ImageField(upload_to='portrait')
    passwd = CharField(max_length = 250)
    status = CharField(max_length = 2,choices = TEACHER_STATUS)
    gmt_create = DateTimeField(auto_now_add = True)
    gmt_modify = DateTimeField(auto_now_add = True)

    class Meta:
        ordering=['name']
        db_table='teacher'
	order_with_respect_to = 'class_id'

    def __unicode__(self):
        return self.name


RELATIONSHIPWITHCHILD=(
    (u'p','父母'),
    (u'F','亲戚'),
    (u'PF','父母朋友')
)

class Parents(Model):
    #user_name= CharField(max_length=20)  
    name= CharField(max_length=20)  
    address = CharField(max_length = 250)
    email = CharField(max_length = 250)
    telephone = CharField(max_length=20,unique = True)
    gender = CharField(max_length=1,choices=ADULT_GENDER)
    invitation_code = CharField(max_length = 20)
    relationshipWithCode=CharField(max_length = 2,choices = RELATIONSHIPWITHCHILD)
    age = IntegerField(3)
    passwd = CharField(max_length = 250)
    head_portrait = ImageField(upload_to='portrait')
    gmt_create = DateTimeField(auto_now_add = True)
    gmt_modify = DateTimeField(auto_now_add = True)

    class Meta:
        db_table = 'parents'
        ordering = ['name']

    def __unicode__(self):
        return self.name

class ParentGroup(Model):
    gmt_create = DateTimeField(auto_now_add = True)
    gmt_modify = DateTimeField(auto_now_add = True)
    description = TextField()
    parents = ManyToManyField(Parents)
    owner_parent_id = IntegerField()

    class Meta:
        db_table = 'parentgroup'

    def __unicode__(self):
        return self.description
 

GENDER_CHOICES=(
    (u'B','boy'), #0
    (u'G','girl'), #1
)

class Kid(Model):
    name= CharField(max_length=20)  
    age = IntegerField(3)
    gender = CharField(max_length=1,choices = GENDER_CHOICES)
    head_portrait = ImageField(upload_to='portrait')
    class_id = ForeignKey(Class)
    gmt_create = DateTimeField(auto_now_add = True)
    gmt_modify = DateTimeField(auto_now_add = True)
    teachers = ManyToManyField(Teacher)
    parents = ManyToManyField(Parents)
    parentgroup = OneToOneField(ParentGroup)

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

