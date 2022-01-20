import unittest
from datetime import datetime, date, timedelta
import logging
from src.models.job_model import JobModel
from src.storage.tiny_db_dao import TinyDBDAO


class DBTesting(unittest.TestCase):
    def setUp(self) -> None:
        logging.getLogger().setLevel(logging.INFO)
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
                                               "plus we have a document "
                                               "containig the last update "
                                               "date. So we "
                                               "should have 2 entries")

    def test2_check_delete_expired_jobs_functionality(self):
        expired_job = JobModel()
        expired_job.title = "EXPIRED_TEST_JOB"
        today = datetime.now()
        expired_job.closing_date = (today - timedelta(days=2)).date()

        non_expired_job = JobModel()
        non_expired_job.title = "NON_EXPIRED_TEST_JOB"
        non_expired_job.closing_date = (today + timedelta(days=2)).date()

        self.test_db.insert_jobs([expired_job, non_expired_job])

        db_contents = self.test_db.db.all()
        self.assertTrue(len(db_contents) == 3, "we should have 2 jobs and "
                                               "the update_date inside the db")

        self.test_db.delete_all_expired_jobs()
        db_contents = self.test_db.db.all()
        self.assertTrue(len(db_contents) == 2, "we should have only 1 job "
                                               "inside the db now, "
                                               "as we have deleted one "
                                               "expired job ")
        found_non_expired_job = False
        for doc in db_contents:
            if 'title' in doc.keys():
                if doc['title'] == "NON_EXPIRED_TEST_JOB":
                    found_non_expired_job = True
        self.assertTrue(found_non_expired_job, "did not found non-expired "
                                               "job?!")
