# Baby Names Analysis with Spark and SQL

Baby names were downloaded from social security website and analyzed with the Spark / SQL plus time series analysis inside the python notebook `babynames.ipynb`. The notebook can be viewed [HERE](https://nbviewer.jupyter.org/github/camalot2011/showcases/blob/master/babynames_SP/babynames.ipynb).

Some key findings:
- Baby dataset contains 51 comma separated text file corresponding to each states. No missing data or capital letter mishandling are found.

- Mary is the all time favorite girls' name while James is for boys.

- The most ambiguous name taking into consideration of popularity in 2013 is Charlie. In 1945, that is Leslie.

- Tyler has the largest percentage increase (although dropped in recent year) since 1980. Jennifer has the largest percentage decrease at the same period.

- Mary, Shirley, Helen had even larger decrease in popularity than Jennifer before 1980. There were 39 names having larger increase in popularity than Tyler before 1980.

- Time series analysis on the name counts in the whole nation shows three baby booms in consistent with the American history.

- Base line of the population is fitted with exponential model.

- The residuals from the exponential model show no rigid periodicity. Residuals have autocorrelation up to 15 years.

- The residuals are fitted with the moving average to predict 1 year ahead of time. Forward chaining cross validation is used to train the model. The combined model provides decent population estimation in recent years.
