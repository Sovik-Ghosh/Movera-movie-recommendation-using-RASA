<div style="display: flex; flex-direction: row;">
  <img src="/assets/app.logomakr.com_28ja6E-ezgif.com-crop.gif" alt="Flow Image" style="width: 1000px; height: auto;">
</div>

The new era enhances the visual experience with creative arts and computer-generated imagery. Therefore, to showcase visually stimulated movies, ’Movera’, a chatbot has been developed to take movie requests as user input and then process the best movie recommendation.

## TECHNOLOGY

The chatbot uses an extensive range of frameworks:-
- ***Python-3.9***: The primary programming language used for external API calls, custom action builds, and variable logic.
- ***RASA***: The core of the chatbot is built using the Rasa framework, including Rasa NLU for Natural language Understanding and Rasa Core for story management.
- ***TMDB API***: The bot leveraged The Movie Database API to fetch information about movies including title, genre, vote average, director’s name, actor’s name, etc.

### INSTALLATION

1. Clone the repository:

   ```bash
   https://github.com/Sovik-Ghosh/Movera-movie-recommendation-using-RASA.git
   ```

2. Create a virtual environment:
    ```bash
    python3 -m venv rasa
    ```

3. Activate the virtual environment:
    ```bash
    source rasa/bin/activate
    ```

4. Install dependencies (if any) and set up your development environment.
   ```bash
   pip3 -r requirements.txt
   ```

## FLOW DIAGRAM

<div style="display: flex; flex-direction: row;">
  <img src="/assets/Flow.png" alt="Flow Image" style="width: 50%; height: auto;">
</div>

## Running the Chatbot

1. Open two terminal windows

2. Activate the virtual environment on each window:
    ```bash
    source rasa/bin/activate
    ```
    

3. Run the code:
    - First Window:
      ```bash
      rasa run actions
      ```
    - Second Window:
      ```bash
      rasa shell
      ```

4. Test the chatbot.

## SAMPLE

![Sample conversation](/assets/sample.png)

## CONFUSION MATRIX

<div style="display: flex; flex-direction: row;">
  <img src="/assets/story_confusion_matrix.png" alt="Confusion matrix" style="width: 100%; height: auto;">
</div>

## Customizing and Extending

Feel free to customize the project to implement your strategies and behaviors for extending chatbot variations.

You can modify the existing data .yml files.

1. [NLU](data/nlu.yml):
  - Rasa NLU contains training data that was collected and annotated from the example.json file which is  then divided and classified into two intents categorised as FindMovies and Other.

    - ***FindMovies*** - It contains training data that asks for system recommendations for popular movies, specific genre requests, and specific actor or director movie requests. It also contains system enquiry for the director, genre, or star of a particular movie recommended by the system. Entities such as ‘genre’, ‘title’, ‘aggregate_rating’, ‘director’, and ‘starring’ are marked by entity value in ‘[]’ followed by entity name in ‘()’. Additionally, new entities named ‘request’ and ‘request_alt’ are created to handle enquiry about the director’s name, genre, and actor’s name, and to request an alternate movie recommendation based on the previous search.

    - ***Other*** - It contains training data that affirms or denies the system recommendation. Additional entities like ‘negate’ and ‘thanks’ are created to handle dynamic questioning. It either prompts further help or replies with a goodbye.

2. [Stories](data/stories.yml):

  - Rasa stories contain paths for training the data. It defines example conversations between the user and the chatbot or the agent. Rasa’s machine-learning model, dialogue management system learns from the training data that showcases different paths a model can take during a conversation. Movera's story path states that when the current intent is ‘FindMovies’ it performs ‘action_offer’, else if the intent is ‘Other’ it performs ‘action_bye’, which are custom actions respectively.


3. [Rules](data/rules.yml):

  - Rasa rules contain an absolute function call when a particular intent is detected. It defines that when a specific intent is detected a particular response will be performed irrespective of the story path. Movera’s rule path states that when intent ‘FindMovies’ is detected it will perform the custom action ‘action_offer’. Similarly, when intent ‘Other’ is detected it will always trigger the custom action ‘action_bye’. Rules are not mandatory but helpful when there are story clashes, or when adequate story path and proper training data have not been provided.



4. [Domain](domain.yml):

  - The Rasa domain file contains the complete universe of Movera. It consists of all the intents, entities, slots, responses, and actions.


5. [Custom Actions](actions/actions.py):

  - Movera has been designed with two custom actions for dynamic results based on the user’s search. The custom actions either offer the user movie recommendations or answers to the user’s enquiry.

    - ***action_offer***: The action_offer function with the help of configurations like ‘DIETClassifier’, and ‘CRFEntityExtractor’ detects the intent of the user’s dialogue, and extracts the relevant entities to process a featured movie recommendation further. This function is triggered when the intent ‘FindMovies’ is detected. It creates a dictionary of entity types and entity values to account for the director’s name, actor’s name, and genre related enquiry. It sends slot values and utters responses like utter_offer, utter_inform_gendir, utter_inform_genre, utter_inform_director, and utter_inform_starring.

    - ***action_bye***: The action_bye function is triggered when the intent ‘Other’ is detected. This function when prompted utters responses like utter_more and utter_goodbye.


6. [TMDB](utils/util.py):

  - Movera uses ‘tmdbv3api’ as the backend to perform multiple queries and prompt the best movie recommendations. A modular approach has been used to adhere to different enquiries.

    - **get_genre**: This function takes in the movie title and returns the genre name.

    - **get_director**: This function takes in the movie title and returns the director’s name.

    - **get_starring**: This function takes in the movie title and returns the actor’s name.

    - **search_movies_by_genre_director_actor**: This function takes in the director’s name, actor’s name, and genre and recommends a movie title and movie aggregate rating based on user search. 

    - **get_movie**: This function recommends popular movies.

Additionally, you can explore advanced features provided by [RASA](https://rasa.com/).

## Contributing

If you would like to contribute to this project, please follow our [contribution guidelines](CONTRIBUTING.md). We welcome bug reports, feature requests, and pull requests.

## License

This project is licensed under the [MIT License](LICENSE).
