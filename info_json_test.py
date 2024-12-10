import json
import datetime
import random

start_date = datetime.date(2024, 1, 1)
end_date = datetime.date(2024, 12, 31)
amounts = [50000, 150000, 200000, 300000, 450000]

data = []

for month in range(1, 13):
    for day in range(1, 31): #  5 วันต่อเดือน
        try:
            current_date = datetime.date(2024, month, day)
            amount = random.choice(amounts) * random.choice([1, -1])
            data.append([current_date.strftime("%Y-%m-%d"), amount, "ລາຍການຈຳລອງ"])
        except ValueError: #  จัดการกรณีวันที่ไม่ถูกต้อง เช่น 31 ก.พ.
            pass

with open("account_data.json", "w") as f:
    json.dump(data, f, indent=4)

print("Generated account_data.json")