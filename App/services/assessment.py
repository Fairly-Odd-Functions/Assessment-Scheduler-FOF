from datetime import datetime, time

def validate_dates(startDate, endDate):
    errors = []

    if not isinstance(startDate, datetime):
        errors.append("Invalid Start Date. It Must Be A Datetime Object.")
    if not isinstance(endDate, datetime):
        errors.append("Invalid End Date. It Must Be A Datetime Object.")

    if startDate > endDate:
        errors.append("Start Date Must Be Before End Date.")

    if errors:
        return {"Error Message": errors}
    return {"startDate": startDate, "endDate": endDate}

def validate_times(startTime, endTime):
    errors = []

    if isinstance(startTime, datetime):
        startTime = startTime.time()
    elif not isinstance(startTime, time):
        errors.append("Invalid Start Time. It Must Be A Time Object.")

    if isinstance(endTime, datetime):
        endTime = endTime.time()
    elif not isinstance(endTime, time):
        errors.append("Invalid End Time. It Must Be A Time Object.")

    if startTime >= endTime:
        errors.append("Start Time Must Be Before End Time.")

    if errors:
        return {"Error Message": errors}
    return {"startTime": startTime, "endTime": endTime}
