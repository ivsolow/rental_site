from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0002_feedback_equipment_feedback_user_and_more'),
    ]

    operations = [
        migrations.RunSQL('ALTER TABLE feedback_feedback DROP COLUMN rental_id;'),
    ]