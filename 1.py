import datetime
dt_now = datetime.datetime.now()
date_string = "2023-07-20"
date_obj = datetime.datetime.strptime(date_string, "%Y-%m-%d").date()
day_of_week = dt_now.strftime('%A')
print(day_of_week)