# Stock Picking Web App

I have define an algorithm to look for the stock price signal pattern. The folder contains a `Stock_checking.Rmd` file with the codes in R and a subfolder including the scripts for the shiny webapp `Server` and `User interface`. To view the web app, please click [HERE](https://camalot2011.shinyapps.io/Stockapp/) .


Parameter explanations:
- end data: choose the **last day** of the market value you want to look at
- fluctuation range: choose the amount of price variation in the **flat region** of the signal
- drop ratio: choose the ratio of price drop before the **flat region**
- days for price drop: control the length of the **flat region**
- symbol of interest: input the symbols **within** the picked stock symbols
- data freq: choose between 'daily' and 'weekly'
- date range: choose the date range for viewing the ticker price signal