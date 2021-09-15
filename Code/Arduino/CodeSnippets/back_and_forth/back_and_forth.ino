//int analogPin = 3;
int data = 0;
char userInput;

int A_1 = 10;
int A_2 = 9;
int A_PWM = 8;


//Counting Function
int count = 0;      //Blanck variable to count high low transitions

int errorPin1 = 2;
int errorPin2 = 3;

int limit1 = 5;
int limit2 = 6;

int count_pin = 3;  //This will be the sensor to count pulses
                    //Right now I'm using a switch that I flip 
                    //back and forth by hand
int test_pin = 4;   //Hooked to oscilloscope to see what's running

int lastState = 0;  //Stores switch state
int switchState = 0;//To check switch state

int k = 0;          //For calling count func
int kPrevious = 0 ; //For remembering previous value delivered by 
                    //count func

const byte numChars = 32;
char receivedChars[numChars];

boolean newData = false;

int direct = 0;     //Direction motor moves forward or backward
int count_till = 0; //Limit that my system should count to then stop
int sped = 0;       //PWM wave

int check = 0;
int Status;

void setup() {
  Serial.begin(9600);
  pinMode(A_1, OUTPUT);
  pinMode(A_2, OUTPUT);
  pinMode(A_PWM, OUTPUT);

  digitalWrite(A_1, LOW);
  digitalWrite(A_2, LOW);
  digitalWrite(A_PWM, LOW);

  pinMode(limit1, INPUT);
  pinMode(limit2, INPUT);

  pinMode(count_pin, INPUT);
  pinMode(test_pin, OUTPUT);
  //attachInterrupt(digitalPinToInterrupt(errorPin1), errorCheck, FALLING);
  //attachInterrupt(digitalPinToInterrupt(errorPin2), errorCheck, FALLING);
}

void Forward();
void Reverse();
void Stop();
//int Move(direct);
int counter();

int atlimit1 = digitalRead(limit1);
int atlimit2 = digitalRead(limit2);
int last_direct = 1;

void loop() {
  //recvWithStartEndMarker();
  //showNewData(direct, count_till, sped);
  //while(direct != 0){
    
    if(last_direct == 0){
      k=counter();
      if(digitalRead(limit1) == 1 && digitalRead(limit2) == 1){
          Forward();
          Serial.println(k);      
        }
      else{
        //delay(5000);
        if(digitalRead(limit1) != 1 || digitalRead(limit2) != 1){
          Reverse();
          Serial.println(k);
        } 
        else{
        last_direct = 1; 
        k=0;
        //delay(5000);
            
      }    
    }
    }
    if(last_direct == 1){
      k=counter();
      if(digitalRead(limit1) == 1 && digitalRead(limit2) == 1){
          Reverse();
          Serial.println(k); 
        }
      else{
        //delay(5000);
        if(digitalRead(limit1) != 1 || digitalRead(limit2) != 1){
          Forward();
          Serial.println(k);
        }
        else{
        last_direct = 0;
        k=0; 
        //delay(5000);
        }
      }     
    }
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

int showNewData(int &direct, int &count_till, int &sped){
  //Convert from ASCII to decimal
  if (newData == true){
     direct = (receivedChars[0] & 0xf);
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
/*
int Move(int direct){//int count_till, int count){
  
    if (direct == 1) {
      Forward();
    }
    
    if (direct == 2) {
      Reverse();
    }
}*/
/*
int pwm(int sped){

  for(int i = 0; i < 99; i++){
    if(i <= sped){
      digitalWrite(A_PWM, HIGH);
    }
    else{
      digitalWrite(A_PWM, LOW);
    }
  }
  
}
*/

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

int counter() {       //rest){
    //if(reset==1)
      //count = 0
    int switchState = digitalRead(count_pin);
  
    if(lastState != switchState){
       if(switchState == HIGH){ 
        count++;
        //Serial.println(count);
       }
       
    }
  lastState = switchState;
  return count;
}

/*
//Lets use attatch interrupt somewhere here
int returnMessage(int Status){
  if (Status == 1){
    Serial.println("Error: Motor Load Open ");
  }
  if (Status == 2){
    Serial.println("Error: Detected Over Current ");
  }
  if (Status == 3){
    Serial.println("Error: Detected Over Thermal ");
  }
  if (Status == 4){
    Serial.println("Error: Unknown ");
  }
}

void errorCheck(){
  int error1 = digitalRead(errorPin1);
  int error2 = digitalRead(errorPin2);

  if(error1 == HIGH && error2 == HIGH){
    Status = 0;
  }
  if(error1 == HIGH && error2 == LOW){
    Status = 1;
  }
  if(error1 == LOW && error2 == HIGH){
    Status = 2;
  }
  if(error1 == LOW && error2 == LOW){
    Status = 3;
  }
  returnMessage(Status);
}*/
