import os
from flask import Flask, render_template_string


app = Flask(__name__)




video_list = [
    {"id": 1, "title": "Introduction to Shakespeare", "filename": "intro.mp4"},
    {"id": 2, "title": "Grammar Basics: Nouns and Verbs", "filename": "grammar.mp4"},
    {"id": 3, "title": "The Art of the Short Story", "filename": "stories.mp4"}
]


@app.route('/')
def home_page():
    html_layout = 
    return render_template_string(html_layout, videos=video_list)


@app.route('/video/<int:video_id>')
def watch_video(video_id):
    
    selected_video = next((v for v in video_list if v['id'] == video_id), None)
    
    if not selected_video:
        return "Lesson not found", 404

    html_layout = 
    return render_template_string(html_layout, video=selected_video)


if __name__ == '__main__':
    
    
    app.run(debug=True)