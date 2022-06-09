# Sentiment Analysis of News Articles
This program scrapes recent articles from news websites and performs sentiment analysis of the same.





## Description
Websites from which the articles are to be scraped can be added to the news_sites json file. The Scraper.py file implements a program that crawls the links give in this json file and collects the 10 most recent articles.
 The scraped articles are stored in the news_scraped json file. The format in which the scraped news articles are stored is as follows: 
```javascript
{
	"news_sites": {
		news_site_name: {
			"items": [{
					"title": "",
					"link": "",
					"text": "",
					"published": ""]
				}
			}
		}
	}
```
The code for preprocessing and conducting the sentiment analysis of the articles is present in the SentimentAnalysis.py file. The preprocessing steps include splitting each article insto sentences, removing special characters such as "#", "%" etc., removing stop words, removing punctuation and lemmatization of the sentences.

The VADER (Valence Aware Dictionary and sEntiment Reasoner) lexicon library is used to compute the sentiment of the articles. This has been done in two ways:\
    1. By computing the VADER score for each sentence in the article text, taking an average of the scores for all sentences in the text and assigning the final sentiment based on this average.\
    2. By computing the sentiment score for both the article heading and the article text and assigning the sentiment by taking a weighted average of the scores for both (after running for different set of articles, assigned the weights: 0.4 for article heading and 0.6 for article text) 

Pie charts were plotted to show the distribution of the news articles based on the sentiment computed using both the above methods (using Plotly).




## Results
The distribution of tweets using both the methods explained for the articles scraped were:
Neutral: 30% 
Negative: 50 %
Positive: 20%
![alt text](https://github.com/kirthikagurumurthy/MINDS-Programming-Challenge/blob/main/Visualizations/piechart_sentiment_text.png)
![alt_text](https://github.com/kirthikagurumurthy/MINDS-Programming-Challenge/blob/main/Visualizations/piechart_weighted_sentiment_text_heading.png)
By manually labelling the tweets as positive, negative and neutral, the accuracy for the sentiment analysis using only the article text was 90% and the accuracy for the sentiment analysis using both the text and the heading (weighted average) is 80%. 
The time taken for scraping the websites: 5.9 s
The time taken for preprocessing the articles, conducting sentiment analysis and plotting the pie charts: 6.1 s
