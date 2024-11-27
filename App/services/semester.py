import re

def validate_dates(academic_year, start_date, end_date):
    errors = []
    if not re.match(r'^\d{4}/\d{4}$', academic_year):
        errors.append("Academic Year Must Be In The Format YYYY/YYYY (e.g., 2024/2025).")

    start_year, end_year = academic_year.split('/')
    if int(end_year) - int(start_year) != 1:
        errors.append("Start Year and End Year Must Be One Year Apart.")

    if str(start_date.year) != start_year:
        errors.append(f"Start Date Year ({start_date.year}) Doesn't Match The Academic Year Start Year ({start_year}).")

    if str(end_date.year) != end_year:
        errors.append(f"End Date Year ({end_date.year}) Doesn't Match The Academic Year End Year ({end_year}).")

    if start_date >= end_date:
        errors.append("Start Date Must Be Before End Date.")

    return errors

def validate_academic_year(academic_year):
    errors = []
    if not re.match(r'^\d{4}/\d{4}$', academic_year):
        errors.append("Academic Year Must Be In The Format YYYY/YYYY (e.g., 2024/2025).")

    start_year, end_year = academic_year.split('/')
    if int(end_year) - int(start_year) != 1:
        errors.append("Start Year and End Year Must Be One Year Apart.")

    return errors