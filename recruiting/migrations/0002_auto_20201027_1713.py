# Generated by Django 3.1.2 on 2020-10-27 14:13

from django.conf import settings
from django.contrib.auth.models import User
from django.db import migrations, models
import django.db.models.deletion

from recruiting.models import Company


def company_owner_update(apps, schema_editor):
    for company in Company.objects.all():
        new_user = User.objects.create_user(username=f'{company.name} owner', password='1234')
        company.owner = new_user
        company.save()


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recruiting', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='owner',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE,
                                       to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='ApplicationResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('written_username', models.CharField(max_length=100)),
                ('written_phone', models.CharField(max_length=12)),
                ('written_cover_letter', models.CharField(max_length=300)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications',
                                           to=settings.AUTH_USER_MODEL)),
                ('vacancy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications',
                                              to='recruiting.vacancy')),
            ],
        ),
        migrations.RunPython(company_owner_update)
    ]
