# Generated by Django 3.1.7 on 2021-05-08 22:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bbapp', '0017_remove_book_reported'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(blank=True, default=uuid.uuid4, max_length=100, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('book', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='book', to='bbapp.book')),
                ('buyer', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='buyer', to=settings.AUTH_USER_MODEL)),
                ('seller', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='seller', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]