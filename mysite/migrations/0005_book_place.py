# Generated by Django 4.2.7 on 2023-11-07 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0004_alter_book_chapter'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='place',
            field=models.CharField(choices=[('藏書中', '藏書中'), ('外借中', '外借中')], default='藏書中', max_length=5),
        ),
    ]
