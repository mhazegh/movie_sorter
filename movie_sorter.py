#!/usr/bin/env python
import os
import argparse
import urllib2
import json


def main():
    ''' Setup parser and determine behavior for options. '''
    parser = argparse.ArgumentParser(description=('Sort movies based on '
                                                  'genre and score.'))
    parser.add_argument('-f',
                        '--filepath',
                        default='test_movies.txt',
                        help=('Path to file which contains list of movies.'))
    parser.add_argument('-g',
                        '--genre',
                        default='All',
                        choices=['Action & Adventure',
                                 'Animation',
                                 'Comedy',
                                 'Documentary',
                                 'Drama',
                                 'Horror',
                                 'Mystery & Suspense',
                                 'Romance',
                                 'Science Fiction & Fantasy',
                                 'All'],
                        help='Genre to sort by.')
    parser.add_argument('-s',
                        '--score_type',
                        default='critics_score',
                        choices=['critics_score',
                                 'audience_score'],
                        help='Which type of score to rank by.')
    parser.add_argument('-a',
                        '--actor',
                        help='Search for movies with a specific actor.')
    parser.add_argument('-u',
                        '--update',
                        action='store_true',
                        default=False,
                        help='Update the json file.')
    parser.add_argument('-r',
                        '--rebuild',
                        action='store_true',
                        default=False,
                        help='Completely rebuild the json file.')
    args = parser.parse_args()

    if args.update or args.rebuild:
        movie_dict = build_dict(args.filepath, args.rebuild)
    else:
        try:
            movie_dict = json.load(open('movie_data.json', 'r'))
        except IOError:
            print ('Error: movie_data.json not found in current directory. '
                   'Build it by using the -u option.')
            return
        sort_movies(movie_dict, args.genre, args.score_type, args.actor)


def sort_movies(movie_dict, genre='All',
                score_type='critics_score',
                actor=None):
    ''' Sorts movies based on arguments and prints results to console. '''
    sep = '-'*50
    if actor:
        matching_movies = []
        for movie in sorted(movie_dict.items(),
                            key=lambda (k, v): v[score_type],
                            reverse=True):
            if actor.lower() in [a.lower() for a in movie[1]['actors']]:
                matching_movies.append((movie[1],
                                        movie[1][score_type]))

        print '{0}\n{1}\n{0}'.format(sep, actor)
        for tup in matching_movies:
            print '\t {0} {1}'.format(tup[0], tup[1])

    elif genre == 'All':
        # For each genre, print out movies that belong to that genre
        # and their scores.
        action_and_adventure = []
        animation = []
        comedy = []
        documentary = []
        drama = []
        horror = []
        mystery_and_suspense = []
        romance = []
        scifi = []

        action_and_adventure_str = 'Action & Adventure'
        animation_str = 'Animation'
        comedy_str = 'Comedy'
        documentary_str = 'Documentary'
        drama_str = 'Drama'
        horror_str = 'Horror'
        mystery_and_suspense_str = 'Mystery & Suspense'
        romance_str = 'Romance'
        scifi_str = 'Science Fiction & Fantasy'

        # Iterate through the dictionary once and classify each movie.
        for movie in sorted(movie_dict.items(),
                            key=lambda (k, v): v[score_type],
                            reverse=True):
            if action_and_adventure_str in movie[1]['genres']:
                action_and_adventure.append((movie[0],
                                             movie[1][score_type]))
            if animation_str in movie[1]['genres']:
                animation.append((movie[0], movie[1][score_type]))
            if comedy_str in movie[1]['genres']:
                comedy.append((movie[0], movie[1][score_type]))
            if documentary_str in movie[1]['genres']:
                documentary.append((movie[0], movie[1][score_type]))
            if drama_str in movie[1]['genres']:
                drama.append((movie[0], movie[1][score_type]))
            if horror_str in movie[1]['genres']:
                horror.append((movie[0], movie[1][score_type]))
            if mystery_and_suspense_str in movie[1]['genres']:
                mystery_and_suspense.append((movie[0],
                                             movie[1][score_type]))
            if romance_str in movie[1]['genres']:
                romance.append((movie[0], movie[1][score_type]))
            if scifi_str in movie[1]['genres']:
                scifi.append((movie[0], movie[1][score_type]))

        print '{0}\n{1}\n{0}'.format(sep, action_and_adventure_str)
        for tup in action_and_adventure:
            print '\t {0} {1}'.format(tup[0], tup[1])

        print '{0}\n{1}\n{0}'.format(sep, animation_str)
        for tup in animation:
            print '\t {0} {1}'.format(tup[0], tup[1])

        print '{0}\n{1}\n{0}'.format(sep, comedy_str)
        for tup in comedy:
            print '\t {0} {1}'.format(tup[0], tup[1])

        print '{0}\n{1}\n{0}'.format(sep, documentary_str)
        for tup in documentary:
            print '\t {0} {1}'.format(tup[0], tup[1])

        print '{0}\n{1}\n{0}'.format(sep, drama_str)
        for tup in drama:
            print '\t {0} {1}'.format(tup[0], tup[1])

        print '{0}\n{1}\n{0}'.format(sep, horror_str)
        for tup in horror:
            print '\t {0} {1}'.format(tup[0], tup[1])

        print '{0}\n{1}\n{0}'.format(sep, mystery_and_suspense_str)
        for tup in mystery_and_suspense:
            print '\t {0} {1}'.format(tup[0], tup[1])

        print '{0}\n{1}\n{0}'.format(sep, romance_str)
        for tup in romance:
            print '\t {0} {1}'.format(tup[0], tup[1])

        print '{0}\n{1}\n{0}'.format(sep, scifi_str)
        for tup in scifi:
            print '\t {0} {1}'.format(tup[0], tup[1])
    else:
        matching_movies = []
        for movie in sorted(movie_dict.items(),
                            key=lambda (k, v): v[score_type],
                            reverse=True):
            if genre in movie[1]['genres']:
                matching_movies.append((movie[0],
                                        movie[1][score_type]))

        print '{0}\n{1}\n{0}'.format(sep, genre)
        for tup in matching_movies:
            print '\t {0} {1}'.format(tup[0], tup[1])


def build_dict(filepath='test_movies.txt', rebuild=False):
    '''
    Queries rotten tomatoes for movie data, creates a dictionary out of the
    data, dumps it to movie_data.json, returns the dictionary.
    '''
    if rebuild:
        movie_dict = {}
        write_flag = 'w'
    else:
        try:
            movie_dict = json.load(open('movie_data.json', 'r'))
        except IOError:
            movie_dict = {}
        write_flag = 'wa'

    # Get a list of movies in the specified directory.
    white_list = ('.avi', '.mp4')

    try:
        movies = [os.path.splitext(m)[0] for m
                  in open(filepath, 'r').read().splitlines()
                  if m.endswith(white_list)]
    except IOError:
        print 'Error: Could not open {}'.format(filepath)

    movies = [m for m in movies if m not in movie_dict]
    key = 'jjzq2ekfmxjzymr6qqc3x47e'

    # Build a dictionary of titles, scores, and ids.
    for num, movie in enumerate(movies):
        print '{} of {} - {}'.format(num+1, len(movies), movie)
        cleaned_movie = movie.replace(' ', '+')
        url = ('http://api.rottentomatoes.com/api/'
               'public/v1.0/movies.json?apikey={0}'
               '&q={1}&page_limit=1'.format(key, cleaned_movie))
        try:
            response = urllib2.urlopen(url)
            data = json.load(response)
            movie_id = data['movies'][0]['id']
            title = data['movies'][0]['title']
            critics_score = data['movies'][0]['ratings']['critics_score']
            audience_score = data['movies'][0]['ratings']['audience_score']
            actors = [a['name'] for a in data['movies'][0]['abridged_cast']]
            rt_link = data['movies'][0]['links']['alternate']
            movie_dict[title] = {'id': movie_id,
                                 'critics_score': critics_score,
                                 'audience_score': audience_score,
                                 'actors': actors,
                                 'rt_link': rt_link}
        except (IndexError, urllib2.URLError):
            print 'Error fetching data for {}'.format(movie)
            continue

        try:
            # We have to use the 'id' found in the previous query to
            # get the genre of a movie.
            url = ('http://api.rottentomatoes.com/api/'
                   'public/v1.0/movies/'
                   '{0}.json?apikey={1}'.format(movie_id, key))
            response = urllib2.urlopen(url)
            data = json.load(response)
            print data
            raw_input()
            genres = data['genres']
            movie_dict[title]['genres'] = genres
        except (IndexError, urllib2.URLError):
            print 'Error fetching genre for {}'.format(movie)
            movie_dict[title]['genres'] = []

        try:
            url = ('http://api.rottentomatoes.com/api/'
                   'public/v1.0/movies/'
                   '{0}/similar.json?apikey={1}'.format(movie_id, key))
            response = urllib2.urlopen(url)
            data = json.load(response)
            similar = [a['title'] for a in data['movies']]  
            movie_dict[title]['similar'] = similar
        except (IndexError, urllib2.URLError):
            print 'Error fetching similar movies for {}'.format(movie)
            movie_dict[title]['similar'] = []
       

    # Dump our updated movie dictionary to a .json file.
    with open('movie_data.json', write_flag) as data_file:
        json.dump(movie_dict, data_file, indent=4)

    return movie_dict

if __name__ == '__main__':
    main()
