# Generated by Django 5.1.2 on 2024-10-20 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coach_nutr', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coachnutri',
            name='bio',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='coachnutri',
            name='profile_picture',
            field=models.ImageField(null=True, upload_to='user_pictures/'),
        ),
        migrations.AlterField(
            model_name='coachnutri',
            name='specialization',
            field=models.CharField(choices=[('fitness', 'Fitness'), ('yoga', 'Yoga')], max_length=50, null=True),
        ),
    ]