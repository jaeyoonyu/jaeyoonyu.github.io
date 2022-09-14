---
layout: page
title: "Python Code - Basic"
---

Python is a powerful tool for **accounting research** and **data analytics**. 
On this webpage, I share some python code **snippets that I use often (and I forget)**. The snippets are mainly relevant to the following topics: 
* Data wrangling;
* Visualization;
* Regular expression;
* Textual analysis;
* Web-scraping.
<br/>


---
All code files are stored <a href="https://github.com/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code" target="_blank">here</a>. Check anything you're interested in:

* **Python functions.**
    * [zip()](https://nbviewer.org/github/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code/function-zip.ipynb): useful when turning (a1,a2,..), (b1,b2..),... into ((a1,b1), (a2, b2),..). <br/>
    * [map()](https://nbviewer.org/github/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code/function-map.ipynb): useful when executing a function for multiple iterable objects.<br/>

* **Pandas.**
    * [agg()](https://nbviewer.org/github/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code/pandas-method-agg.ipynb): useful when aggregating variables by groups. <br/>
    * [apply()](https://nbviewer.org/github/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code/pandas-method-apply.ipynb): useful when executing a function for multiple columns. <br/>
    * [crosstab()](https://nbviewer.org/github/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code/pandas-method-crosstab.ipynb): useful when preparing frequency table. <br/>
    * [cut()](https://nbviewer.org/github/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code/pandas-method-cut.ipynb): useful when segmenting and sorting data values into bins. Notably, **bin widths don't have to be the same**. <br/>
    * fillna(): (coming soon). <br/>
    * [groupby()](https://nbviewer.org/github/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code/pandas-method-groupby.ipynb). <br/>
    * [melt()](https://nbviewer.org/github/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code/pandas-method-melt.ipynb): wide-form to long-form. <br/>
    * [options and settings](https://nbviewer.org/github/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code/pandas-options.ipynb): e.g., the maximum columns and rows to display.
    * pivot (coming soon).
    * [pivot_table()](https://nbviewer.org/github/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code/pandas-method-pivot_table.ipynb): useful when preparing frequency table. <br/>
    * [sidetable](https://nbviewer.org/github/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code/sidetable.ipynb): useful when displaying cumulative distributions.
    * [value_counts()](https://nbviewer.org/github/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code/pandas-method-crosstab.ipynb): useful when preparing frequency table. <br/>
    * zfill(): (coming soon).
    * [Reshaping: imbalanced to balanced panel](https://nbviewer.org/github/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code/imbalanced-to-balanced-df.ipynb).<br/>
    


* [FinanceDataReader](https://nbviewer.org/github/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code/intro-FinanceDataReader.ipynb): to download historical stock return data of US firms, etc.

* **SQL in Python (sqlite3).**
    * [Introduction to SQL: Part I.](https://nbviewer.org/github/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code/intro-to-sql-part1.ipynb)<br/>
    * [Introduction to SQL: Part II.](https://nbviewer.org/github/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code/intro-to-sql-part2.ipynb)<br/>

* **Regular expression (regex)** - coming soon.    

* **geopandas** - coming soon.    

* **Webscraping.**
    * pandas.read_html().
        * [Industry list (SIC) from SEC.](https://nbviewer.org/github/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code/sec-sic-classification.ipynb)<br/>
        * [Dow Jones 30 from Wikipedia.](https://nbviewer.org/github/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code/DJ30.ipynb)<br/>
        * [S&P500 from Wikipedia.](https://raw.githack.com/jaeyoonyu/jaeyoonyu.github.io/main/_code/SP500.html)<br/>
        * [S&P1500 from Wikipedia.](https://raw.githack.com/jaeyoonyu/jaeyoonyu.github.io/main/_code/SP1500.html)<br/>        
        * [Russell1000 from Wikipedia.](https://raw.githack.com/jaeyoonyu/jaeyoonyu.github.io/main/_code/Russell1000.html)<br/>        
     * requests (coming soon).
     * beautifulsoup (coming soon).
     * selenium (coming soon).
     
* **Visualization.**
    * barplot() (coming soon).
    * countplot() (coming soon).
    * [lineplot().](https://nbviewer.org/github/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code/visual-lineplot.ipynb)
    * [areaplot().](https://nbviewer.org/github/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code/visual-areaplot.ipynb)
    * [jointplot().](https://nbviewer.org/github/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code/visual-jointplot.ipynb)
    * [regplot().](https://nbviewer.org/github/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code/visual-regplot.ipynb)
    * [lmplot().](https://nbviewer.org/github/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code/visual-lmplot.ipynb)
    * [heatmaplot(), useful for correlation table.](https://nbviewer.org/github/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code/visual-heatmap.ipynb)
