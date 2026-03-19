📁 Project Structure
project/
│
├── src/
│   ├── main.py
│   └── transform.py
│
├── data/
│   ├── input/        # raw CSV files
│   ├── output/       # cleaned data

## Clients Table

- ลบช่องว่างในค่า string
- เปลี่ยน empty string → NULL
- ลบ client_id ที่ซ้ำหรือว่าง
- ตรวจสอบให้ client_id เป็น primary key

---

## Instruments Table

- ลบช่องว่างในค่า string
- เปลี่ยน empty string → NULL
- ลบ instrument_id ที่ซ้ำหรือว่าง
- ตรวจสอบให้ instrument_id เป็น primary key

---

## Trades Table

- ลบช่องว่างในค่า string
- เปลี่ยน empty string → NULL
- ตรวจสอบ trade_id เป็น primary key
- เปลี่ยนค่า numeric (`quantity`, `price`, `fees`) เป็นตัวเลข
- แปลงเวลา `trade_time` เป็น format `YYYY-MM-DD HH:MM:SS`
- ทำให้ string column เช่น `side`  เป็น uppercase
- ตรวจสอบ foreign key: client_id ต้องอยู่ใน clients, instrument_id ต้องอยู่ใน instruments
