import csv
from pathlib import Path
from django.core.management.base import BaseCommand
from django.db import transaction
from subway.models import Station

def parse_bool(value, default=True) -> bool:
    if value is None:
        return default
    s = str(value).strip().lower()
    if s == "":
        return default
    return s in {"1", "true", "t", "y", "yes", "on"}

class Command(BaseCommand):
    help = "Seed subway stations from CSV (idempotent: update_or_create by station_code)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            default="subway/management/seed_data/stations.csv",
            help="Path to stations csv",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete all Station rows before seeding",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        file_path = Path(options["file"]).resolve()
        if not file_path.exists():
            self.stderr.write(self.style.ERROR(f"CSV not found: {file_path}"))
            return

        if options["clear"]:
            Station.objects.all().delete()
            self.stdout.write(self.style.WARNING("Cleared Station table."))

        created = updated = skipped = 0

        with file_path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader, start=2):
                code = (row.get("station_code") or "").strip()
                name = (row.get("station_name") or "").strip()

                if not code:
                    skipped += 1
                    continue
                if not name:
                    skipped += 1
                    continue

                is_enabled = parse_bool(row.get("is_enabled"), default=True)

                obj, was_created = Station.objects.update_or_create(
                    station_code=code,
                    defaults={
                        "station_name": name,
                        "is_enabled": is_enabled,
                    },
                )
                created += int(was_created)
                updated += int(not was_created)

        self.stdout.write(
            self.style.SUCCESS(f"Done. created={created}, updated={updated}, skipped={skipped}")
        )
