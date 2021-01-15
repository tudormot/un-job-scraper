import _pickle as cPickle


class icf_model_state():
    job_list = []
    job_hash = []


class icf_loader:
    def get_icf_model(self):
        PICKLE_FILE = 'icf_state.p'
        # try to load icf_model from file, if file does not exist, create a new icf_model
        try:
            with open(PICKLE_FILE, "rb") as input_file:
                model = cPickle.load(input_file)
        except FileNotFoundError:
            print('Warning! Pickle file does not seem to exist. Creating new empty model of site')
            model = icf_model()

        return model


class icf_model:
    def __init__(self):
        pass


    def create(self, jobs):
        pass
    def delete(self,jobs):
        pass
