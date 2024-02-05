# Generated by Django 4.2.7 on 2024-02-05 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_remove_accountinvitation_is_accepted_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='is_setup',
        ),
        migrations.RemoveField(
            model_name='accountdomain',
            name='is_pending',
        ),
        migrations.RemoveField(
            model_name='accountdomain',
            name='is_valid',
        ),
        migrations.AddField(
            model_name='account',
            name='domains',
            field=models.ManyToManyField(related_name='account_domains', to='account.accountdomain'),
        ),
        migrations.AddField(
            model_name='account',
            name='invitations',
            field=models.ManyToManyField(related_name='account_invitations', to='account.accountinvitation'),
        ),
        migrations.AddField(
            model_name='account',
            name='status',
            field=models.CharField(default='draft', max_length=30),
        ),
        migrations.AddField(
            model_name='account',
            name='users',
            field=models.ManyToManyField(related_name='account_users', to='account.accountuser'),
        ),
        migrations.AddField(
            model_name='accountdomain',
            name='status',
            field=models.CharField(default='draft', max_length=30),
        ),
    ]
