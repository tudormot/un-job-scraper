import numpy as np
import time



def fuzzy_delay(s):
    # waits for a fuzzy amount of time. +-10% of specified time
    tol = s / 10.
    fuzz = np.random.uniform(low=-tol, high=tol)
    delay = s + fuzz
    time.sleep(delay)
