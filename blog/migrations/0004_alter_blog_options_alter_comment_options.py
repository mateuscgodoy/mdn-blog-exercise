# Generated by Django 5.0.6 on 2024-05-12 13:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_author_writes_since_alter_blog_created_at_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'get_latest_by': '-created_at', 'ordering': ['-created_at', 'title']},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'get_latest_by': '-created_at', 'ordering': ['-created_at']},
        ),
    ]
