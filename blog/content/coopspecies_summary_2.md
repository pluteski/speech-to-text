Title:  Key Lessons from A Cooperative Species, Part 2.
Subtitle:    14 Lessons from "A Cooperative Species, Human Reciprocity and Its Evolution" By Samuel Bowles & Herbert Gintis, 2011.
Project:     Life in Motion
Author:      Mark Plutowski
Affiliation: Economics in Motion
Web:         https://pluteski.github.io
Date:        2018-10-08


# Lessons from cooperative economics, Part 2


# Overview
This is Part 2 of "14 lessons from [A Cooperative Species]"(https://press.princeton.edu/titles/9474.html) By Samuel Bowles & Herbert Gintis, 2011.  This part argues that noncooperative game theory falls short in explaining human behavior.

[Part 0 gives the highlights of the 14 lessons.](https://pluteski.github.io/speech-to-text/key-lessons-from-a-cooperative-species-part-0.html)

[Part 1 gives a broad brush introduction to competing theories.](https://pluteski.github.io/speech-to-text/key-lessons-from-a-cooperative-species-part-1.html)



# Cooperative Homo economicus (aka The Econ)
The book argues that human levels of cooperation are impossible to model with only noncooperative game theory. (It turns out that several years later, theoretical computer scientists and algorithmic economists have supported their view using constructive proofs.)

A major goal of economic theory has been to explain widespread voluntary cooperation among groups of people. 

The **fundamental theorem of welfare economics** underlying classical economics seemed to agree with Adam Smith’s view that self-regarding behaviors support socially valued economic outcomes. 

Individuals maximize their utility given a set of market-determined **prices** over which they exercise no control. They thus interact with a list of prices, not with each other. 

As a result, the payoffs for each individual do not depend on the actions of others. This is because individuals are content and may even prefer to interact through prices alone. Therefore they have no incentive to engage in strategic personal interactions. All relevant aspects of exchanges are assumed to be covered by complete contracts, enforceable at no cost to the exchanging party. 

A **complete contract** ensures that any aspect of a transaction will be explicitly stated in the contract and implemented as stated. The enforcement in case of breach of contract is entrusted to a third party, such as a court of law. Enforcement is assumed to impose no costs on the injured party.

It turns out that complete contracts are practically impossible without institutions. Even with institutions contracts are largely ineffective. Cost of enforcement is nonzero and often very high. This mechanism requires extraordinary cognitive capacities among the individuals and lots of time to deal with negotiation in advance, and time to monitor and enforce the contract. 

It also turns out that computational theorists have shown that it is unlikely that a group containing more than a few human participants would ever figure out how to play this game effectively -- and if they did, they would quickly abandon it for a number of reasons. 

The solutions to these games are extremely difficult to find and maintain except under implausible conditions. These conditions may be suitable for nonhuman players, such as corporations, governments, or algorithms, but are practically impossible for humans to play well. In fact, people often settle into game play that ends up being worse for everyone involved.


## Evolutionary Dynamics

The authors use a common phrase “folk theorem” to refer to [a class of game theories](https://en.wikipedia.org/wiki/Folk_theorem_(game_theory)). This phrase is commonly used by economists and is not intended in a pejorative manner. These are called “folk” theorems because they were so widely known among game theorists in the 1950’s even though no one had published them.  In a sense, they were donated to the community -- a notable act of altruism by otherwise ardent proponents of self-interest!

All **folk theorems** are based on a **stage game**, that is, an interaction played an indefinite number of times, with a constant, strictly positive, probability that in each period the game will continue for an additional period 

A strategy in this game that dictates following one course of action until a certain condition is met and then following a different strategy for the rest of the game is called a **trigger strategy**

It turns out that the existence of trigger strategies is an achilles heal for folk theorem models.  It is [extremely difficult to] come to a working arrangement among numerous independent strategic agents, at least _in the absence of a regulating institution to which all are committed_. This "institution" might be a centralized court of law, or an ad hoc committee, or a strong group leader -- or, internalized group norms upheld by decentralized enforcement. 

The n-player reciprocal altruism model can sustain a high level of cooperation only in very small groups. 

Apparently, directed punishment appears to solve the problem of cooperation in large groups. There is a catch, however. Because punishing costs the punisher, self-regarding players have no incentive to carry out the punishment. Thus, this model does not work assuming self-regarding players. 

[Part 0](https://pluteski.github.io/speech-to-text/key-lessons-from-a-cooperative-species-part-0.html) showed that people avidly punish defectors even at a cost to themselves. This provides a solution to this problem, but one that is based on social preferences rather than self-interest. 

**This coordination problem in a noncooperative game is largely because the information each has on the others’ actions is subject to error.** 

## Private information makes things worse
Noncooperative dynamics work well when all information is public.  But the only way the self-regarding Econ can work together effectively is if all information is public, all agents are omniscient, and ever watchful.

There is another approach to constructing Nash equilibria for repeated games with private signals that actually **DOES** work, but where players use strictly mixed strategies.  This means that they randomize over various actions rather than taking a single action in each period.  This is suitable for algorithms in a bot net or algorithmic trading market, and are probably the way that AI will negotiate in the future internet of things.

The book claims that human players cannot or will not ever actually use such mixed strategies, because mixed strategies break down under fairly mild stress.  However, it turns out that AI agents can handle this optimally even where information is private, by using randomized mixed strategies.


## Irrelevant solutions
It is plausible that with the assistant of information tools, individuals could coordinate given full knowledge of the game and the choices of the other players. But when knowledge is imperfect or private and the choices of the other players are not known the noncooperative algorithms fail miserably. Providing the human players with tools to collect and process the available data is not enough -- agents need to be omniscient mind-readers.

It turns out that we now know that Nash equilibrium are extremely difficult to find and maintain except in the simplest of cases. 

The problem with achieving a Nash equilibrium is that individuals may have differing beliefs about how other players will behave, and moreover, these beliefs may simply be incompatible.  When this is the case, achieving coordination much less true cooperation would be akin to a miracle. 

Individuals may also have incorrect ideas about what other players believe concerning the individuals own behavior. Therefore, individuals may choose best responses to strategies that the other players in fact are not playing, resulting in game play that is very far from any Nash equilibrium. 


## Fatal flaws of the Econ's approach

If there is a Nash equilibrium with private signals, individuals have no particular incentive to play the strategies that implement the equilibrium, because many other strategies have the same payoffs as the equilibrium payoffs. 

Moreover, the equilibrium exists only if private signals are very close to being public, so all individuals receive nearly the same signal concerning the behavior of any given group member. 

When this is not the case, the equilibrium will not exist. Thus, these models apply only to forms of cooperation where all members observe the actions of nearly all others with a high level of accuracy.

In other words, the classical econ theories only work with inhuman players.  The **Econ** cannot be **Human**.

## Correlated Equilibria 

There is an alternative game-theoretic equilibrium concept that does not share the weaknesses associated with the Nash equilibrium described above: **the correlated equilibrium** along with a correlating device.

A correlating device is something that sends out signals, private or public, to the players of a game, indicating which pure strategy each should play. 

A correlated equilibrium is a situation in which there is a correlating device such that, if all players follow the advice of the correlating device, no player can do better by switching to an alternative strategy.

The book argues that correlated equilibrium rather than Nash equilibrium is the appropriate equilibrium concept for game theory. Theoretical computational science and algorithmic economics have since provided additional strong support for this argument.

* Assuming players have common knowledge of the game, its rules, and its payoffs, as well as a common belief concerning the probability of the natural events (the so-called moves by Nature) associated with the game, the strategies chosen by rational individuals can then always be modeled as a correlated equilibrium with an appropriate correlating device. 
* The notion of a correlating device is quite abstract, but one form of correlating device is well known and performs precisely the social function of signaling actions to individuals that, when followed, may lead to a socially efficient outcome. This device is the social norm which, like the choreographer in a ballet, is instituted to issue precise instructions that, when followed, produce the desired outcome. 
* For instance, the system of traffic lights in a city’s street network instruct drivers when to stop and when to go, and it is normally in the interest of drivers to obey these signals as long as others do so, to avoid accidents. In other words, drivers obey a social norm.

A cooperative equilibrium supported by social norms is one in which not only is the equilibrium strategy evolutionarily stable, but also the social norms are themselves an evolutionary adaptation, stable against invasion by competing social norms

We posit that groups have social norms specifying how a game ought to be played and that these norms are identified as social norms by group members.

Social norms do not ensure equilibrium, because error, mutation,migration, deliberate violation of the norm, and other dynamical forces may lead individuals to reject beliefs or behavior fostered by the norm. 

* This may occur because the beliefs might conflict with an individual’s personal experience.
* Or its suggested behavior may be rejected as not in the individual’s best interest.
* The action fostered by a social norm must be a best response to the behaviors of the other group members, given the beliefs engendered by the social norm and the individual’s updating. 
* Social norms cannot be introduced as a deus ex machina, as if laid down by a centralized authority, without violating the objective to provide a “bottom-up” theory of cooperation that does not presuppose preexisting institutional forms of cooperation. 
* Social norm are thus discretionary, because any institution that is to enforce behavior should itself be modeled within the dynamical system, unless plausible reasons are given for taking a macro-level institution as unproblematically given. 
* Nor are social norms fixed in stone. A group’s social norms are themselves subject to change, those groups producing better outcomes for their members sometimes but not always displacing groups with less effective social norms, and changing social and demographic conditions leading to the evolutionary transformation of social norms within groups.

## The Missing Choreographer

The **fundamental** (“invisible hand”) **theorem of welfare economics** supposedly models decentralized market interactions, but on close inspection requires an extraordinary level of coordination that is not explained.

Humans are exceptional in the range of cooperation among large numbers of substantially unrelated individuals. 

Examples of this include:

* The global division of labor.
* Global market exchange. 
* Democracy.
* Warfare. 

These are today sustained as a result of a mixture of self-regarding and social preferences operating under the influence of strong institutions of governance, along with socialization that favor cooperators. 

Something coordinates their actions so as to punish cheaters and protect honest participants from exploitation. Social norms and institutions that accomplish this evolved over millennia through trial and error. 

The private nature of information makes it practically impossible to coordinate the targeted punishment of cheaters. 

### How did our ancestors achieve this?
In many hunter-gatherer societies certain information is made public.  

Examples of this include: 
* Eating in public so that food can be shared fairly and cheaters be easier to catch.
* Japanese shrimp fishermen who pool income across boats deliberately land their catch at an appointed time of day.

### How does modern society achieve this?
In most modern societies a court of law converts private information about a legal conflict to public information. This is the basis of punishment in civil or criminal trials involving elaborate processes that have evolved over centuries. These rely on commonly agreed upon rules of evidence and ethical norms of appropriate behavior. Even with the benefit of these preexisting social preferences, these complex institutions frequently fail.

Secondly, cooperation often unravels due to vigilantism.  This is when a civid minded individual tries to punish a defector on their own, perhaps by simply withdrawing their cooperation with the perceived transgressor. This can be mistaken by others as itself a violation of a cooperative norm, inviting a spiral of further defections. 

* In virtually all surviving societies with substantial populations, this problem is addressed by the creation of a corps of specialists entrusted with carrying out the more severe of society’s punishments. 
* Their uniforms convey the civic purpose of the punishments they mete out, 
* their professional norms, it is hoped, ensure that the power to punish is not used for personal gain. 
* Like court proceedings, these policing, penal, and related institutions work imperfectly

A key message here is that while institutions and ethics matter, social norms and morals are still required to uphold ethics.  Institutions as yet still cannot provide the truly decentralized agreement required to cooperate effectively in small to medium sized groups except in very narrowly defined classes of transactions. 

An implicit message here is that forcing human participants to work together through purely competitive means only -- that is, non-cooperative dynamics only, without the assistance of a correlating signal -- people will inevitably revert to behaviors such as what is seen in many of the noncooperative games.  Groups will also succumb to various social dilemmas. 

They criticize the the classical economics “folk theorem” as relying on  fictive Rube Goldberg strategies. At this time in the book, the phrase "folk theorem" seems to be used almost spitefully, as if to say it is too ad hoc and unscientific. One thing for sure is that the authors think the classical economics models are not simpler than their version of cooperative economics.

___

** Part 0 : ** 
[Overview of 14 key lessons of cooperative economics](https://pluteski.github.io/speech-to-text/key-lessons-from-a-cooperative-species-part-0.html).

** Part 1 : ** 
[Overview of competing alternatives](https://pluteski.github.io/speech-to-text/key-lessons-from-a-cooperative-species-part-2.html).

** Part 3 : ** 
[Evolutionary economics, rise of institutions, and the co-evolution of genes and culture](https://pluteski.github.io/speech-to-text/key-lessons-from-a-cooperative-species-part-3.html).

___
