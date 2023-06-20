from datetime import datetime

def create_file_name(prefix, suffix):
    now = datetime.now()
    time = now.strftime("%Y%m%d_%H%M%S")

    return "{}_{}{}".format(prefix, time, suffix)
