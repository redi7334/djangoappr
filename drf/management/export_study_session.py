from django.core.management.base import BaseCommand
from core.models import Subject, StudySession
import pandas as pd
from pathlib import Path


class Command(BaseCommand):
    help = "Export all StudySessions to a CSV file"

    def handle(self, *args, **options):
        queryset = StudySession.objects.all().values(
            "id",
            "datetime",
            "duration_minutes",
            "notes",
        )

        if not queryset.exists():
            self.stdout.write(self.style.WARNING("No StudySessions found"))
            return

        # Convert queryset → DataFrame
        df = pd.DataFrame.from_records(queryset)


        # Output file
        output_dir = Path("exports")
        output_dir.mkdir(exist_ok=True)

        output_file = output_dir / "study_sessions.csv"

        df.to_csv(output_file, index=False)

        self.stdout.write(
            self.style.SUCCESS(
                f"Exported {len(df)} StudySessions to {output_file}"
            )
        )