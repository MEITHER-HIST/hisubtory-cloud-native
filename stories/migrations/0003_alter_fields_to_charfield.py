from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cut',
            name='image',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='episode',
            name='source_url',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='webtoon',
            name='thumbnail',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
