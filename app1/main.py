import sqlite3

connect = sqlite3.connect("customer.db")

connect.execute("DROP TABLE IF EXISTS CUSTOMER ")

connect.execute("""
CREATE TABLE CUSTOMER
                (ID INT PRIMARY KEY NOT NULL,
                NAME TEXT NOT NULL,
                AGE INT NOT NULL);
""")
connect.execute("INSERT INTO CUSTOMER(ID,NAME,AGE) VALUES(1, 'Carson', 19)")
connect.execute("INSERT INTO CUSTOMER(ID,NAME,AGE) VALUES(2, 'Dancan', 20)")

custome_data = connect.execute("""
SELECT * FROM CUSTOMER;
""")
for col in custome_data:
    print(col)
connect.close()