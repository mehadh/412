from django.db import models
import os
class Voter(models.Model):
    '''
    model on one voter / show all data etc
    '''
    voter_id_number = models.CharField(max_length=20)
    first_name = models.TextField()
    last_name = models.TextField()
    street_number = models.TextField()
    street_name = models.TextField()
    apartment_number = models.TextField(null=True, blank=True)
    zip_code = models.TextField()
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_registration = models.DateField(null=True, blank=True)
    party_affiliation = models.TextField()
    precinct_number = models.TextField()
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()
    voter_score = models.IntegerField()
    
    def __str__(self):
        '''string rep of this'''
        return f'{self.first_name} {self.last_name} ({self.street_name}, {self.zip_code})'
    
def load_data():
    """Load data from newton_voters.csv in the same directory."""
    import csv
    from datetime import datetime

    # Clear old data
    Voter.objects.all().delete()
    print("🧹 Deleted existing Voter records.")

    # Path to the CSV next to this file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, 'newton_voters.csv')

    with open(csv_path, encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        print(f"📋 Headers: {headers}")

        for row in reader:
            if len(row) < 17:
                print(f"⚠️ Skipping incomplete row: {row}")
                continue

            def parse_bool(val):
                return val.strip().lower() in ['1', 'true', 'yes']

            def parse_date(val):
                try:
                    return datetime.strptime(val.strip(), '%Y-%m-%d').date()
                except Exception:
                    return None

            try:
                voter = Voter(
                    voter_id_number=row[0].strip(),
                    last_name=row[1].strip(),
                    first_name=row[2].strip(),
                    street_number=row[3].strip(),
                    street_name=row[4].strip(),
                    apartment_number=row[5].strip() if row[5].strip() else None,
                    zip_code=row[6].strip(),
                    date_of_birth=parse_date(row[7]),
                    date_of_registration=parse_date(row[8]),
                    party_affiliation=row[9].strip(),
                    precinct_number=row[10].strip(),
                    v20state=parse_bool(row[11]),
                    v21town=parse_bool(row[12]),
                    v21primary=parse_bool(row[13]),
                    v22general=parse_bool(row[14]),
                    v23town=parse_bool(row[15]),
                    voter_score=int(row[16].strip()),
                )
                voter.save()
                print(f"✅ Saved: {voter}")
            except Exception as e:
                print(f"❌ Failed to save row: {row}")
                print(f"   Error: {e}")
