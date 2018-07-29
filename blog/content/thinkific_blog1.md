Title:  How to showcase your Apache Spark skills
Subtitle:    Selecting good code projects
Project:     Learn Apache Spark
Author:      Mark Plutowski
Affiliation: Plutoware Delimited
Web:         https://pluteski.github.io
Date:        2018-07-29



<p align="center">
<img src="https://github.com/pluteski/speech-to-text/blob/master/blog/content/images/spark/L4.UI.DAG.png" alt="Spark UI DAG" width="300px"/>
<br>
<b>Figure 0</b>
</p>

# How to spotlight Apache Spark skills 
How do you prove your capability as a Apache Spark data scientist when you don’t have much to show? Perhaps this is because you don’t have much experience.  Perhaps it is because the work you do does not lend itself to being shown to others.  You may have done impressive work, but have nothing to show for it because most developers work for companies that don’t publish their code as open source. 

I am going to give you some tips for bringing your skills out of the dark 
and into the light. 

## Publish your work
Publishing a code project is a great way to introduce yourself to an interviewer. This also provides them with ample talking points for various styles of interview questions.  Doing this makes the interviewers job easier. 
By doing so you are giving them context on what you already know, and providing talking points for interview questions. 
Interviewers in the software industry are often stretched thin; making their job easier puts them into a better mood while also demonstrating your preparedness. 

This can be helpful for many types of interview questions, including behavioral questions, situational questions, coding challenges, and system design challenges. 

As an example, take [this python repo](https://github.com/pluteski/first2017mp) I published on github.
I developed this during my role as a mentor for a robotics team.  
The repo uses [the readme](https://github.com/pluteski/first2017mp/blob/master/README.md) to explain the project at a high level manner while also 
giving a developer a quick start guide. 
Often overlooked, [the repo wiki](https://github.com/pluteski/first2017mp/wiki)
is a great way to elaborate further in breadth as well as depth.

The wiki is a great place to provide visuals that allow readers to quickly get a sense of what your project does. 
[Figure 1](https://github.com/pluteski/first2017mp/raw/master/images/stage3_paths_ne.png) 
and [Figure 2](https://github.com/pluteski/first2017mp/raw/master/images/stage2_fleur_de_lis.png) 
are two of the most visually appealing visualizations that give the reader an idea at a glance of what is being done and how, and draw the reader in to learn more.

<p align="center">
<img src="https://github.com/pluteski/first2017mp/raw/master/images/stage2_fleur_de_lis.png" alt="Fleur-de-lis search pattern (copyright Mark E Plutowski)" width="300px"/>
<br>
<b>Figure 1</b>
</p>

<p align="center">
<img src="https://github.com/pluteski/first2017mp/raw/master/images/stage3_paths_ne.png" alt="Sample trajectories (copyright Mark E Plutowski)" width="400px"/>
<br>
<b>Figure 2</b>
</p>


## Show what you know
In this article I will show you how you can showcase your skills. By doing so, you will also learn new relevant skills along the way.  I’ll show you how publishing your work using self-explanatory visualizations can separate your from the pack.  I’ll also show how to select a coding project that demonstrates useful skills that are immediately applicable in a production setting.  Furthermore, by setting this up for yourself, you will also acquire new skills that are valuable for the coding challenge portion of the interview, as well as being directly transferable to the job itself.

## Know what you show
To utilize this approach effectively, you must be intimately familiar with every line of content in your repo. The best way to achieve this is to create an original work of your own design, developed step by step from start to finish by yourself. Once you get started this may not take as long as you expect. On the other hand, there may be steps that blossom into much more time-intensive investment than you expected.  That's actually ok -- it gives you something interesting to explain when discussing your process. 

## Hone your edge, gain a new one
Someone who has well organized and nontrivial open source code will be prioritised over other similarly experienced candidates, but because their competencies are easier to evaluate.  By providing visibility you simplify the job of the recruiters and interviewers, while simultaneously preparing yourself for the interview, as well as learning relevant skills that will be useful on the job.



Source: https://github.com/pluteski/first2017mp/raw/master/images/stage2_fleur_de_lis.png 

Figure 1. Fleur-de-lis search pattern used by an algorithm that I developed. Not only does it illustrate a key step, it is also an interesting visualization. 


Source : https://github.com/pluteski/first2017mp/raw/master/images/stage3_paths_ne.png 

Figure 2 : sample trajectories found by the planner

You can use the readme page or the wiki home page as a starting point to link to other pages that delve further into background knowledge you needed to provide context for what you were trying to accomplish and why your approach is sensible. 

For example, this Background page of this repo gives a brief primer in the section on Alternative Approaches. The next sections explain the why, what, and how of the project. This gives an interviewer ample opportunity to explore your breadth of understanding of a field of interest. 

The Related Approaches page of the repo gives a brief primer into specific techniques that were considered, which one was selected, and why. This gives an interviewer opportunity to explore your depth of understanding of specific techniques. 

The Planning Stages page of the repo gives an overview of what the code actually does.  It gives links to python notebooks containing visualizations, such as this sample trajectories notebook. This allows an interviewer to review your code and see how it behaves on actual data. Note the use of visualizations.  

The test page of the repo showcases data from tests designed to simulate the code under realistic conditions and demonstrate its use of compute resources. This type of presentation demonstrates a data-driven mindset. 

You wouldn’t necessarily need all of these pages.  This serves to illustrate the various types of information that may can be shown, and which are useful for showcasing your competencies.

Using these assets an interviewer could explore multiple aspects of your skill as a developer, such as your ability to  

* Decompose a novel problem
* Design a system
* Set up a new code repository
* Organize a code repository
* Write performant code
* Visualize key results
* Communicate complex ideas 
* Write effective documentation

Providing these assets gives the interviewer opportunity to derive behavioral questions. It gives you ample content you can use to answer those behavioral questions. You can tell about a time you encountered a certain type of situation, and how you approached it, and refer to the published solution. Use the STAR technique, by describing the situation (S), distilling it down to a single task (T), and the key action (A) you used to solve it, concluding with the result (R ). 

It also provides code screeners example code that can be used as a starting point for more in depth exploration of your skills. Instead of selecting a random problem, they may choose a coding challenge that is within your wheelhouse. 

## Showcasing your repo

Getting off and running is greatly simplified by reviewing other code repos. Review code repositories relevant to your own goals and learn how to distinguish effective ones from half-baked ones. Pick one or two to serve as a role model for your own design, and then make it your own.

## Ideas for a coding project 
Many new developers make the mistake of picking code projects similar to what they encountered in the education system. These are frequently not relevant to what is relevant to a real-world job as a commercial software developer. Interviewers want to see that you can learn quickly, but also that you are familiar with heterogeneous aspects of a development task, are able to handle complexity, have an attention to detail that is not taught in the university environment, and know how to handle the messiness of real-world data. 

Your mission is to showcase your ability to apply Apache Spark to a nontrivial dataset. As a general rule of thumb -- if you didn’t need to perform any data cleansing or preprocessing on the dataset, the data wasn’t messy enough to be realistic.  If your solution ran in a few seconds it was not challenging enough to test your algorithms. If it didn’t exhaust at least half of the memory available to your system and run the fan to cool off the cpu, then you probably could increase the complexity of the task, either by tackling a larger dataset, or by taking on a more challenging problem based on the dataset.

The key to choosing a code project to show in your portfolio is 

* Indicating that this is an original creation of your own making,
* Demonstrating competencies relevant to your target role, and
* Showing that you understand the priorities of real world application.

**Here are some ideas for code projects.**

## Migrate an existing solution to Spark 
In this case, there might already be an existing solution for solving a problem.  Your mission is to migrate the solution to Apache Spark and compare the results. Many such datasets and associated solution exist online. You would be welcome to try your hand at one of mine, the FIRST robotics motion planner problem. 

## Use Spark to analyze a nontrivial data set
By nontrivial here I mean something that takes more than a few seconds to process.  If the data set does not push the compute resources of your development environment you might use an inefficient solution instead of a performant one.  If you use a nontrivial dataset you can showcase the difference between an inefficient algorithm and a performant algorithm.  It also makes the results more interesting, and gives you more to talk about. 

My Apache Spark SQL course on Thinkific showcases a code project based around a 6.5 MiB dataset containing 1,095,695 words, 128,467 lines, and 41,762 distinct words.  The analyses it uses are especially customized for this dataset -- the analyses you choose for the dataset of your choice also indicate your ability to pose interesting questions, create queries for answering those questions, and efficiently implementing those queries on a large dataset. 

## Compare Spark with an alternative computing platform
In this approach, you select a data set, perform an analysis of it using two different programming languages or computing platforms. For example you might first ue scikit-learn, numpy, or pandas, and then do the same analysis using Apache Spark.  Or, you might compare and contrast Hive vs Spark. 

I had performed a similar exercise myself (2016). A couple years later, Databricks published the results of a similar study on their blog, Benchmarking Apache Spark on a Single Node Machine - The Databricks Blog. 
Use Spark along with a cloud api 
Cloud apis provide powerful means of handling large datasets for certain applications; however, preparing the data for upload to the cloud api may require substantial preprocessing. Cloud apis can also generate a lot of log data.  For example, I  evaluated IBM Watson and the Google Cloud speech-to-text cloud apis, and then compared the results (cf., on bleu scores and transcription rates, and on transcription rate for noisy recordings) by analyzing the log data.  In this case, I used sqlite to run the queries. When I redo this I plan to use Spark SQL instead. 

This type of project gives you even more to talk about: how to integrate Spark with a cloud api, what operations are suitable for Spark and which ones are more suitable to do within the cloud api, what post-processing analytics steps are there for which Spark is especially suitable.  Provide visuals where meaningful, e.g. Figure 5.  Your wiki can also show resource consumption by screenshotting the Spark UI, such as shown in Figure 0.



Source: https://learn-apache-spark.thinkific.com/courses/spark-sql 

Figure 3. Frequent 5-tuple analysis on The Collected Works of Sherlock Holmes corpus


## Use Spark to extract training features from a data set
Many data science jobs require the ability to train statistical models based on feature data gleaned from raw data. There is an abundance of data that you could use to demonstrate your ability to perform this. 

My Apache Spark SQL course shows how to extract moving-window n-tuples from a text corpus. Figure 4 illustrates this for 4-tuples, though it is easily generalizable to arbitrary length n-tuples. This would provide a good starting point for a feature extractor that vectorizes this into a form that can be provided as input to a neural network model. 

**Examples of modeling tasks**
* Statistically improbable phrases
* Anomaly detection 
* Topic modeling
* Recommender
* Trend analysis

**Examples of relevant models**
* Approximate K Nearest Neighbors
* Alternating Least Squares
* K-means clustering
* Streaming

If you can generate features for one of these types of models or tasks start-to-finish end-to-end, you are probably able to handle other modeling tasks.




Source: https://learn-apache-spark.thinkific.com/courses/spark-sql 

Figure 4. Moving n-tuple features from The Collected Works of Sherlock Holmes corpus



Source: https://github.com/pluteski/speech-to-text/blob/master/images/bleu_score_deciles.png?raw=true

Figure 5. Bleu score analysis comparing speech-to-text cloud apis


# Conclusion
There are many ways to learn Apache Spark and apply it realistically to nontrivial datasets; however, when it comes to interviewing it still comes down to communicating your understanding effectively.  You can accomplish much of this up-front in advance, while sharpening your skills, by tackling a code project, publishing it, and writing up key results in a  visually appealing way.  

To learn more and see additional tips and project ideas, see my insanely low-priced online courseware : Learn Apache Spark.



<-- call the Markdown Preview command via the Command Palette: 
control+shift+p to call up the Command Palette, 
type "Preview", 
select "Markdown Preview: Python Markdown: Preview in Browser", and 
hit enter 

option-CMD-O

-->
