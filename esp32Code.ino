
#include <esp32cam.h>
#include <WebServer.h>
#include <WiFi.h>

const char* WIFI_SSID = "lauro";
const char* WIFI_PASS = "lauro1995";

WebServer server(80);

static auto loRes = esp32cam::Resolution::find(800, 600);
static auto hiRes = esp32cam::Resolution::find(1024, 768);

void serveJpg()
{
   auto frame = esp32cam::capture();
   if (frame == nullptr){
     Serial.println("CAPTURE FAIL");
     server.send(503, "", "");
     return;
   }
   Serial.printf("CAPTURE OK %dx%d %db\n", frame->getWidth(), frame->getHeight(),
                  static_cast<int>(frame->size()));

   server.setContentLength(frame->size());
   server.send(200, "image/png");
   WiFiClient client = server.client();
   frame->writeTo(client);
}

void handleJpgLo()
{
  if (!esp32cam::Camera.changeResolution(loRes)){ 
    Serial.println("SET-LO-RES FAIL");
  }
  serveJpg();
}

void handleJpgHi()
{
  if (!esp32cam::Camera.changeResolution(hiRes)){ 
    Serial.println("SET-HI-RES FAIL");
  }
  serveJpg();
}

void setup()
{
  Serial.begin(115200);
  Serial.println();

  {
    using namespace esp32cam;
    Config cfg;
    cfg.setPins(pins::AiThinker);
    cfg.setResolution(hiRes);
    cfg.setBufferCount(2);
    cfg.setJpeg(80);

    bool ok = Camera.begin(cfg);
    Serial.println(ok ? "CAMERA OK" : "CAMERA FAIL");
  }

 WiFi.persistent(false);
 WiFi.mode(WIFI_STA);
 WiFi.begin(WIFI_SSID, WIFI_PASS);
 while (WiFi.status() != WL_CONNECTED) {
    delay(500);

 }

 Serial.print("http://");
 Serial.print(WiFi.localIP());
 Serial.println("/cam-lo.png");

 Serial.print("http://");
 Serial.print(WiFi.localIP());
 Serial.println("/cam-hi.png");

 server.on("/cam-lo.png", handleJpgLo);
 server.on("/cam-hi.png", handleJpgHi);

 server.begin();
 }
 void loop()
 {
  server.handleClient();
}

