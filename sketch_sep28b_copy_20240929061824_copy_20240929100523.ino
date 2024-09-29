/*
  The LCD will display readings from a temperature sensor, humidity sensor, photoresistor and US sensor
*/

#include <LiquidCrystal.h>                  
LiquidCrystal lcd(13, 12, 11, 10, 9, 8);               

float humidity = 0;
float light = 0;
float celsius = 0;
float height = 0;

int buttonCounter = 0;
int buttonNow = 0;
int buttonPrev = 0;

void setup() {

  Serial.begin(9600);
  //Output for led nightlight
  pinMode(6, OUTPUT);

  //I/O for US
  pinMode(4, OUTPUT);
  pinMode(7, INPUT);

  //Inputs for Button
  pinMode(2, INPUT_PULLUP);
  pinMode(1, INPUT_PULLUP);
  //Initalize screen
  lcd.begin(16, 2); 
  lcd.clear();
} 

void loop() {

  //Get distance from HCSR04
  height = (0.33 - getDistance()*7.7/316.95)*100;

  //Get humidity from DH11
  humidity = (analogRead(A0)* 0.004882813 - 3)*5/2;

  //Get temperature from TMP36
  celsius = analogRead(A2)* 0.004882813;

  //Get light from photoresistor
  light = analogRead(A1)/1000;
  
  //Set LCD
  lcd.clear(); 
  lcd.setCursor(0,0); 
  
  buttonPrev = buttonNow;
  buttonNow = buttonCheck();

  if (buttonNow == 1){
    if (buttonPrev == 0){
      if (buttonCounter == 3){
        buttonCounter = 0;
      }
      else{
        buttonCounter++;
      }
    } 
  }

  switch (buttonCounter){
    case 0:
      lcd.print("Degrees C: ");
      lcd.print(celsius);
      lcd.print("C");
      lcd.setCursor(0,1); 
      lcd.print("Degrees F: ");
      lcd.print(celsius*9/5+32);
      lcd.print("F");
      lcd.setCursor(0,0); 
      break;
    case 1:
      lcd.print("Height: ");
      lcd.print(height);
      lcd.print("cm");
      break;
    case 2:
      lcd.print("Light: ");
      lcd.print(light);
      lcd.print("LU");
      break;
    default:
      lcd.print("Humidity: ");
      lcd.print(humidity);
      lcd.print("RH");
      break;
  };

  Serial.print(celsius); 
  Serial.print(",");
  Serial.print(height);
  Serial.print(",");
  Serial.print(light);
  Serial.print(",");
  Serial.println(humidity);
  
  delay(1000); 

  if (photoresistor < threshold) {
    digitalWrite(13, HIGH);         // Turn on the LED
  } else {
    digitalWrite(13, LOW);          // Turn off the LED
  }
  if (b)

}

float getDistance()
{
  float echoTime;                   
  float calculatedDistance;        

  digitalWrite(4, HIGH);
  delayMicroseconds(10);
  digitalWrite(4, LOW);

  echoTime = pulseIn(7, HIGH);      

  calculatedDistance = echoTime / 148.0;  

  return calculatedDistance;
}

int buttonCheck() {
  if (digitalRead(2) == LOW) {
    return 1;
  } 
  return 0;
}