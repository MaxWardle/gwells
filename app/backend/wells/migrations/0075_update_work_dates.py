from django.db import migrations
from django.db.models import F


# This can be deleted when doing next squash of migrations because it's a one time update
def migrate_work_dates(apps, schema_editor):
    activity_submission = apps.get_model('wells', 'ActivitySubmission')

    activity_submission.objects.filter(well_activity_type__code__contains="CON").update(
        construction_start_date=F('work_start_date'))
    activity_submission.objects.filter(well_activity_type__code__contains="CON").update(
        construction_end_date=F('work_end_date'))

    activity_submission.objects.filter(well_activity_type__code__contains="LEGACY").update(
        construction_start_date=F('work_start_date'))
    activity_submission.objects.filter(well_activity_type__code__contains="LEGACY").update(
        construction_end_date=F('work_end_date'))

    activity_submission.objects.filter(well_activity_type__code__contains="ALT").update(
        alteration_start_date=F('work_start_date'))
    activity_submission.objects.filter(well_activity_type__code__contains="ALT").update(
        alteration_end_date=F('work_end_date'))

    activity_submission.objects.filter(well_activity_type__code__contains="DEC").update(
        decommission_start_date=F('work_start_date'))
    activity_submission.objects.filter(well_activity_type__code__contains="DEC").update(
        decommission_end_date=F('work_end_date'))


def reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('wells', '0074_auto_20190418_2237'),
    ]

    operations = [
        migrations.RunPython(migrate_work_dates, reverse),
    ]
