from datetime import datetime

def validate_dates(startDate, dueDate):
    errors = []

    try:
        start_date = datetime.strptime(startDate, "%Y-%m-%d").date()
    except ValueError:
        errors.append("Invalid Start Date Format. Use YYYY-MM-DD.")
        start_date = None

    try:
        end_date = datetime.strptime(dueDate, "%Y-%m-%d").date()
    except ValueError:
        errors.append("Invalid Due Date Format. Use YYYY-MM-DD.")
        end_date = None

    if not start_date or not end_date:
        return {"Error": errors}

    if start_date >= end_date:
        errors.append("Start Date Must Be Before Due Date.")

    if errors:
        return {"Error": errors}
    return {"startDate": start_date, "dueDate": end_date}
