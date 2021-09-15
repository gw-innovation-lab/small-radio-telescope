/* Small Radio Telescope - Motor Control
   Winona State University Research
   Clayton G. Hanson
      The SRT pivots on its stand 180 degrees on the x-y 
   plane relative to the flat of the Earth. A second motor
   allows the dish of the SRT to pivot on top of its mount
   180 degrees relative with 90 degrees being straight up
   towards the zenith.
      The motors take 36 volts direct current. When +36 
   volts is given the motor will move in the opposite 
   direction as when the motor is given -36 volts. 
   A Pololu TB67H420FTG Dual/Single Motor Driver Carrier 
   will be used to switch the direction of current as needed.
   These will be turned on and off using an Arduino Uno.
      Two limit switches are used to stop the motors movement 
   when the gear reaches 0 degrees or 180 degrees. A reed 
   sensor will be used to count the pulses by magnetizing 
   and de-magnitizing as the motor turns, it will be read as
   either a high or low voltage.
*/

int A_1 = 10;       //These pins out put forward, reverse and the
int A_2 = 9;        //pulse width to the Pololu chip.
int A_PWM = 8;

int RevLimit = 6;   //CCW Pins for limit switches to stop motors at
int ForLimit = 7;   //CW 0 and 180 degrees.
int forward_check;  //Stores the digital read to check against 
int reverse_check;  //if statements.


//Counting Function variables
int count = 0;      //Blank variable to count high low transitions.
int count_pin = 4;  //This will be the sensor to count pulses.

int lastState = 0;  //Stores switch state.
int switchState = 0;//To check switch state.

int k;          //For calling counter function.

const byte numChars = 32;       //These establish a variable for the
char receivedChars[numChars];   //string being read from the Pi.

boolean newData = false;        //Reset for new data from the Pi.

int direct = 0;     //Direction motor moves forward or backward.
int count_till = 0; //Limit that my system should count to then stop.
int sped = 0;       //PWM wave speed.

void setup() {
  
  Serial.begin(9600);         //Begin Serial connection.
  
  pinMode(A_1, OUTPUT);       //Initialize output pins.
  pinMode(A_2, OUTPUT);
  pinMode(A_PWM, OUTPUT);

  digitalWrite(A_1, LOW);     //Write output pins low so the
  digitalWrite(A_2, LOW);     //motors are off when the 
  digitalWrite(A_PWM, LOW);   //Arduino is turned on.

  pinMode(count_pin, INPUT_PULLUP);  //Initialize snesor pins.
  pinMode(ForLimit, INPUT_PULLUP);
  pinMode(RevLimit, INPUT_PULLUP);
}

void loop() {
  SerialInputFromPi();    //Reads a string from the Pi
  translateString(direct, count_till, sped);
  Move(count);            //Move the motor to meet the conditions.
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
      Stop();
      
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

int translateString(int &direct, int &count_till, int &sped){
  //Convert from ASCII to decimal if there is new data availible.
  if (newData == true){
     direct = (receivedChars[0] & 0xf);               //Direction of motor.
     count_till = (receivedChars[2] & 0xf)*1000       //Count limit.
                      + (receivedChars[3] & 0xf)*100 
                      + (receivedChars[4] & 0xf)*10 
                      + (receivedChars[5] & 0xf);
     sped = (receivedChars[7]& 0xf)*100               //PWM speed.
                  + (receivedChars[8]& 0xf)*10
                  +(receivedChars[9]& 0xf);
    Serial.print(direct);
    Serial.print(count_till);
    Serial.println(sped);
    newData = false;                                  //Data recieve
  }                                                   //complete.
}

int Move(int &count){                   //Primary function for motor use.
    k = counter();                      //Calls counting function so when 
    if (k >= count_till) {              //count is achieved motor stops. 
      direct = 0;
      count = 0;
      }
    if (direct == 0) {                  //When not moving direct = 0,
      Stop();                           //motor is stopped.
    }
    if (direct == 1) {                  //Direct = 2, reverse motion
      forward_check = digitalRead(ForLimit);
      if(forward_check == 1){           //so long as limit isn't triggered.
          Forward();
        }        
      else{
        Stop();
        Serial.println("Forward Limit");
        Serial.println(k);
        count=0;
        direct = 0;
      }
    }
    if (direct == 2) {                  //Direct = 2, reverse motion
      reverse_check = digitalRead(RevLimit);
      if(reverse_check == 1){           //so long as limit isn't triggered.
        Reverse();
      }
      else{
        Stop();
        Serial.println("Reverse Limit");
        Serial.println(k);
        count=0;
        direct = 0;
      }
    }
}

void Forward() {                    //Forward function.
  for (int i = 0; i < 101; i++){    
    digitalWrite(A_1, HIGH);        //These writes are consistent,
    digitalWrite(A_2, LOW);         //they set the direction.
    if (i <= sped){         
      digitalWrite(A_PWM, HIGH);    //If statements are nested in 
    }                               //this for loop to set the
    else{                           //PWM speed for the motor.
      digitalWrite(A_PWM, LOW);
    }
  }
}

void Reverse() {                    //Reverse function.
  for (int i = 0; i < 101; i++){    
    digitalWrite(A_1, LOW);         //These writes are consistent,
    digitalWrite(A_2, HIGH);        //they set the direction.
    if (i <= sped){
      digitalWrite(A_PWM, HIGH);    //If statements are nested in
    }                               //this for loop to set the
    else{                           //PWM speed for the motor.
      digitalWrite(A_PWM, LOW);
    }
  }
}

void Stop() {                   //Stop function.
  digitalWrite(A_1, LOW);
  digitalWrite(A_2, LOW);
  digitalWrite(A_PWM, LOW);
}

int counter() {
    int switchState = digitalRead(count_pin);   //Read switch, store value,
    if(lastState != switchState){               //so long as there was no switch
       if(switchState == HIGH){                 //change; do nothing. If switch
        count++;                                //change add 1 to count.  
       }
    }
  lastState = switchState;
  return count;
}
