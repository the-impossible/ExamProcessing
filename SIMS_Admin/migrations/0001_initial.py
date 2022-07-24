# Generated by Django 4.0 on 2021-12-30 11:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('SIMS_Authentication', '0002_alter_accounts_options_remove_accounts_username_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Levels',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Classes',
                'db_table': 'Classes',
            },
        ),
        migrations.CreateModel(
            name='StaffRoles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Roles',
                'db_table': 'Staff Roles',
            },
        ),
        migrations.CreateModel(
            name='StudentRoles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Roles',
                'db_table': 'Student Roles',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('studentID', models.CharField(db_index=True, max_length=10, unique=True)),
                ('acct', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='SIMS_Authentication.accounts')),
                ('level', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='SIMS_Admin.levels')),
                ('role', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='SIMS_Admin.studentroles')),
            ],
            options={
                'verbose_name_plural': 'Students',
            },
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('staffID', models.CharField(db_index=True, max_length=10, unique=True)),
                ('email', models.CharField(db_index=True, max_length=10, unique=True)),
                ('phone', models.CharField(db_index=True, max_length=14, unique=True)),
                ('acct', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='SIMS_Authentication.accounts')),
                ('level', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='SIMS_Admin.levels')),
                ('role', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='SIMS_Admin.staffroles')),
            ],
            options={
                'verbose_name_plural': 'Staffs',
            },
        ),
    ]