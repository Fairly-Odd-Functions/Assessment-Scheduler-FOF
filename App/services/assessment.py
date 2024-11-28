from datetime import datetime

def validate_dates(startDate, dueDate):
    errors = []

    if not isinstance(startDate, datetime):
        errors.append("Invalid Start Date. It Must Be A Datetime Object.")
    if not isinstance(dueDate, datetime):
        errors.append("Invalid Due Date. It Must Be A Datetime Object.")

    if startDate >= dueDate:
        errors.append("Start Date Must Be Before Due Date.")

    if errors:
        return {"Error Message": errors}
    return {"startDate": startDate, "dueDate": dueDate}
