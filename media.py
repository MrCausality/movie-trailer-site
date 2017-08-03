import webbrowser

class Video():
    '''This class defines some variables for 
    both the Movie and TvShow classes'''

    def __init__(self, title, duration, synopsis,
                 initial_release, poster_image_url):
        self.title = title
        self.duration = duration
        self.synopsis = synopsis
        self.initial_release = initial_release
        self.poster_image_url = poster_image_url

class Movie(Video):
    ''''This class provides a way to store movie related information.'''

    def __init__(self, title, duration, synopsis, initial_release,
                 poster_image_url, trailer_youtube_url, rating):
        Video.__init__(self, title, duration, synopsis,
                       initial_release, poster_image_url)
        self.trailer_youtube_url = trailer_youtube_url
        self.rating = rating

    def show_trailer(self):
        webbrowser.open(self.trailer_youtube_url)

# Currently unused.  Class exists for future expansion into tv shows with
# new seasons that just hit
class TvShow(Video):
    '''This class provides a way to store TV show related information.'''

    def __init__(self, title, duration, synopsis, initial_release,
                 poster_image_url, number_of_seasons, number_of_episodes,
                 network):
        Video.__init__(self, title, duration, synopsis,
                       initial_release, poster_image_url)
        self.number_of_seasons = number_of_seasons
        self.number_of_episodes = number_of_episodes
        self.network = network
