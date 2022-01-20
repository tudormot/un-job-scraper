import unittest
from datetime import date

from src.models.job_model import JobModel


class ModelsTesting(unittest.TestCase):
    def test_0_icf_str_to_datetime(self):
        icf_string = '03.02.2010'
        expected_date = date(year=2010, day=3, month=2)
        self.assertEqual(expected_date,
                         JobModel.closing_date_icf_str_to_datetime(
                             icf_string),"closing_date_icf_str_to_datetime "
                                         "not working apparently ")

