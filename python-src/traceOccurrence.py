# Reads traces line by line to be processed.
def read_traces():
	file_in = open("traces.txt", "r")
	# Keeps track of the number of times a packet is sent toward a specific 24bit IP.
	ips = dict()
	for line in file_in:
		get_occurrence(line, ips)
	
	write_occurrences(ips)
	get_max_occurrences(ips)

	file_in.close()

# Processes each line and maps a 24bit IP to the number of times that IP occurs.
def get_occurrence(line, ips):
	data = line.split(" ")
	# Any line with less that 6 tokens is considered invalid.
	if len(data) < 6:
		return ips
	dest_ip = data[5][:-1]
	byte_list = dest_ip.split(".")
	# If the split IP has less than 3 bytes it's invalid.
	if len(byte_list) < 3:
		return ips
	# Reconstruct IP to 24 bits.
	ip_24_bits = byte_list[0] + "." + byte_list[1] + "." + byte_list[2]
	# If the IP is reoccurring increment it's occurrence, else add it to the dictionary.
	if ip_24_bits in ips:
		ips[ip_24_bits] = ips[ip_24_bits] + 1
	else:
		ips[ip_24_bits] = 1
	return ips

# Writes all IPs followed by the number of times the occur to a file.
def write_occurrences(ips):
	file_out = open("traceOccurrences.txt", "w")
	for ip in ips:
		file_out.write("Dest IP: " + ip + " occurs " +  str(ips[ip]) + " times.\n")
	file_out.close()

# Finds the top N occurrences of a specific IP.
def get_max_occurrences(ips):
	max_list = list()
	max_n = 10
	for ip in ips:
		# If we don't have N entries in the list yet.
		if len(max_list) < max_n:
			max_list.append((ip, ips[ip]))
		else:
			# Compare each pair with the occurrences and replace when you find a greater occurrence.
			for pair in max_list:
				if ips[ip] >= pair[1]:
					max_list[max_list.index(pair)] = (ip, ips[ip])
					break

	write_max_occurrences(max_list);

# Writes the top N occurrences to a file.
def write_max_occurrences(max_list):
	file_out = open("maxOccurrences.txt", "w")
	file_out.write("Top N max occurrences.\n\n")
	for pair in max_list:
		file_out.write(str(max_list.index(pair) + 1) + ". Dest IP: " + pair[0] + " occurs " + str(pair[1]) + " times.\n")
	file_out.close()

read_traces()
