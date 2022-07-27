---
layout: page
title: "Python Code - Applications"
---
Python is a strong tool for accounting research and data analytics. Using databases for accounting research, I share python codes that cover <br> 
* how to get data from WRDS;<br>
* how to handle data using Pandas;<br>
* how to prepare distributions;<br>
* how to visualize data, either static or dynamic.<br>

---

All code files are stored <a href="https://github.com/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code" target="_blank">here</a>. Check anything you're interested in:

* [How to get access to WRDS in Python.](https://nbviewer.org/github/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code/wrds-intro.ipynb)<br/>
* Download data from WRDS: [Compustat ](https://nbviewer.org/github/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code/wrds-download-compustat.ipynb); Audit Analytics ([Audit Opinions](https://nbviewer.org/github/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code/wrds-download-compustat.ipynb); [CAMs](https://nbviewer.org/github/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code/wrds-download-AuditAnalytics-CAM.ipynb); [IPOs](https://nbviewer.org/github/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code/wrds-download-AuditAnalytics-ipo.ipynb); [SOX404](https://nbviewer.org/github/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code/wrds-download-AuditAnalytics-sox404)).<br/>
* Can we get <b>IPO years from Compustat</b>? Yes we can. Check [the distribution of IPO years.](https://nbviewer.org/github/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code/Compustat-ipodate.ipynb)<br/>
* Yearly distribution of <b>loss firms</b>: More than half are loss firms in 2020.<br>
    * [Version 1. Using matplotlib after aggregating data method](https://nbviewer.org/github/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code/compustat-loss-firm-distribution-v1.ipynb) <br>
    * [Version 2. Using seaborn and raw data method](https://nbviewer.org/github/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code/compustat-loss-firm-distribution-v2.ipynb) <br>
* [SEC filing distribution](https://nbviewer.org/github/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code/SEC_filings_dist.ipynb) provided by SEC EDGAR.<br/>
* Does the <b>earning kink at zero</b> still exist? Maybe not any more. [Check the distribution.](https://nbviewer.org/github/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code/is-there-kink-around-zero.ipynb)<br/>
* <b>Seaborn</b> allows to visualize data with multiple dimensions: [scatterplot of firm size, profitability, and auditor size.](https://nbviewer.org/github/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code/sctterplot-ROA-size-Big4.ipynb)<br/>
* <b>Plotly</b>, allowing us to identify outliers visually: [Scatter plot of ROA-leverage.](https://rawcdn.githack.com/jaeyoonyu/blog-posting/6bfcbbd164951cd69941ee2a33b779f5d519c769/plotly-hovering.html)<br/>
* <b>Plotly for animated visualization</b><br>
    * Bubble plot for [auditors' client distribution](https://nbviewer.org/github/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code/audit-analytics-client-distribution.ipynb).<br/>
    * Bubble plot for [asset, sales, and market value](https://nbviewer.org/github/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code/compustat-bubble-plot-animation.ipynb).
    
    
    



---
<h1>Examples of interactive plots</h1> 
<h3> Example 1. How many clients for each audit firm? 
{% include client-dist-figure.html %}

<br>
<br>
<h3> Example 2. Scatter plots
{% include dynamic-scatter-mv-at.html %}


<!-- To render HTML and get a link:
https://raw.githack.com/
-->

<!-- To render .ipynb with dynamic plots:
Use nbviewer
-->
