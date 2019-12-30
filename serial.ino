/*
 *  BRAINTECH PRIVATE LIMITED 
 *  JOHN MELODY MELISSA 
 */
int k;
void setup() {
  // initialize serial:
  Serial.begin(115200);
 
}

void loop() {
  // if there's any serial available, read it:
  while (Serial.available() > 0) {
    int k = Serial.read();
    Serial.println(k); 
    // Serial.println(k, HEX);  //**for HEX
    }
  
}
