#include <FastLED.h>
#define NUM_LEDS 105
#define LED_PIN     7 // Define the pin connected to the WS2812B LEDs

CRGB leds[NUM_LEDS];

void setup() {
  FastLED.addLeds<WS2812B, LED_PIN, GRB>(leds, NUM_LEDS);
  Serial.begin(9600); // Start serial communication
}
// PV — Room 2    0 - 13
// Room 2 — Chargers 14 - 31
// Chargers — Grid : 32 - 56
// Grid — Room 2: 57 - 68
// Room 2 — Room 1: 69 - 78
// Room 1 — Grid : 79 - 104

//defining constraints:
int a = 0;
int b = 13;
int c = 14;
int d = 31;
int e = 32;
int f = 56;
int g = 57;
int h = 68;
int z = 69;
int j = 78;
int k = 79;
int l = 104;

void loop() {
  CRGB pulseColor = CRGB(0, 0, 255);
  if (Serial.available() > 0) {
    char command = Serial.read();
    if (command == 'gR1') {
      for(int i = l; i > k; i -= 2) { // goes in reverse
        leds[i] = pulseColor;
        if(i - 1 > k) leds[i - 1] = pulseColor;
        FastLED.show();
        delay(70); // Adjust the speed of the pulses here

        // Clear the LEDs for the next iteration
        leds[i] = CRGB::Black;
        if(i - 1 > k) leds[i - 1] = CRGB::Black;
      }
    }
    if (command == 'R2R1') {
      for(int i = z; i < j; i += 2) {
        leds[i] = pulseColor;
        if(i + 1 < j) leds[i + 1] = pulseColor;
        FastLED.show();
        delay(70); // Adjust the speed of the pulses here
        // Clear the LEDs for the next iteration
        leds[i] = CRGB::Black;
        if(i + 1 < j) leds[i + 1] = CRGB::Black;
      }
    }
    if (command == 'gR2') {
      for(int i = g; i < h; i += 2) {
        leds[i] = pulseColor;
        if(i + 1 < h) leds[i + 1] = pulseColor;
        FastLED.show();
        delay(70); // Adjust the speed of the pulses here
        // Clear the LEDs for the next iteration
        leds[i] = CRGB::Black;
        if(i + 1 < h) leds[i + 1] = CRGB::Black;
      }
    }
    if (command == 'R2g') {
      for(int i = h; i > g; i -= 2) { // goes in reverse
        leds[i] = pulseColor;
        if(i - 1 > g) leds[i - 1] = pulseColor;
        FastLED.show();
        delay(70); // Adjust the speed of the pulses here

        // Clear the LEDs for the next iteration
        leds[i] = CRGB::Black;
        if(i - 1 > g) leds[i - 1] = CRGB::Black;
      }
    }
    if (command == 'SR2') {
      for(int i = a; i < b; i += 2) {
        leds[i] = pulseColor;
        if(i + 1 < b) leds[i + 1] = pulseColor;
        FastLED.show();
        delay(70); // Adjust the speed of the pulses here
        // Clear the LEDs for the next iteration
        leds[i] = CRGB::Black;
        if(i + 1 < b) leds[i + 1] = CRGB::Black;
      }
    }
    if (command == 'R2C') {
      for(int i = c; i < d; i += 2) {
        leds[i] = pulseColor;
        if(i + 1 < d) leds[i + 1] = pulseColor;
        FastLED.show();
        delay(70); // Adjust the speed of the pulses here
        // Clear the LEDs for the next iteration
        leds[i] = CRGB::Black;
        if(i + 1 < d) leds[i + 1] = CRGB::Black;
      }
    }
    if (command == 'CR2g') {
      for(int i = e; i < f; i += 2) {
        leds[i] = pulseColor;
        if(i + 1 < f) leds[i + 1] = pulseColor;
        FastLED.show();
        delay(70); // Adjust the speed of the pulses here
        // Clear the LEDs for the next iteration
        leds[i] = CRGB::Black;
        if(i + 1 < f) leds[i + 1] = CRGB::Black;
      }
    }
    if (command == 'gCR2') {
      for(int i = f; i > e; i -= 2) { // goes in reverse
        leds[i] = pulseColor;
        if(i - 1 > e) leds[i - 1] = pulseColor;
        FastLED.show();
        delay(70); // Adjust the speed of the pulses here

        // Clear the LEDs for the next iteration
        leds[i] = CRGB::Black;
        if(i - 1 > e) leds[i - 1] = CRGB::Black;
      }
    }
  } // Other tasks for your Arduino loop
}