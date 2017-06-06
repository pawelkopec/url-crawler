# url-crawler
## What does he do?
Url-crawler automatically builds a tree of resources available on a website
like html documents, images, etc.

## What do I need?
Python 3.5 with packages **requests** and **html**.

## How does he crawl?
Crawler starts at a domain name with no futher path. He looks for tags 
that can contain domain's resources (\<a>, \<img> etc.) and tries them out. 
If these resources contain links to other resources - he repeats
the procedure all over again.  
  
You can provide crawler with some paths you want him to check first. You
can also provide him with an path predictor that will think up of new paths
for example by finding patterns in the ones already found. 
