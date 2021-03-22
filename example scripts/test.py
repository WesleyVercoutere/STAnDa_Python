import datetime

dateTimeString = "3/9/2021 1:58:33 PM"

dt = (datetime.datetime.strptime(dateTimeString, '%m/%d/%Y %I:%M:%S %p'))

print(dt.day)