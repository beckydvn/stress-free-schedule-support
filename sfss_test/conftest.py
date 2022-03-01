import os
import pytest

def pytest_configure(config):
    '''
    Delete database file if existed. So testing can start fresh.
    '''
    print('Setting up environment...')
    db_file = 'db.sqlite'
    if os.path.exists(db_file):
        os.remove(db_file)
