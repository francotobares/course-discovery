"""
Management command to import, create, and/or update course and course run information for
executive education courses.
"""
import logging

from django.apps import apps
from django.core.management import BaseCommand, CommandError
from django.db.models.signals import post_delete, post_save

from course_discovery.apps.api.cache import api_change_receiver, set_api_timestamp
from course_discovery.apps.core.models import Partner
from course_discovery.apps.course_metadata.data_loaders.csv_loader import CSVDataLoader

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Import course and course run information from a CSV available on a provided csv path.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--partner_code',
            help='The short code for a specific partner to import courses to, defaults to "edx".',
            default='edx',
            type=str,
        )
        parser.add_argument(
            '--csv_path',
            help='Path to the CSV file',
            type=str,
            required=True
        )
        parser.add_argument(
            '--is_draft',
            help='The boolean value which is used to toggle draft courses',
            type=bool,
            default=False
        )
        parser.add_argument(
            '--start_index',
            help='The integer value, startiing from 0, which is used to give initial index of the batch. Default is 0.',
            type=int,
            required=False
        )
        parser.add_argument(
            '--batch_size',
            help='The integer value, startiing from 1, which is used to give size of the batch. Default is length of csv.',
            type=int,
            required=False
        )

    def handle(self, *args, **options):
        """
        Example usage: ./manage.py import_course_metadata --partner_code=edx --csv_path=test.csv --start_index=0 --batch_size=10
        """

        # The signal disconnect has been taken from refresh_course_metadata management command.
        # We only want to invalidate the API response cache once data loading
        # completes. Disconnecting the api_change_receiver function from post_save
        # and post_delete signals prevents model changes during data loading from
        # repeatedly invalidating the cache.
        for model in apps.get_app_config('course_metadata').get_models():
            for signal in (post_save, post_delete):
                signal.disconnect(receiver=api_change_receiver, sender=model)

        partner_short_code = options.get('partner_code')
        csv_path = options.get('csv_path')
        # its default value is False, it will be treated as True if passed by any value via command-line
        is_draft = options.get('is_draft')
        start_index = options.get('start_index')
        batch_size = options.get('batch_size')
        try:
            partner = Partner.objects.get(short_code=partner_short_code)
        except Partner.DoesNotExist:
            raise CommandError(  # pylint: disable=raise-missing-from
                "Unable to locate partner with code {}".format(partner_short_code)
            )

        try:
            loader = CSVDataLoader(
                partner, csv_path=csv_path, is_draft=is_draft, start_index=start_index, batch_size=batch_size)
            logger.info("Starting CSV loader import flow for partner {}".format(partner_short_code))
            loader.ingest()
        except Exception as exc:
            raise CommandError(  # pylint: disable=raise-missing-from
                "CSV loader import could not be completed due to unexpected errors.\n{}".format(exc)
            )
        else:
            set_api_timestamp()
            logger.info("CSV loader import flow completed.")
