package main

import (
	"github.com/huin/goserial"
	"io"
	"fmt"
	"bytes"
	"bufio"
	"os"
	"strconv"
	"strings"
	"encoding/binary"
)
//import "github.com/huin/goserial"

const arduino_name = "/dev/cu.usbserial-DA00SVW5"
type SerialConnection io.ReadWriteCloser
type ArduinoCommand struct {
	IsSpecialCommand bool
	LedAddress int
	Red, Blue, Green int
}

func main() {
	// Find the device that represents the Arduino serial connection.

	serial := connect()
	//read(serial)
	//send(serial)
	for {
		reader := bufio.NewReader(os.Stdin)
		text, _ := reader.ReadString('\n')
		text = strings.TrimSpace(text)
		split := strings.Split(text,",")
		if len(split)<5{
			continue
		}
		var command ArduinoCommand
		command.IsSpecialCommand,_ = strconv.ParseBool(split[0])
		command.LedAddress,_ = strconv.Atoi(split[1])
		command.Red,_ = strconv.Atoi(split[2])
		command.Green,_ = strconv.Atoi(split[3])
		command.Blue,_ = strconv.Atoi(split[4])
		fmt.Printf("%+v\n", command)
		send(serial, command)
	}

	serial.Close()


	// When connecting to an older revision Arduino, you need to wait
	// a little while it resets.
	//time.Sleep(1 * time.Second)
}

func send(serial SerialConnection, command ArduinoCommand){
	//b := byte(command.LedAddress)
	bs := make([]byte, 8)
	addr64 := uint64(command.LedAddress)
	binary.BigEndian.PutUint64(bs, addr64)
	addrByte := bs[6:8]
	special := byte(0)
	if command.IsSpecialCommand{
		special = byte(1)
	}
	var buffer [6]byte
	buffer[0] = special
	buffer[1] = addrByte[0]
	buffer[2] = addrByte[1]
	buffer[3] =  byte(command.Red)
	buffer[4] =  byte(command.Green)
	buffer[5] =  byte(command.Blue)
	//fmt.Printf("%b\n", buffer[0:6])
	//println(len(buffer[0:6]))
	serial.Write(buffer[0:6])
	read(serial)
}

func read(serial SerialConnection)([]byte){
	buffer := make([]byte,10)
	serial.Read(buffer)
	var position int = bytes.IndexByte(buffer, 0)
	fmt.Printf("%d\n", buffer[0:position])
	return buffer
}

func connect()(SerialConnection){
	c := &goserial.Config{Name: arduino_name, Baud: 9600}
	s, err := goserial.OpenPort(c)
	if err != nil {
		println("Arduino not connected")
		s.Close()
	}
	//s.Write([]byte{byte(0)})
	return s
}
