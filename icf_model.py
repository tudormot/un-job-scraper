from web_adapter import *
from tinydb import TinyDB, Query


# class icf_model_state():
#     def __init__(self):
#         self.job_list = []
#         self.job_hash = {}


# class icf_loader:
#     def get_icf_model(self):
#         PICKLE_FILE = 'icf_state.p'
#         # try to load icf_model from file, if file does not exist, create a new icf_model
#         try:
#             with open(PICKLE_FILE, "rb") as input_file:
#                 model = cPickle.load(input_file)
#         except FileNotFoundError:
#             print('Warning! Pickle file does not seem to exist. Creating new empty model of site')
#             model = icf_model()
#
#         return model


class icf_model:
    def __init__(self):
        self.db =  TinyDB('db.json')

    def delete_expired_jobs(self):
        pass

    def create(self, jobs):
        result = upload_jobs(jobs)
        #TODO: should check if jobs were uploaded successfully
        for job in jobs:
            self.db.insert(job)

        pass
    def delete(self,jobs):
        raise Exception('Not Implemented yet!')
        pass

    def set_last_update(self,update):
        self.db.insert({'last_updated':str(update)})
