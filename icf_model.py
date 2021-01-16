from web_adapter import *
from tinydb import TinyDB, Query
import datetime



class icf_model:
    def __init__(self):
        self.db =  TinyDB('db.json')
        self.query = Query()

    def delete_expired_jobs(self):
        print("INFO: deleting expired jobs")
        curr = datetime.datetime.now()
        test_func = lambda s: self._closingdatestr_to_date(s) < curr
        self.db.search(self.query.closing_date.test(test_func))


    def create(self, jobs):
        results = upload_jobs(jobs)
        for i, result in enumerate(results):
            if result['success']:
                self.db.insert(jobs[i])

    def delete(self,jobs):
        raise Exception('Not Implemented yet!')

    def set_last_update(self,update):
        self.db.remove(self.query.last_updated.exists())
        self.db.insert({'last_updated':str(update)})

    def get_last_update(self):
        response = self.db.search(self.query.last_updated.exists())
        return self._str_to_date(response[0]['last_updated'])

    @staticmethod
    def _str_to_date(s):
        "eg date : 2021-01-15 09:20:06"
        return datetime.datetime(year = int(s[0:4]),
                                 month=int(s[5:7]),
                                 day=int(s[8:10]),
                                 hour=int(s[11:13]),
                                 minute=int(s[14:16]),
                                 second=int(s[17:19]))

    @staticmethod
    def _closingdatestr_to_date(s):
        list = s.split('.')
        return datetime.datetime(year = list[2],
                                 month= list[1],
                                 day=list[0],
                                 hour=23,
                                 minute=59,
                                 second=59)