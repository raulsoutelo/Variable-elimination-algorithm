# Variable elimination algorithm

In this repository I have implemented from scratch the Bruteforce and Variable elimination algorithms to 
perform exact inferece in probabilistic graphical models. The Bayesian network and the fictitious conditional
probability tables have been taken from the paper: 

@article{lauritzen1988local,
  title={Local computations with probabilities on graphical structures and their application to expert systems},
  author={Lauritzen, Steffen L and Spiegelhalter, David J},
  journal={Journal of the Royal Statistical Society. Series B (Methodological)},
  pages={157--224},
  year={1988},
  publisher={JSTOR}
}

The code is able to infer the joint probability for any combination of variables, providing the others are either 
unknown or seen (True or false).

How to use the code:

In order to run the code you only have to run the main.py script. First, some units tests will be run. 
Then, you will create the network with the data from the json file and you will be asked to give a value for each
variable (evidence (True or False), unknown or queried). All functionalities are implemnted in the Net and Factor classes.
If only one variable is queried, the program will output the probability of this variable. If more than one is queried,
a table will be output with the joint distribution of all queried variables.

In order to use the code to perform inference in a different Bayesian network, please create another json file describing
the Bayesian network in which to do inference in the same manner than the one given. 

Validate the implementation (Unit tests):

The original algorithm intended to perform inference was the variable elimination algortithm. In order to test the
implementation, I have decided to implement the naive algorithm as well (Bruteforce). They share very little code
which was reviewed carefully. Both algortihms provided the same output for each possible input. 

Complexity of the algorithms:

The Bruteforce algorithm combines all factors (in our case, probability distributions) into a 
new and big factor and marginalize over the variables that are not queried. This requires creating a new factor
whose scope are all the variables involved in the problem.
For binary variables, being n the number of variables, the complexity of the bruteforce algorithm is 2^(n) 
because we need to fill in in the table the values of 2^(n) positions. 
This means that it cannot be bounded in polynomial time. This is a NP-hard problem.

In the variable elimination algortihm, we keep eliminating variables by combining the factors that contain
this variable. For example, if we want to eliminate b by combining the factors F1(a,b) and F2(b,c), we need 
to create a factor F3'(a,b,c) and marginalize over b to get F3(a,c). For binary variables, the complexity of
this operation would be 2^(3). In general, the complexity of the variable elimination algorithm (for binary 
variables) would be n*2^(k), being n the number of variables and k the maximum size of the factor created before
marginalizing.

Choosing the right ordering to eliminate the variables to eliminate is also a NP-hard problem. In practice,
there are heuristics that give reasonably good performance. In this implementation, I have used the Min-neighbors
policy that consists of choosing the variable with less dependent variables. Since after combining factors, the 
new factor is not a probability distribution anymore, I consider a Markov Network (undirected) and calculate the
dependent variables as the ones that share any factor.
