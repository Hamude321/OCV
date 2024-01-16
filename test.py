from datetime import datetime, date

currentDateAndTime = datetime.now()
currentTime = currentDateAndTime.strftime("%H:%M")

# lul = datetime.strptime('16:00', '%H:%M')
# regtime = datetime.strftime(lul, '%H:%M')

# a = datetime.combine(date.today(), currentTime) - datetime.combine(date.today(), regtime)

# print(regtime)
# print(a)

currentTime.replace(':','')
print(currentTime.replace(':',''))