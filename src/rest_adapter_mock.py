from typing import List, Dict

from src.models.job_model import JobModel


class RESTAdapterMock:
    """a dummy object that always return success until we get the connection
    with icf back up """
    def __init__(self):
        self.jobs_uploaded_to_icf: List[Dict] = []

    def upload_jobs(self, jobs:List[JobModel]):
        response = []
        for job in jobs:
            if job.id in self.jobs_uploaded_to_icf:
                response.append({'failure': True, 'reason': 'can\'t upload '
                                                            'as job already '
                                                            'present on '
                                                            'website'})
            else:
                response.append({'success': True})
                self.jobs_uploaded_to_icf.append(job.id)
        return response

    def delete_jobs(self, jobs):
        response = []
        for job in jobs:
            if job.id in self.jobs_uploaded_to_icf:
                response.append({'success': True})
                self.jobs_uploaded_to_icf.remove(job.id)
            else:
                response.append({'failure': True, 'reason': 'can\'t delete '
                                                            'as job is not '
                                                            'present on '
                                                            'website'})
        return response
