# Reads traces line by line and sends them to be processed.
def readTraces():
	fileOut = open("parsedTraces.txt", "w")
	fileIn = open("traces.txt", "r")
	for line in fileIn:
		writeTraces(line, fileOut)
	fileIn.close()
	fileOut.close()
		
# Writes the formated lines to a file.
def writeTraces(line, fileOut):
	data = line.split(" ")
	if len(data) < 6:
		return
	fileOut.write("Packet start.\n")
	fileOut.write("Time: " + data[1] + "\n")
	fileOut.write("Source IP: " + data[3] + "\n")
	fileOut.write("Destination IP: " + data[5][:-1] + "\n\n")
	
readTraces()
