# Generated by Django 3.0.2 on 2020-01-16 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deals', '0006_comment_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='body',
            field=models.TextField(),
        ),
    ]
