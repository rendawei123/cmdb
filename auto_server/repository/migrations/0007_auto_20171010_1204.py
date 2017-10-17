# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-10 04:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0006_server_server_status_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, verbose_name='用户名')),
                ('password', models.CharField(max_length=32, verbose_name='密码')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='repository.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='BusinessUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='业务线')),
            ],
            options={
                'verbose_name_plural': '业务线表',
            },
        ),
        migrations.CreateModel(
            name='ErrorLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=16)),
                ('content', models.TextField()),
                ('create_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': '错误日志表',
            },
        ),
        migrations.CreateModel(
            name='IDC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='机房')),
                ('floor', models.IntegerField(default=1, verbose_name='楼层')),
            ],
            options={
                'verbose_name_plural': '机房表',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='标签')),
            ],
            options={
                'verbose_name_plural': '标签表',
            },
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
                ('users', models.ManyToManyField(to='repository.UserProfile')),
            ],
            options={
                'verbose_name_plural': '用户组表',
            },
        ),
        migrations.AddField(
            model_name='server',
            name='cabinet_num',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='机柜号'),
        ),
        migrations.AddField(
            model_name='server',
            name='cabinet_order',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='机柜中序号'),
        ),
        migrations.AddField(
            model_name='errorlog',
            name='server_obj',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='repository.Server'),
        ),
        migrations.AddField(
            model_name='businessunit',
            name='contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='c', to='repository.UserGroup'),
        ),
        migrations.AddField(
            model_name='businessunit',
            name='manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='m', to='repository.UserGroup'),
        ),
        migrations.AddField(
            model_name='server',
            name='business_unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='repository.BusinessUnit'),
        ),
        migrations.AddField(
            model_name='server',
            name='idc',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='repository.IDC'),
        ),
        migrations.AddField(
            model_name='server',
            name='tags',
            field=models.ManyToManyField(to='repository.Tag'),
        ),
    ]