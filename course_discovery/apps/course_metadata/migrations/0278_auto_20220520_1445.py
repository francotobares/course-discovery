# Generated by Django 3.2.13 on 2022-05-20 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_metadata', '0277_external_urls_help_text_updates'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='enterprise_subscription_inclusion',
            field=models.BooleanField(default=False, help_text='This field signifies if this course is in the enterprise subscription catalog'),
        ),
        migrations.AddField(
            model_name='courserun',
            name='enterprise_subscription_inclusion',
            field=models.BooleanField(default=False, help_text='Caculated field based on if course is included in enterprise subscription catalog, and course run is self-paced'),
        ),
        migrations.AddField(
            model_name='historicalcourse',
            name='enterprise_subscription_inclusion',
            field=models.BooleanField(default=False, help_text='This field signifies if this course is in the enterprise subscription catalog'),
        ),
        migrations.AddField(
            model_name='historicalcourserun',
            name='enterprise_subscription_inclusion',
            field=models.BooleanField(default=False, help_text='Caculated field based on if course is included in enterprise subscription catalog, and course run is self-paced'),
        ),
        migrations.AddField(
            model_name='historicalorganization',
            name='enterprise_subscription_inclusion',
            field=models.BooleanField(default=False, help_text="This field signifies if any of this org's courses are in the enterprise subscription catalog"),
        ),
        migrations.AddField(
            model_name='historicalprogram',
            name='enterprise_subscription_inclusion',
            field=models.BooleanField(default=False, help_text='Caculated field based on if all courses in this program are included in the enterprise subscription catalog'),
        ),
        migrations.AddField(
            model_name='organization',
            name='enterprise_subscription_inclusion',
            field=models.BooleanField(default=False, help_text="This field signifies if any of this org's courses are in the enterprise subscription catalog"),
        ),
        migrations.AddField(
            model_name='program',
            name='enterprise_subscription_inclusion',
            field=models.BooleanField(default=False, help_text='Caculated field based on if all courses in this program are included in the enterprise subscription catalog'),
        ),
    ]