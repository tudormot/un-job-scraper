class JobModel:
    """dataclass that contains all information regarding a job"""
    title: str
    organisation: str
    country: str
    city: str
    office: str
    grade: str
    closing_date: str
    closing_date_pretty: str
    tags: []
    original_job_link: str
    extra_information: str
    id : int
