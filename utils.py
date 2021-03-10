import numpy as np
import time
from config import args


def fuzzy_delay(s):
    #waits for a fuzzy amount of time. +-10% of specified time
    tol = s/10.
    fuzz = np.random.uniform(low = -tol, high= tol)
    delay = s+fuzz
    if args['fast'] is True:
        delay /=2.
    time.sleep(delay)

#
# if __name__ == "__main__":
#     LAST_UPDATE_DATE = "2021-02-17 09:20:06"
#     change_last_updated_date_manually(LAST_UPDATE_DATE)