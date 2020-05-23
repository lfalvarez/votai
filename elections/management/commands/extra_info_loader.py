from django.core.management.base import BaseCommand
from elections.models import Election
import csv


class Command(BaseCommand):
    help = 'Carga informacion extra desde un CSV'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', nargs='+', type=str)

    def handle(self, *args, **options):
        file_path = options['csv_file'][0]
        extrainfo = csv.reader(open(file_path, 'rt'), delimiter=',', quotechar='"', lineterminator='\n')
        # Remove header
        next(extrainfo)
        for line in extrainfo:
            if line:
                election_name, extra_info_title, extra_info_content = line[0].strip(), line[1].strip(), line[2].strip()
                try:
                    election = Election.objects.get(name=election_name)
                    election.extra_info_title = extra_info_title
                    election.extra_info_content = extra_info_content
                    election.save()
                except Exception as e:
                    print('excepción con la elección ' + election_name)
                    print(e)
