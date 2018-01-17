Title:  The dirt on Hashgraph
Subtitle:    What we know about Hashgraph c.2017
Project:     Cryptocurious
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

#### About the author
I am just an interested learner coming up to speed on blockchain technologies, distributed ledger technologies,
and decentralized consensus systems.
At the time of writing this article I have no investment in any cryptocurrency, I do not work for or represent
any organization related to cryptocurrencies or distributed ledger technologies.
As of the time this article was posted, I am still learning about this area.

So why am I writing this?

Hashgraph impressed on me the value of [gossip](https://hashgraph.com/faq/#how-does-it-work).
Instead of waiting to share your opinion until you are absolutely certain of what you know, a
"gossip protocol" says to share your observations early and often.
So, here are mine about Hashgraph.
Hashgraph mathematically proves that
gossip can allow decentralized participants to rapidly share what they
have observed (as well as what they have heard second-hand from others),
and rapidly agree on what is to be believed. Who am I to argue with math?

## How does Hashgraph use gossip?

Suppose you are a member of a gossip network.
You tell some random participant what you know.  They tell you what they know.
Later, they tell some random participant what they know, which includes some
(possibly second hand) information they learned from you.
Eventually, participants are able to tally not only what they have observed,
but also what other participants are likely to have observed, based
on the gossip they've shared.  Given enough second-hand information
from enough credible witnesses, they can even predict the opinion of
participants with whom they have not communicated.

Timestamps are also calculated incorporating the consensus opinion of
when a event was observed, to counteract accidental or intentional timestamp errors.

As we know from human nature, gossip spreads like wildfire.
Unlike how rumormills work in human society, when marshalled cleverly with the
proper algorithms, gossip turns out to be provably fair.


## How does Hashgraph compare to Bitcoin?
Distributed consensus is an extremely useful concept in distributed computing.
For decades it was doable only among a small number of computers ("nodes").
Nakamoto's Bitcoin cryptocurrency  [presented a new way to achieve scalable decentralized consensus](http://vukolic.com/iNetSec_2015.pdf).

Despite Bitcoin demonstrating tremendous value, its blockchain plus Proof-of-Work (PoW) approach
presents several pitfalls. It is:

* Wasteful since PoW expends huge amounts of computing power [by design](http://www.nasdaq.com/article/byzantine-fault-tolerance-the-key-for-blockchains-cm810058).
* Slow, limited to tens of transactions per second.
* Subject to allowing huge backlog of unconfirmed transactions to accumulate.
* Network bandwidth intensive.
* [Susceptible to a 25% economic attack](https://arxiv.org/abs/1311.0243).
* [Heavyweight](https://bitcoin.org/en/full-node). Full nodes must download the entire blockchain, currently 60 GB.  [Lightweight nodes must trust the full nodes](https://en.bitcoin.it/wiki/Full_node).

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

Activity is divided into rounds.  At the beginning of a round,
each node communicates state with some random other node.
Since these two nodes already have a channel open, the random other node then shares back
state of its own that it knows first hand, perhaps along with some state that
it previously learned from another node.
After a new event has seen at least 2/3 of previous events, a round is concluded and a new round begins.

When the new round is created, nodes say if they agree
upon the data contained in events of the preceding round.
The algorithm doesn't consider this to be voting per se, instead calling it a virtual election.
There is no leader to present a motion for vote, nor to tally votes.
Instead, to reach consensus on the events in the previous round,
nodes [verify that they are connected to these events](https://medium.com/ibbc-io/hashgraph-for-dummies-90ddde3be9e2).

(More strictly speaking,
it is actually about finding paths through the graph that connect events in the current round with past events in the previous round.
Please see : [How it Works (Graphically)](http://www.swirlds.com/downloads/SWIRLDS-TR-2016-02.pdf).)

At this point, some applications could [dump all previous events](http://ajitvadakayil.blogspot.com/2017/10/blockchain-smart-contracts-part-8-capt.html).
In applications where the transaction timeseries can be
summarized by sufficient statistics, the hashgraph
history could be archived. This also means that _a new node doesn't need to load the entire hashgraph history_,
greatly reducing the space required and allowing a [smartphone to act as a node](https://squawker.org/technology/blockchain-just-became-obsolete-the-future-is-hashgraph/).
There is no notion of full node and lightweight node, meaning that all nodes can participate in consensus and see the full ledger.

## Virtual elections: better than regular elections?
Many people consider Hashgraph to be more comparable to PBFT, Paxos, Raft, Zab,
and other consensus seeking systems that rely on leaders and
traditional voting schemes.
But Hashgraph eschews the comparison, because it doesn't use
traditional voting.
It comes to consensus about what happened, and when,
by cleverly tallying highly compressed event logs
based on "famous witnesses" that ["strongly see"](https://www.swirlds.com/downloads/SWIRLDS-TR-2016-02.pdf) events.

If the timestamp of an event log is corrupted by a bad clock or is maliciously doctored,
this will usually have no effect on the consensus timestamp, because consensus opinion on
when something occurred is the median of timestamps observed by credible witnesses.

Unlike some other directed acyclic graph algorithms, or even Paxos,
it really is quite easy to step through the Hashgraph algorithm.
I couldn't do it more succinctly here.
I'll again point the interested reader to whitepapers for how it works :
[graphically](http://www.swirlds.com/downloads/SWIRLDS-TR-2016-02.pdf),
and [example voting scenarios](http://www.swirlds.com/downloads/Swirlds-and-Sybil-Attacks.pdf).

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

### Performance
Paypal and Visa tend to be held up as benchmarks or
at the very least as future milestones for a DLT to achieve in order to
replace an existing mainstream currency, payment system, or other commercial transaction logging systems.

Here are the transactions per second (tps) of PoW versus Paypal and Visa :

* PoW Blockchain (Etherium, Bitcoin) : **< 10 tps**
* Paypal : **[200 tps](http://www.altcointoday.com/bitcoin-ethereum-vs-visa-paypal-transactions-per-second/)**
* Visa : **[2K tps](https://mybroadband.co.za/news/security/190348-visanet-handling-100000-transactions-per-minute.html)** to **[50K x/sec](https://lightning.network/lightning-network-paper.pdf)**

Of these, only PoW is a BFT DLT.

To be fair, because of its positioning and licensing, Hashgraph is more directly comparable to Hyperledger, which is
another scalable DLT using a Practical Byzantine Fault Tolerance (PBFT) consensus algorithm.
Other comparable enterprise-grade transaction processing systems include
LMAX and its variants, such as [LMAX Disruptor](http://lmax-exchange.github.io/disruptor/)
and Bitshares. LMAX is not a DLT, and Bitshares is billed as a decentralized exchange.
That said, if we are going to use Visa and Paypal for comparison, then we might as well
include these for context. Their ts/sec are as follows:

* [Hyperledger](https://www.hyperledger.org/about) : **[1K tps](https://www.altoros.com/blog/hyperledgers-sawtooth-lake-aims-at-a-thousand-transactions-per-second/)** to **[10K tps](https://medium.com/chain-cloud-company-blog/hyperledger-vs-corda-pt-1-3723c4fa5028)**
* Bitshares : **[100K tps](https://bitshares.org/technology/industrial-performance-and-scalability/)**
* LMAX : **[100K tps (2010)](https://qconsf.com/sf2010/sf2010/presentation/LMAX+-+How+to+do+over+100K+concurrent+transactions+per+second+at+less+than+1ms+latency.html)** to **[6M tps](https://martinfowler.com/articles/lmax.html)**

Hashgraph's inventor says it will be able to attain [250K+ tps](https://www.hiddenforcespod.com/leemon-baird-hashgraph-distributed-ledger-technology-blockchain/),
more with sharding.



## The bad
So what is the catch?

Hashgraph is currently being deployed in [private, permissioned-based networks](https://hashgraph.com/faq/#is-there-a-cryptocurrency),
although its designers propose means for implementing [nonpermissioned and hybrid networks](http://www.swirlds.com/downloads/Swirlds-and-Sybil-Attacks.pdf).
How well it can be adapted to a truly decentralised public ledger remains to be seen, because it assumes that a node can determine :

* Addresses of random nodes in the network for messaging, and
* The number of other nodes N in the network

This is because the algorithm requires a node to be able to (a) pick another node at random, and (b) know the value of ⅔ * N.
It needs a means of registering and unregistering of members in the network,
whereas public blockchains allow nodes to sign in and out to the network without any notice.

The following seem to be the major showstoppers for many members of the cryptocurrency development community:

1. [There is no Hashgraph public ledger or cryptocurrency](https://hashgraph.com/faq/#is-there-a-cryptocurrency).
2. US Patents #[9,646,029](http://www.leemon.com/papers/2017b.pdf), #[9,529,923](http://www.leemon.com/papers/2016b4.pdf), #[9,390,154](http://www.leemon.com/papers/2016b3.pdf).
3. Requires a license to use.

## A passing thought
[Arrow's Theorem](http://tech.mit.edu/V123/N8/8voting.8n.html) proves that no voting system is fair.
I'm no [voting theorist](https://www.princeton.edu/~cuff/voting/theory.html),
but in my (extremely humble) opinion, Hashgraph comes pretty close.
It makes one want to believe in democracy again. Real-time continuous nationwide elections anyone?


## Acknowledgments
Thanks for helpful edits to [Josh Quittner](https://medium.com/@twittner),
[Will Huang](https://github.com/thewillhuang), [Gregory Kennedy](https://www.linkedin.com/in/gregorykennedy/)
and [Marcus Plutowski](https://blog.valkyrierobotics.com/).


## Concluding remark
[DYOR](https://scontent.cdninstagram.com/t51.2885-15/s320x320/e35/25009793_144878492834781_2739446234354810880_n.jpg) !
Consider this to be informed gossip. But do share your gossip with me too. The math says to, so, yeah just do what the math says.


