# Generated by Django 5.1.4 on 2025-03-15 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0019_basicdetails_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='educationdetails',
            name='academic_gap',
            field=models.CharField(choices=[('YES', 'Yes'), ('NO', 'No')], default=None, max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='educationdetails',
            name='gap_duration',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='educationdetails',
            name='gap_from',
            field=models.DateField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='educationdetails',
            name='gap_reason',
            field=models.TextField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='educationdetails',
            name='gap_to',
            field=models.DateField(default=None, null=True),
        ),
    ]
