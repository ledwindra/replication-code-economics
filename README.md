# About

In late March 2021, a friend of mine sent me a paper titled [The influence of hidden researcher decisions in applied microeconomics](https://onlinelibrary.wiley.com/doi/full/10.1111/ecin.12992). Then I read the author's thread on [Twitter](https://twitter.com/nickchk/status/1374058480219213824). That leads me to the following question:

```
Is making replication code more of a norm or an exception to (micro/empirical)economists?
```

It may be true that there are public resources out there, but they may be scattered and not centralized in a place where communities can easily look up to, such as GitHub, where for other programming languages we can see on GitHub [topics](https://github.com/topics) such as [Awesome X](https://github.com/topics/awesome). It's not surprising that economists are not used to sharing stuffs on this place, but fortunately it looks like the numbers are growing recently.

So here's my attempt to nowcast total repositories using Stata that describe "replication code" in the keywords. From the figure below I am optimistic that open-sourcing research is becoming more popular. However, it still doesn't count publicly available codes on elsewhere, such as GitLab, Bitbucket, journal websites, or the authors' academic/personal websites.

This repository is automatically updated at 12.00 AM UTC every day to nowcast this trend. The only metric that I use is numbers of public repositories that use Stata and have "replication code" in the keywords (not case sensitive). Also, it doesn't take into account the field of study in the replication codes. It is possible that people who use Stata also come from fields of study other than economics. Lastly, economists may increasingly use Python or R (order doesn't matter), which are not covered here yet since my assumption is that economists still mainly use Stata. I can be wrong here, though.


## GitHub API
![replication-code-stata](./img/replication-code-stata.png)

## AEA Deposit on ICPSR
![replication-code-stata](./img/aea-deposit-icpsr.png)
