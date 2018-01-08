Title:  The dirt on Hashgraph
Subtitle:    What we know about Hashgraph c.2017
Project:     cryptocurious
Author:      Mark Plutowski
Affiliation: Plutosoft Delimited
Web:         https://pluteski.github.io
Date:        2018-01-07


![emonocle byEMIIA](https://1.bp.blogspot.com/-DpZwufJmu_Y/Wh6lGuTNRmI/AAAAAAAABUU/0W2PLj5w-j4ql9RE8Otwk5DrB3UcgKOGQCLcBGAs/s1600/hashgraph%2B%25282%2529.gif)
<p style="text-align: right;"><em>(emonocle byEMIIA)</em></p>


## _pssst!_ ... _have you heard about Hashgraph?_
[Hashgraph](https://hashgraph.com) is a distributed ledger technology (DLT)
released by [Swirlds](http://www.swirlds.com/) (think: "Shared Worlds") in 2016.
It promises some of the most important benefits of blockchain without its biggest limitations.
It is comprised of a graph data structure which together with
the [Swirlds distributed consensus algorithm](http://www.swirlds.com/downloads/SWIRLDS-TR-2016-01.pdf)
provides [asynchronous byzantine fault tolerance](https://hashgraph.com/faq/#what-is-bft), using what it calls "gossip about gossip."

_Whaaaat?_  A system based on second hand rumors and some sort of whisper logs? We're really supposed to trust this thing?
Read on to find out.

## How does Hashgraph compare to Bitcoin?
Distributed consensus is an extremely useful concept in distributed computing.
For decades it was doable only among a small number of computers ("nodes").
Nakamoto's Bitcoin cryptocurrency  [presented a new way to achieve scalable decentralized consensus](http://vukolic.com/iNetSec_2015.pdf).

Bitcoin protocol does not implement consensus
in the traditional distributed computing sense.
[Instead it achieves consensus via probabilistic agreement](http://vukolic.com/iNetSec_2015.pdf).

A primary goal of a cryptocurrency is to [totally order](http://mathworld.wolfram.com/TotallyOrderedSet.html) transactions
on a [distributed ledger](https://www.investopedia.com/terms/d/distributed-ledgers.asp).
Cryptocurrencies avoid the need for a [trusted third party to timestamp transactions](https://en.wikipedia.org/wiki/Cryptocurrency#Timestamping)
added to the ledger.
Hashgraph also provides a total order on a distributed transaction ledger,
but does so using a [different approach](https://steemit.com/steemit/@decryptson/hashgraph).
Whereas the Bitcoin network builds up its transaction history in the form of a “blockchain”,
adding [a new block on top of the previous block every ten minutes](https://bitcoinmagazine.com/articles/selfish-mining-a-25-attack-against-the-bitcoin-network-1383578440/),
Hashgraph grows a time directed acyclic graph akin to a braided forest of trees
using "virtual voting" and ["gossip about gossip"](https://hashgraph.com/faq/#how-does-it-work).

Despite Bitcoin demonstrating tremendous value, its blockchain plus Proof-of-Work (PoW) approach
presents several pitfalls. It is:

* Wasteful since PoW expends huge amounts of computing power [by design](http://www.nasdaq.com/article/byzantine-fault-tolerance-the-key-for-blockchains-cm810058).
* Slow, limited to tens of transactions per second.
* Subject to allowing huge backlog of unconfirmed transactions to accumulate.
* Network bandwidth intensive.
* [Susceptible to a 25% economic attack](https://arxiv.org/abs/1311.0243).

## Virtual elections: better than actual elections?
Many people consider Hashgraph to be more comparable to PBFT, Paxos, Raft, Zab,
and other consensus seeking systems that rely on leaders and voting schemes.
But Hashgraph eschews the comparison, because it doesn't use voting.
It comes to consensus about what happened, and when,
by cleverly tallying highly compressed event logs
based on "famous witnesses" that ["strongly see"](https://www.swirlds.com/downloads/SWIRLDS-TR-2016-02.pdf) events.

Suppose you are a member of a gossip network.
You tell some random participant what you know.  They tell you what they know.
Later, they tell some random participant what they know, which includes some
(possibly second hand) information they learned from you.
Eventually, participants are able to tally not only what they have observed,
but also what other participants are likely to have observed, based
on the gossip they've shared.  Given enough second-hand information
from enough credible witnesses, they can even predict the opinion of
participants with whom they have not communicated.

If the timestamp of an event log is corrupted by a bad clock or is maliciously doctored,
this will usually have no effect on the consensus timestamp, because consensus opinion on
when something occurred is the median of timestamps observed by credible witnesses.


[Arrow's Theorem](http://tech.mit.edu/V123/N8/8voting.8n.html) proves that no voting system is fair.
I'm no [voting theorist](https://www.princeton.edu/~cuff/voting/theory.html),
but in my (extremely humble) opinion, Hashgraph comes pretty close.
It makes one want to believe in democracy again. Real-time continuous nationwide elections anyone?


## Hashgraph: the good
It is [fast](https://hackernoon.com/demystifying-hashgraph-benefits-and-challenges-d605e5c0cee5),
[fair](https://hashgraph.com/faq/#what-is-fairness),
and [secure](https://hashgraph.com/faq/#preventing-sybil-attacks).
It promises the following:

* Total ordering of events.
* Strong [Byzantine Fault Tolerance](http://the-paper-trail.org/blog/barbara-liskovs-turing-award-and-byzantine-fault-tolerance/) (BFT),
the gold standard of industrial grade distributed consensus.
* Minimal network bandwidth, because it passes things only around once.
* Provable 100% certainty on the order of transactions.

Because it is fast and requires low network bandwidth, it can be used as a distributed memory system.
Because it provides a total order on transactions, it can be used as a multi-master database.
Because it does not use Proof-of-Work, it does not require unnecessary computation.

Before we discuss its tx/sec (transactions/second), let's review the tx/sec of other DLTs :

* Proof-of-Work Blockchain (Etherium, Bitcoin) : **< 10 tx/sec**
* Paypal : **[200 tx/sec](http://www.altcointoday.com/bitcoin-ethereum-vs-visa-paypal-transactions-per-second/)**
* Visa : **[2K tx/sec](https://mybroadband.co.za/news/security/190348-visanet-handling-100000-transactions-per-minute.html)**
    * Visa claims that its system has additional capacity to handle upwards of 50K tx/sec.

Hashgraph's inventor says it can attain [250K+ tx/sec](https://www.hiddenforcespod.com/leemon-baird-hashgraph-distributed-ledger-technology-blockchain/).

To be fair, because of its positioning and licensing, Hashgraph is most directly comparable to Hyperledger, which is
also a scalable DLT using a Practical Byzantine Fault Tolerance (PBFT) consensus algorithm.
Other enterprise-grade commercial systems include
LMAX and its variants, such as [LMAX Disruptor](http://lmax-exchange.github.io/disruptor/)
and Bitshares.  Their ts/sec are as follows:

* [Hyperledger](https://www.hyperledger.org/about) : **[1K tx/sec](https://www.altoros.com/blog/hyperledgers-sawtooth-lake-aims-at-a-thousand-transactions-per-second/)** to **[10K tx/sec](https://medium.com/chain-cloud-company-blog/hyperledger-vs-corda-pt-1-3723c4fa5028)**
* Bitshares : **[100K tx/sec](https://bitshares.org/technology/industrial-performance-and-scalability/)**
* LMAX : **[100K tx/sec (2010)](https://qconsf.com/sf2010/sf2010/presentation/LMAX+-+How+to+do+over+100K+concurrent+transactions+per+second+at+less+than+1ms+latency.html)** to **[6M tx/sec](https://martinfowler.com/articles/lmax.html)**

## The bad
So what is the catch?

Hashgraph is only deployed in [private, permissioned-based networks](https://hackernoon.com/demystifying-hashgraph-benefits-and-challenges-d605e5c0cee5). Whether it can be adapted to a truly decentralised public ledger remains to be seen, because it assumes that a node can determine :

* Addresses of random nodes in the network for messaging, and
* The number of other nodes N in the network

This is because the algorithm requires a node to be able to (a) pick another node at random, and (b) know the value of ⅔ * N.  It needs a means of registering and unregistering of members in the network,
whereas public blockchains allow nodes to sign in and out to the network without any notice. It is sometimes called a Permissioned Blockchain because
[there is no hashgraph public ledger or cryptocurrency and is currently only implemented on permissioned networks](https://hashgraph.com/faq/#is-there-a-cryptocurrency).

Finally, the following seem to be a major showstopper for many members of the cryptocurrency development community:

1. Requires a license to use.
2. US Patents #[9,646,029](http://www.leemon.com/papers/2017b.pdf), #[9,529,923](http://www.leemon.com/papers/2016b4.pdf), #[9,390,154](http://www.leemon.com/papers/2016b3.pdf).


#### About the author
I am just an interested learner coming up to speed on blockchain technologies, distributed ledger technologies,
and decentralized consensus systems.
At the time of writing this article I have no investment in any cryptocurrency, I do not work for or represent
any organization related to cryptocurrencies or distributed ledger technologies.
As I am still learning about this area, I am not an expert.

So why am I writing this?

Hashgraph impressed on me the value of [gossip](https://hashgraph.com/faq/#how-does-it-work).
Instead of waiting to share your opinion until you are absolutely certain of what you know, a
"gossip protocol" says to share your observations early and often.
So, here are mine about Hashgraph.
Hashgraph mathematically proves that
gossip can allow decentralized participants to rapidly share what they
have observed (as well as what they have heard second-hand from others),
and rapidly agree on what is to be believed. Who am I to argue with math?

## Concluding remark
[DYOR](https://pbs.twimg.com/media/DPT6qNIW0AE0RB4.jpg) !
Consider this to be informed gossip. But do share yours with me too. The math says to, so, yeah just do what the math says.


