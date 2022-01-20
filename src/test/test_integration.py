import logging


# class DBTesting(unittest.TestCase):
#     def setUp(self) -> None:
#         logging.getLogger().setLevel(logging.INFO)
#         TEST_DB_NAME = 'test.db'
#         self.test_db = TinyDBDAO(TEST_DB_NAME)
#         self.addCleanup(self.test_db._delete_underlying_database)
#         self.addCleanup(self.test_db.terminate)