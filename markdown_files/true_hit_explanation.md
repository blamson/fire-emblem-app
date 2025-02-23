### Basic Random Variables and Dice

Before we dive into the complicated stuff like 2RN let's start with the basics and discuss a 1RN system.
1RN, or, 1 Random Number, is basically just a dice roll. It is what we would refer to as a **Uniform Random Variable** in the probability world.

Each side of the die is equally likely to happen. This is what we see in the first 5 Fire Emblem games. 
It's just a really big 100 sided dice in those games!

Let's look at a six sided die as an example. There's only six sides we can land on. Or, in other words, there are only six possible *outcomes*.
Each side of this die has the same chance of being rolled as well, assuming it's not a weighted die! So each side has a probability of 1/6.

I'm gonna use some mathematical notation but don't let it freak you out. 
We'll say $P(X=x)$ represents the probability that the random dice falls on a specific number. The big $X$ is our *random variable*
or, in other words, the die being rolled. The little $x$ is the side of the die we're interested in rolling.
So, if $x=2$ we're interested in the probability that we roll a 2. Which we'd write as $P(X=2)$.

So for the table below, the first row shows the probability that the die lands on 1. Or, mathematically, $P(X=1)$.

| $x$ | $P(X=x)$      |
|-----|---------------|
| 1   | $\frac{1}{6}$ |
| 2   | $\frac{1}{6}$ |
| 3   | $\frac{1}{6}$ |
| 4   | $\frac{1}{6}$ |
| 5   | $\frac{1}{6}$ |
| 6   | $\frac{1}{6}$ |

With this table we can do a lot, like find out the probability we get less than 5. For this we just add up the four rows below 5!
So we get $P(X < 5) = 4/6$. See, not too bad!

This may seem basic to some but I consider this to be a key building block for what's coming next. 
Now, let's discuss how things change when we add another die into the mix.

### Joint Random Variables

So, say we want to roll two dice. These dice have 4 sides ranging from 0 to 3. One of the dice will be $X$, the other will be $Y$.
Of course, for each die all sides are equally likely. So each side has a probability of $1/4$.

Individually, the tables look like so

| $x$ | $P(X=x)$      |
|-----|---------------|
| 0   | $\frac{1}{4}$ |
| 1   | $\frac{1}{4}$ |
| 2   | $\frac{1}{4}$ |
| 3   | $\frac{1}{4}$ |

| $y$ | $P(Y=y)$      |
|-----|---------------|
| 0   | $\frac{1}{4}$ |
| 1   | $\frac{1}{4}$ |
| 2   | $\frac{1}{4}$ |
| 3   | $\frac{1}{4}$ |

But things change if we start caring about the pairs of sides. So like, if we wanted the chance of die X landing on a 0
and die Y landing on 1, or $P(X=0, Y=1)$. The chance of that happening is actually $1/4 \cdot 1/4 = 1/16$.

Why did that change so much? Well, you don't have 4 outcomes or even 8 outcomes anymore,
you actually end up with $4 \cdot 4 = 16$ outcomes! That complicates things quite a bit. Let the table below show the change in scale.

|  | $X=0$          | $X=1$ | $X=2$ | $X=3$ |
|---|----------------|---|---|---|
| $Y=0$ | $\frac{1}{16}$ | $\frac{1}{16}$ | $\frac{1}{16}$ | $\frac{1}{16}$ |
| $Y=1$ | $\frac{1}{16}$ | $\frac{1}{16}$ | $\frac{1}{16}$ | $\frac{1}{16}$ |
| $Y=2$ | $\frac{1}{16}$ | $\frac{1}{16}$ | $\frac{1}{16}$ | $\frac{1}{16}$ |
| $Y=3$ | $\frac{1}{16}$ | $\frac{1}{16}$ | $\frac{1}{16}$ | $\frac{1}{16}$ |

Crazy right? Well don't let it intimidate you. If you roll a 0 on one die you can still roll 0, 1, 2 or 3 on the other die!
So we just get an explosion in the number of outcomes.

Where things get interesting is that each each individual pair of dice rolls
are equally likely, but that may not apply to things we care about *with those pairs*. Let me explain.

What if we want the probability that, if we were to add the dice together, that their sum would be equal to some value?
Let's explore that! Mathematically, we would write this as $P(X + Y = z)$ where $z$ is some arbitrary number we pick.

So if we're adding sides together what kinda numbers can we get? Well the smallest value is $0+0=0$ and the largest is $3+3=6$.
But are those as likely as other sums? Let's see...

We'll count up the number of dice combinations that give us different number values and see which is most likely!
Let's let $Z$ be the sum of the two dice for simplicity! $Z$ will be our two dice rolls, $z$ will be the number we pick.

For notation, I'll be doing $(\text{Dice 1 Roll}, \text{Dice 2 Roll})$ or, $(X, Y)$ for short. 

| $z$ | Outcomes satisfying $Z=z$    | $P(Z=z)$ |
|-----|------------------------------|----------|
| 0   | $(0,0)$                      | $1/16$   |
| 1   | $(0,1), (1,0)$               | $2/16$   |
| 2   | $(1,1), (2,0), (0,2)$        | $3/16$   |
| 3   | $(3,0), (2,1), (1,2), (0,3)$ | $4/16$   |
| 4   | $(3,1), (1,3), (2,2)$        | $3/16$   |
| 5   | $(3,2), (2,3)$               | $2/16$   |
| 6   | $(3,3)$                      | $1/16$   |

What we see is that some sums have way more dice rolls that work for them. 6 is super unlikely because you need both rolls
to be 3. Same with 0. Getting a sum of 3 though is really quite common as there are many combinations of rolls that get us there!

### The Key Takeaway

The table above is why true hit differs from displayed hit.

Remember, 2RN takes the average of the two dice. Which is mostly the same as this example. So most of the outcomes will end up
closer to the middle. 

The two dice individually may be **uniform random variables** but not that is not what happens when you combine them!

The math is a little more involved since we have two 100 sided dice, but this is the crux of it. 
To really put it in perspective, notice how landing both zeros has a $1/16$ chance here? Well,
with two 100 sided dice we have a total of $100 \cdot 100 = 10000$ possible outcomes. 
So it becomes a $1/10000$ chance or a percent chance of $0.01\%$. That's a hundredth of a percent!

Below is a plot to help visualize how extreme this gets. Notice how in the 1RN system it stays at the same percent chance
regardless of the hit rate whereas in the 2RN it looks more triangular? That's because of the outcomes getting smushed
into the center! You'll also notice just how many more bars there are on the joint version. 
That's just like we saw with the table being so much bigger in our example!

