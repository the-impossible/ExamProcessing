# Generated by Django 4.0 on 2022-01-06 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SIMS_Authentication', '0003_alter_accounts_othername_alter_accounts_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounts',
            name='picture',
            field=models.ImageField(default='user.png', null=True, upload_to=''),
        ),
    ]