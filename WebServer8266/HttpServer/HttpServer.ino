/*********
 * Coding done by Andy Wong-MYBOTIC
 * Control the LED by using webserver and update the information to webserver
*********/

#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>

MDNSResponder mdns;

// Replace with your network credentials
const char* ssid = "JohnMelodyCindy";
const char* password = "ilovecindy";

ESP8266WebServer server(80);
String webSite="";
int sensorPin=12;
int led0=13;
int led1= 4;
int led2 = 5;
int ledSensor=16;

  
void setup(void){
  
  webSite +="<meta http-equiv='refresh' content='3'><title>ESP8266 Demo</title>\n";
  webSite += "<style>body{ background-color: #cccccc; font-family: Arial, Helvetica, Sans-Serif; Color: #000088; }</style>\n";
  webSite +="<h2 dir=\"rtl\" style=\"text-align: left;\"><img alt=\"\" src=\"http://www.mybotic.com.my/webshaper/pcm/pictures/Mybotic-Logo-(5).jpg\" style=\"float: left; height: 103px; width: 999px; border-width: 15px; border-style: solid;\" /></h2>\n";
  webSite +="<p> &nbsp;</p><p>&nbsp;</p><p>&nbsp;</p><p>&nbsp;</p><p>&nbsp;</p>\n";
  webSite+="<button onclick='myFunction()'>HOME</button>";
  webSite+="<script>function myFunction() {location.reload();}</script>";
  webSite +="<h1>ESP8266 Web Server</h1><p>LED #1 <a href=\"socket1On\"><button>ON</button></a>&nbsp;<a href=\"socket1Off\"><button>OFF</button></a></p>\n";
  webSite += "<p>LED #2 <a href=\"socket2On\"><button>ON</button></a>&nbsp;<a href=\"socket2Off\"><button>OFF</button></a></p>\n";
  webSite +=" <p><h2>Condition read from flamesensor</h2></p>\n";
  
  // preparing GPIOs
  pinMode(led0, OUTPUT);
  digitalWrite(led0, LOW);
  pinMode(led1, OUTPUT);
  digitalWrite(led1, LOW);
  pinMode(led2, OUTPUT);
  digitalWrite(led2, LOW);
  pinMode(sensorPin,INPUT);
  pinMode(ledSensor,OUTPUT);
  
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  Serial.println("");
  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  digitalWrite(led0,HIGH);
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  
 if (mdns.begin("esp8266", WiFi.localIP())) {
   Serial.println("MDNS responder started");
  }
    server.on("/", [](){
    server.send(200, "text/html", webSite);
    });
  server.on("/socket1On", [](){
    server.send(200, "text/html", webSite);
    digitalWrite(led1, HIGH);
  });
  server.on("/socket1Off", [](){
    server.send(200, "text/html", webSite);
    digitalWrite(led1, LOW);
  });
  server.on("/socket2On", [](){
    server.send(200, "text/html", webSite);
    digitalWrite(led2, HIGH); 
  });
  server.on("/socket2Off", [](){
    server.send(200, "text/html", webSite);
    digitalWrite(led2, LOW);
  });
    
  server.begin();
  Serial.println("HTTP server started");
}
 
void loop(void){
  server.handleClient();
  String sentences="<p>Flame is detected!!!</p>";
  if(WiFi.status() != WL_CONNECTED)
  {
    digitalWrite(led0, LOW);
    Serial.println("");
    Serial.print("Wifi is disconnected!");
    Serial.println("");
    Serial.print("Reconnecting");
    Serial.println("");
    //WiFi.begin(ssid,password);
    
    while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    }
    digitalWrite(led0,HIGH);
  }
 
  if(digitalRead(sensorPin) ==LOW) 
  {
   Serial.print("Flame is detected");
   Serial.println("");
   webSite+=sentences;
   digitalWrite(ledSensor,HIGH);
   delay(300);
   
  }
  else                            //if no detect
  {
   digitalWrite(ledSensor,LOW);
  }

} 
