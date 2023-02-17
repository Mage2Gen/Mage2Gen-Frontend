from django.core.management.base import BaseCommand, CommandError
import csv
from django.db import connection
import os

class Command(BaseCommand):
    help = 'Import mage2methods.csv to database'

    def add_arguments(self, parser):
        parser.add_argument('main_version', nargs='+', type=int)

    def handle(self, *args, **options):
        for main_version in options['main_version']:
            main_version = str(main_version)
            with connection.cursor() as cursor:
                print('removing old records for version')
                cursor.execute("DELETE FROM mage2gen_mage2methods WHERE main_version = " + main_version + ";")
                print('Start reading CSV')
                with open(os.path.join(os.path.dirname(''), 'mage2gen' + main_version + '/snippets/mage2methods.csv'), 'r') as fin:  # `with` statement available in 2.5+
                    mage2methods = csv.reader(fin, delimiter=';', quotechar="'")
                    to_db = []
                    for row in mage2methods:
                        if len(row) == 3:
                            to_db.append([main_version, row[0], row[1], row[2]])
                print('Start insert to table')
                cursor.executemany("INSERT INTO mage2gen_mage2methods (main_version, full_classname, method, parameters) VALUES (%s, %s, %s, %s);", to_db)
                print('Successfully inserted mage2methods')

