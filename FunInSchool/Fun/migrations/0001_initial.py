# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'ordering': ['name'],
                'db_table': 'city',
            },
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('gmt_create', models.DateTimeField(auto_now_add=True)),
                ('gmt_modify', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['name'],
                'db_table': 'class',
            },
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('city', models.ForeignKey(to='Fun.City')),
            ],
            options={
                'ordering': ['name'],
                'db_table': 'district',
            },
        ),
        migrations.CreateModel(
            name='Kid',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('age', models.IntegerField(verbose_name=3)),
                ('gender', models.CharField(max_length=1, choices=[('B', 'boy'), ('G', 'girl')])),
                ('head_portrait', models.ImageField(upload_to='portrait')),
                ('gmt_create', models.DateTimeField(auto_now_add=True)),
                ('gmt_modify', models.DateTimeField(auto_now_add=True)),
                ('class_id', models.ForeignKey(to='Fun.Class')),
            ],
            options={
                'ordering': ['name'],
                'db_table': 'Kid',
            },
        ),
        migrations.CreateModel(
            name='Moment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=250)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='moments')),
                ('gmt_create', models.DateTimeField(auto_now_add=True)),
                ('gmt_modify', models.DateTimeField(auto_now_add=True)),
                ('kid', models.ManyToManyField(to='Fun.Kid')),
            ],
            options={
                'ordering': ['title'],
                'db_table': 'moment',
            },
        ),
        migrations.CreateModel(
            name='ParentGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gmt_create', models.DateTimeField(auto_now_add=True)),
                ('gmt_modify', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField()),
                ('owner_parent_id', models.IntegerField()),
            ],
            options={
                'db_table': 'parentgroup',
            },
        ),
        migrations.CreateModel(
            name='Parents',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=250)),
                ('email', models.CharField(max_length=250)),
                ('telephone', models.CharField(unique=True, max_length=20)),
                ('gender', models.CharField(max_length=1, choices=[('m', '\u7537'), ('f', '\u5973')])),
                ('invitation_code', models.CharField(max_length=20)),
                ('relationshipWithCode', models.CharField(max_length=2, choices=[('p', '\u7236\u6bcd'), ('F', '\u4eb2\u621a'), ('PF', '\u7236\u6bcd\u670b\u53cb')])),
                ('age', models.IntegerField(verbose_name=3)),
                ('passwd', models.CharField(max_length=250)),
                ('head_portrait', models.ImageField(upload_to='portrait')),
                ('gmt_create', models.DateTimeField(auto_now_add=True)),
                ('gmt_modify', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['name'],
                'db_table': 'parents',
            },
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'ordering': ['name'],
                'db_table': 'province',
            },
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.CharField(unique=True, max_length=250)),
                ('name', models.CharField(max_length=50)),
                ('gmt_create', models.DateTimeField(auto_now_add=True)),
                ('gmt_modify', models.DateTimeField(auto_now_add=True)),
                ('district', models.ForeignKey(to='Fun.District')),
            ],
            options={
                'ordering': ['name'],
                'db_table': 'school',
            },
        ),
        migrations.CreateModel(
            name='SchoolAdministator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('telephone', models.CharField(unique=True, max_length=20)),
                ('email', models.CharField(max_length=250)),
                ('passwd', models.CharField(max_length=250)),
                ('gmt_create', models.DateTimeField(auto_now_add=True)),
                ('gmt_modify', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['name'],
                'db_table': 'schooladministator',
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=250)),
                ('telephone', models.CharField(unique=True, max_length=20)),
                ('gender', models.IntegerField(verbose_name=1, choices=[('m', '\u7537'), ('f', '\u5973')])),
                ('age', models.IntegerField(verbose_name=3)),
                ('head_portrait', models.ImageField(upload_to='portrait')),
                ('passwd', models.CharField(max_length=250)),
                ('gmt_create', models.DateTimeField(auto_now_add=True)),
                ('gmt_modify', models.DateTimeField(auto_now_add=True)),
                ('class_id', models.ForeignKey(to='Fun.Class')),
            ],
            options={
                'ordering': ['name'],
                'db_table': 'teacher',
            },
        ),
        migrations.AddField(
            model_name='school',
            name='school_admin',
            field=models.OneToOneField(to='Fun.SchoolAdministator'),
        ),
        migrations.AddField(
            model_name='parentgroup',
            name='parents',
            field=models.ManyToManyField(to='Fun.Parents'),
        ),
        migrations.AddField(
            model_name='kid',
            name='parentgroup',
            field=models.OneToOneField(to='Fun.ParentGroup'),
        ),
        migrations.AddField(
            model_name='kid',
            name='parents',
            field=models.ManyToManyField(to='Fun.Parents'),
        ),
        migrations.AddField(
            model_name='kid',
            name='teachers',
            field=models.ManyToManyField(to='Fun.Teacher'),
        ),
        migrations.AddField(
            model_name='class',
            name='school',
            field=models.ForeignKey(to='Fun.School'),
        ),
        migrations.AddField(
            model_name='city',
            name='province',
            field=models.ForeignKey(to='Fun.Province'),
        ),
        migrations.AlterOrderWithRespectTo(
            name='teacher',
            order_with_respect_to='class_id',
        ),
        migrations.AlterOrderWithRespectTo(
            name='school',
            order_with_respect_to='district',
        ),
        migrations.AlterOrderWithRespectTo(
            name='class',
            order_with_respect_to='school',
        ),
    ]
