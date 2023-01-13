# Football Players Churn Prediction
* Scraped the stats of all players in the 5 best european leagues (Spanish, English,French,German and Italian) since season 09/10 to 21/22 season.
* Scraped the league classifications at the end of each season.
* Merged and standarized the scraped data with the tranfer window season downloaded from a github repository (link in references).
* Explored the information to discover insights.
* Engineered features to reduce multiconilearity and add more value to the data.
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
 *	Apps
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
 *	Offsides_won
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
 *	Long_passes
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
