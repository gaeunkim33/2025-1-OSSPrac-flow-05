import os
from flask import Flask, request, render_template, send_from_directory, redirect, url_for

app = Flask(__name__)

all_students_data = []

@app.route('/')
def index():
    return render_template('index.html')  


@app.route('/input')
def input_page():
    return render_template('input.html')

@app.route('/image/<path:filename>')
def serve_image(filename):
    image_folder = os.path.join(os.path.dirname(__file__), 'image')
    return send_from_directory(image_folder, filename)



@app.route('/result', methods=['GET', 'POST'])
def result_page():
    global all_students_data
    
    if request.method == 'POST':
        names = request.form.getlist('name[]')
        student_numbers = request.form.getlist('StudentNumber[]')
        email = request.form.getlist('email[]')
        major = request.form.getlist('major[]')
        mbti = request.form.getlist('mbti[]')
        color = request.form.getlist('color[]')
        tel = request.form.getlist('tel[]') 

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
                photo_filename.append("None")  
        
        for i in range(len(names)):
            student_data = (
                names[i], 
                student_numbers[i], 
                genders[i], 
                email[i], 
                major[i], 
                languages[i], 
                color[i], 
                mbti[i], 
                photo_filename[i],
                tel[i] if i < len(tel) else "" 
            )
            all_students_data.append(student_data)

    return render_template('result.html', students=all_students_data)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/clear')
def clear_data():
    global all_students_data
    all_students_data = []
    return redirect(url_for('result_page'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)