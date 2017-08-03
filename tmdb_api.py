import requests
import datetime as dt

class TMDB:
    '''This class provides several methods for gathering movie metadata
    from The Movie Database'''
    api_url = 'https://api.themoviedb.org/3'
    api_key = '0bf0413b190061ce12afb24493b06a50'

    # api_key currently hardcoded, but could easily be adjusted to accept it
    # from another source, potentially securely
    # def __init__(self, api_key):
    #     self.api_key = api_key

    def make_endpoint(self, prefix, suffix, page=1):
        '''Takes a string for prefix and suffix, combines with the stored API
        key, and generates the endpoint for use in the API'''
        endpoint = prefix + '?api_key=' + self.api_key + '&page=' + str(page)\
                   + '&' + suffix
        return(endpoint)

    def get(self, endpoint, paras=None):
        '''Takes an endpoint, sends http request to the API,
         and returns the JSON response'''
        uri = self.api_url + endpoint
        response = requests.get(uri, params=paras)
        if response.status_code == 404:
            print(response.status_code)
        else:
            return response.json()

    def get_now_showing(self):
        '''Returns array of metadata for all movies with a USA
        theatrical release in the last 30 days'''
        now_showing = []
        today = dt.date.today()
        one_month_ago = today - dt.timedelta(days=31)
        prefix = '/discover/movie'
        suffix = 'primary_release_date.gte=' + str(one_month_ago) \
                 + '&primary_release_date.lte=' + str(today) \
                 + '&with_release_type=3&region=US'
        endpoint =  self.make_endpoint(prefix, suffix)
        # api returns data in multiple pages.  This section gets total pages,
        # iterates through all pages, and appends the data to a single array.
        total_pages = self.get_pages(endpoint)
        for i in range(1, total_pages+1):
            endpoint = self.make_endpoint(prefix, suffix, i)
            request = self.get(endpoint)
            now_showing += request['results']
        return(now_showing)

    def get_pages(self, endpoint):
        '''Returns the number of pages of data in an API response'''
        return((self.get(endpoint))['total_pages'])

    def get_movie(self, id):
        '''Takes a movie ID and returns that single movie object'''
        endpoint = self.make_endpoint('/movie/' + str(id),
                                      'append_to_response=videos, releases')
        movie = self.get(endpoint)
        return(movie)

    def get_title(self, movie):
        '''Takes a movie object and returns the title of the movie'''
        try:
            title = movie['title']
            return(title)
        except:
            return(None)

    def get_poster_url(self, movie):
        '''Takes a movie object and returns the poster url of the movie'''
        try:
            path = movie['poster_path']
            poster_image_url = 'http://image.tmdb.org/t/p/w185' + path
            return(poster_image_url)
        except:
            return(None)

    def get_trailer_url(self, movie):
        '''Takes a movie object and returns the official trailer
         url of the movie.  If no trailer is found, instead returns 
         the trailer for a movie titled 'No Trailer' '''
        try:
            trailers = movie['videos']['results']
            yt_id = trailers[0]['key']
            for trailer in trailers:
                if trailer['name'] == 'Official Trailer':
                    yt_id = trailer['key']
                    break
        except:
            yt_id = 'lOeiw_BJPas'

        trailer_url = 'https://www.youtube.com/watch?v=' + yt_id
        return(trailer_url)

    def get_rating(self, movie):
        '''Takes a movie object and returns the Rating of that movie,
        or 'Unknown' if rating cannot be found'''
        try:
            releases = movie['releases']['countries']
            for release in releases:
                if release['iso_3166_1'] == 'US':
                    rating = release['certification']
                    break
        except:
            rating = 'Unknown'
        if rating == '':
            rating = 'Unknown'
        return(rating)

    def get_runtime(self, movie):
        '''Takes a movie object and returns the runtime of the movie,
        or 'Unknown' if runtime cannot be found'''
        try:
            runtime = str(dt.timedelta(minutes=(movie['runtime'])))
            h, m, s = runtime.split(':')
            return(h + 'h ' + m + 'm')
        except:
            return('Unknown')

    def get_synopsis(self, movie):
        '''Takes a movie object and returns the synopsis of the movie,
        or 'No synopsis found' if synopsis cannot be found'''
        try:
            synopsis = movie['overview']
            return(synopsis)
        except:
            return('No synopsis found')

    def get_release_date(self, movie):
        '''Takes a movie object and returns release year,
        or 'Unknown Year' if release cannot be found'''
        try:
            release = movie['release_date'][0:4]
            return(release)
        except:
            return('Unknown Year')
