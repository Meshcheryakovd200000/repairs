# Generated by Django 4.2.1 on 2023-06-30 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Repair',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('featured_image', models.ImageField(blank=True, default='default.jpg', null=True, upload_to='repairs/%Y/%m/%d')),
                ('demo_link', models.CharField(blank=True, max_length=200, null=True)),
                ('source_link', models.CharField(blank=True, max_length=200, null=True)),
                ('vote', models.IntegerField(default=0)),
                ('vote_percent', models.IntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('tags', models.ManyToManyField(blank=True, to='repairs.tag')),
            ],
        ),
    ]
