# Generated by Django 4.2.4 on 2023-08-27 21:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
        ('repairs', '0002_repair_owner'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='repair',
            options={'ordering': ['-created']},
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(blank=True, null=True)),
                ('value', models.CharField(choices=[('up', 'Up Vote'), ('down', 'Down Vote')], max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.profile')),
                ('repair', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repairs.repair')),
            ],
            options={
                'unique_together': {('owner', 'repair')},
            },
        ),
    ]
