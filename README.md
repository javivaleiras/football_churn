# Football Players Churn Prediction
* Scraped the stats of all players in the 5 best european leagues (Spanish, English,French,German and Italian) since season 09/10 to 21/22 season.
* Scraped the league classifications at the end of each season.
* Merged and standardized the scraped data with the transfer window season downloaded from a Github repository (link in references).
* Explored the information to discover insights.
* Engineered features to reduce multicollinearity and add more value to the data.
* Dealt with the imbalanced dataset using various techniques such as SMOTETomek, StratifiedKFold, etc.
* Tested different models lazily to decide wich one opitimize.
* Optimized Random Forest Classifier and K-Nearest Neighbors using GridSearchCV to reach the best model.
* Built a client facing API using Flask.

## Objective
The objective is to predict, using player information such as team, team position etc and stats as goals, minutes played etc if a player will leave his current team
for the next season.
## Scope of the proyect
* All the stats are full season stats so we are only coniderating summer trades because winter trades are more influenced by mid-season stats.
* All players of all teams of this 5 leagues are considered: La Liga (Spain), Premier League (England), Serie A (Italy), Bundesliga (Germany) and Ligue 1 (France).
## Code and Resources Used 
**Python Version:** 3.8.5 

**Packages:** pandas, numpy, sklearn, matplotlib, seaborn, selenium, flask, joblib 

**For Web Framework Requirements:**  ```pip install -r requirements.txt``` or ```conda create --name <env> --file requirements.txt```

**Player Tranfsers CSV:** https://github.com/ewenme/transfers 

## Web Scraping
Scraped a football website with stats of all players per league and an historic of all leagues classification. To each pair league/season, we got the following:
### Players Data
 *  Name
 *	Club
 *	Age
 *	Position
 *	Appearances
 *	Mins
 *	Goals
 *	Assists
 *	Yel
 *	Red
 *	Shots
 *	Ps%
 *	Aerials won
 *	Motm
 *	Rating
 *	Tackles
 *	Interceptions
 *	Fouls
 *	Offsides won
 *	Clearances
 *	Dribbled
 *	Blocks
 *	Own goals
 *	Key passes
 *	Dribblings
 *	Fouled
 *	Offsides
 *	Dispossed
 *	Bad controls
 *	Avg passes
 *	Crosses
 *	Long passes
 *	Through passes
 *	League
 *	Season

### Leagues Data
 *  Position
 *  Club
 *  League
 *  Season

## Data Wrangling
After scraping the data I had to combine it with the one that had all transfers data so I would know for each player if at the end of this season he
would leave the team. To do that I had to:
 *  Match the number of season in both datasets because the transfers one had data since early 90s seasons.
 *  Clean the seasons dataset to obtain just the out summer trades and remove the end of loan trades.
 *  Match the club names because same teams would have different names in both datasets.
 *	Discover some special cases that made the merge complex:
	*  The seasons x/y stats correspond to the x+1/y+1 trade. Example: a trade in the summer of 10/11 season correspond to 09/10 stats. 
	*  The player could have played in a team last season and be traded by another team because he played on a loan.

Finally, a dataset with all players information plus a column which indicated if the player was traded or not was obtained.

## Data Cleaning & EDA
After scraping the data, I needed to clean it up so that it was usable for our model. I made the following changes and created the following variables:

 *	Adjusted the format of all variables to reduce memory usage.
 *	Added both values of apps feature to make it a single number variables.
 *	Replaced the "-" for na values.
 *	Grouped all positions to form 5 groups: goalkeepers, defenders, defensive midfielders, offensive midfielders and forwards.
 *	Dealt with the high number of null values.
 *	Dropped the stats of the players of the last 3 teams of each league because they added noise since we don´t have the trades for teams that had been relegated last season.
 *	Dropped goalkeepers from the dataframe because we don´t have any specific goalkeeper stat.
 *	Created from each variable a new one that penalized low appereances so,for example, a player that played just 1 game and made 4 shoots would be less important than a player that made 4 shoots per game in 20 games.
 *	Created a feature that weighed the average passes with the passes success ratio.
 *	Categorized appeareances using deciles to reduce multicollinearity.
 
All the decision were taken based on insights I discovered in the EDA process in which I also looked at the distributions of the data, the value counts for the various categorical variables etc.

## Model Building 

First, I adjusted the types of the variables to reduce memory usage and then I transformed the categorical variables into dummy variables using the one hot encoder and scaled down the values of the numerical features as well. I also created a list of models and tried all of them using the holdout method to get a hint of which one would perform better.

Once I got the results, I decided to test more with K-Nearest Neighbors Classifier and Random Forest Classifier and tried them using 3 techniques to reduce the problem of the imbalanced data: SMOTETomek, SMOTE and StratifiedKFold.

Based on the results, I decided to hyperparametrize Random Forest using StratifiedKFold but I finally ended up hyperparameterizing KNN and testing SMOTETomek as well just in case.

I discovered that the best hyperparameters were overfitting, mainly because of max depth so I had to tune this parameter manually tp finally obtain a model with low variance.

Finally, I wanted to test, just in case, SMOTETomek with Random Forest and KNN with StratifiedKFold but both tests didn´t overcome Random Forest.

## Model performance
The Random Forest model far outperformed the other approaches. 
*	**Random Forest** : Prescision = 0.65 Recall: 0.62 F1-Score: 0.67

## Productionization 
In this step, I built a flask API endpoint that was hosted on a local webserver. The API endpoint takes in a request with a list of stats of the player and some information as the club, position etc and transform it using the techniques and encoders used in the notebooks to finally give a prediction wether the player will leave or not leave his current club.
