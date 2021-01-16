class JobModel:
    """dataclass that contains all information regarding a job"""

    def __init__(self):
        self.title = ''
        self.organisation = ''
        self.country = ''
        self.city = ''
        self.office = ''
        self.grade = ''
        self.closing_date = ''
        self.closing_date_pretty = ''
        self.tags = []
        self.original_job_link = ''
        self.extra_information = ''
        self.id = None
        self.job_category = 'Search All Jobs'
        self.job_type = None

    def as_dict(self):
        return {
            "title": self.title,
            "organisation": self.organisation,
            "country": self.country,
            "city": self.city,
            "office": self.office,
            "grade": self.grade,
            "closing_date": self.closing_date,
            "tags": self.tags,
            "original_job_link": self.original_job_link,
            "extra_information": self.extra_information,
            "id": self.id,
            "job_category" : self.job_category
        }
