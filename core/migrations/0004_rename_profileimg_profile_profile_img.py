# Generated by Django 4.2.3 on 2023-08-02 09:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_rename_profile_img_profile_profileimg'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='profileimg',
            new_name='profile_img',
        ),
    ]
