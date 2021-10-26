from urllib.request import Request, urlopen
import json
import config
import os
import shutil

def edit_tuple(function, values):
	url=config.url+function
	print(url)
	values = json.dumps(values).encode('utf-8')
	print(values)
	request = Request(url, data=values, headers=config.headers)
	request.get_method = lambda: 'PUT'

	response_body = urlopen(request).read()
	print(response_body)


def get_value(function, os_id):
	url=config.url+function+'/'+os_id
	request = Request(url, headers=config.headers)
	response_body = urlopen(request).read()
	string = response_body.decode('utf-8')
	json_obj = json.loads(string)
	return json_obj

def dictionary_response(function):
	url=config.url+function
	request = Request(url, headers=config.headers)
	response_body = urlopen(request).read()
	string = response_body.decode('utf-8')
	json_obj = json.loads(string)
	return json_obj

def string_response(function):
	url=config.url+function
	request = Request(url, headers=config.headers)
	response_body = urlopen(request).read()
	string = response_body.decode('utf-8')
	return string

def parser_file(filename):
	print("Parsing file: " + filename)
	f = open(filename)
	lines = f.readlines()
	f.close()

	json_obj = json.loads(lines[0])
	return json_obj


def removing_existing_file(filename):
	filename = filename.replace('//','/')
	if os.path.exists(filename):
		shutil.copy(filename,filename +'.bkp')
		os.remove(filename)
		print("Removing file: " + filename)

def create_output_dir(outputDir):
	if (not os.path.exists(outputDir)):
		os.makedirs(outputDir, exist_ok=True)
		print("Creating output directories: " + outputDir)
