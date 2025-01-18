# Generated by Django 5.1.3 on 2025-01-07 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume_app', '0003_remove_additionalcourse_completion_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('image_path', models.ImageField(upload_to='templates/images/')),
            ],
        ),
    ]
