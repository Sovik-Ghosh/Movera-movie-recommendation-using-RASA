from tmdbv3api import TMDb, Movie, Genre, Discover, Search, Person
import random

class Utils():
    def __init__(self):
        self.tmdb = TMDb()
        self.tmdb.api_key = 'a0a749627e43b8856046f70f3a06b3bc'
        self.tmdb.debug = True
        self.movie = Movie()
        self.genre = Genre()
        self.discover = Discover()
        self.search = Search()
        self.person = Person()

    def get_genre_name(self, title):
        response = self.search.movies(title)
        if response:
            genre = self.movie.details(response[0].id).genres
            return genre[0].name
        else:
            return None
        
    def get_director(self, title):
        response = self.search.movies(title)
        if response:
            details = self.movie.credits(response[0].id)
            director = next((crew.name for crew in details['crew'] if crew.job == 'Director'), None)
            if director:
                return director
            else:
                return None
        else:
            return None
        
    def get_starring(self, title):
        response = self.search.movies(title)
        if response:
            details = self.movie.credits(response[0].id)
            actors = [cast.name for cast in details.cast]
            if actors:
                return actors[0]
            else:
                return None
        else:
            return None

    def get_genre(self, genre_name):

        if genre_name is not None:
            genres = self.genre.movie_list()
            matching_genre = next((g for g in genres if g.name.lower() == genre_name.lower()), None)

            if matching_genre:
                return matching_genre['id']
            else:
                return None
        else:
            return None
    
    def search_movies_by_genre_director_actor(self, genre_name= None, director_name = None, actor_name = None):
        
        genre_id = self.get_genre(genre_name)
        director_id = None
        actor_id = None
        
        if director_name is not None:
            search_directors = self.search.people(director_name)
            
            if search_directors:
                director = search_directors[0]
                director_id = director.id
                
        if actor_name is not None:
            search_actors = self.search.people(actor_name)
                
            if search_actors:
                actor = search_actors[0]
                actor_id = actor.id

        find = lambda x: str(x) if x is not None else None
        search_params = {
            'sort_by': 'popularity.desc'
        }

        genre_param = find(genre_id)
        if genre_param:
            search_params['with_genres'] = genre_param

        director_param = find(director_id)
        if director_param:
            search_params['with_crew'] = director_param

        actor_param = find(actor_id)
        if actor_param:
            search_params['with_cast'] = actor_param

        movies = self.discover.discover_movies(search_params)

        result_movies = []
        c = 0
        for movie in movies:
            result_movies.append(movie)
            c = c+1

        return c , result_movies

    def get_movie(self):
        popular = self.movie.top_rated()
        list_p = []
        c = 0
        for p in popular:
            c = c + 1
            list_p .append([p.title, p.vote_average])
        return c, list_p