# Generated by Django 3.2.7 on 2021-10-26 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0009_responsenotitobuyer'),
    ]

    operations = [
        migrations.AddField(
            model_name='responsenotitobuyer',
            name='description',
            field=models.TextField(default='test'),
            preserve_default=False,
        ),
    ]