# Get mutual fund data from Tangerine website
from selenium import webdriver
import pandas as pd
import datetime
import matplotlib.pyplot as plt


# scrape data from website
url='https://www.tangerine.ca/en/products/investing/performance/'
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument("--headless")
# chromeOptions.add_argument("--remote-debugging-port=9222")
chromeOptions.add_argument('--no-sandbox')
browser = webdriver.Chrome(executable_path='chromedriver.exe',options=chromeOptions)
browser.get(url)
nav = browser.find_element_by_id("nav-history")
table=nav.text

# turn text into df
rows=table.split('\n')
elements=[]
for r in rows[1:]:
    elements.append(r.split(' '))
df=pd.DataFrame(elements)
df.columns=['Month','Day','Year','Balanced Income','Balanced','Balanced Growth','Dividen','Equity Growth']

# data cleasing
current_year=datetime.datetime.now().year
df_use=df.loc[df.Year.astype(int)>=current_year,:].copy()
df_use['date']=pd.to_datetime(df_use.Year+' '+df_use.Month+' '+df_use.Day.str[:-1],format='%Y %B %d')
df_use.Balanced=df_use.Balanced.str[1:].astype(float)
df_use['Equity Growth']=df_use['Equity Growth'].str[1:].astype(float)
df_use['Balanced Income']=df_use['Balanced Income'].str[1:].astype(float)
df_use['Balanced Growth']=df_use['Balanced Growth'].str[1:].astype(float)
df_use['Dividen']=df_use['Dividen'].str[1:].astype(float)

# data visualization
plt.style.use('seaborn-colorblind')
fig, ax = plt.subplots(figsize=(10,5))
ax.plot(df_use.date,df_use.Balanced,color='blue',label='Balanced')
ax.plot(df_use.date,df_use['Equity Growth'],color='green',label='Equity Growth')
ax.plot(df_use.date,df_use['Balanced Income'],color='black',label='Balanced Income')
ax.plot(df_use.date,df_use['Balanced Growth'],color='yellow',label='Balanced Growth')
ax.plot(df_use.date,df_use['Dividen'],color='pink',label='Dividen')

ax.set_title('Tangerine 5 Mutual Funds')
legend = ax.legend(loc='best', shadow=False)
# Put a nicer background color on the legend.
legend.get_frame().set_facecolor('C0')

plt.show()
