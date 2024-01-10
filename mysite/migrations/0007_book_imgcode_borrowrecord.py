# Generated by Django 4.2.4 on 2024-01-10 05:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0006_customuser_customgroup'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='imgcode',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='BorrowRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('borrow_date', models.DateField()),
                ('return_date', models.DateField(blank=True, null=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mysite.book')),
                ('borrower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mysite.customuser')),
            ],
        ),
    ]
