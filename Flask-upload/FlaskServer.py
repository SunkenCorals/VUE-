import os
import uuid
from flask import Flask, request, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__,
            static_folder='./static',
            template_folder='./templates')


# 输出
@app.route('/')
def hello():
    return render_template('index.html')

# 设置允许的文件格式、大小
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
app.config['UPLOAD_FOLDER'] = os.getcwd()
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


# 添加路由
@app.route('/index')
def hello_index():
    return render_template('index.html')



@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        files = request.files.getlist('file')
        filelist = []
        urllist = []
        for file in files:
            filename = file.filename
            filetype = filename.split('.')[-1]
            print(filename)
            print(filetype)
            # 有文件夹则添加，没有即自动创建
            uploadpath = os.getcwd() + os.sep + 'static/file'
            if not os.path.exists(uploadpath):
                os.mkdir(uploadpath)
            filename = str(uuid.uuid1()) + '.' + filetype
            print(filename)
            file.save(uploadpath + os.sep + filename)
            filelist.append(filename)
            # 照片回显url
            url = url_for("static", filename="file/" + filename)
            urllist.append(url)

        return render_template('upload.html', msg='文件上传成功!', filelist=filelist, urllist=urllist)
    else:
        return render_template('upload.html', msg='等待上传...')

if __name__ == '__main__':
    app.run(port=8000, debug=True)
