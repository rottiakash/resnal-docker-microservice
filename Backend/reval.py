from resanal.models import Result,Fetch
import mysql.connector 
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="admin123",
auth_plugin='mysql_native_password'
)
mycursor = mydb.cursor()
mycursor.execute("use MyDB")
mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM reval")

myresult = mycursor.fetchall()

for x in myresult:
    print(x)
    subject = Fetch.objects.filter(usn__usn=x[0],subcode=x[1])
    if len(subject) == 1:
        subject = subject[0]
        subject.extmarks = x[2]
        subject.totalmarks = subject.intmarks + subject.extmarks
        subject.save()