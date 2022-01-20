import unittest
from datetime import date

from src.models.job_model import JobModel


class ModelsTesting(unittest.TestCase):
    def test_0_icf_str_to_datetime(self):
        expected_icf_string = '03.02.2010'
        d = date(year=2010, day=3, month=2)
        self.assertEqual(expected_icf_string,
                         JobModel.closing_date_to_icf_str_closing_date(d),
                         "closing_date_icf_str_to_datetime "
                         "not working apparently ")

