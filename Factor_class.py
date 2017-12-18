class Factor:
    def __init__(self):
        # the elements object is a dictionary where the key is the element and
        # the value is an index to look for the number in the object table. 
        # For example, if we have two elements 'a' and 'b' with index 3 and 1
        # respectively, in order to look for the number in the table for a=1
        # and b=0, we have to go to the position a*2**(3) + b*2**(1) = 1*8 
        # + 0*2 = 8. 
        self.elements = {}
        self.table = {}
 
    def _fillin_initial_element(self, key, value):
        if type(value) == list:        
            self.elements[key] = 0 
            self.table[0] = value[0]  
            self.table[1] = value[1]
        elif type(value) == dict: 
            if type(value['conditional_upon']) == unicode:
                self.elements[value['conditional_upon']] = 1
                self.elements[key] = 0
                for i in range(4):
                    self.table[i] = value[str(3-i)][2]
            elif type(value['conditional_upon']) == list:
                i = 0
                length = len(value['conditional_upon'])
                for elements_ in value['conditional_upon']:
                    self.elements[elements_] = length - i
                    i += 1
                self.elements[key] = 0
                for j in range(2**(i + 1)):
                    self.table[j] = value[str(2**(i + 1) - 1 - j)][i + 1]                                            
            else:
                raise NameError('Unpexted type!')
        else:
            raise NameError('Unpexted type!')

    def _set_evidence(self, element2set, value):
        if element2set in self.elements:
            for j in self.table.keys():
                variables2check = self._address2var(j)
                if variables2check[element2set] == 1 and value == 1:
                    address1 = self._var2address(variables2check)
                    variables2check[element2set] = 0
                    address2 = self._var2address(variables2check)
                    self.table[address2] = self.table[address1]
                    del self.table[address1]
                elif variables2check[element2set] == 0 and value == 0:
                    variables2check[element2set] = 1
                    address1 = self._var2address(variables2check)
                    del self.table[address1] 
            empty_index = self.elements[element2set]
            del self.elements[element2set]
            self._reorder(empty_index)

    def _build_factor(self, factors_involved):
        # we get the scope of the new factor and assign and index to each 
        # element               
        i = 0
        for factor in factors_involved:
            for element in factor.elements:
                if element not in self.elements:
                    self.elements[element] = i
                    i += 1
        # we fill in the table with the values from the previous factors
        for j in range(2**i):
            variables2check = self._address2var(j)
            output = 1
            for factor in factors_involved:
                address = factor._var2address(variables2check)
                output = output * factor.table[address] 
            self.table[j] = output
      
    def _var2address(self, variables2check):
        address = 0
        for element in self.elements:
            address += variables2check[element] * 2**self.elements[element]
        return address  

    def _address2var(self, address):
        max_index = 0
        for element in self.elements:
            if self.elements[element] > max_index:
                max_index = self.elements[element]
        binary_list = list(bin(2**(max_index + 1) + address))
        variables2check = {}
        for element in self.elements:
            variables2check[element] = int(binary_list[- 1
                                                  - self.elements[element]])
        return variables2check      

    def _marginalize(self, element2marginalize):
        for j in self.table.keys():   
            variables2check = self._address2var(j)
            if variables2check[element2marginalize] == 0:
                address1 = self._var2address(variables2check)
                variables2check[element2marginalize] = 1
                address2 = self._var2address(variables2check)
                self.table[address1] = (self.table[address1] 
                                      + self.table[address2])
                del self.table[address2]
        empty_index = self.elements[element2marginalize]
        del self.elements[element2marginalize]
        self._reorder(empty_index)

    def _reorder(self, empty_index):
        # in case that the indices are not consecutive (one has been removed
        # due to been known or marginalized), we move the element with the 
        # highest index to the empty index
        if empty_index < len(self.elements) and len(self.elements) > 0: 
            # we identify the element whose index will be moved
            for element in self.elements:
                if self.elements[element] == len(self.elements):
                    max_index_element = element 
                    break
            # we change the address of all values where max_index_element is
            # set to 1
            for j in self.table:
                variables2check = self._address2var(j)
                if variables2check[max_index_element] == 1:
                    address1 = self._var2address(variables2check)
                    variables2check[max_index_element] = 0
                    address2 = (self._var2address(variables2check) 
                                                   + 2**(empty_index))
                    self.table[address2] = self.table[address1]
                    del self.table[address1]
            self.elements[max_index_element] = empty_index    

    def _normalize(self):
        normalizer = 0
        for values in self.table:
            normalizer += self.table[values]
        for values in self.table:
            self.table[values] = self.table[values]/normalizer
            
