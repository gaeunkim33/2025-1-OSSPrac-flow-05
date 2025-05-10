import os
from flask import Flask, request, render_template, send_from_directory

app = Flask(__name__)

# 최초 메인 페이지를 보여주는 루트 경로
@app.route('/')
def index():
    return render_template('index.html')  # 위 HTML 코드를 form.html 파일로 저장해야 합니다

# 학생 정보를 입력하는 경로

@app.route('/input')
def input():
    return render_template('input.html')

@app.route('/image/<path:filename>')
def serve_image(filename):
    image_folder = os.path.join(os.path.dirname(__file__), 'image')
    return send_from_directory(image_folder, filename)

# 제출된 데이터를 처리하여 출력하는 경로
@app.route('/result', methods=['POST'])
def result():
    # 각 학생의 이름과 학번 데이터를 리스트로 받음
    names = request.form.getlist('name[]')
    student_numbers = request.form.getlist('StudentNumber[]')
    email = request.form.getlist('email[]')
    major = request.form.getlist('major[]')
    mbti = request.form.getlist('mbti[]')
    photos = request.form.getlist('photo[]')

    genders = []
    languages = []
        
    for i in range(len(names)):
        gender_value = request.form.get(f'gender_{i}')
        genders.append(gender_value)
        langs = request.form.getlist(f'language_{i}')
        languages.append(langs)
    color = request.form.getlist('color[]')

    # 데이터를 템플릿으로 전달하여 출력 페이지 생성
    return render_template('result.html', students=zip(names, student_numbers, genders, email, major, languages, color, mbti, photos))

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
