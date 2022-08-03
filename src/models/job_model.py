from dataclasses import dataclass
from datetime import date
from typing import Optional


class JobModel:
    """dataclass that contains all information regarding a job"""

    def __init__(self):
        self.title = ''
        self.organisation = ''
        self.country = ''
        self.city = ''
        self.office = ''
        self.grade = ''
        # no timezoneinfo given by unjobs.org, hence storing as datetime.date
        self.closing_date: Optional[date] = None
        self.tags = []
        self.original_job_link = ''
        self.extra_information = ''
        self.id = None
        self.job_category = []
        self.job_type = None

    def as_dict(self) -> dict:
        job_dict = {
            "title": self.title,
            "organisation": self.organisation,
            "country": self.country,
            "city": self.city,
            "office": self.office,
            "grade": self.grade,
            "closing_date": self.closing_date_to_icf_str_closing_date(
                self.closing_date),
            "tags": self.tags,
            "original_job_link": self.original_job_link,
            "extra_information": self.extra_information,
            "id": self.id,
            "job_category": self.job_category,
            "job_type": self.job_type
        }
        return {k: job_dict[k] for k in job_dict if job_dict[k] is not None}

    @staticmethod
    def closing_date_to_icf_str_closing_date(d: date) -> str:
        return d.strftime("%d.%m.%Y")

    def __str__(self):
        dict_repr = self.as_dict()
        try:
            dict_repr.pop("extra_information")
        except KeyError:
            pass
        return dict_repr.__str__()
