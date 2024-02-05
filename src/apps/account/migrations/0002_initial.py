# Generated by Django 4.2.7 on 2024-02-05 12:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
        ('data', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='accountuser',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='accountuser_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='accountuser',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='accountuser_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='accountinvitation',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.account'),
        ),
        migrations.AddField(
            model_name='accountinvitation',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='accountinvitation_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='accountinvitation',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='accountinvitation_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='accountdomain',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.account'),
        ),
        migrations.AddField(
            model_name='accountdomain',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='account',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.country'),
        ),
        migrations.AddField(
            model_name='account',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='account',
            name='timezone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.timezone'),
        ),
    ]
