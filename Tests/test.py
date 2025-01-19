from datetime import datetime, timedelta

# test = '19:51'

# 2209 - 2199

# 2204-2154 = 10

# split = test.split(':')


# if int(split[1])>=50:
#     test = int(test.replace(':','')) + 50
#     print(test)
# else:
#     print (test)
time_change = timedelta(minutes=10) 

string_time = '22:30'
formatted_time = datetime.strptime(string_time, '%H:%M')

currentDateAndTime = datetime.now()
current_Time = currentDateAndTime.strftime("%H:%M")

new_time = formatted_time+time_change-currentDateAndTime

days = new_time.days
hours, remainder = divmod(new_time.seconds, 3600)
minutes, seconds = divmod(remainder, 60)
# If you want to take into account fractions of a second
seconds += new_time.microseconds / 1e6

print(hours)
print(minutes)
print(seconds)

