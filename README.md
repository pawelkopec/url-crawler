# url-crawler
## What is it for?
Url-crawler automatically builds a tree of active URLs on a website.
It enables you to quickly prepare a structure of resources available 
on the server together with received status codes.

## What do I need?
Python 3.5 with packages requests and html.

## How does he crawl?
Crawler starts at a domain name with no further path. He looks for other 
links with the same domain base and tries if they are working. If they are -
he repeats the procedure all over again.  
  
You can provide crawler with some paths you want him to check first. You
can also provide him with an path predictor that will think up of new paths
for example by finding patterns in the ones already found.
