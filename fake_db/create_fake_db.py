import random
from faker import Faker
import pandas as pd
from datetime import datetime

import sys
sys.path.append('..')
from models import *


def create_fake_sources():
    """Generate fake Sources."""
    faker = Faker()
    source_sheet = pd.read_excel(open('fake_db.xlsx', 'rb'), sheet_name='Source')
    n = 0
    for idx, row in source_sheet.iterrows():
        source = Source(upn=row['UPN'],
                        name=row['Name'],
                        age=row['Age'],
                        sex=row['Sex'],
                        dx=row['DX'],
                        wbc=row['WBC'],
                        pb_blast=row['Pb_Blast'],
                        bm_blast=row['BM_Blast'],
                        karyotype=row['Karyotype'],
                        fab=row['FAB'],
                        yearbanked=row['YearBanked'])
        db.session.add(source)
        db.session.commit()
        n += 1
    print(f'Added {n} fake Sources to the database.')


def create_fake_samples():
    """Generate fake Sources."""
    faker = Faker()
    sample_sheet = pd.read_excel(open('fake_db.xlsx', 'rb'), sheet_name='Sample')
    n = 0
    for idx, row in sample_sheet.iterrows():
        sample = Sample( usn=row['USN'],
                        upn=row['UPN'],
                        name=row['Name'],
                        type=row['Type'],
                        collectiondate=datetime.strptime(faker.date(), '%Y-%m-%d').date(),
                        time_point_weeks=row['Time_point_weeks'])
        db.session.add(sample)
        db.session.commit()
        n += 1
    print(f'Added {n} fake Samples to the database.')

db.create_all()

if __name__ == '__main__':
    create_fake_sources()
    create_fake_samples()
