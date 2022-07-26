---
layout: page
title: "Python Code - Applications"
---

I share some **python code** for accounting and finance research here. Open a link in a new window if you'd like to stay on this page. When possible, a code file includes interesting figures.<br/>


* [How to get access to WRDS in Python.](https://nbviewer.org/github/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code/wrds-intro.ipynb)<br/>
* Download data from WRDS: [Compustat ](https://nbviewer.org/github/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code/wrds-download-compustat.ipynb); [Audit Analytics-Audit Opinions](https://nbviewer.org/github/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code/wrds-download-compustat.ipynb); [Audit Analytics-CAMs](https://nbviewer.org/github/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code/wrds-download-AuditAnalytics-CAM.ipynb); [Audit Analytics-IPOs](https://nbviewer.org/github/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code/wrds-download-AuditAnalytics-IPO.ipynb).<br/>
* Yearly distribution of <b>loss firms</b>: More than half are loss firms in 2020.<br>
    * [Version 1. Using matplotlib after aggregating data method](https://nbviewer.org/github/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code/compustat-loss-firm-distribution.ipynb) <br>
    * [Version 2. Using seaborn and raw data method](https://nbviewer.org/github/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code/compustat-loss-firm-distribution.ipynb) <br>

* <b>Seaborn</b> allows to visualize data with multiple dimensions: [scatterplot of firm size, profitability, and auditor size.](https://nbviewer.org/github/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code/sctterplot-ROA-size-Big4.ipynb)<br/>
* Can we get <b>IPO years from Compustat</b>? Yes we can. Check [the distribution of IPO years.](https://nbviewer.org/github/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code/Compustat-ipodate.ipynb)<br/>
* [SEC filing distribution provided by SEC EDGAR.](https://github.com/jaeyoonyu/sec-archives/blob/master/SEC_filings_dist.ipynb)<br/>
* Does the <b>earning kink</b> exist at zero? Maybe not any more.[Check the distribution.](https://nbviewer.org/github/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code/is-there-kink-around-zero.ipynb)<br/>
* Navigate data with <b>plotly</b>, allowing us to identify outliers visually: [Scatter plot of ROA-leverage.](https://rawcdn.githack.com/jaeyoonyu/blog-posting/6bfcbbd164951cd69941ee2a33b779f5d519c769/plotly-hovering.html)<br/>
* <b>Plotly for dynamic visualization</b><br>
    * Check the bubble plot for [auditors' client distribution](https://nbviewer.org/github/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code/client-dist.ipynb).
    * Check the bubble plot for [asset, sales, and market value](https://nbviewer.org/github/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code/compustat-bubble-plot-animation.ipynb).



---
Click the play button below to see the dynamic visualization!
{% include client-dist-figure.html %}

Click the play button below to see the dynamic visualization!
{% include dynamic-scatter-mv-at.html %}


<!-- To render HTML and get a link:
https://raw.githack.com/
-->

<!-- To render .ipynb with dynamic plots:
Use nbviewer
-->
