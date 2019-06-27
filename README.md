# NBAAllStarPredictor
I used an NBA API (https://github.com/swar/nba_api) to fetch NBA players' regular season stats. Using these stats 
(43,000 individual seasons), I trained an ML model with TensorFlow to predict whether a player would be named an all-star or not.

**Seasonfetcher.py** is used to make calls to NBA.com, retrieve the desired stats, and save them to a CSV file which I upload to my Google Drive.

**AllStarPredictor.ipynb** actually uses these stats to train the model using the file in my Google Drive.
I created and ran this notebook on Google Colab, and it will not run within this project since tensorflow, matplotlib, sklearn, etc. are not in the lib folder.
