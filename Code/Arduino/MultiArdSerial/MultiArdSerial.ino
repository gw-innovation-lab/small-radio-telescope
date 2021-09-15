const byte numChars = 32;       //These establish a variable for the
char receivedChars[numChars];   //string being read from the Pi.

boolean newData = false;        //Reset for new data from the Pi.
int direct = 0;

void setup() {
  Serial.begin(9600);         //Begin Serial connection.
  pinMode(13, OUTPUT);
}

void loop() {
  SerialInputFromPi();    //Reads a string from the Pi
  translateString(direct);
  blink182();
}

void SerialInputFromPi(){
  static boolean recvInProgress = false;  //Continues action till the
                                          //input is complete.
  static byte ndx = 0;                    //Digits are recieved one at
                                          //at a time and numbered ndx.
  char startMarker = '<';                 //Strings are sent in the
  char endMarker = '>';                   //format <#,####,###> .
  char rc;

  //While loop runs so long as there are characters coming in and
  //the end marker hasn't been recieved.
  while (Serial.available() > 0 && newData == false){
     rc = Serial.read();

     if (recvInProgress == true){
      
      if (rc != endMarker){         //Continue till endmarker recieved.
        receivedChars[ndx] = rc;
        ndx++;
        
        if(ndx >= numChars){        //If the string is too long the 
          ndx = numChars - 1;       //final digit is overwritten.
        }
        
      }
      else{
        receivedChars[ndx] = '\0';  //The end marker was recieved, now
        recvInProgress = false;     //there is new data.
        ndx = 0;
        newData = true;
      }
     }
     else if (rc == startMarker){   //If the start marker comes in
        recvInProgress = true;      //lets function know its recieving.
      }
  }
}

int translateString(int &direct){
  //Convert from ASCII to decimal if there is new data availible.
  if (newData == true){
    direct = (receivedChars[0] & 0xf);               //Direction of motor.
    //Serial.print(direct);
    newData = false;                                  //Data recieve
  }                                                   //complete.
}

int remain = 0;

void blink182(){
  if (direct == 1){
    for (int i = 2; i < 12; i++){
      remain = i % 2;
      if (remain == 0){
        digitalWrite(13, HIGH);
        delay(1000);
      }
      if (remain == 1){
        digitalWrite(13, LOW);
        delay(1000);
      }
      if (i == 11){
        Serial.println("Task 2 Complete");
        direct = 0;
      }
    }
  }
}

