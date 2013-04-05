from django.core.management.base import BaseCommand, CommandError
from tentrack.models import Week

class Command(BaseCommand):
    args = '<week_id ...>'
    help = 'Closes the last week and start a new week for posting matches'

    def handle(self, *args, **option):
        try:
            week = Week.objects.order_by('-id')[0]
        except Week.DoesNotExist:
            raise CommandError('Week does not exist')

        week.open = False
        week.finalize() # check duplicates, post pgain, mvp, etc.
        week.save()
        self.stdout.write('Successfully closed week "%s"\n' % week.id)
        new_week = Week(open=True) # open new week
        new_week.save()
        self.stdout.write('Successfully opened week "%s"\n' % new_week.id)
