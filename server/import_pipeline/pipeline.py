"""Connects the filters. The output of each filter is the input of the next."""
from . import reader
from . import validator
from . import normalizer
from . import university_email_filter
from . import duplicate_filter
from . import transformer
from . import writer


def log(step, data):
    print(f"{step:<17} {len(data)} records")
    return data


def run(filename, student_service):
    data = log("READ", reader.process(filename))
    data = log("VALIDATE", validator.process(data))
    data = log("NORMALIZE", normalizer.process(data))
    data = log("UNIVERSITY EMAIL", university_email_filter.process(data))
    data = log("CHECK DUPLICATES", duplicate_filter.process(data))
    data = log("TRANSFORM", transformer.process(data))
    data = log("STORE", writer.process(data, student_service))
    return data
