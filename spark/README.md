# Stack Overflow Analysis with Spark

In this folder, I perform the analysis on the stack overflow posts using the pyspark framework. The `stack_overflow.ipynb` notebook is the main file contains all the explanation. All the test work was done inside the [notebook](https://nbviewer.jupyter.org/github/camalot2011/showcases/blob/master/spark/stack_overflow.ipynb).

There are also one utility scripts `myutils.py` and three python scripts. Those were used to submit jobs to the Google Cloud Platform. The command lines were all inside the python notebook mentioned above.

Some key findings are:
- the ratio of upvote increases with the favorite counts
- The average answer ratio for high reputation users (99 highest) is **0.92776** vs **0.19994** (on average)
- Users with higher reputation make more posts regardless of answers or questions
- Questions asked between 10:00 and 20:00 have higher ratio of getting answered within 3 hours
- Veterans have much bettern first question metrics than the ones from the brief users
- A `Word2Vec` model and a **classification** model for the tags of the posts
