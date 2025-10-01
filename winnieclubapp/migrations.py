from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('winnieclubapp', 'last_migration_name'),  # update this to your latest migration
    ]

    operations = [
        migrations.RemoveField(
            model_name='sale',
            name='product_name',
        ),
    ]
