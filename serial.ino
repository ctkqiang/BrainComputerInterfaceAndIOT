/** 
 *  @AUTHOR: JOHN MELODY MELISSA 
 */

int s;
void setup() {
  // initialize serial:
  Serial.begin(115200);
 
}

void loop() {
  // IF  THERE 'S ANY SERIAL AVAILABLE, READ IT:
  while (Serial.available() > 0) {
    int s = Serial.read();
    Serial.println(k); 
    //Serial.println(k, HEX);  //**FOR HEX
    } 
}
