import pymysql

conn = pymysql.connect(host = 'localhost', user = 'root', password = 'Anukul@123', database = 'secureatm')
curr = conn.cursor()


# curr.execute("INSERT INTO `users` (name, mobileno,email,accountno) VALUES(%s, %s, %s, %s)", ("Akash Bendre","9011336713","akash@gmail.com","12345678998"))
# conn.commit()
# curr.close()
# conn.close()