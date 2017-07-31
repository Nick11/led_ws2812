# LED Controller
 for WS2812b RGB LEDs using an Arduino

## Installation

### Tools Used
- Eclipse for Scala
- sbt build tool http://www.scala-sbt.org/0.13/docs/Setup.html
 - sbt eclipse plugin(https://github.com/typesafehub/sbteclipse): simply run in terminal: sbt eclipse
- Arduino IDE

### Setup Arduino
Open the arduino/ws2812_controller.ino file and upload it to the connected arduino board

### Setup Scala Server
#### Dependencies
- jSerialComm (https://github.com/Fazecast/jSerialComm/wiki/Installation) for Arduino communication. Is getting installed by sbt.
- Java-Arduino-Communication-Library (https://github.com/HirdayGupta/Java-Arduino-Communication-Library) for Arduino communication. Is getting installed by sbt.
#### Import int eclipse
In eclipse: File → Import → Existing Projects into Workspace

### Setup iOS App

