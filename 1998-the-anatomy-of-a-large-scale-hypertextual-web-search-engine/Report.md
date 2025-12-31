# Anatomy of Web Search Engine

## Introduction
Many moons ago when the web was young, but booming, two graduate students named Sergey Brin and Lawrence Page set out to create a search engine that would revolutionize the way we find information online. Their paper, "The Anatomy of a Large-Scale Hypertextual Web Search Engine," published in 1998, introduced the world to Google and the concept of PageRank. However, PageRank is not just for ranking web pages; it is a pretty powerful algorithm that can be applied to various areas, including social network analysis, recommendation systems, and even biology.

You might ask, "Why PageRank?" Well, like I said earlier, the web was growing rapidly, and other search engines at the time were struggling to keep up. The developers realized that all web pages are not created equal, and some pages have more importance than others. They came up with the idea to use the link structure of the web to determine the importance of a page. More links to a page, more importance it has. 

## PageRank Algorithm
The core idea of the PageRank algorithm is that you are a random surfer who starts on a random web page and clicks on links randomly. The probability of landing on a particular page is determined by the number of links pointing to it and the importance of the pages linking to it. The algorithm assigns a score to each page based on this probability, which is then used to rank the pages in search results.

### Mathematical Formulation
They modeled the Web as a directed graph where:
- **Nodes** web pages
- **Edges** hyperlinks

PageRank is defined recursively. If page $A$ has inbound links from pages $T_1, T_2, \dots , T_n$ then:

$$
PR(A) = (1 - d) + d \left( 
\frac{PR(T_1)}{C(T_1)} +
\frac{PR(T_2)}{C(T_2)} + \cdots +
\frac{PR(T_n)}{C(T_n)}
\right)
$$

- $C(T_i)$ number of outbound links from page $T_i$
- $d$ damping factor (usually set to 0.85)

## Implementation
My implementaion uses the iterative power method implementation of PageRank. The algorithm starts with an initial guess for the PageRank of each page (usually 1/N, where N is the total number of pages) and iteratively updates the PageRank values until they converge to a stable state.

## Results
Here are the top 10 pages ranked by PageRank from a sample web graph:

Top 10 nodes by PageRank:
- Node 0: 0.118951
- Node 1: 0.071731
- Node 9: 0.043543
- Node 20: 0.031476
- Node 2: 0.020445
- Node 36: 0.018275
- Node 55: 0.016345
- Node 24: 0.013816
- Node 30: 0.013130
- Node 46: 0.012626

## Discussion
Our results are as expected you can also run a sanity check by verifying that the sum of all PageRank values is equal to 1: 

```print(sum(pagerank_scores.values()))```

The top-ranked pages are those with the most inbound links from other important pages, which aligns with the principles of the PageRank algorithm.

## References
- Brin, Sergey, and Lawrence Page. "The anatomy of a large-scale hypertextual Web search engine." *Computer Networks and ISDN Systems*, vol. 30, no. 1-7, 1998, pp. 107–117. Elsevier, doi:10.1016/S0169-7552(98)00110-X.
