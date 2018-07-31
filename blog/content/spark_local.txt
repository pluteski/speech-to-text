


This is an interesting question. I was curious about this myself, when I chanced into the opportunity to investigate it first hand.

I found that there actually are benefits to writing an application using Spark even when ran in standalone mode, i.e. single node cluster.

Recently, I had just finished rewriting a machine learning application that was originally written using Numpy, Scikit-learn and multiprocessing. The rewrite used the latest version of Spark, pyspark and spark.ml.

By the time I completed the rewrite, I couldn’t immediately run it on a cluster, because I wasn’t yet ready to upgrade our Spark cluster to the latest version of Spark. Rather than waiting I ran the Spark application on a production server using standalone mode.

Here’s what I learned.

Even though pyspark’s spark.ml is similar to scikit-learn, and in places almost identical syntactically, the original application needed to be rewritten completely from the ground up - very little of the original code survived in the final Spark application.
Spark encourages one to remain within a more strictly functional style. Parts of the original code that were written in a procedural style were much slower than the same portion of code rewritten to utilize Spark dataframes.
The ease of use of Python with the performance of Java.
Reading from and writing to file alone are worth the price of admission. I found dealing with file input and output generally to be easier in Spark, especially S3 (AWS). Parquet is much more compact than pickled data. I measured the file sizes of my pickled trained models and training data — and they were much much smaller in parquet.
It only took me only about an hour to deploy the Spark application from my laptop to the production server, from the time I began to download the Spark source to the Ubuntu server, build, and configure; to when I had the application running on the full dataset and writing out results to the backend servers. Spark standalone on Ubuntu behaves exactly the same as does on Mac OS.
Running on the very same server as the original application, the Spark version was able to load more training examples into memory.
Running on the very same server as the original application, the Spark version was able to finish the task in less time.
Debugging is more of a challenge with Spark. Because of lazy evaluation the actual issue might be far upstream of where the exception occurs. Memory issues are of course more of a challenge.
Subjectively, I prefer working in Spark to python. Python is already pretty pleasant to work in compared to other languages (I’m looking at you Java); Spark takes pleasantville to a whole new level for me. I personally find Spark’s dataframes easier to work with than Panda’s.
Spark provides the means to use sql not just for querying an external database but for simplifying your program logic.
The Spark web UI helps greatly in tuning as well as for general insights. I found that it was easier to use the visualizations in standalone mode than when running on a cluster, because I can pause the application in standalone and peruse the visualizations at my leisure.
It would likely require more effort up front to write a new application using Spark instead of Python. That said, having had my experience, I would actually consider doing just that even if I planned to run it only in standalone mode. And then there’s the knowledge of whenever you need it, the scale-out is there waiting for you.