Apriori-based query expansion system for Chinese IR 
=============================

This is the python-based prototype of Chinese query expansion system using CKIP eHownet dictionary and association mining algorithm – Apriori in order to explore more query options for user in Google. However, as this still belongs to init version and prototype, codes of interface, HTTP server and database use simple sqlite and CGI script for development and it doesn’t integrate the web-framework like Django and doesn't use the ways like multiprocessing or threading to improve cal performance. In addition, the full usage of ehownet through SQL is not for free, thus the number of terms in the current dictionary to expand the user query is limited. 

Introduction to utilizing CKIP ehownet: 
http://www.aclclp.org.tw/use_ckip_c.php    

=============================
Usage: 

1.	Jieba is required to be installed in advance (easy_install jieba or pip install jieba)
2.	Run simple_httpd.py to start the http development server
3.	Open index.html by any your preferred browser to enter the entry of the system

=============================
Online Demo in Google Chrome Web Store:

still under construction... but will see it soon

=============================
Features: 

1. make use Web Search API to get web snippet from Google index server   
2. Use Bag of word and TF/IDF for feature exaction
3. Use Apriori to mine the association rule in a webpage and use eHowbet and a simple weighted scheme to prioritize the rules


=============================
Reference:

Chinese word segmentation using Jieba 
https://github.com/fxsjy/jieba

Google Web Search API
https://developers.google.com/web-search/docs/?hl=zh-TW

Apriori algorithm
http://en.wikipedia.org/wiki/Apriori_algorithm
