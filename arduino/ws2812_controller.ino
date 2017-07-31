    // Simple NeoPixel test.  Lights just a few pixels at a time so a
    // 1m strip can safely be powered from Arduino 5V pin.  Arduino
    // may nonetheless hiccup when LEDs are first connected and not
    // accept code.  So upload code first, unplug USB, connect pixels
    // to GND FIRST, then +5V and digital pin 6, then re-plug USB.
    // A working strip will show a few pixels moving down the line,
    // cycling between red, green and blue.  If you get no response,
    // might be connected to wrong end of strip (the end wires, if
    // any, are no indication -- look instead for the data direction
    // arrows printed on the strip).
     
    #include <Adafruit_NeoPixel.h>
     
    #define PIN 2
    #define N_LEDS 144
     
    Adafruit_NeoPixel strip = Adafruit_NeoPixel(N_LEDS, PIN, NEO_GRB + NEO_KHZ800);
     
    void setup() {
      Serial.begin(9600); // set the baud rate
      //Serial.println("open");
      strip.begin();
      clearLEDs();
      strip.show();
    }
     
    void loop() {
      
      //chase(strip.Color(105, 0, 0)); // Red
      //chase(strip.Color(0, 105, 0)); // Green
      //chase(strip.Color(0, 0, 105)); // Blue
      
      if(Serial.available()>5){ // only send data back if data has been sent
        byte ctrl_byte = Serial.read();
        byte addr_byte_1 = Serial.read();
        byte addr_byte_2 = Serial.read();
        int addr = addr_byte_1 << 8 | addr_byte_2;
        char red = Serial.read(); // read the incoming data
        char green = Serial.read(); // read the incoming data
        char blue = Serial.read(); // read the incoming data

        if(ctrl_byte == 1)
        {
          Serial.write(N_LEDS);
        }
        else
        {
        
          uint32_t color = strip.Color(red, green, blue);
          Serial.write(green);
          set_color(addr, color);
        }
      }
    }

    static void set_color(uint16_t led_id, uint32_t color)
    {
          strip.setPixelColor(led_id, color); // Draw new pixel
          strip.show();
    }
    
    static void chase(uint32_t c) {
      for(uint16_t i=0; i<strip.numPixels()+4; i++) {
          strip.setPixelColor(i  , c); // Draw new pixel
          strip.setPixelColor(i-4, 0); // Erase pixel a few steps back
          strip.show();
          delay(25);
      }
    }

    // Sets all LEDs to off, but DOES NOT update the display;
    // call leds.show() to actually turn them off after this.
    void clearLEDs()
    {
      for (int i=0; i<N_LEDS; i++)
      {
        strip.setPixelColor(i, 0);
      }
    }
