---
layout: page
title: "Visuals"
---
On this webpage, I share some figures that I've generated using Python. Note that this page might not work properly on your mobile device. For <b>dynamic plots</b>, you can
- zoom in and out;
- click the <b>play button</b> to see how the figure changes;
- <b>mouse over the data point</b> you're interested in.
<br>

---

<h2> 1. Correlation heatmap  </h2>

<img src="/assets/images/correlation-heatmap.jpg" class="inline">

Click here for the [Code](https://nbviewer.org/github/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code/visual-heatmap.ipynb).<br/>

---

<h2> 2. Earnings kink at zero: Does it still exist?  </h2>

<img src="/assets/images/earnings-kink-static.jpg" class="inline">
<br>
{% include earnings-kink-dynamic.html %}


Click here for the [Code](https://nbviewer.org/github/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code/is-there-kink-around-zero.ipynb).<br/>

---

<h2> 3. Distribution of earnings announcement dates  </h2>
<br>
<img src="/assets/images/earnings-ann-date-dist.jpg" class="inline">

<b>The Q1 distribution is more dispersed</b> as many firms prepare 10-K and are subject to year-end audits.<br/>

Click here for the [Code](https://nbviewer.org/github/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code/earnings-ann-date-dist.ipynb).<br/>

---

<h2> 4. How many clients for each audit firm? </h2>

{% include client-dist-figure.html %}
Click here for the [Code](https://raw.githack.com/jaeyoonyu/jaeyoonyu.github.io/main/_code/audit-analytics-client-distribution.html).  
<br>

---
<h2> 5. Scatter plots: ROA & SALES </h2>

{% include dynamic-scatter-plot.html %}

Click here for the [Code](https://raw.githack.com/jaeyoonyu/jaeyoonyu.github.io/main/_code/compustat-bubble-plot-animation.html).

---

<h2> 6. Yearly distribution of bankruptcies  </h2>

<img src="/assets/images/bankruptcy-dist.jpg" class="inline">

Click here for the [Code](https://nbviewer.org/github/jaeyoonyu/jaeyoonyu.github.io/blob/main/_code/wrds-download-AuditAnalytics-bankrupt.ipynb).<br/>

---