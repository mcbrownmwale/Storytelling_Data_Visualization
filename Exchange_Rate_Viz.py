#!/usr/bin/env python
# coding: utf-8

# # Storytelling Data Visualization on Exchange Rate


##### Importing the necessary Libraries ######

# Import Pandas and Numpy for Data Analysis and Wrangling
import pandas as pd
import numpy as np

# Import Searborn and Matplotlib for Data Visualisation
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.style as style  # - Set visualisation style
style.use('bmh')


### Read in the Dataset and Inspect the Dataset
exchange_rates = pd.read_csv('euro-daily-hist_1999_2020.csv')
print("The basic structure of the dataset:", exchange_rates.info(), sep = '\n\n')


### Display the five records of the Dataset
print("The first five rows of the dataset:", exchange_rates.head(), sep = '\n\n')


### Display the last five records of the Dataset
print("The last five rows of the dataset:", exchange_rates.tail(), sep = '\n\n')

### Data Cleaning ###

# 1. Renaming Columns
new_column_names = []
for column_name in exchange_rates.columns:
    column_name = column_name.replace('[', '')
    column_name = column_name.replace(' ]', '')
    column_name = column_name.replace(' ', '_')
    column_name = column_name.lower()
    new_column_names.append(column_name)
exchange_rates.columns = new_column_names
exchange_rates.rename(columns={'period\\unit:': 'time'}, inplace = True)
# - Display the cleaned columns
print("A list of cleaned columns:", exchange_rates.columns, sep = '\n\n')


# 2. Dropping Unnecessary Columns and Change the Datatype of 'time' column
exchange_rates['time'] = pd.to_datetime(exchange_rates['time'])
euro_to_dollar = exchange_rates[['time', 'us_dollar']]
print("Data Structere for the remaining columns:", euro_to_dollar.info(), sep = '\n\n')

# 3. Sorting Records
euro_to_dollar = euro_to_dollar.sort_values(['time'])
print("Sorted Records:", euro_to_dollar.head(), sep = '\n\n')

# 4. Clean `us_dollar` column and change its datatype
euro_to_dollar['us_dollar'] = euro_to_dollar[euro_to_dollar['us_dollar'] != '-']['us_dollar'].astype('float')
euro_to_dollar.reset_index(drop = True, inplace = True)
euro_to_dollar.dropna(inplace = True)
print("Basic Information for the cleaned dataset:", euro_to_dollar.info(), sep = '\n\n')

# Rolling Mean
euro_to_dollar['rolling_mean'] = euro_to_dollar['us_dollar'].rolling(30).mean()
print("The first five records for the cleaned dataset:", euro_to_dollar.head(), sep = '\n\n')


##### PLOT THE CHART ######

# Initialise a figure
fig = plt.figure(figsize = (10, 6))

# Define subplots
ax1 = plt.subplot(2, 3, 1)
ax2 = plt.subplot(2, 3, 2)
ax3 = plt.subplot(2, 3, 3)
ax4 = plt.subplot(2, 3, (4,6))
axes = [ax1, ax2, ax3, ax4]

# Plot a number line in each subplot
for ax in axes:
    ax.plot(euro_to_dollar['time'], euro_to_dollar['rolling_mean'], color = 'gray', alpha = 0.5, lw = 0.7)
    ax.grid(False)

# George W. Bush (2001 - 2009)
bush_time = euro_to_dollar[(euro_to_dollar['time'].dt.year >= 1999) & (euro_to_dollar['time'].dt.year < 2009)]
ax1.plot(bush_time['time'], bush_time['rolling_mean'], color = 'blue', lw = 1)
ax1.set_title('George Bush (2000 - 2008)', fontdict = {'size':12, 'weight': 'bold', 'color': 'blue'})
ax1.axvline(pd.to_datetime('2009-01-01'), lw = 0.5 , color = 'black', alpha = 0.5)
ax1.set_yticks([0.8, 1.0, 1.2, 1.4, 1.6])
ax1.set_xticks([pd.to_datetime('2000-01-01'), pd.to_datetime('2009-01-01'),
                pd.to_datetime('2017-01-01'), pd.to_datetime('2021-01-01')],
              ['2000', '2009', '2017', '2021'])
ax1.tick_params(labelbottom = False, labeltop = True, bottom = False, top = True, labelcolor = 'gray')

# Barrack Obama (2009 - 2017)
obama_time = euro_to_dollar[(euro_to_dollar['time'].dt.year >= 2009) & (euro_to_dollar['time'].dt.year < 2017)]
ax2.plot(obama_time['time'], obama_time['rolling_mean'], color = 'g', lw = 1)
ax2.set_title('Barrack Obama (2009 - 2016)', fontdict = {'size':12, 'weight': 'bold', 'color': 'g'})
ax2.axvline(pd.to_datetime('2009-01-01'), lw = 0.5 , color = 'black', alpha = 0.5)
ax2.axvline(pd.to_datetime('2017-01-01'), lw = 0.5 , color = 'black', alpha = 0.5)
ax2.set_xticks([pd.to_datetime('2000-01-01'), pd.to_datetime('2009-01-01'),
                pd.to_datetime('2017-01-01'), pd.to_datetime('2021-01-01')],
              ['2000', '2009', '2017', '2021'])
ax2.tick_params(labelbottom = False, labeltop = True, bottom = False, top = True, labelcolor = 'gray')
ax2.set_yticks([])

# Donald J. Trump (2017 - 2021)
trump_time = euro_to_dollar[(euro_to_dollar['time'].dt.year >= 2017) & (euro_to_dollar['time'].dt.year < 2021)]
ax3.plot(trump_time['time'], trump_time['rolling_mean'], color = 'orange', lw = 1)
ax3.set_yticks([])
ax3.set_title('Donald Trump (2017 - 2020)', fontdict = {'size':12, 'weight': 'bold', 'color': 'orange'})
ax3.axvline(pd.to_datetime('2017-01-01'), lw = 0.5 , color = 'black', alpha = 0.5)
ax3.set_xticks([pd.to_datetime('2000-01-01'), pd.to_datetime('2009-01-01'),
                pd.to_datetime('2017-01-01'), pd.to_datetime('2021-01-01')],
              ['2000', '2009', '2017', '2021'])
ax3.tick_params(labelbottom = False, labeltop = True, bottom = False, top = True, labelcolor = 'gray')

# All presidency
ax4.plot(bush_time['time'], bush_time['rolling_mean'], color = 'blue', label = 'Bush')
ax4.plot(obama_time['time'], obama_time['rolling_mean'], color = 'g', label = 'Obama')
ax4.plot(trump_time['time'], trump_time['rolling_mean'], color = 'orange', label = 'Trump')
ax4.legend()
ax4.set_xticks([pd.to_datetime('2000-01-01'), pd.to_datetime('2005-01-01'), pd.to_datetime('2009-01-01'),
                pd.to_datetime('2013-01-01'), pd.to_datetime('2017-01-01'), pd.to_datetime('2021-01-01')],
              ['2000', '2005', '2009', '2013', '2017', '2021'])
ax4.set_yticks([0.8, 1.0, 1.2, 1.4, 1.6])
ax4.tick_params(labelcolor = 'gray')

plt.tight_layout(pad = 0)
plt.text(x = 10280, y = 2.62, s = 'EURO-USD Exchange Rates Under the Presidency of George W. Bush, Barrack Obama and the First Term of Donald Trump',
            fontdict = {'weight':'semibold', 'size': '10', 'color': 'white'}, backgroundcolor = 'gray')

plt.text(x = 10300, y = 0.65, s = '©MCBROWN WILFRED MWALE'+' '*141 + 'KASIWA ACADEMY', backgroundcolor = 'gray', color = 'white')
plt.savefig('euro_usd_exchange_rates.png', bbox_inches = 'tight')

plt.show()

