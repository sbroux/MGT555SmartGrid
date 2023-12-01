#include <FastLED.h>

#define LED_PIN     7 // Define the pin connected to the WS2812B LEDs
#define NUM_LEDS    20 // Define the total number of LEDs in your strip
#define FIRST_LED_COUNT 10 // Number of LEDs to turn red

CRGB leds[NUM_LEDS];

void setup() {
  FastLED.addLeds<WS2812B, LED_PIN, GRB>(leds, NUM_LEDS);
  Serial.begin(9600); // Start serial communication
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    if (command == 'r') {
      fill_solid(leds, FIRST_LED_COUNT, CRGB::Red); // Turn first LEDs red
      fill_solid(&(leds[FIRST_LED_COUNT]), NUM_LEDS - FIRST_LED_COUNT, CRGB::Black); // Turn off remaining LEDs
      FastLED.show();
      Serial.flush();
      
    }
    if (command == 'b') {
      fill_solid(&(leds[FIRST_LED_COUNT]), NUM_LEDS - FIRST_LED_COUNT, CRGB::Blue); // Turn last LEDs blue
      fill_solid(leds, FIRST_LED_COUNT, CRGB::Black); // Turn off first LEDs
      FastLED.show();
      Serial.flush();
    }
  }
  // Other tasks for your Arduino loop
}