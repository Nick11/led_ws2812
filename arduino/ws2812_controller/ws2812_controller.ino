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
    #define N_LEDS 90
     
    Adafruit_NeoPixel strip = Adafruit_NeoPixel(N_LEDS, PIN, NEO_GRB + NEO_KHZ800);
     
    void setup() {
      connect();
      strip.begin();
      //clearLEDs();
      strip.show();
    }
     
    void loop() {
      //If the server dis- and reconnects
      if (!Serial){
        connect();
      }
      //chase(strip.Color(105, 0, 0)); // Red
      //chase(strip.Color(0, 105, 0)); // Green
      //chase(strip.Color(0, 0, 105)); // Blue
      
      if(Serial.available()>5){ // only send data back if data has been sent
        byte ctrl_byte = Serial.read();
        char ctrl_char = char(ctrl_byte);

        if(ctrl_char == char(0))
        {
          //uint32_t color = strip.Color(red, green, blue);
          Serial.println("set color");
          int addr = read_address();
          uint32_t color = read_color();
          set_color(addr, color);
        }
        else if(ctrl_char == 'n')
        {
          int addr = read_address();
          uint32_t color = read_color();
          Serial.write(N_LEDS);
        }
        else if(ctrl_char == 'a')
        {
          int addr = read_address();
          uint32_t color = read_color();
          set_all(color);
          Serial.println("set all");
        }
        else if(ctrl_char == 'd')
        {//disconnect
            Serial.println("closed");
            strip.Color(255, 0, 0);
            //Serial.end();
            connect();
        }
        else if(ctrl_char == 'b')
        {//burst, set all leds
          Serial.println("set burst");
          uint32_t total_count = read_address();
          for(uint16_t i=0; i<total_count*5; i=i+5)
          {
            int addr = read_address();
            uint32_t color = read_color();
            strip.setPixelColor(addr, color);
          }
          strip.show();
        }
        else{
          int addr = read_address();
          uint32_t color = read_color();
        }
      }
    }
    
    static uint32_t read_color()
    {
      char red = Serial.read(); // read the incoming data
      char green = Serial.read(); // read the incoming data
      char blue = Serial.read(); // read the incoming data
      uint32_t color = strip.Color(red, green, blue);
      return color;
    }

    static int read_address()
    {
      byte addr_byte_1 = Serial.read();
      byte addr_byte_2 = Serial.read();
      int addr = addr_byte_1 << 8 | addr_byte_2;
      return addr;
    }
    
    static void connect()
    {
      
      Serial.begin(12000); // set the baud rate
      clearLEDs();
      while (!Serial) {
        delay(25); // wait for serial port to connect. Needed for Leonardo only
      }
      set_all(strip.Color(0, 0, 255));
      char read_char = ' ';
      while (Serial.available()<= 5 && read_char != 'o')
      {
        read_char = char(Serial.read());
        delay(25);
      }
      set_all(strip.Color(0, 255, 0));
      Serial.println("open");
    }
    
    static void set_color(uint16_t led_id, uint32_t color)
    {
          strip.setPixelColor(led_id, color); // Draw new pixel
          strip.show();
    }


    static void set_all(uint32_t color)
    {
      for(uint16_t i=0; i<strip.numPixels()+4; i++) {
          strip.setPixelColor(i  , color);
      }
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
