void I_Scan();
void J_Scan();
int j;
int i;
void J_Scan() {
  //for loops will act as a scanning function over a 2d sky
  //i and j will act as coordinates on a plane
  //be safe kids
  //for each j run an entire i then add a j
  for (j = 0; j < 3;) {
    if (j == 0) {
      I_Scan();
    }
    if (j > 0, j < 3) {
      Plus_Motor2();
      delay(1000);
      Motors_OFF;
      I_Scan();
      if (j == 3) {
        Plus_Motor2();
        delay(1000);
        Motors_OFF;
        I_Scan();
        Minus_Motor2();
        delay(3000);
        Motors_OFF();
      }
    }
  }
}

void I_Scan() {
  for (i = 0; i < 4; i++) {

    if (i == 0) {
      delay(1000);//read the first piece of sky
    }
    if (i > 0, i < 3) {
      Plus_Motor1();
      delay(1000); //move to next space, adjust time as needed
      //or seriel read sensor here
      Motors_OFF();//Don't leave it on dummy
    }
    if (i == 3) {
      Plus_Motor1();
      delay(1000);
      Motors_OFF();
      Minus_Motor1();
      delay(3000);
      Motors_OFF();
      j++;
    }
  }
}

