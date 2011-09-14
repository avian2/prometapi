from django.core.management.base import BaseCommand

class Command(BaseCommand):
	def handle(self, *args, **options):
		from prometapi.models import dump_data
		from prometapi.bicikeljproxy.models import BicikeljData
		import datetime
		
		if len(args):
			day = datetime.datetime.strptime(args[0], '%Y-%m-%d')
		else:
			day = datetime.datetime.now() - datetime.timedelta(2)
		
		dump_data(model=BicikeljData, day=day)