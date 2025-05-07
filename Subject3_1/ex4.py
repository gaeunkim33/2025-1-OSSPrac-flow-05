from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def input():
    return render_template('input.html')

# 제출된 데이터를 처리하여 출력하는 경로
@app.route('/result', methods=['POST'])
def result():
    # 각 학생의 이름과 학번 데이터를 리스트로 받음
    names = request.form.getlist('name[]')
    student_numbers = request.form.getlist('StudentNumber[]')
    languages = request.form.getlist('language[]')
    major = request.form.getlist('major[]')
    genders = []
        
    for i in range(len(names)):
        gender_value = request.form.get(f'gender_{i}')
        genders.append(gender_value)

    # 데이터를 템플릿으로 전달하여 출력 페이지 생성
    return render_template('result.html', students=zip(names, student_numbers, genders), languages=languages)

if __name__ == '__main__':
    app.run(debug=True)