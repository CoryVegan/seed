# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-06-07 21:10
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.contrib.postgres.fields.jsonb


class Migration(migrations.Migration):

    dependencies = [
        ('orgs', '0003_auto_20160412_1123'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('seed', '0067_auto_20170602_0740'),
    ]

    operations = [
        migrations.CreateModel(
            name='GreenAssessment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('award_body', models.CharField(blank=True, max_length=100, null=True)),
                ('recognition_type', models.CharField(choices=[('AWD', 'Award'), ('CRT', 'Certification'), ('LBL', 'Label'), ('PRT', 'Participant'), ('RAT', 'Rating'), ('SCR', 'Score'), ('ZER', 'Zero Energy Ready Home')], default='CRT', max_length=3)),
                ('description', models.TextField(blank=True, null=True)),
                ('is_numeric_score', models.BooleanField()),
                ('is_integer_score', models.BooleanField(default=True)),
                ('validity_duration', models.DurationField(blank=True, default=None, null=True)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orgs.Organization')),
            ],
        ),
        migrations.CreateModel(
            name='GreenAssessmentProperty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(blank=True, max_length=50, null=True)),
                ('status', models.CharField(blank=True, max_length=50, null=True)),
                ('status_date', models.DateField(blank=True, null=True)),
                ('_metric', models.FloatField(blank=True, null=True)),
                ('_rating', models.CharField(blank=True, max_length=100, null=True)),
                ('version', models.CharField(blank=True, max_length=50, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('target_date', models.DateField(blank=True, null=True)),
                ('eligibility', models.NullBooleanField()),
                ('_expiration_date', models.DateField(blank=True, null=True)),
                ('extra_data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={})),
                ('assessment', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='seed.GreenAssessment')),
                ('view', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seed.PropertyView')),
            ],
        ),
        migrations.CreateModel(
            name='GreenAssessmentPropertyAuditLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('changed_fields', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('record_type', models.IntegerField(blank=True, choices=[(0, 'ImportFile'), (1, 'UserEdit'), (2, 'UserCreate')], null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('ancestor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='gapauditlog__ancestor', to='seed.GreenAssessmentPropertyAuditLog')),
                ('greenassessmentproperty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gapauditlog__assessment', to='seed.GreenAssessmentProperty')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orgs.Organization')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='gapauditlog__parent', to='seed.GreenAssessmentPropertyAuditLog')),
                ('property_view', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='gapauditlog__view', to='seed.PropertyView')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GreenAssessmentURL',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('property_assessment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='urls', to='seed.GreenAssessmentProperty')),
            ],
        ),
        migrations.AlterField(
            model_name='propertyauditlog',
            name='record_type',
            field=models.IntegerField(blank=True, choices=[(0, 'ImportFile'), (1, 'UserEdit'), (2, 'UserCreate')], null=True),
        ),
        migrations.AlterField(
            model_name='taxlotauditlog',
            name='record_type',
            field=models.IntegerField(blank=True, choices=[(0, 'ImportFile'), (1, 'UserEdit'), (2, 'UserCreate')], null=True),
        ),
        migrations.AlterUniqueTogether(
            name='greenassessment',
            unique_together=set([('organization', 'name', 'award_body')]),
        ),
    ]
