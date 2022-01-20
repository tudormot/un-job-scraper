import unittest
from datetime import datetime, date

from src.models.job_model import JobModel
from src.storage.tiny_db_dao import TinyDBDAO


class DBTesting(unittest.TestCase):
    def setUp(self) -> None:
        TEST_DB_NAME = 'test.db'
        self.test_db = TinyDBDAO(TEST_DB_NAME)
        self.addCleanup(self.test_db._delete_underlying_database)
        self.addCleanup(self.test_db.terminate)

    def test_0_check_last_update_date_on_DB_creation(self):
        expected_date = datetime(year=1,
                                 month=1,
                                 day=1)
        self.assertEqual(self.test_db.get_last_update(), expected_date,
                         "db last update date is not initializing properly")

    def test_1_add_and_get_from_DB(self):
        job: JobModel = JobModel()
        job.title = 'TEST_JOB'
        job.organisation = "MOTKAZH"
        job.closing_date = date(day=12, year=2012, month=12)

        self.test_db.insert_jobs([job])
        db_contents = self.test_db.db.all()
        print('db_contents is  : ', db_contents)
        self.assertTrue(len(db_contents) == 2, "we added only one job to db, "
                                               "plus we have a document containig the last update date. So we " \
                                               "should have 2 entries")

