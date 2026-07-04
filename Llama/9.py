class Video:
    def __init__(self, title, video_url):
        self.title = title
        self.video_url = video_url

class Category:
    def __init__(self, name):
        self.name = name
        self.videos = []

    def add_video(self, video):
        self.videos.append(video)

class VideoStreamer:
    def __init__(self):
        self.categories = {}

    def add_category(self, name):
        self.categories[name] = Category(name)

    def add_video(self, title, video_url, category_name):
        if category_name in self.categories:
            self.categories[category_name].add_video(Video(title, video_url))
        else:
            raise ValueError("Category does not exist")

    def get_category(self, name):
        return self.categories.get(name)

    def play_video(self, title, category_name):
        for category in self.categories.values():
            if category.name == category_name:
                videos = [video for video in category.videos if video.title.lower() == title.lower()]
                if not videos:
                    raise ValueError("Video does not exist")
                return videos[0].video_url
        raise ValueError("Category or video does not exist")

def main():
    video_streamer = VideoStreamer()

    
    video_streamer.add_category('Movies')
    video_streamer.add_category('TV Shows')

    
    video_streamer.add_video('The Shawshank Redemption', 'https://www.youtube.com/watch?v=6o2f9DZ5jA8', 'Movies')
    video_streamer.add_video('The Dark Knight', 'https://www.youtube.com/watch?v=7cCgJl6eN1w', 'Movies')
    video_streamer.add_video('Breaking Bad', 'https://www.youtube.com/watch?v=zUUMvLJtLQ4', 'TV Shows')

    
    print(video_streamer.play_video('The Shawshank Redemption', 'Movies'))

if __name__ == "__main__":
    main()