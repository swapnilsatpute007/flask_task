import os
from app import app
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from werkzeug.exceptions import HTTPException

def read_file(file,start_line,end_line):
    with open(file,'r') as f:
        file_data = f.readlines()
        if start_line and end_line:
            file_content = file_data[start_line:end_line+1]
        elif start_line and not end_line:
            file_content = file_data[start_line:]
        else:
            file_content = file_data
        return file_content
    

@app.route('/getfile', methods=['GET'])
def getfile():
    start_point = 0
    end_point = -1
    start_line  = request.args.get('start_line', None)
    if start_line:
        try:
            start_point = int(start_line)
            app.logger.info('Start Point: {}'.format(start_point))
        except TypeError:
            app.logger.error('Error in converting start line into integer')
            raise HTTPException(
                status_code=400,
                detail="The object is not converted into integer")
            
    end_line  = request.args.get('end_line', None)
    if end_line:
        try:
            end_point = int(end_line)
            app.logger.info('End Point: {}'.format(end_point))
        except TypeError:
            app.logger.error('Error in converting end line into integer')
            raise HTTPException(
                status_code=400,
                detail="The object is not converted into integer")
            
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        app.logger.info('File Path: {}'.format(file_path))
        
    if not file:
        file_path = app.config['UPLOAD_FOLDER']+"/file1.txt"
        app.logger.info('File Path: {}'.format(file_path))
        
    if file_path:
        file_content = read_file(file_path,start_point,end_point)
        app.logger.info('message : Sucessfully reterived file data, filedata:  {}'.format(file_content))
        response = jsonify({'message' : 'Sucessfully reterived file data','filedata':file_content})
        response.status_code = 200
        return response
    else:
        app.logger.error('message : No file selected for uploaded')
        response = jsonify({'message' : 'No file selected for uploaded'})
        response.status_code = 400
        return response
    
if __name__ == "__main__":
    app.run(debug = True)