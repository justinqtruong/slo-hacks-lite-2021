#include <LiquidCrystal.h>

LiquidCrystal lcd = LiquidCrystal(13,12,11,10,9,8); //initialize led
int greenLight = 2;
int redLight = 3;
int pin;
const int trigPin = 4;
const int echoPin = 5;
double duration, distance;
int sum = 0;
const int buzzer = 6;

void setup(){
  pinMode(greenLight, OUTPUT);
  pinMode(redLight, OUTPUT);
  pinMode(trigPin, OUTPUT);
  pinMode(buzzer, OUTPUT);
  pinMode(echoPin, INPUT);
  Serial.begin(9600);
  turnOn(greenLight);
  lcd.begin(16,2);//led
  lcd.setCursor(2, 0);//led
  lcd.print("Player 1: ");//led
  lcd.print(sum);//led
  lcd.setCursor(2, 1);//led
  lcd.print("Player 2: ");//led
  lcd.print(sum);//led

}

void loop(){  
  findDistance(); 
  delay(100);
  checkGameStatus();
  delay(100);
  //if(Serial.available()) {
  //     data = Serial.read();
  //     Serial.println("player2" or "player1");
  //}
  

}

void findDistance(){
 digitalWrite(trigPin, LOW); 
 delayMicroseconds(2); 
 digitalWrite(trigPin, HIGH); 
 delayMicroseconds(10); 
 digitalWrite(trigPin, LOW);
 duration = pulseIn(echoPin, HIGH);
 distance = (duration*.0343)/2;
 if (distance < 40){      
     sum++;
     Serial.print("Player 1 Score: ");
     Serial.println(sum);
     lcd.setCursor(2, 0);//led
     lcd.print("Player 1: ");//led
     lcd.print(sum);//led
     lcd.setCursor(2, 1);//led
     lcd.print("Player 2: ");//led
     lcd.print(sum);//led
}
  
}



void turnOn(int pin){ 
  digitalWrite(pin, HIGH);
}
           
void turnOff(int pin){
  digitalWrite(pin, LOW);
}

int getSum(){return sum;}    


void checkGameStatus(){
  if (sum >= 10){
    turnOff(greenLight);
    turnOn(redLight);
    //tone(buzzer,500);
    getSum();
    lcd.clear();
    lcd.setCursor(2, 0);
    lcd.print("Player One WINS ");
    lcd.setCursor(2, 1);
    lcd.print("Virtual BP");
    
  

    // Serial.println("player1" or "player2");
    Serial.println("Virtual BP Win");
    delay(1000);
    lcd.clear();
    sum = 0;
    turnOff(redLight);
    turnOn(greenLight);
    //noTone(buzzer);
    lcd.setCursor(2, 0);
    lcd.print("Player 1: ");
    lcd.print(sum);
    lcd.setCursor(2, 1);
    lcd.print("Player 2: ");
    lcd.print(sum);
    
  }
}
