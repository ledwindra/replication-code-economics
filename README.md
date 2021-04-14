# About

In late March 2021, a friend of mine sent me a paper titled [The influence of hidden researcher decisions in applied microeconomics](https://onlinelibrary.wiley.com/doi/full/10.1111/ecin.12992). Then I read the author's thread on [Twitter](https://twitter.com/nickchk/status/1374058480219213824). That leads me to the following question:

```
Is making replication code more of a norm or an exception to (micro/empirical)economists?
```

It may be true that there are public resources out there, but they may be scattered and not centralized in a place where communities can easily look up to, such as GitHub, where for other programming languages we can see on GitHub [topics](https://github.com/topics) such as [Awesome List](https://github.com/topics/awesome). It's not surprising that economists are not used to sharing stuffs on this place, but fortunately it looks like the numbers are growing recently.

This repository is automatically updated at 12.00 AM UTC every day to nowcast this trend. Currently there are two data sources that I'm using:

## GitHub API
The only metric that I use is total numbers of public repositories that use Stata and have "replication code" in the keywords (not case sensitive). Also, it doesn't take into account the field of study in the replication codes. It is possible that people who use Stata also come from fields of study other than economics. Plot example as follows:

![replication-code-stata](./img/replication-code-stata.png)

## AEA Deposit on ICPSR
American Economic Association deposits, where I scrape all of DOIs of each journal (nine in total). Then I compare the proportions of papers that have deposits on [Open Inter-university Consortium for Political and Social Research (ICPSR)](https://www.openicpsr.org/) to total papers published in AEA. The idea is to see the trends of replication over time so I don't have to hard-code the search process which I may overlook. Plot example as follows:

![replication-code-stata](./img/aea-deposit-icpsr.png)

# PS
Don't hesitate to reach me out or submit issues [here](https://github.com/ledwindra/replication-code-economics/issues).
