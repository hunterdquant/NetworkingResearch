package main

import (
	"fmt"
	"bufio"
	"os"
	"strings"
	"time"
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
	go checkTimeout(ips)
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
		fmt.Printf(ip24bits + " has a T/O of %g\n", val)
		ips[ip24bits] = ips[ip24bits] + getAdditionalTime(ips[ip24bits])
	} else if len(ips) <= 10000 {
		fmt.Println("Caching: " + ip24bits)
		ips[ip24bits] = .010
	}
	return ips
}

func checkTimeout(ips map[string]float64) {
	for {
		prevTime := time.Now()
		for ip := range(ips) {
			ips[ip] = ips[ip] - (time.Duration.Seconds(time.Since(prevTime)))
			if ips[ip] <= 0 {
				fmt.Println("Removing " + ip + " from the cache. ")
				delete(ips, ip)
			}
		}
	}
}

func getAdditionalTime(timeOut float64) float64 {
	return .010-timeOut/1000
}
