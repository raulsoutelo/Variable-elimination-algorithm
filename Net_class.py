from Factor_class import Factor          

class Net:

    def __init__(self, Bayesian_Net):
        self.list_of_factors = []
        self.evidence = {}
        self.var2eliminate = []
        for element in Bayesian_Net:
            self.evidence[element] = 5
            my_factor = Factor()
            my_factor._fillin_initial_element(element, Bayesian_Net[element])
            self.list_of_factors.append(my_factor)

    def _print_factors(self):
        for element in self.list_of_factors:
            print element.elements
            print element.table
    
    # auxiliary function to pass from base10 to base3 and define the variables
    def _ternary(self, n):
        if n == 0:
            return '0'
        nums = []
        while n:
            n, r = divmod(n, 3)
            nums.append(str(r))
        return ''.join(reversed(nums))

    def _define_variables(self, by_hand = True, code = None):
        # we define for each variable if it is in the conditioning set (and 
        # its value), it is a queried one or needs to be marginalized
        if by_hand:
            for element in self.evidence:
                try:
                    self.evidence[element] = int(raw_input('Set the ' 
                                       + element + ' variable (0:False, '
                                       + '1:True, 2:unknown or 3:queried): '))
                except ValueError:
                    print 'It has to be an integer! it will be set to unknown'
                    self.evidence[element] = 2
        # if it is not by hand, we try all possible combinations 
        else:
            self.evidence['dyspnea'] = 3
            ternary_code = list(self._ternary(code + 3**7))
            self.evidence['travel_to_asia'] = int(ternary_code[-1])
            self.evidence['tuberculosis'] = int(ternary_code[-2])
            self.evidence['smoking'] = int(ternary_code[-3])
            self.evidence['lung'] = int(ternary_code[-4])
            self.evidence['bronchitis'] = int(ternary_code[-5])
            self.evidence['xray'] = int(ternary_code[-6])
            self.evidence['tuberculosis_or_cancer'] = int(ternary_code[-7])

        # we check that the evidence is correct (case-dependent issue)
        if (((self.evidence['lung'] == 1 
                  or self.evidence['tuberculosis'] == 1)
                  and self.evidence['tuberculosis_or_cancer'] == 0) 
                  or ((self.evidence['lung'] == 0 
                  and self.evidence['tuberculosis'] == 0)
                  and self.evidence['tuberculosis_or_cancer'] == 1)): 
            return False
        else:
            return True 
        
    def _set_evidence_net(self):                        
        # we update the factors function of the evidence and update the 
        # list of variables to be marginalized
        no_queried_variables = True
        for element in self.evidence:
            if self.evidence[element] == 0 or self.evidence[element] == 1:
                for factor in self.list_of_factors[:]:
                    factor._set_evidence(element, self.evidence[element])
                    if len(factor.elements) == 0:
                        self.list_of_factors.remove(factor)
            elif self.evidence[element] == 2:
                self.var2eliminate.append(element)
            else:
                no_queried_variables = False
        if no_queried_variables:
            raise NameError('No queried variables!')
                   
    def _calculate_cost(self, element):   # We use min-neighbors 
        dependent_elements = []
        for factor in self.list_of_factors:
            if element in factor.elements:
                for element_ in factor.elements:
                    if ((element_ not in dependent_elements) 
                                         and element_ != element):
                        dependent_elements.append(element_)
        return len(dependent_elements)
    
    def _choose_var2eliminate(self):
        try:
            next_var2eliminate = self.var2eliminate[0]
            cost_var2eliminate = self._calculate_cost(next_var2eliminate)
            for element in self.var2eliminate:
                aux_cost_var2eliminate = self._calculate_cost(element)
                if aux_cost_var2eliminate < cost_var2eliminate:
                    next_var2eliminate = element 
                    cost_var2eliminate = aux_cost_var2eliminate
            return next_var2eliminate
        except:
            return None

    def _eliminate_variable(self, element):
        factors_involved = []
        for factor in self.list_of_factors:
            if element in factor.elements:
                factors_involved.append(factor)
        new_factor = Factor()
        new_factor._build_factor(factors_involved)
        new_factor._marginalize(element)
        # we delete the previous factors
        for factor in factors_involved[:]:
            self.list_of_factors.remove(factor)
        # we add the new factor
        if len(new_factor.elements) > 0:
            self.list_of_factors.append(new_factor)
        # we delete the variable we have just deleted  
        self.var2eliminate.remove(element) 

    def _mult_factors(self): 
        new_factor = Factor()
        new_factor._build_factor(self.list_of_factors)
        # we delete the previous factors
        for factor in self.list_of_factors[:]:
            self.list_of_factors.remove(factor)
        # we add the new factor
        self.list_of_factors.append(new_factor)

    def _variable_elimination(self):
        self._set_evidence_net()
        # if there are variables to eliminate we keep eliminating them
        while True:
            var2eliminate = self._choose_var2eliminate()
            if var2eliminate == None:
                break
            self._eliminate_variable(var2eliminate)
        # we multiply all remaining factors
        if len(self.list_of_factors) > 1:
            self._mult_factors()
        # we normalize the remaining factor
        self.list_of_factors[0]._normalize()

    def _bruteforce(self):
        self._set_evidence_net()
        new_factor = Factor()
        new_factor._build_factor(self.list_of_factors)
        for element in self.var2eliminate[:]:
            new_factor._marginalize(element)
        # we delete the previous factors
        for factor in self.list_of_factors[:]:
            self.list_of_factors.remove(factor)
        # we add the new factor
        self.list_of_factors.append(new_factor)     
        # we normalize the remaining factor
        self.list_of_factors[0]._normalize()  


