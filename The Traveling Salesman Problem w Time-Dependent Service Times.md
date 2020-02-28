The Traveling Salesman Problem w/ Time-Dependent Service Times

https://www.cirrelt.ca/documentstravail/CIRRELT-2014-48.pdf



Interesting papers:

* Time-dependent asymmetric traveling salesman problem with time windows: Properties and an exact algorithm -- https://www.sciencedirect.com/science/article/abs/pii/S0166218X18304827#! -- requested the article.
* An asymmetric TSP with time windows and with time-dependent travel times and costs: An exact solution through a graph transformation -- https://www.sciencedirect.com/science/article/abs/pii/S0377221706011854 -- requested the article
* The Time Dependent Traveling Salesman Problem: Polyhedra and Algorithm -- complicated
* Solving Time Dependent Traveling Salesman Problems with Time Windows -- http://www.optimization-online.org/DB_FILE/2018/05/6640.pdf -- good paper, but we don't have time windows
  * Called TSPTW
  * TD-TSPTW
  * Second objective is the duration objective -- decrease duration the most
  * Based on Dynamic Discretization Discovery (DDD) -- Boland 2017
  * "While the computational performance of existing methods for the TD-TSPTW is highly sensitive to the frequency with which travel times change, our results indicate that the new solution method is not"
* https://www.researchgate.net/publication/11769087_Optimization_of_the_time-dependent_traveling_salesman_problem_with_Monte_Carlo_methods -- this seems promising!
  * http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.548.8500&rep=rep1&type=pdf
  * Physical optimization algorithms
* Step 1: Use simulated annealing:  https://toddwschneider.com/posts/traveling-salesman-with-simulated-annealing-r-and-shiny/ 

1. Make random, acceptable, day trips (maybe from 10 locations)
2. Use MCMC or simulated annealing to pick a route for the first day
3. Then do the same for day 2 with the leftover trips

How many api calls? 

Permutations of 10 things chosen 2:

10!/ (10 -2)! = 10 * 9 = 90. So there are 90 combinations - then I need at least 48 pulls of each 48 * 90 = 4320

https://cloud.google.com/maps-platform/pricing/sheet/

* Make a postgres db
* Use distance matrix -https://developers.google.com/maps/documentation/distance-matrix/intro -- it says you can have multiple elements per request? Look at advanced
* make database of place_ids for places. (do the geocoding ahead of time).

15 = 10080 calls.





Plan:

For each 2 places, it's going to be 96 elements called. 

If we have 15 places, that's 15 p 2, or 15 * 14 = 210. 210 * 96 = 1260 + 18900 = 20160

So man, 15 places is it for the month. 