meetup-food-finder
==================

Hit Meetup.com API, find events with food.

Credit for the idea goes to my coworker, Fuk Yeung, who loves to find all things free.


Ultimately, the idea is to refine this and have it find events in a given city that have food (and ascertain that it is definitely free, if possible). Right now, it simply searches event descriptions for the words "refreshments", "pizza", and "food", and exports information to a .csv.

While this program's results are certainly attractive to the cheap college student or 20-something who wants a free meal and, hey, maybe meet some cool people or learn something in the process, I think it could be vastly useful to homeless or impoverished individuals living in cities with an active meetup community (like Boston) who are often worried about their next meal.

When this program is in a more impressive and useful state, I will throw it in a Django app and host it somewhere.


To run it, simply clone the repo and run python find_food.py. You can option include -z and a zip code as an argument. It will default to 02110 - Boston.
