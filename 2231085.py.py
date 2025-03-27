def run(path) :     
    # import modules here 
    import pandas as pd
import re

    # logic 
    df = pd.read_excel(path)
    email_pattern = r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
excel_file = pd.ExcelFile("C:\Users\Ujjawal Mishra\Downloads\Data Engineering\Data Engineering\data - sample.xlsx")
attendance_data = pd.read_excel(excel_file, "Attendance_data")
student_data = pd.read_excel(excel_file, "Student_data")

attendance_data['attendance_date'] = pd.to_datetime(attendance_data['attendance_date'])
ab_students = attendance_data[attendance_data['status'] == 'Absent']

absent_records = []
for student_id, st_absences in ab_students.groupby('student_id'):
    st_absences['absence_group'] = st_absences['attendance_date'].diff().dt.days.ne(1).cumsum()
    for _, ab_period in st_absences.groupby('absence_group'):
        if len(ab_period) > 3:
        absent_record.append([student_id,
                           ab_period.iloc[0]['attendance_date'],   # First date
                           ab_period.iloc[-1]['attendance_date'],  # Last date
                           len(ab_period)])
long_absences = pd.DataFrame(
    absent_records, 
    columns=['student_id', 'start_date', 'end_date', 'days_absent'])

detailed_absences = long_absences.merge(student_data, on='student_id', how='left')

def create_parent_message(row):
    if pd.notna(row['parent_email']) and re.match(email_pattern, str(row['parent_email'])):
        return "Dear Parent, your child {} was absent from {} to {} for {} days. Please ensure their attendance improves.".format(
            row['student_name'], row['start_date'].date(), 
            row['end_date'].date(), row['days_absent'])
        return None
    
detailed_absences['parent_message'] = detailed_absences.apply(create_parent_message, axis=1)
    # return your output
    print("Students with Long Absences:")
print(detailed_absences[['student_id', 'student_name', 'start_date', 'end_date', 'days_absent', 'parent_email', 'parent_message']])
    return df