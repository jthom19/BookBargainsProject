# Generated by Django 3.1.7 on 2021-05-07 18:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bbapp', '0016_book_isbn13conf'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='reported',
        ),
    ]