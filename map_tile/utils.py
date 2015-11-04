from flask import Response, send_file
from PIL import Image
import os 
def parse_file_info_headers (headers) :
	"""
	:param  request headers
	"""
	infos = headers.split (';')
	data = dict ()
	for info in infos : 
		_info = info.split('=')
		data.setdefault (_info[0],_info[1])
	return data

def serve_data (full_path_file, headers) :
	"""
	Using default flask server 
	:param full_path_file
	:param  request headers
	"""
	return  send_file(full_path_file)
	
def get_path () :
	path = os.path.dirname(os.path.realpath(__file__))
	return os.path.join (path , 'uploads') 
def get_image ():
	return Image.open (os.path.join(get_path (), 'plan.jpg'))
	
def get_map_tile (zoom, x, y):
	"""
		:param zoom 
		:param x
		:param y
	"""
	image_width = 1000
	image_height = 783
	image = get_image ()
	zoom = zoom - 15
	print ">>>> %d " % zoom
	if zoom > 0 :
		image = image.resize ((image_width * 2, image_height * 2), Image.ANTIALIAS)
		image.save(os.path.join(get_path (), 'plan_2.jpg'), "JPEG")
	tile_width = 256
	tile_height = 256
	#(left, upper, right, lower)
	return image.crop ((x * tile_width, y * tile_height,  (x + 1) * tile_width, (y + 1) * tile_height))
