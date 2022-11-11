import json
import requests

# provides a movie (or bands, TV shows, etc.) as a query input
def get_movies_from_tastedive(name_string):
    baseurl = 'https://tastedive.com/api/similar'
    params_diction = {}
    params_diction['q'] = name_string
    params_diction['type'] = 'movies'
    params_diction['limit'] = 5
    testdive_resp = requests.get(baseurl, params = params_diction)
    return testdive_resp.json()

def extract_movie_titles(lst_data):
    name_data = lst_data['Similar']['Results']
    titles_lst = [name['Name'] for name in name_data]
    return titles_lst

def get_related_titles(lst_movie_titles):
    lst = []
    for movie in lst_movie_titles: 
        lst.extend(extract_movie_titles(get_movies_from_tastedive(movie)))
    return list(set(lst))

# provides a movie title as a query input and get back data about the movie
def get_movie_data(title_movie):
    baseurl = 'http://www.omdbapi.com/'
    params_dict = {}
    params_dict['t'] = title_movie 
    params_dict['r'] = 'json'
    params_dict['apikey'] = ['86897038']
    omdbapi_req = requests.get(baseurl, params = params_dict)
    return omdbapi_req.json()

def get_movie_rating(movie_data_dict):
    OMDB_movie_rating = 0
    for i in movie_data_dict['Ratings']:
        if i['Source'] == 'Rotten Tomatoes':
            OMDB_movie_rating = int(i['Value'][:-1]) 
       
    return OMDB_movie_rating

def get_sorted_recommendations(list_movie_titles):
    list_movie = get_related_titles(list_movie_titles)
    rate_movie = {}
    
    for movie in list_movie:
        rate = get_movie_rating(get_movie_data(movie))
        rate_movie[movie] = rate
        sorted_lst_movie = {m[0]: m[1] for m in sorted(rate_movie.items(), key = lambda item: (item[1], item[0]), reverse = True)}
    print(sorted_lst_movie)
   
    return sorted_lst_movie
    
get_sorted_recommendations(["Mean Girls", "Booksmart", "Tootsie"])