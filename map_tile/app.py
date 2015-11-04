from flask import Flask, request
from werkzeug import Response
import os, json, random, base64
from utils  import parse_file_info_headers, serve_data, get_map_tile
from cStringIO import StringIO
app = Flask(__name__)

# config port
app.config['PORT'] = 4000
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'json', 'csv'])

# This is the path to the upload directory
directory = os.path.join (os.path.dirname(os.path.abspath(__file__)), 'uploads')

if not os.path.exists(directory):
    os.makedirs(directory)

app.config['UPLOAD_FOLDER'] = directory

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
	return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']
		 
# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
	data = request.data
	print len(data)
	print request.headers
    #@see http://flask.pocoo.org/docs/0.10/api/#flask.Request.data
	info = parse_file_info_headers(request.headers['Content-Info'])
	filename = info.get('name')
	id = info.get('id', None)
	size = info.get('size', None)
	seek = info.get('seek', None)
	print "filename : %s, id : %s, seek : %s , size % s" % (filename, id, seek, size)
	if id is None :
		id = "X-" + str(random.random())
	# filename	
	
	temp_filename_path = os.path.join(app.config['UPLOAD_FOLDER'], '%s.%s.temp' % (filename , id)) ;
	print ">>> " + temp_filename_path 
    # TODO Check if the file is one of the allowed types/extensions        
	with open(temp_filename_path, 'ab') as target:
		target.write (data)
        target.close ()
	
	if (seek is not None) and (int(seek) >= int(size)) :
		print ">>> enter to final stage"
		print ">>>  seek %s " % seek
		print ">>>  size %s " % size
		target_name = os.path.join(app.config['UPLOAD_FOLDER'], filename)
		if not os.path.exists(target_name):
			os.rename(temp_filename_path, target_name)
		else :
			print '>>>> file already exists !'
		return json.dumps ({ 'success' : True })
	else:
		return json.dumps ({ 'id' : id })
	
	
@app.errorhandler(500)
def internal_error(error):
	print error
	return "500 error"

@app.errorhandler(400)
def internal_error(error):
	print error
	return "400 error"
	
@app.after_request
def after_request(response):
	response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3001')
	response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,Content-Info')
	response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
	return response
# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    full_file_path = os.path.join (directory, filename)
    return serve_data(full_file_path, request.headers)
	
# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/map-tiles/<int:z>/<int:x>/<int:y>.png')
def tile(z, x, y):
	#<string:layername_64>/
	#layername_64
    """ serve a tile request """
    #print layername_64 
    #layername = "%s" % base64.urlsafe_b64decode(str(layername_64))
    #if not os.path.isfile(layername):
    #   return "Map file not found: %s" % layername
    try:
        with app.open_resource('image') as f:
            f.seek (0)
            """"'data:image/png;base64,' +"""
            #contents = "data:image/png;base64,%s" % f.read()
            contents = f.read()
        return Response(base64.b64decode(contents), content_type = 'image/png',  mimetype="image/png")
    except Exception, e:
        return "Tile could not be retrieved: %s" % str(e)
		
# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/tiles/<int:z>/<int:x>/<int:y>.png')
def get_tile(z, x, y):
	output = StringIO()
	image = get_map_tile (int(z), int(x), int(y))
	image.save(output, format='JPEG')
	im_data = output.getvalue()
	content = base64.b64encode(im_data)
	html = "<img src='data:image/jpg;base64,%s'/></body>" % content
	return Response(base64.b64decode(content), content_type = 'image/JPEG',  mimetype="image/JPEG")
	return html #Response(html) #content_type = 'image/JPEG',  mimetype="image/JPEG"
    


@app.route("/")
def hello():
	return "Hello World!"

if __name__ == "__main__":
    app.run(port=app.config['PORT'], debug=True)
