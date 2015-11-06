import time, threading

prev_time = time.time()
delta_time = 0 

# Reads traces line by line to be processed.
def read_traces():
	file_in = open("traces.txt", "r")
	# Keeps track of the number of times a packet is sent toward a specific 24bit IP.
	ips = dict()
	thread = threading.Thread(target=check_timeout(ips))
	thread.start()
	thread.join()
	for line in file_in:
		check_timeout(ips)
		cache(line, ips)

	
	file_in.close()


# Processes each line and maps a 24bit IP to the number of times that IP occurs.
def cache(line, ips):
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
		print(ip_24_bits + " has a T/O of " + str(ips[ip_24_bits]))
		ips[ip_24_bits] = ips[ip_24_bits] + get_additional_time(ips[ip_24_bits])
	elif len(ips) <= 10000:
		print("Caching: " + ip_24_bits)
		ips[ip_24_bits] = .010
	return ips

def check_timeout(ips):
	global prev_time
	delta_time = time.time() - prev_time
	prev_time = time.time()
	for ip in ips.keys():
		ips[ip] = ips[ip] - delta_time
		if ips[ip] <= 0:
			print("Removing " + ip + " from the cache. " + str(delta_time))
			del ips[ip]

def get_additional_time(time_out):
	return .010-time_out/1000

read_traces()
