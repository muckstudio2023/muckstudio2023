# Generated by Django 3.2.15 on 2023-08-13 21:42

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='LikedPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
    ]
