# Generated by Django 3.1 on 2020-09-02 08:34

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Mywebsite', '0003_auto_20200902_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tb_news',
            name='news_detail',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
