                                    Fresh Tomatoes

What is it?
-----------

Fresh Tomatoes is a simple website that provides a list of all movies currently in theaters
in the United States.  It provides metadata for each film via a hover overlay, and direct
access to the trailers for the film with a simple click.  This site is generated dynamically
using The Movie Database's API, and can be easily set to refresh at any desired interval.

A live version of this code can be found at http://movies.robost4r.com

Pre-requisites
-----------

Fresh Tomatoes only requires modules from within the Python standard library.
- requests
- OS
- re
- datetime
- webbrowser

All code was originally written in Python 3.4, but has been tested down to Python 2.7

How-to run
----------
You will need an API key from The Movie Database.  This is easily attained by signing
up on their website and describing your project.

Once you have attained this API key, enter it at the top of the "tmdb_api.py" file.
No further customization is required.

Once your API key is entered, run the "main.py" file, and it will output
"fresh_tomatoes.html" in the same directory as the script, and open it in your webbrowser
for inspection.

To-Do:
----------
Logical next steps in this project:
- Add small links on the tile overlay that lead to a Google search for showtimes near user,
  and the wikipedia entry for the film.
- Design a more elegant way of dealing with text overflow on movie tiles with exceptionally
  long synposes.
- Make use of the TV show class to expand site to include TV shows whose seasons are currently
  running, or in the case of Netflix, recently released.

Authors
----------
Udacity Full Stack Web Developer staff - Base code for the "fresh_tomatoes.py" file.
Eric Johnson - Modifications to the "fresh_tomatoes.py" file, and all other code.

Atrributions
----------
Hover overlay: https://stackoverflow.com/questions/18322548/black-transparent-overlay-on-image-hover-with-only-css
TMDb API: https://www.themoviedb.org/documentation/api
