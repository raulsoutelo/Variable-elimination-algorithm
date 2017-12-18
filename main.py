import json

from Net_class import Net

# We load the Bayesian Net from the json file
with open('BN_TB.json') as data_file:    
    Bayesian_Net = json.load(data_file)

# We run UNIT TESTS by comparing (for all possible configurations) the output
# of the bruteforce and the variable elimination algorithms.
for i in range(3**7):
    Net_var_elimin = Net(Bayesian_Net)
    Net_bruteforce = Net(Bayesian_Net)
    correct_variables = Net_var_elimin._define_variables(False, i)
    if correct_variables: 
        _ = Net_bruteforce._define_variables(False, i)
        Net_var_elimin._variable_elimination()
        Net_bruteforce._bruteforce()
        if (len(Net_var_elimin.list_of_factors) != 1
                     or abs(Net_var_elimin.list_of_factors[0].table[1] 
                     - Net_bruteforce.list_of_factors[0].table[1]) > 0.00001
                     or len(Net_var_elimin.list_of_factors[0].elements) != 1):
            raise NameError('Unit tests failed!')    
print 'all unit tests passed!'
    
# We create the network
my_Net = Net(Bayesian_Net)

# we ask the user to divide the variables into unknown(to be marginalized),
# evidence(either 0 or 1) or queried
correct_variables = False
while correct_variables == False:
    correct_variables = my_Net._define_variables()
    if correct_variables == False:
        print 'Wrong variables due to a deterministic factor! Try again!'    

#we run the variable elimination algortihm
my_Net._variable_elimination()
 
# we print the output!
if len(my_Net.list_of_factors[0].elements) == 1:
    print ('the probability of the queried variable is: ' 
                  + str(my_Net.list_of_factors[0].table[1]))
else:
    print 'the prob for the joint distribution of the queried variables is: '
    my_Net._print_factors()
