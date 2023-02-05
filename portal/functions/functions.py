import datetime

# Function to convert string to datetime
def str2date(date_time):
	format = '%Y-%m-%d'
	datetime_str = datetime.datetime.strptime(date_time, format)
	return datetime_str

# date_time = '2023-02-23'
# new_date = str2date(date_time)
# print(type(new_date))
