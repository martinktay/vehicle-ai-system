// ============================================================================
// vehicle_system.ino - Agentic AI-Driven Multi-Fuel Vehicle Optimization
// ============================================================================
//
// Board: ESP32
// Purpose: Stable hardware demo firmware for LCD, Serial Dashboard, and Cloud
// Dashboard.
//
// Demo flow:
//   - DS18B20 / thermistor represents engine temperature.
//   - Ultrasonic distance represents fuel level.
//   - Close flat object to ultrasonic sensor = high fuel.
//   - Move object away = fuel level falls.
//   - Low fuel triggers relay 2 and CNG recommendation.
//   - High temperature triggers relay 1, LPG recommendation, buzzer, and red LED.
//
// Output contracts:
//   - Serial prints v1 JSON for the Serial Dashboard /api/latest pipeline.
//   - WiFi POST sends v2 JSON for the Cloud Dashboard /api/telemetry pipeline.
//
// ============================================================================

#include <WiFi.h>
#include <HTTPClient.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <LiquidCrystal.h>
#include "config.h"

// ============================================================================
// DEMO TUNING
// ============================================================================

const int ULTRASONIC_SAMPLE_COUNT = 7;
const float DISTANCE_SMOOTHING_ALPHA = 0.30;  // Higher = faster, lower = smoother.
const int FUEL_CHANGE_STEP_PERCENT = 2;

const int LOW_FUEL_ENTER_PERCENT = 18;
const int LOW_FUEL_EXIT_PERCENT = 25;
const int RELAY2_ENTER_PERCENT = 20;
const int RELAY2_EXIT_PERCENT = 28;

const float HIGH_TEMP_ENTER_C = TEMP_HIGH_THRESHOLD;
const float HIGH_TEMP_EXIT_C = TEMP_HIGH_THRESHOLD - 4.0;
const float CRITICAL_TEMP_ENTER_C = TEMP_CRITICAL;
const float CRITICAL_TEMP_EXIT_C = TEMP_CRITICAL - 4.0;

const int LOW_LIGHT_ENTER = 450;
const int LOW_LIGHT_EXIT = 650;

// ============================================================================
// HARDWARE INITIALIZATION
// ============================================================================

OneWire oneWire(PIN_DS18B20);
DallasTemperature ds18b20(&oneWire);

LiquidCrystal lcd(
  PIN_LCD_RS,
  PIN_LCD_E,
  PIN_LCD_D4,
  PIN_LCD_D5,
  PIN_LCD_D6,
  PIN_LCD_D7
);

// ============================================================================
// GLOBAL STATE
// ============================================================================

float temperature = 28.0;
float distanceCm = FUEL_TANK_FULL_CM;
float rawDistanceCm = FUEL_TANK_FULL_CM;
float smoothedDistanceCm = FUEL_TANK_FULL_CM;

int fuelPercent = 100;
int stableFuelPercent = 100;
int ldrValue = 0;
int thermistorValue = 0;

String fuelMode = "PETROL";
String systemStatus = "NORMAL";
String relay1State = "OFF";
String relay2State = "OFF";
String decisionReason = "System starting up";
float costSaved = 0.0;
float co2Reduction = 0.0;

bool ds18b20Available = false;
bool wifiConnected = false;
bool lowFuelLatched = false;
bool relay2Latched = false;
bool highTempLatched = false;
bool criticalTempLatched = false;
bool lowLightLatched = false;

unsigned long lastWifiAttempt = 0;
unsigned long lastTelemetryTime = 0;

// ============================================================================
// SETUP
// ============================================================================

void setup() {
  Serial.begin(SERIAL_BAUD_RATE);
  delay(500);

  Serial.println();
  Serial.println("============================================================");
  Serial.println("  Agentic AI-Driven Multi-Fuel Vehicle Optimization System");
  Serial.println("  Vehicle ID: " VEHICLE_ID);
  Serial.println("============================================================");

  lcd.begin(16, 2);
  showLCDMessage("Vehicle AI Sys", "Initializing...");

  ds18b20.begin();
  ds18b20Available = ds18b20.getDeviceCount() > 0;

  Serial.print("[SENSOR] DS18B20 devices found: ");
  Serial.println(ds18b20.getDeviceCount());

  pinMode(PIN_ULTRASONIC_TRIG, OUTPUT);
  pinMode(PIN_ULTRASONIC_ECHO, INPUT);

  pinMode(PIN_LED_RED, OUTPUT);
  pinMode(PIN_LED_GREEN, OUTPUT);
  pinMode(PIN_LED_YELLOW, OUTPUT);

  pinMode(PIN_BUZZER, OUTPUT);
  digitalWrite(PIN_BUZZER, LOW);

  pinMode(PIN_RELAY_1, OUTPUT);
  pinMode(PIN_RELAY_2, OUTPUT);
  digitalWrite(PIN_RELAY_1, LOW);
  digitalWrite(PIN_RELAY_2, LOW);

  digitalWrite(PIN_LED_GREEN, HIGH);
  digitalWrite(PIN_LED_RED, LOW);
  digitalWrite(PIN_LED_YELLOW, LOW);

  connectWiFi();

  showLCDMessage("System Ready", wifiConnected ? "WiFi: OK" : "WiFi: Offline");
  Serial.println("[INIT] Setup complete. Entering main loop.");
  Serial.println("============================================================");

  delay(1500);
}

// ============================================================================
// MAIN LOOP
// ============================================================================

void loop() {
  unsigned long now = millis();

  readTemperature();
  readUltrasonic();
  readLDR();
  readThermistor();

  calculateFuelPercent();
  updateDemoLatches();
  selectFuelMode();
  determineStatus();
  controlOutputs();

  if (now - lastTelemetryTime >= TELEMETRY_INTERVAL_MS) {
    lastTelemetryTime = now;

    updateLCD();

    String serialPayload = buildSerialDashboardJSON();
    Serial.println(serialPayload);

    String cloudPayload = buildCloudTelemetryJSON();
    sendTelemetryToCloud(cloudPayload);
  }

  if (!wifiConnected && (now - lastWifiAttempt >= WIFI_RETRY_INTERVAL_MS)) {
    connectWiFi();
  }

  delay(100);
}

// ============================================================================
// SENSOR READING FUNCTIONS
// ============================================================================

void readTemperature() {
  if (ds18b20Available) {
    ds18b20.requestTemperatures();
    float temp = ds18b20.getTempCByIndex(0);

    if (temp != DEVICE_DISCONNECTED_C && temp > -55.0 && temp < 125.0) {
      temperature = temp;
      return;
    }
  }

  // Demo fallback: if DS18B20 is missing, use thermistor analog as a rough
  // temperature input so the dashboard still moves during a video demo.
  int rawThermistor = analogRead(PIN_THERMISTOR);
  temperature = map(rawThermistor, 0, 4095, 25, 80);
}

void readUltrasonic() {
  float samples[ULTRASONIC_SAMPLE_COUNT];
  int validSamples = 0;

  for (int i = 0; i < ULTRASONIC_SAMPLE_COUNT; i++) {
    float reading = readSingleDistanceCm();

    if (reading >= FUEL_TANK_FULL_CM && reading <= FUEL_TANK_EMPTY_CM) {
      samples[validSamples] = reading;
      validSamples++;
    }

    delay(12);
  }

  if (validSamples == 0) {
    return;
  }

  sortFloatArray(samples, validSamples);

  rawDistanceCm = samples[validSamples / 2];
  smoothedDistanceCm =
    (smoothedDistanceCm * (1.0 - DISTANCE_SMOOTHING_ALPHA)) +
    (rawDistanceCm * DISTANCE_SMOOTHING_ALPHA);

  distanceCm = constrain(smoothedDistanceCm, FUEL_TANK_FULL_CM, FUEL_TANK_EMPTY_CM);
}

float readSingleDistanceCm() {
  digitalWrite(PIN_ULTRASONIC_TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(PIN_ULTRASONIC_TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(PIN_ULTRASONIC_TRIG, LOW);

  long duration = pulseIn(PIN_ULTRASONIC_ECHO, HIGH, 30000);
  if (duration <= 0) {
    return -1.0;
  }

  return (duration * 0.0343) / 2.0;
}

void readLDR() {
  ldrValue = analogRead(PIN_LDR);
}

void readThermistor() {
  thermistorValue = analogRead(PIN_THERMISTOR);
}

// ============================================================================
// FUEL CALCULATION & DECISION ENGINE
// ============================================================================

void calculateFuelPercent() {
  int calculatedFuelPercent = 0;

  if (distanceCm <= FUEL_TANK_FULL_CM) {
    calculatedFuelPercent = 100;
  } else if (distanceCm >= FUEL_TANK_EMPTY_CM) {
    calculatedFuelPercent = 0;
  } else {
    calculatedFuelPercent = (int)map(
      (long)(distanceCm * 100),
      (long)(FUEL_TANK_FULL_CM * 100),
      (long)(FUEL_TANK_EMPTY_CM * 100),
      100,
      0
    );
    calculatedFuelPercent = constrain(calculatedFuelPercent, 0, 100);
  }

  if (abs(calculatedFuelPercent - stableFuelPercent) >= FUEL_CHANGE_STEP_PERCENT) {
    stableFuelPercent = calculatedFuelPercent;
  }

  fuelPercent = stableFuelPercent;
}

void updateDemoLatches() {
  lowFuelLatched = updateLatch(
    lowFuelLatched,
    fuelPercent <= LOW_FUEL_ENTER_PERCENT,
    fuelPercent >= LOW_FUEL_EXIT_PERCENT
  );

  relay2Latched = updateLatch(
    relay2Latched,
    fuelPercent <= RELAY2_ENTER_PERCENT,
    fuelPercent >= RELAY2_EXIT_PERCENT
  );

  highTempLatched = updateLatch(
    highTempLatched,
    temperature >= HIGH_TEMP_ENTER_C,
    temperature <= HIGH_TEMP_EXIT_C
  );

  criticalTempLatched = updateLatch(
    criticalTempLatched,
    temperature >= CRITICAL_TEMP_ENTER_C,
    temperature <= CRITICAL_TEMP_EXIT_C
  );

  lowLightLatched = updateLatch(
    lowLightLatched,
    ldrValue <= LOW_LIGHT_ENTER,
    ldrValue >= LOW_LIGHT_EXIT
  );
}

void selectFuelMode() {
  if (lowFuelLatched) {
    fuelMode = "CNG";
    decisionReason = "Low fuel - switched to CNG reserve";
    costSaved = 2.50;
    co2Reduction = 1.80;
    return;
  }

  if (highTempLatched) {
    fuelMode = "LPG";
    decisionReason = "High temp - LPG selected for cooler operation";
    costSaved = 1.80;
    co2Reduction = 1.20;
    return;
  }

  if (lowLightLatched) {
    fuelMode = "LPG";
    decisionReason = "Low light - LPG efficiency mode";
    costSaved = 1.50;
    co2Reduction = 1.00;
    return;
  }

  fuelMode = "PETROL";
  decisionReason = "Normal conditions - Petrol mode";
  costSaved = 0.50;
  co2Reduction = 0.30;
}

void determineStatus() {
  if (criticalTempLatched) {
    systemStatus = "HIGH TEMP";
  } else if (lowFuelLatched) {
    systemStatus = "LOW FUEL";
  } else if (fuelMode == "LPG" || fuelMode == "CNG") {
    systemStatus = "EFFICIENT";
  } else {
    systemStatus = "NORMAL";
  }
}

// ============================================================================
// OUTPUT CONTROL
// ============================================================================

void controlOutputs() {
  if (systemStatus == "HIGH TEMP") {
    digitalWrite(PIN_LED_RED, HIGH);
    digitalWrite(PIN_LED_GREEN, LOW);
    digitalWrite(PIN_LED_YELLOW, LOW);
  } else if (systemStatus == "LOW FUEL") {
    digitalWrite(PIN_LED_RED, LOW);
    digitalWrite(PIN_LED_GREEN, LOW);
    digitalWrite(PIN_LED_YELLOW, HIGH);
  } else if (systemStatus == "EFFICIENT") {
    digitalWrite(PIN_LED_RED, LOW);
    digitalWrite(PIN_LED_GREEN, HIGH);
    digitalWrite(PIN_LED_YELLOW, HIGH);
  } else {
    digitalWrite(PIN_LED_RED, LOW);
    digitalWrite(PIN_LED_GREEN, HIGH);
    digitalWrite(PIN_LED_YELLOW, LOW);
  }

  if (systemStatus == "HIGH TEMP") {
    tone(PIN_BUZZER, 1000, 200);
  } else {
    noTone(PIN_BUZZER);
  }

  if (highTempLatched) {
    digitalWrite(PIN_RELAY_1, HIGH);
    relay1State = "ON";
  } else {
    digitalWrite(PIN_RELAY_1, LOW);
    relay1State = "OFF";
  }

  if (relay2Latched) {
    digitalWrite(PIN_RELAY_2, HIGH);
    relay2State = "ON";
  } else {
    digitalWrite(PIN_RELAY_2, LOW);
    relay2State = "OFF";
  }
}

// ============================================================================
// LCD DISPLAY
// ============================================================================

void updateLCD() {
  lcd.clear();

  lcd.setCursor(0, 0);
  lcd.print("T:");
  lcd.print(temperature, 1);
  lcd.print("C F:");
  lcd.print(fuelPercent);
  lcd.print("%");

  lcd.setCursor(0, 1);
  lcd.print(fuelMode);
  lcd.print(" ");

  int availableChars = 16 - fuelMode.length() - 1;
  if (availableChars < 0) {
    availableChars = 0;
  }

  lcd.print(systemStatus.substring(0, availableChars));
}

void showLCDMessage(String line1, String line2) {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(line1.substring(0, 16));
  lcd.setCursor(0, 1);
  lcd.print(line2.substring(0, 16));
}

// ============================================================================
// SERIAL DASHBOARD TELEMETRY - v1 SCHEMA
// ============================================================================

String buildSerialDashboardJSON() {
  String json = "{";

  json += "\"timestamp\":\"" + String(millis()) + "\",";
  json += "\"engine_temperature\":" + String(temperature, 2) + ",";
  json += "\"fuel_line_temperature\":" + String(temperature, 2) + ",";
  json += "\"ambient_temperature\":" + String(estimateAmbientTemperature(), 2) + ",";
  json += "\"current_fuel_mode\":\"" + fuelMode + "\",";
  json += "\"ai_recommendation\":\"" + escapeJson(decisionReason) + "\",";
  json += "\"relay_state_1\":" + boolToJson(relay1State == "ON") + ",";
  json += "\"relay_state_2\":" + boolToJson(relay2State == "ON") + ",";
  json += "\"overheat_flag\":" + boolToJson(systemStatus == "HIGH TEMP") + ",";
  json += "\"system_status\":\"" + systemStatus + "\",";
  json += "\"network_status\":\"" + String(wifiConnected ? "connected" : "disconnected") + "\",";
  json += "\"power_source\":\"usb\",";
  json += "\"fuel_percent\":" + String(fuelPercent) + ",";
  json += "\"distance_cm\":" + String(distanceCm, 2);

  json += "}";
  return json;
}

// ============================================================================
// CLOUD TELEMETRY - v2 SCHEMA
// ============================================================================

String buildCloudTelemetryJSON() {
  String json = "{";

  json += "\"vehicle_id\":\"" + String(VEHICLE_ID) + "\",";
  json += "\"vehicle_type\":\"keke\",";
  json += "\"temperature\":" + String(temperature, 2) + ",";
  json += "\"distance_cm\":" + String(distanceCm, 2) + ",";
  json += "\"fuel_percent\":" + String(fuelPercent) + ",";
  json += "\"fuel_mode\":\"" + fuelMode + "\",";
  json += "\"status\":\"" + systemStatus + "\",";
  json += "\"relay1\":\"" + relay1State + "\",";
  json += "\"relay2\":\"" + relay2State + "\",";
  json += "\"ldr\":" + String(ldrValue) + ",";
  json += "\"thermistor\":" + String(thermistorValue) + ",";
  json += "\"cost_saved\":" + String(costSaved, 2) + ",";
  json += "\"co2_reduction\":" + String(co2Reduction, 2) + ",";
  json += "\"reason\":\"" + escapeJson(decisionReason) + "\",";
  json += "\"timestamp_source\":\"device\"";

  json += "}";
  return json;
}

// ============================================================================
// CLOUD CONNECTIVITY
// ============================================================================

void connectWiFi() {
  lastWifiAttempt = millis();

  if (String(WIFI_SSID) == "YOUR_WIFI_SSID") {
    Serial.println("[WIFI] Skipping - placeholder SSID.");
    wifiConnected = false;
    return;
  }

  Serial.print("[WIFI] Connecting to ");
  Serial.print(WIFI_SSID);
  Serial.print("...");

  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  unsigned long startAttempt = millis();

  while (
    WiFi.status() != WL_CONNECTED &&
    millis() - startAttempt < WIFI_CONNECT_TIMEOUT_MS
  ) {
    delay(500);
    Serial.print(".");
  }

  if (WiFi.status() == WL_CONNECTED) {
    wifiConnected = true;
    Serial.println(" OK!");
    Serial.print("[WIFI] IP Address: ");
    Serial.println(WiFi.localIP());
  } else {
    wifiConnected = false;
    Serial.println(" FAILED - local mode continues");
  }
}

void sendTelemetryToCloud(String jsonPayload) {
  if (!wifiConnected || WiFi.status() != WL_CONNECTED) {
    wifiConnected = false;
    return;
  }

  HTTPClient http;
  http.begin(CLOUD_ENDPOINT);
  http.addHeader("Content-Type", "application/json");
  http.setTimeout(2500);

  int httpCode = http.POST(jsonPayload);

  if (httpCode == 200 || httpCode == 201) {
    Serial.println("[CLOUD] Telemetry uploaded OK");
  } else if (httpCode > 0) {
    Serial.print("[CLOUD] Server returned: ");
    Serial.println(httpCode);
  } else {
    Serial.print("[CLOUD] Upload failed: ");
    Serial.println(http.errorToString(httpCode));
  }

  http.end();
}

// ============================================================================
// HELPERS
// ============================================================================

bool updateLatch(bool currentState, bool enterCondition, bool exitCondition) {
  if (currentState) {
    return !exitCondition;
  }
  return enterCondition;
}

void sortFloatArray(float values[], int count) {
  for (int i = 0; i < count - 1; i++) {
    for (int j = i + 1; j < count; j++) {
      if (values[j] < values[i]) {
        float temp = values[i];
        values[i] = values[j];
        values[j] = temp;
      }
    }
  }
}

float estimateAmbientTemperature() {
  return constrain(temperature - 3.0, 20.0, 45.0);
}

String boolToJson(bool value) {
  return value ? "true" : "false";
}

String escapeJson(String value) {
  value.replace("\\", "\\\\");
  value.replace("\"", "\\\"");
  return value;
}
