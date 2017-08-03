import webbrowser
import os
import re
import datetime as dt

now = dt.datetime.now().strftime('%Y-%m-%d %H:%M')


# Styles and scripting for the page
main_page_head = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta charset="utf-8">
    <title>Currently in Theaters</title>

    <!-- Bootstrap 3 -->
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap-theme.min.css">
    <script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
    <script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js"></script>
    <style type="text/css" media="screen">
        body {
            padding-top: 80px;
        }
        h2 { 
            display: block;
            font-size: 1.5em;
            margin-top: 0.83em;
            margin-bottom: 0.83em;
            margin-left: 0;
            margin-right: 0;
            font-weight: bold;
            overflow: hidden;
            white-space: nowrap;
        }
        #trailer .modal-dialog {
            margin-top: 200px;
            width: 640px;
            height: 480px;
        }
        .hanging-close {
            position: absolute;
            top: -12px;
            right: -12px;
            z-index: 9001;
        }
        #trailer-video {
            width: 100%;
            height: 100%;
        }
        .movie-tile {
            margin-bottom: 40px;
            padding-top: 20px;
        }
        .movie-tile:h2 {
            overflow: hidden;
            white-space; nowrap;
        }
        .movie-tile:after, .movie-tile:before {
            position:absolute;
            opacity: 0;
            transition: .5 ease;
            -webkit-transition: all 0.5s;
        }
        .movie-tile:after {
            content:'\A';
            width:100%; height:100%;
            top:0; left:0;
            background:rgba(20,20,20,0.75);
        }
        .movie-tile:before {
            white-space: pre-wrap;
            content: attr(data-content);
            width: 250px;
            color:#fff;
            z-index:1;
            padding:4px 10px;
            font-size: medium;
            text-align:left;
            vertical-align: middle;
            line-height: 20px;
            word-wrap: normal;
            box-sizing:border-box;
            -moz-box-sizing:border-box;
        }
        .movie-tile:hover:after, .movie-tile:hover:before {
            opacity:1;
        }
        .scale-media {
            padding-bottom: 56.25%;
            position: relative;
        }
        .scale-media iframe {
            border: none;
            height: 100%;
            position: absolute;
            width: 100%;
            left: 0;
            top: 0;
            background-color: white;
        }

    </style>
    <script type="text/javascript" charset="utf-8">
        // Pause the video when the modal is closed
        $(document).on('click', '.hanging-close, .modal-backdrop, .modal', function (event) {
            // Remove the src so the player itself gets removed, as this is the only
            // reliable way to ensure the video stops playing in IE
            $("#trailer-video-container").empty();
        });
        // Start playing the video whenever the trailer modal is opened
        $(document).on('click', '.movie-tile', function (event) {
            var trailerYouTubeId = $(this).attr('data-trailer-youtube-id')
            var sourceUrl = 'http://www.youtube.com/embed/' + trailerYouTubeId + '?autoplay=1&html5=1';
            $("#trailer-video-container").empty().append($("<iframe></iframe>", {
              'id': 'trailer-video',
              'type': 'text-html',
              'src': sourceUrl,
              'frameborder': 0
            }));
        });
        // Animate in the movies when the page loads
        $(document).ready(function () {
          $('.movie-tile').hide().first().show("fast", function showNext() {
            $(this).next("div").show("fast", showNext);
          });
        });
    </script>
</head>
'''


# The main page layout and title bar
main_page_content = '''
  <body>
    <!-- Trailer Video Modal -->
    <div class="modal" id="trailer">
      <div class="modal-dialog">
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">
            <img src="https://lh5.ggpht.com/v4-628SilF0HtHuHdu5EzxD7WRqOrrTIDi_MhEG6_qkNtUK5Wg7KPkofp_VJoF7RS2LhxwEFCO1ICHZlc-o_=s0#w=24&h=24"/>
          </a>
          <div class="scale-media" id="trailer-video-container">
          </div>
        </div>
      </div>
    </div>

    <!-- Main Page Content -->
    <div class="container">
      <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
        <div class="container">
          <div class="navbar-header">
            <a class="navbar-brand" href="#">Currently in Theaters</a>
          </div>
        </div>
      </div>
    </div>
    <div class="container">
      {movie_tiles}
    </div>
  <footer>
  <p align="right">
    <small>
      Metadata used with permission from 
      <a href="https://www.themoviedb.org/en"> The Movie Database.</a>
      <br>
      Last updated: {last_updated}
    </small>
  </p>
  </footer>
  </body>

</html>
'''


# A single movie entry html template
movie_tile_content = '''
<div class="col-md-6 col-lg-4 movie-tile text-center" data-trailer-youtube-id="{trailer_youtube_id}" data-toggle="modal" data-target="#trailer" data-content="{movie_info}">
    <img src="{poster_image_url}" width="220" height="342">
    <h2>{movie_title}</h2>
</div>
'''


def get_movie_info(movie):
    '''Gathers data for movie and formats information
    to be used in hover overlay of movie tiles'''
    return(movie.title + ' (' + movie.initial_release  + ')\nRated: '
           + movie.rating + '\nDuration: ' + movie.duration +
           '\n\n' + movie.synopsis)


def create_movie_tiles_content(movies):
    # The HTML content for this section of the page
    content = ''
    for movie in movies:
        try:
            info = get_movie_info(movie)
            # Extract the youtube ID from the url
            youtube_id_match = re.search(
                r'(?<=v=)[^&#]+', movie.trailer_youtube_url)
            youtube_id_match = youtube_id_match or re.search(
                r'(?<=be/)[^&#]+', movie.trailer_youtube_url)
            trailer_youtube_id = (youtube_id_match.group(0) if youtube_id_match
                                  else None)

            # Append the tile for the movie with its content filled in
            content += movie_tile_content.format(
                movie_title=movie.title,
                poster_image_url=movie.poster_image_url,
                trailer_youtube_id=trailer_youtube_id,
                movie_info=info
            )
        except:
            print('Failed')
    return content


def open_movies_page(movies):
    # Create or overwrite the output file
    output_file = open('fresh_tomatoes.html', 'w')

    # Replace the movie tiles placeholder generated content
    rendered_content = main_page_content.format(
        movie_tiles=create_movie_tiles_content(movies),
        last_updated=now)

    # Output the file
    output_file.write(main_page_head + rendered_content)
    output_file.close()

    # open the output file in the browser (in a new tab, if possible)
    url = os.path.abspath(output_file.name)
    webbrowser.open('file://' + url, new=2)