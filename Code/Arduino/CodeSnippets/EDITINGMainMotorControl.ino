int data = 0;
char userInput;

int A_1 = 10;
int A_2 = 9;
int A_PWM = 8;

int for_limitPin = 4;
int rev_limitPin = 5;

//Counting Function
int count = 0;      //Blanck variable to count high low transitions

int errorPin1 = 2;
int errorPin2 = 3;

int count_pin = 7;  //This will be the sensor to count pulses
                    //Right now I'm using a switch that I flip 
                    //back and forth by hand

int k = 0;          //For calling count func
int kPrevious = 0 ; //For remembering previous value delivered by 
                    //count func

const byte numChars = 32;
char receivedChars[numChars];

boolean newData = false;

int direct = 0;     //Direction motor moves forward or backward
int count_till = 0; //Limit that my system should count to then stop
int sped = 0;       //PWM wave

int func = 0;

void setup() {
  Serial.begin(9600);
  pinMode(A_1, OUTPUT);
  pinMode(A_2, OUTPUT);
  pinMode(A_PWM, OUTPUT);

  digitalWrite(A_1, LOW);
  digitalWrite(A_2, LOW);
  digitalWrite(A_PWM, LOW);

  pinMode(count_pin, INPUT);
  pinMode(test_pin, OUTPUT);
}

void loop() {
  recvWithStartEndMarker();
  showNewData(func, count_till, sped);
  Move(func);
}  

void recvWithStartEndMarker(){
  static boolean recvInProgress = false;
  static byte ndx = 0;
  char startMarker = '<';
  char endMarker = '>';
  char rc;
  
  while (Serial.available() > 0 && newData == false){
     rc = Serial.read();

     if (recvInProgress == true){
      
      if (rc != endMarker){
        receivedChars[ndx] = rc;
        ndx++;
        
        if(ndx >= numChars){
          ndx = numChars - 1;
        }
        
      }
      else{
        receivedChars[ndx] = '\0';
        recvInProgress = false;
        ndx = 0;
        newData = true;
      }
      
     }
     else if (rc == startMarker){
        recvInProgress = true;
      }
  }
}

int showNewData(int &func, int &count_till, int &sped){
  //Convert from ASCII to decimal
  if (newData == true){
     func = (receivedChars[0] & 0xf);
     count_till = (receivedChars[2] & 0xf)*1000
                      + (receivedChars[3] & 0xf)*100 
                      + (receivedChars[4] & 0xf)*10 
                      + (receivedChars[5] & 0xf);
     sped = (receivedChars[7]& 0xf)*100 
                  + (receivedChars[8]& 0xf)*10
                  +(receivedChars[9]& 0xf);

    newData = false;    
  }
}

int Move(int func){//int count_till, int count){
  Direction(func);
    if (direct == 0){
      Stop();
    }
    
    if (direct == 1) {
      Forward();
    }
    
    if (direct == 2) {
      Reverse();
    }
}

int pwm(int sped){

  for(int i = 0; i < 101; i++){
    if(i <= sped){
      digitalWrite(A_PWM, HIGH);
    }
    else{
      digitalWrite(A_PWM, LOW);
    }
  }
}


void Forward() {
  digitalWrite(A_1, HIGH);
  digitalWrite(A_2, LOW);
  digitalWrite(A_PWM, HIGH);
}

void Reverse() {
  digitalWrite(A_1, LOW);
  digitalWrite(A_2, HIGH);
  digitalWrite(A_PWM, HIGH);
}

void Stop() {
  digitalWrite(A_1, LOW);
  digitalWrite(A_2, LOW);
  digitalWrite(A_PWM, LOW);
  
}

int Direction(int func){
  if(digitalRead(for_limitPin) == 1 && func == 1){
    direct = 1;
  }
  if(digitalRead(rev_limitPin) == 1 && func == 2){
    direct = 2;
  }
  else{
    direct = 0;  
  }
  return direct;
}

int counter() {      
    int switchState = digitalRead(count_pin);
    if(lastState != switchState){
       if(switchState == HIGH){ 
        count++;

       }
       
    }
  lastState = switchState;
  return count;
}
