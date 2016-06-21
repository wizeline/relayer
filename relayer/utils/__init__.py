def get_elapsed_time_in_milliseconds(start_time, end_time):
    elapsed_time = end_time - start_time
    return elapsed_time.microseconds / 1000.0 + elapsed_time.seconds * 1000
