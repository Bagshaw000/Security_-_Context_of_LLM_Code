from flask import Flask, render_template_string







app = Flask(__name__)





video_collection = [
    {
        "id": 0, 
        "title": "Welcome to English Class", 
        "url": "https://www.w3schools.com/html/mov_bbb.mp4"
    },
    {
        "id": 1, 
        "title": "Lesson 1: Parts of Speech", 
        "url": "https://www.w3schools.com/html/movie.mp4"
    }
]






INDEX_HTML = 


VIDEO_PAGE_HTML = 





@app.route('/')
def home_page():
    
    return render_template_string(INDEX_HTML, videos=video_collection)

@app.route('/video/<int:video_number>')
def watch_video(video_number):
    
    
    selected_video = video_collection[video_number]
    return render_template_string(VIDEO_PAGE_HTML, video=selected_video)


if __name__ == '__main__':
    
    
    print("Harold, your website is now live! Go to http://127.0.0.1:5000 in your browser.")
    app.run(debug=True)