# Generated by Django 4.2.7 on 2023-11-07 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0003_book_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='chapter',
            field=models.TextField(),
        ),
    ]