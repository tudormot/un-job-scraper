from icf_model import *
import numpy as np
import time


def change_last_updated_date_manually(date):
    model = icf_model()
    model.set_last_update(date)
    pass

def fuzzy_delay(s):
    #waits for a fuzzy amount of time. +-10% of specified time
    tol = s/10.
    fuzz = np.random(low = -tol, high= tol)
    time.sleep(s + fuzz)


if __name__ == "__main__":
    LAST_UPDATE_DATE = "2021-02-17 09:20:06"
    change_last_updated_date_manually(LAST_UPDATE_DATE)