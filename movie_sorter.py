import os
import argparse
import urllib2
import json


def main():
    parser = argparse.ArgumentParser(description=('Sort movies based on '
                                                  'various criteria.'))
    parser.add_argument('-d',
                        '--directory',
                        required=True,
                        help=('Directory where movies are stored.'))
    parser.add_argument('-s',
                        '--sort',
                        choices=['score', 'genre'],
                        help=('Sort by either rotten tomates '
                              'score or genre.'))
    args = parser.parse_args()

    if 'movie_data.json' in os.listdir('.'):
        movie_dict = json.load(open('movie_data.json', 'r'))
        sort_movies(movie_dict, args.sort)
    else:
        movie_dict = build_dict(args.directory, args.sort)
        sort_movies(movie_dict, args.sort)


def sort_movies(movie_dict, sort_key='score'):
    if sort_key == 'score':
        # Print out a list of movies sorted by score.
        for movie in sorted(movie_dict.items(),
                            key=lambda (k, v): v["critics_score"],
                            reverse=True):
            print movie[1]['title'], movie[1]['critics_score']

    elif sort_key == 'genre':
        # For each genre, print out movies that belong to that genre
        # and their scores.
        action_and_adventure = []
        comedy = []
        drama = []
        horror = []
        mystery_and_suspense = []

        action_and_adventure_str = 'Action & Adventure'
        comedy_str = 'Comedy'
        drama_str = 'Drama'
        horror_str = 'Horror'
        mystery_and_suspense_str = 'Mystery & Suspense'

        # Iterate through the dictionary once and classify each movie.
        for movie in sorted(movie_dict.items(),
                            key=lambda (k, v): v["critics_score"],
                            reverse=True):
            if action_and_adventure_str in movie[1]['genres']:
                action_and_adventure.append((movie[1]['title'],
                                             movie[1]['critics_score']))
            if comedy_str in movie[1]['genres']:
                comedy.append((movie[1]['title'], movie[1]['critics_score']))
            if drama_str in movie[1]['genres']:
                drama.append((movie[1]['title'], movie[1]['critics_score']))
            if horror_str in movie[1]['genres']:
                horror.append((movie[1]['title'], movie[1]['critics_score']))
            if mystery_and_suspense_str in movie[1]['genres']:
                mystery_and_suspense.append((movie[1]['title'],
                                             movie[1]['critics_score']))

        print '-'*50
        print action_and_adventure_str
        print '-'*50
        for tup in action_and_adventure:
            print '\t {0} {1}'.format(tup[0], tup[1])

        print '-'*50
        print comedy_str
        print '-'*50
        for tup in comedy:
            print '\t {0} {1}'.format(tup[0], tup[1])

        print '-'*50
        print drama_str
        print '-'*50
        for tup in drama:
            print '\t {0} {1}'.format(tup[0], tup[1])

        print '-'*50
        print horror_str
        print '-'*50
        for tup in horror:
            print '\t {0} {1}'.format(tup[0], tup[1])

        print '-'*50
        print mystery_and_suspense_str
        print '-'*50
        for tup in mystery_and_suspense:
            print '\t {0} {1}'.format(tup[0], tup[1])


def build_dict(directory):
    # Load previous dictionary.
    movie_dict = json.load(open('movie_data.json', 'r'))

    # Get a list of movies in the specified directory.
    white_list = ('.avi', '.mp4')
    movies = [os.path.splitext(m)[0] for m
              in open('test_movies.txt', 'r').read().splitlines()
              if m.endswith(white_list)]
    key = 'jjzq2ekfmxjzymr6qqc3x47e'

    # Build a dictionary of titles, scores, and ids.
    for movie in movies:
        if movie not in movie_dict:
            cleaned_movie = movie.replace(' ', '+')
            url = ('http://api.rottentomatoes.com/api/'
                   'public/v1.0/movies.json?apikey={0}'
                   '&q={1}&page_limit=1'.format(key, cleaned_movie))
            response = urllib2.urlopen(url)
            data = json.load(response)
            try:
                id = data['movies'][0]['id']
                title = data['movies'][0]['title']
                critics_score = data['movies'][0]['ratings']['critics_score']
                audience_score = data['movies'][0]['ratings']['audience_score']
                movie_dict[movie] = {'id': id,
                                     'title': title,
                                     'critics_score': critics_score,
                                     'audience_score': audience_score}
            except IndexError:
                print 'Could not find {}'.format(movie)

    # Loop through the movies again to get their genre.
    # We have to use the 'id' found in the previous query to
    # get the genre of a movie.
    for movie in movie_dict:
        url = ('http://api.rottentomatoes.com/api/'
               'public/v1.0/movies/'
               '{0}.json?apikey={1}'.format(movie_dict[movie]['id'], key))
        response = urllib2.urlopen(url)
        data = json.load(response)
        try:
            genres = data['genres']
            movie_dict[movie]['genres'] = genres
        except IndexError:
            print 'Could not get genre for {}'.format(movie)

    # Dump our updated movie dictionary to a .json file.
    with open('movie_data.json', 'wa') as fp:
        json.dump(movie_dict, fp, indent=4)

    return movie_dict

if __name__ == '__main__':
    main()
