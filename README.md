# Portfolio_Optimization_Medium
A code that helps you run scenarios to assess which stock create the best portfolio at minimum risk and maximum return with past information.
---

If you don't have any Idea how to create a stock portfolio, this will help you.
Big disclosure, I'm not any financial advice. 
This is an exercise on how to create a portfolio testing 10,000 combination of stocks, and finding if there was one combination that has:
Better Returns than the Market
Has the Same or lower Risk

For this we need 
Market Benchmark: We need to define what we will consider as our market benchmark. This will be the financial asset we will compare returns and risk against our portfolio. 
Portfolio of Stocks: we will use any list of stocks, commodities, etc. In my case, I will use some random stocks that I know. Again, this list is no financial advice. (I promise this is the last "warning" over this😅)

Let's start our journey.
Tools to use
We will be working with Python and the following packages:

Packages used for this projectAlso we need a function called download you can check the link of the website from Analyzing Alpha. 

Step 1: Setting Up our Variables
Now we need to set some key variables. 
Benchmark: in this case S&P 500 that is represented by "^GSPC"
Portfolio: List of stocks we're analyzing.
Start Date: When do we want to start analyzing the data
End Date: When do we want to finish analyzing the data
Number of Scenarios: How many random combinations we want to test. 
Output Lists: We need a place to store our Return, Risk, and Portfolios Distribution (Combinations). 

Technical disclaimer: All this exercise can be done with functions or classes, it's a WIPStep 2: Downloading and Cleaning the Data
We will download all the financial data from our benchmark (df) and portfolio (df2) from the start to end date.
After downloading the data, we need to drop all empty values. I did it this way for simplicity, but you could have a different approach if you want.

Step 3: Analyzing our Market Benchmark
Now with our clean data we select the variable we want. To familiarize yourself with the data, let me show you what download function recovers from any stock:
In this case we will be using "Close" which is the last price traded of this stock at the end of a day.
Now we procede to select the information, calculate our daily returns and add the Benchmark Return and Risk to our lists:

The daily returns are the variation of the Close price between two days. 
Step 4: Analyze our Portfolio Data
We follow the same procedure as the previous step but with 2 extras.
We need to create a loop/sequence that will do this exercise 10,000 times.
We need to create a random distribution for generating each portfolio and making it unique.

You can do this with the following code:

Step 5: Select the Best Portfolio
The criterion for the best portfolio is to have the minimum risk, meaning that the stock is at least as volatile as the market. For understanding the risk we've being using the Standard Deviation. I leave you a link to Investopedia that can help.
And once we have calculated this "minimum risk" we will find the highest return possible. This way we are finding a porfolio that in the past has performed better than the market.
Step 6: Let's do some visuals
We're going to plot the risk on the x-axis and the return on the y-axis
In this next image, you can see the market performing (red dot) and then the maximum return at the minimum risk. Meaning that if you would've held that portfolio between start and end date, you would've had a better portfolio than the market benchmark.
This graph will depend to the stocks that you want to analyze. For example if we choose only Apple, Google and Amazon Stocks, our exercise looks like this:
Where the stocks we selected had higher returns (y-axis) but also higher risk (x-axis)

---

As mentioned, this is not a tool to start your analysis on the portfolio you want to build, and is only showing what happened in the past, not trying to find what is happening in the future.
The optimization power of a simple code is what really amazed me while going through this exercise, because we can map and evaluate complex decisions in a brief period.
