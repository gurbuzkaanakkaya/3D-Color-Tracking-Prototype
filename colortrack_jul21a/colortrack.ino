#include <Servo.h>
#define MotorR1 8
#define MotorR2 9
#define MotorRE 5 
#define MotorL1 10
#define MotorL2 11
#define MotorLE 6
int data_x1 = 0;
int data[0];
Servo myservo_x1;
Servo myservo_y1;




void setup() {
  Serial.begin(9600);
  myservo_x1.attach(4); 
  myservo_y1.attach(5); 
  pinMode(MotorL1, OUTPUT);
  pinMode(MotorL2, OUTPUT);
  pinMode(MotorLE, OUTPUT); 
  pinMode(MotorR1, OUTPUT);
  pinMode(MotorR2, OUTPUT);
  pinMode(MotorRE, OUTPUT);
}

void loop() {
 while (Serial.available() >= 2) {
     for (int i = 0; i < 2; i++) {
      data[i] = Serial.read();
     }
      myservo_x1.write(data[0]);
      myservo_y1.write(data[1]);
      Serial.println(data[0]);
      Serial.println(data[1]);
    
      if (data[0] > 100) {  
         sol();                  
  }
      else if(data[0]<70){
        sag();
  }    
      else
        sabit();
  }
 }


void sag(){  

  digitalWrite(MotorR1, LOW); 
  digitalWrite(MotorR2, HIGH); 
  analogWrite(MotorRE, 80); 

  digitalWrite(MotorL1, LOW); 
  digitalWrite(MotorL2, LOW); 
  analogWrite(MotorLE, 150); 
  
  
}
void sabit(){  

  digitalWrite(MotorR1, HIGH); 
  digitalWrite(MotorR2, HIGH); 
  analogWrite(MotorRE, 0); 

  digitalWrite(MotorL1, HIGH);
  digitalWrite(MotorL2, HIGH); 
  analogWrite(MotorLE, 0); 
  
  
}

void sol(){ 
  digitalWrite(MotorR1, LOW); 
  digitalWrite(MotorR2, LOW); 
  analogWrite(MotorRE, 110); 

  digitalWrite(MotorL1, HIGH); 
  digitalWrite(MotorL2, LOW); 
  analogWrite(MotorLE, 80); 
  
}
