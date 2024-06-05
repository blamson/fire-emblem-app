### The Inequality

You might say "well, why is the probability in the tool giving 0% chance for 0 if it's just really small"?
Shouldnt $1/10000$ still be possible in game? Not quite.

Remember earlier when we added the four rows together for $P(X<4)$? This is essentially an inequality we'd see with the 2RN system as well.
So not only do we combine two random variables, the combination of the two rolls must also be *lower* than the displayed hit. 

What we've really got with this system looks like so:

$$
P\left(\frac{X+Y}{2} < z \right)
$$

So we add the two rolls together, divide them by 2 and see if that is lower than the displayed hit rate.

So, if we were to look at $z=0$ where the displayed hit is 0 what we'd get is $P\left(\frac{X+Y}{2} < 0 \right)$ which isn't possible. 
The lowest value we can get *is* 0. We can't go below it. That's also why there isn't a 199 or 200 on the pmf plot earlier. 
The dice max out at 99, so you can't get $99 + 100 = 199$ or $100 + 100 = 200$. Since you can't possibly get to those values,
a displayed hit above $199/2 = 99.5$ is guaranteed.

### Addressing that division

Let's entertain the smaller hit rates for example here. 

Or, more specifically, a hit rate of 1%. So $z=1$

$$
P\left( \frac{X+Y}{2} < 1 \right)
$$

For this I actually like to move the 2 over to the other side! I think it's more intuitive. So we get

$$
P\left( \frac{X+Y}{2} < 1 \right) = P\left( X+Y < 2 \cdot 1 \right)
$$

Okay, so now this means we need a sum less than 2. Which outcomes satisfy that?

$$
(0,0), (1,0), (0,1)
$$

That's 3 possible outcomes which gives us $3/10000$ or $0.03\%$. Same as the table! Bingo.

### Conclusion: Let's add some perspective and end this

Let's make sure we haven't gotten lost in the math and remember what super low hit rate actually means.

If we were using just a single dice ranging from 0 to 99 (like FE 1-5) and checking for $P(X<1)$ we only have $X=0$ as a possible outcome, but that's still $1/100=1\%$. 
Way more likely (and has probably gotten you killed if you've played Thracia 776). This is why so many of us also have stories of getting killed by $1\%$ critical hits.
Because those just roll a single die. $1/100$ is going to happen eventually. $3/10000$ is FAR less likely.

As for why this results in really high hit rates above 50, remember that we add ALL of the rows that work together.
So there's a ton of outcomes chunked into the middle so those hitrates skyrocket quickly when we add them all together.
This is why low hit rates are so much lower than displayed and high hit rates are so much higher. 
Hit rates below $50\%$ can't benefit from the bulk of the outcomes that sit in the middle, whereas the really high
hit rates can use them to inflate their own probabilities.

To wrap this up I've included another set of plots that showcase how extreme these differences can be. Really examine
how different the upper and lower values get for 1RN and 2RN. I hope this writeup helped provide more insight
into how these games subtly lie to you. It's honestly fascinating and I enjoyed doing this deep dive into the math.
