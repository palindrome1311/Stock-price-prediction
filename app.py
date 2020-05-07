from flask import Flask, render_template
app = Flask(__name__)
import requests
from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer 

import requests
page_link ='https://economictimes.indiatimes.com/markets/stocks'
page_response = requests.get(page_link)
page_content = BeautifulSoup(page_response.content, "html.parser")
et1 = page_content.find(attrs={'data-orefid':'p2146842_3'}).text
et2 = page_content.find(attrs={'data-orefid':'p2146842_4'}).text
et3 = page_content.find(attrs={'data-orefid':'p2146842_5'}).text
#livemint scrape
#page_link ='https://www.livemint.com/market/stock-market-news'
#page_response = requests.get(page_link)
#page_content = BeautifulSoup(page_response.content, "html.parser")
#lm1 = page_content.find(attrs={'id':'listheadline_11581703440744'})
#lm2 = page_content.find(attrs={'id':'listheadline_11581681263375'})
#lm3 = page_content.find(attrs={'id':'listheadline_11581657619914'})

#fb
page_link ='https://finance.yahoo.com/quote/FB?p=FB'
page_response = requests.get(page_link)
page_content = BeautifulSoup(page_response.text, "html.parser")
fb = page_content.find_all('div',attrs={'class':'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text

#alphabet
page_link ='https://finance.yahoo.com/quote/GOOG?p=GOOG&.tsrc=fin-srch'
page_response = requests.get(page_link)
page_content = BeautifulSoup(page_response.text, "html.parser")
google = page_content.find_all('div',attrs={'class':'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text

#amazon
page_link ='https://finance.yahoo.com/quote/AMZN?p=AMZN&.tsrc=fin-srch'
page_response = requests.get(page_link)
page_content = BeautifulSoup(page_response.text, "html.parser")
amzn = page_content.find_all('div',attrs={'class':'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text

#msft
page_link ='https://finance.yahoo.com/quote/MSFT?p=MSFT&.tsrc=fin-srch'
page_response = requests.get(page_link)
page_content = BeautifulSoup(page_response.text, "html.parser")
msft = page_content.find_all('div',attrs={'class':'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text



##ML
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
df=pd.read_csv('Data.csv', encoding = "ISO-8859-1")
train = df[df['Date'] < '20150101']
test = df[df['Date'] > '20141231']
# Removing punctuations
data=train.iloc[:,2:27]
data.replace("[^a-zA-Z]"," ",regex=True, inplace=True)
# Renaming column names for ease of access
list1= [i for i in range(25)]
new_Index=[str(i) for i in list1]
data.columns= new_Index
# Convertng headlines to lower case
for index in new_Index:
    data[index]=data[index].str.lower()
' '.join(str(x) for x in data.iloc[1,0:25])
headlines = []
for row in range(0,len(data.index)):
    headlines.append(' '.join(str(x) for x in data.iloc[row,0:25]))
## implement BAG OF WORDS
countvector=CountVectorizer(ngram_range=(2,2))
traindataset=countvector.fit_transform(headlines)
# implement RandomForest Classifier
randomclassifier=RandomForestClassifier(n_estimators=200,criterion='entropy')
randomclassifier.fit(traindataset,train['Label'])
## Predict for the Test Dataset
test_transform= []
for row in range(0,len(test.index)):
    test_transform.append(' '.join(str(x) for x in test.iloc[row,2:27]))
test_dataset = countvector.transform(test_transform)

#predict

sid_obj = SentimentIntensityAnalyzer() 
sentiment_dict = sid_obj.polarity_scores(et1)
if(sentiment_dict['neg']*100 >15 or sentiment_dict['pos']*100 >15 ):
	if(sentiment_dict['neg']*100 >15):
		et1_pred = 0
		et1_pred = "Stocks will be decreased"
	else:
		et1_pred = 1
		et1_pred = "Stocks will be increased"
else:
    li=['']
    li[0]=et1
    test_dataset = countvector.transform(li)
    et1_pred=randomclassifier.predict(test_dataset)
    if int(et1_pred.flat[0]) ==1:
        et1_pred= "Stocks will be increased"
    else:
        et1_pred="Stocks will be decreased"


sentiment_dict = sid_obj.polarity_scores(et2)
if(sentiment_dict['neg']*100 >15 or sentiment_dict['pos']*100 >15 ):
	if(sentiment_dict['neg']*100 >15):
		et2_pred = 0
		et2_pred = "Stocks will be decreased"
	else:
		et2_pred = 1
		et2_pred = "Stocks will be increased"
else:
    li=['']
    li[0]=et2
    test_dataset = countvector.transform(li)
    et2_pred=randomclassifier.predict(test_dataset)
    if int(et2_pred.flat[0]) ==1:
    	et2_pred= "Stocks will be increased"
    else:
    	et2_pred="Stocks will be decreased"
    
sentiment_dict = sid_obj.polarity_scores(et3)
if(sentiment_dict['neg']*100 >15 or sentiment_dict['pos']*100 >15 ):
	if(sentiment_dict['neg']*100 >15):
		et3_pred = 0
	else:
		et3_pred = 1
else:
    li=['']
    li[0]=et3
    test_dataset = countvector.transform(li)
    et3_pred=randomclassifier.predict(test_dataset)
    if int(et3_pred.flat[0]) ==1:
    	et3_pred= "Stocks will be increased"
    else:
    	et3_pred="Stocks will be decreased"


    
##money control top gainer
page_link ='https://www.moneycontrol.com/stocks/marketstats/index.php'
page_response = requests.get(page_link)
page_content = BeautifulSoup(page_response.text, "html.parser")
top_gainer = page_content.find_all(attrs={'class':'bl_12'})[2].text
top_gainer_current = page_content.find_all(attrs={'class':'b_12'})[2].text
top_loser = page_content.find_all(attrs={'class':'bl_12'})[8].text
top_loser_current = page_content.find_all(attrs={'class':'b_12'})[12].text
top_active_stock = page_content.find_all(attrs={'class':'bl_12'})[26].text
top_active_stock_current = page_content.find_all(attrs={'class':'b_12'})[42].text
price_shocker=page_content.find_all(attrs={'class':'bl_12'})[51].text
price_shocker_current = page_content.find_all(attrs={'class':'b_12'})[77].text



@app.route('/')
def hello_world():
    return render_template('index.html',et1=et1,et2=et2,et3=et3,google=google,facebook=fb,amazon=amzn,microsoft=msft,et1_pred=et1_pred,et2_pred=et2_pred,et3_pred=et3_pred,top_gainer=top_gainer,top_gainer_current=top_gainer_current,top_loser=top_loser,top_loser_current=top_loser_current,top_active_stock=top_active_stock,top_active_stock_current=top_active_stock_current,price_shocker=price_shocker,price_shocker_current=price_shocker_current)
if __name__=='__main__':
	app.run(debug=True)
