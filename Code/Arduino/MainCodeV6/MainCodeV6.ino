/* Small Radio Telescope - Motor Control
   Winona State University Research
   Clayton G. Hanson
      The SRT pivots on its stand 180 degrees on the x-y 
   plane flat the flat of the Earth. A second motor
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
int revLimitReach = 0; //Reverse limit hasn't been reached.
int forLimitReach = 0; //Forward limit hasn't been reached.


//Counting Function variables
int count = 0;      //Blank variable to count high low transitions.
int count_pin = 4;  //This will be the sensor to count pulses.

int lastState = 0;  //Stores switch state.
int switchState = 0;//To check switch state.

int k;          //For calling counter function.
int zeroed = 0;

const byte numChars = 32;       //These establish a variable for the
char receivedChars[numChars];   //string being read from the Pi.

boolean newData = false;        //Reset for new data from the Pi.

int order = 0;
int direct = 0;     //Direction motor moves forward or backward.
int count_till = 0; //Limit that my system should count to then stop.
int sped = 0;       //PWM wave speed.
int request = 0;

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
  translateString(request, order, count_till, sped);
  pickFunction(request);
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

int translateString(int &request, int &order, int &count_till, int &sped){
  //Convert from ASCII to decimal if there is new data availible.
  if (newData == true){
     request = (receivedChars[0] & 0xf);             //Print pulse count.
     order = (receivedChars[2] & 0xf);               //Orders for motor.
     count_till = (receivedChars[4] & 0xf)*1000       //Count limit.
                      + (receivedChars[5] & 0xf)*100 
                      + (receivedChars[6] & 0xf)*10 
                      + (receivedChars[7] & 0xf);
     sped = (receivedChars[9]& 0xf)*100               //PWM speed.
                  + (receivedChars[10]& 0xf)*10
                  +(receivedChars[11]& 0xf);
    
    newData = false;                                  //Data recieve
  }                                                   //complete.
}

int Move(int &count, int &forLimitReach, int &revLimitReach, int &zeroed){                   //Primary function for motor use.
    k = counter();                      //Calls counting function so when 
      if (k == count_till && zeroed == 1) {              //count is achieved motor stops. 
        direct = 0;
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
          delay(5);
          count=2005;
          direct = 0;
          forLimitReach = 1;
          zeroed = 1;
        }
      }
      if (direct == 2) {                  //Direct = 2, reverse motion
        reverse_check = digitalRead(RevLimit);
        if(reverse_check == 1){           //so long as limit isn't triggered.
          Reverse();
        }
        else{
          Stop();
          delay(5);
          count=0;
          direct = 0;
          revLimitReach = 1;
          zeroed = 1;
        }
      }
}

int pickFunction(int &request) {
  if (order == 0){        //Do nothing loop. More of a precaution
    direct = 0;
    Move(count, forLimitReach, revLimitReach, zeroed);
  }
  if (order == 1){        //Forward loop, for direct control.
    direct = 1;
    Move(count, forLimitReach, revLimitReach, zeroed);
  }
  if (order == 2){        //Reverse loop, for direct control.
    direct = 2;
    Move(count, forLimitReach, revLimitReach, zeroed);
  }
  if (order == 3){                    //Order = 3 is the Go Home function.
    GoHome(direct, forLimitReach, revLimitReach);
  }
  if (request == 9){
    k = counter();
    Serial.print(k);
    Serial.println(" ");
    request = 0;
  }
}

int GoHome(int &direct, int &forLimitReach, int &revLimitReach){
    if (count > 1004){                //Count = 1003 is the Home position for now
      if (forLimitReach == 0){        //If the count is higher than 1003 check 
        direct = 1;                   //the forward limit before heading home.
        Move(count, forLimitReach, revLimitReach, zeroed);
      }
      else{
        direct = 2;
        Move(count, forLimitReach, revLimitReach, zeroed);
      }
    }
    if (count < 1002){                //If the count is less than 1003 check the 
      if (revLimitReach == 0){        //reverse limit before going home.
        direct = 2;
        Move(count, forLimitReach, revLimitReach, zeroed);
      }
      else{
        direct = 1;
        Move(count, forLimitReach, revLimitReach, zeroed);
      }
    }
    if(count >= 1002 && count <= 1004){                //Dish is Home. Wait for new order.
      direct = 0;
      forLimitReach = 0;
      revLimitReach = 0;
      order = 0;
    }
}


void Forward() {                //Forward function.
  for (int i = 0; i < 101; i++){
    digitalWrite(A_1, HIGH);
    digitalWrite(A_2, LOW);
    if (i <= sped){
      digitalWrite(A_PWM, HIGH);
    }
    else{
      digitalWrite(A_PWM, LOW);
    }
  }
}

void Reverse() {                //Reverse function.
  for (int i = 0; i < 101; i++){
    digitalWrite(A_1, LOW);
    digitalWrite(A_2, HIGH);
    if (i <= sped){
      digitalWrite(A_PWM, HIGH);
    }
    else{
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
        if(direct == 1){                      //change add 1 to count if 
           count++;                           //motion is forward, subtract
        }                                     //1 if motion is reverse.
        if(direct == 2){
           count--;                             
        }
        
     }
  }
  lastState = switchState;
  return count;
}
