import serial

ser1 = serial.Serial('/dev/ttyACM0', baudrate = 9600, timeout=100)
ser2 = serial.Serial('/dev/ttyACM1', baudrate = 9600, timeout=100)

userInput = input('Direction?: ')
str1 = userInput
str = "<{}>".format(str1)

print(str)

ser1.write(str)
ser2.write(str)

data1=ser1.readline().decode('ascii')
data2=ser2.readline().decode('ascii')

print(data1)
print(data2)