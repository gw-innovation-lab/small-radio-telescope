import serial

ser = serial.Serial('/dev/ttyACM0', baudrate = 9600)


userInput = raw_input('Direction?: ')

if userInput == "Forward":
	str1='1'
if userInput == "Reverse":
	str1='2'


userInput2 = raw_input('Count?: ')

str2="{}".format(userInput2)


userInput3 = raw_input('Speed?: ')

str3="{}".format(userInput3)


str = "<{},{},{}>".format(str1,str2,str3)

print(str)
ser.write(str)