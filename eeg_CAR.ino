/**
 * Copyright 2020 © John Melody Melissa
 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * @Author : John Melody Melissa
 * @Copyright: John Melody Melissa  © Copyright 2020
 * @INPIREDBYGF : Tan Sin Dee <3
 * @Project : Brain Computer Interface Car
 * This is a source code for Mind Controlled Car
 * @DEMONSTARTION : https://vt.tiktok.com/65HrhM/
 *
 */

int runOne, runTwo;
int power = 11;
int carOne, carTwo;
int button;
int inputOne, inputTwo;
int Condition = 1;
int serial;

serial = 9600;
inputOne = 0;
inputTwo = 0;
button = 4;
carOne = 7;
carTwo = 8;

void setup () {
    Serial.begin(serial);
    pinMode(carOne, OUTPUT);
    pinMode(carTwo, OUTPUT);
    pinMode(power, OUTPUT);
    pinMode(button, OUTPUT);
    digitalWrite(power, OUTPUT);
    analogWrite(carOne, 0);
    analogWrite(carTwo, 0);
    // delay(2000);
}

void loop () {
    if (digitalRead (button) == LOW) {
        while (digitalRead (button) == LOW);
        if (Condition == 0) {
            Condition = 1;
            digitalWrite(power, HIGH);
            analogWrite(carOne, 0);
            analogWrite(carTwo, 0);
            delay(1000);
        } else {
          Condition = 0;
          digitalWrite(power, LOW);
          delay(1000);
       }
    } else if (Condition == 0){
      // If There's noBrain Signal,
      // run te car randomly;
      runOne = random(150, 210);
      runTwo = random(150, 210);
      analogWrite(carOne, runOne);
      analogWrite(carTwo, runTwo);
      delay(500);
      // LED Indicate if There's no EEG signal received.
      digitalWrite(13, LOW);
    } else if (Condition == 1){
      digitalWrite(13, HIGH);
      inputOne = analogRead(A0);
      inputTwo = analogRead(A2);
      Serial.print("INPUT ONE = " + inputOne);
      Serial.print("INPUT TWO = " + inputTwo);

      if(inputOne > 400){
      analogWrite(carOne, 0);
      }

      if(inputTwo > 400){
      analogWrite(carTwo, 0);
      }

      if(inputOne < 400 && inputOne > 100){
      analogWrite(carOne, 160);
      }

      if(inputTwo < 400 && inputTwo > 100){
      analogWrite(carTwo, 160);
      }

      if(inputOne < 100 && inputOne > 1){
      analogWrite(carOne, 180);
      }

      if(inputTwo < 100 && inputTwo > 1){
      analogWrite(carTwo, 180);
      }

      if(inputOne == 0){
      analogWrite(carOne, 210);
      }

      if(inputTwo == 0){
      analogWrite(carTwo, 210);
      }

      delay(200);
    } else {
       analogWrite(carOne, 0);
       analogWrite(carTwo, 0);
    }
}
