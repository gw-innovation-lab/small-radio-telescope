import serial

ser1 = serial.Serial('COM5', baudrate = 9600)
ser2 = serial.Serial('COM9', baudrate = 9600)

userInput = input('Direction?: ')
str1 = userInput
str = "<{}>".format(str1)

print(str)
ser1.write(str)
ser2.write(str)