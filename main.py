import media
import fresh_tomatoes
import tmdb_api as db

tmdb = db.TMDB()
now_showing = tmdb.get_now_showing()

movies = []
for movie in now_showing:
    movie_id = tmdb.get_movie(movie['id'])
    movie_obj = media.Movie(tmdb.get_title(movie_id),
                tmdb.get_runtime(movie_id),
                tmdb.get_synopsis(movie_id),
                tmdb.get_release_date(movie_id),
                tmdb.get_poster_url(movie_id),
                tmdb.get_trailer_url(movie_id),
                tmdb.get_rating(movie_id))
    if movie_obj.poster_image_url != None and movie_obj.title != None:
        print("Processing " + movie_obj.title)
        movies.append(movie_obj)

fresh_tomatoes.open_movies_page(movies)
