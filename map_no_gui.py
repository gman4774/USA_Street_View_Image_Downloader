
import csv
import os
import urllib.parse
import urllib.request
import glob
import time
from multiprocessing import Pool
from tqdm import tqdm
from os.path import exists




if not exists('../k.txt') or not exists('data/address.csv'):
	print('Files missing! Verify key file and input data locations.')
	quit()

with open('../k.txt') as key_file:
	key_txt = key_file.readline().strip('\n')

key = "&key=" + key_txt
full_add_list = []

with open('data/address.csv', mode='r') as address_csv:
	reader = csv.reader(address_csv)
	for row in reader:
		full_add_list.append(row[0] + ', ' + row[1] + ', ' + row[2] + ' ' + row[3])

full_add_list.pop(0)

def get_street(address):
	save = 'output/'
	base = "https://maps.googleapis.com/maps/api/streetview?size=1200x800&location="
	MyUrl = base + urllib.parse.quote_plus(address) + key #added url encoding
	fi = address + ".jpg"
	urllib.request.urlretrieve(MyUrl, os.path.join(save, fi))


def pool_handler():
	if speed_input == 'fast':
		speed = 32
	else:
		speed = 2
	if output_clean == 'y':
		files = glob.glob('output/*')
		for f in files:
			os.remove(f)
	p = Pool(speed)
	start_time = time.time()
	rez = tqdm(p.imap(get_street, full_add_list), total=len(full_add_list))
	tuple(rez)
	end_time = time.time()
	print(end_time - start_time)


if __name__ == '__main__':
	speed_input = 'a'
	while speed_input != 'fast' and speed_input != 'slow':
		speed_input = input('Input program speed (fast) or (slow): ')
	output_clean = 'b'
	while output_clean != 'y' and output_clean != 'n':
		output_clean = input('Delete all files in output directory(y) or (n)?')
	
	pool_handler()
	

