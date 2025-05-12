import os
from flask import Flask, request, render_template, send_from_directory

app = Flask(__name__)

# 최초 메인 페이지를 보여주는 루트 경로
@app.route('/')
def index():
    return render_template('index.html')  

# 학생 정보를 입력하는 경로

@app.route('/input')
def input_page():
    return render_template('input.html')

@app.route('/image/<path:filename>')
def serve_image(filename):
    image_folder = os.path.join(os.path.dirname(__file__), 'image')
    return send_from_directory(image_folder, filename)



# 제출된 데이터를 처리하여 출력하는 경로
@app.route('/result', methods=['GET', 'POST'])
def result_page():
    # 각 학생의 이름과 학번 데이터를 리스트로 받음
    names = request.form.getlist('name[]')
    student_numbers = request.form.getlist('StudentNumber[]')
    email = request.form.getlist('email[]')
    major = request.form.getlist('major[]')
    mbti = request.form.getlist('mbti[]')
    color = request.form.getlist('color[]')

    genders = []
    languages = []
        
    for i in range(len(names)):
        gender_value = request.form.get(f'gender_{i}')
        genders.append(gender_value)
        langs = request.form.getlist(f'language_{i}')
        languages.append(langs)

    photo_file = request.files.getlist('photo[]')
    photo_filename = []
    image_folder = os.path.join(os.path.dirname(__file__), 'image')
    os.makedirs(image_folder, exist_ok=True)
    for i, photo in enumerate(photo_file):
        if photo and photo.filename:
            filename = f"{photo.filename}"
            save_path = os.path.join(image_folder, filename)
            photo.save(save_path)
            photo_filename.append(filename)
        else:
            photo_filename.append("None")  # 이미지가 없는 경우 텍스트로 처리

    # 데이터를 템플릿으로 전달하여 출력 페이지 생성
    return render_template('result.html', students=zip(names, student_numbers, genders, email, major, languages, color, mbti, photo_filename))

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)