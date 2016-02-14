/*
  ReadAnalogVoltage
  Reads an analog input on pin 0, converts it to voltage, and prints the result to the serial monitor.
  Attach the center pin of a potentiometer to pin A0, and the outside pins to +5V and ground.

 This example code is in the public domain.
 */

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(250000);
}

// the loop routine runs over and over again forever:
void loop() {
  // read the input on analog pin 0:
  if(Serial.available() > 0) {
    int data = Serial.read();
    if (data>0){
        int count = 0;
        int sum = 0;
        int num =10000;
        for (int i=0; i <= num; i++){
          int sensorValue = analogRead(A1);
          sum  = sum+sensorValue;
          count++;
        }
        double sumf = (double) sum;
        double countf = (double) count;
        Serial.println(sumf/countf);
    }
    if (data==0){
      Serial.print("Ro");
      Serial.println("Roger");
      Serial.flush();
    }
  }
}
