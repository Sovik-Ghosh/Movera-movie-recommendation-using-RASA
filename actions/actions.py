from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import EventType, SlotSet
import random
from utils.util import Utils

class ActionOffer(Action):
    def name(self) -> Text:
        return "action_offer"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[EventType]:
        util = Utils()
        entities = tracker.latest_message.get("entities", [])
        print(entities)
        entity_val = dict()
        for entity in entities:
            if entity['extractor'] == 'CRFEntityExtractor':
                entity_name = entity["entity"]
                entity_value = entity["value"]
                if entity_name in entity_val:
                    entity_val[entity_name] = list(entity_val[entity_name]).append(entity_value)
                else:
                    entity_val[entity_name] = entity_value
            else:
                continue
        print(entity_val)
        if entity_val:
            if 'request' in list(entity_val.keys()):
                title = tracker.get_slot('title')
                if entity_val['request'] == 'genre' or entity_val['request'] == 'kind':
                    genre = util.get_genre_name(title)
                    if genre:
                        dispatcher.utter_message(response="utter_inform_genre", genre = genre, title = title)
                        return [SlotSet("genre", genre)]
                    else:
                        dispatcher.utter_message("I couldn't extract the genre.")
                        return []
                if entity_val['request'] == 'director' or entity_val['request'] == 'directed':
                    director = util.get_director(title)
                    if director:
                        dispatcher.utter_message(response = "utter_inform_director", director = director)
                        return [SlotSet("director", director)]
                    else:
                        dispatcher.utter_message("I couldn't extract the movie title.")
                        return []
                if entity_val['request'] == ['director','genre'] or entity_val['request'] == ['directed','kind'] or entity_val['request'] == ['director','kind'] or entity_val['request'] == ['directed','genre']:
                    genre = util.get_genre_name(title)
                    director = util.get_director(title)
                    if genre and director:
                        dispatcher.utter_message(response = "utter_inform_gendir", director = director, genre = genre)
                        return [SlotSet("genre", genre), SlotSet("director", director)]
                    else:
                        dispatcher.utter_message("I couldn't extract the movie title.")
                        return []
                if entity_val['request'] == 'starred':
                    star = util.get_starring(title)
                    if star:
                        dispatcher.utter_message(response = "utter_inform_starring", starring = star)
                        return [SlotSet("starring", star)]
                    else:
                        dispatcher.utter_message("I couldn't extract the actor.")
                        return []
            elif 'request_alt' in list(entity_val.keys()):
                last_user_messages = tracker.events[-2:]

                if len(last_user_messages) >= 2:
                    entities_last_to_last = last_user_messages[0].get('parse_data', {}).get('entities', [])
                    genre_name = next((entity['value'] for entity in entities_last_to_last if entity['entity'] == 'genre'), None)
                    director_name = next((entity['value'] for entity in entities_last_to_last if entity['entity'] == 'director'), None)
                    actor_name = next((entity['value'] for entity in entities_last_to_last if entity['entity'] == 'starring'), None)
                c, movies = util.search_movies_by_genre_director_actor(genre_name, director_name, actor_name)
                movie = random.choice(movies)
                while(movie.vote_average == 0.0):
                    movie = random.choice(movies)
                if movie:
                    dispatcher.utter_message(response = "utter_offer", count = c, title = movie.title, aggregate_rating = movie.vote_average)
                    return [SlotSet("count", c), SlotSet("title", movie.title),SlotSet("aggregate_rating", movie.vote_average)]
                else:
                    dispatcher.utter_message("I couldn't extract the movie title.")
                    return []
            else:
                if 'genre' in entity_val:
                    genre_name = entity_val['genre']
                else:
                    genre_name = None
                if 'director' in entity_val:
                    director_name = entity_val['director']
                else:
                    director_name = None
                if 'starring' in entity_val:
                    actor_name = entity_val['starring']
                else:
                    actor_name = None
                c, movies = util.search_movies_by_genre_director_actor(genre_name, director_name, actor_name)
                movie = movies[0]
                while(movie.vote_average == 0.0):
                    movie = random.choice(movies)
                if movie:
                    dispatcher.utter_message(response = "utter_offer", count = c, title = movie.title, aggregate_rating = movie.vote_average)
                    return [SlotSet("count", c), SlotSet("title", movie.title),SlotSet("aggregate_rating", movie.vote_average)]
                else:
                    dispatcher.utter_message("I couldn't extract the movie title.")
                    return []
        else:
            c , movies = util.get_movie()
            title, rating = random.choice(movies)
            while(rating == 0.0):
                title, rating = random.choice(movies)
            if title and rating:
                dispatcher.utter_message(response = "utter_offer", count = c, title = title, aggregate_rating = rating)
                return [SlotSet("title", title),SlotSet("aggregate_rating", rating)]
            else:
                dispatcher.utter_message("I couldn't extract the movie title.")
                return []
            
class ActionBye(Action):
    def name(self) -> Text:
        return "action_bye"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[EventType]:
        util = Utils()
        entities = tracker.latest_message.get("entities", [])
        entity_val = dict()
        for entity in entities:
            entity_name = entity["entity"]
            entity_value = entity["value"]
            entity_val[entity_name] = entity_value
        
        if 'negate' in list(entity_val.keys()) or 'thanks' in list(entity_val.keys()):
            dispatcher.utter_message(response = "utter_goodbye")
            return []
        else:
            dispatcher.utter_message(response = "utter_more")
            return []