package main

import (
	"fmt"
	"bufio"
	"os"
	"strings"
)

func main() {
	readLines()
}

func readLines() {
	file, err := os.Open("traces.txt") 
	checkError(err)
	defer func() {
		if err := file.Close; err != nil {
			panic(err)
		}
	}()
	in := bufio.NewScanner(file)
	ips := make(map[string]float64)

	for in.Scan() {
		cache(in.Text(), ips)
	}
}

func checkError(e error) {
	if e != nil {
		panic(e)
	}
}

func cache(line string, ips map[string]float64) map[string]float64 {
	data := strings.Split(line, " ")
	if len(data) < 6 {
		return ips
	}
	if len(data[5]) == 0 {
		return ips
	}
	
	destIp := data[5][0: len(data[5])-1]
	byteList := strings.Split(destIp, ".")
	if len(byteList) < 3 {
		return ips
	}
	ip24bits := byteList[0] + "." + byteList[1] + "." + byteList[2]
	if val, ok := ips[ip24bits]; ok {
		fmt.Println(val)
		ips[ip24bits] += 10
	} else if len(ips) <= 10000 {
		fmt.Println("Caching: " + ip24bits)
		ips[ip24bits] = .010
	}
	return ips
}

func checkTimeout() {

}
