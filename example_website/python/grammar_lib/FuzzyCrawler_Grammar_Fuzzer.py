class FCGFuzzer:
    # Used by Grammar<x>.py files
    Grammar_Definition_Values={}
    optional_Keys_Position=[]
    optional_Definition_Places_Values={}
    compulsary_Keys_Position=[]
    compulsary_Definition_Places_Values={}
    Total_Grammar_keys_Position={}
    Position=[0]
    grammarVals=[]

    def clear(self):
        self.Grammar_Definition_Values={}
        self.optional_Keys_Position=[]
        self.optional_Definition_Places_Values={}
        self.compulsary_Keys_Position=[]
        self.compulsary_Definition_Places_Values={}
        self.Total_Grammar_keys_Position={}
        self.Position=[0]
        self.grammarVals=[]

    def Definition(self,name,values):
        self.Grammar_Definition_Values[name]=values
        self.grammarVals.append(values)
    
    def grammar_input_Parser(self,requirement,name):
        if requirement=='O':
            self.optional_Keys_Position.append(self.Position[0])
            self.optional_Definition_Places_Values[self.Position[0]]=name
        else:
            self.compulsary_Keys_Position.append(self.Position[0])
            self.compulsary_Definition_Places_Values[self.Position[0]]=name
        self.Total_Grammar_keys_Position[self.Position[0]]=name
        self.Position[0]=self.Position[0]+1
    
    def find_Combinations(self,input_List, r):
        pool = tuple(input_List)
        n = len(pool)
        if r > n:
            return
        indices = list(range(r))
        yield list(pool[i] for i in indices)
        while True:
            for i in reversed(range(r)):
                if indices[i] != i + n - r:
                    break
            else:
                return
            indices[i] += 1
            for j in range(i+1, r):
                indices[j] = indices[j-1] + 1
            yield list(pool[i] for i in indices)
    
    def find_all_optional_keys_position_Combinations(self):
        all_optional_keys_position_Combinations=[]
        for i in range(len(self.optional_Definition_Places_Values) + 1):
            combinations_object = self.find_Combinations(self.optional_Definition_Places_Values, i)
            combinations_list = list(combinations_object)
            all_optional_keys_position_Combinations += combinations_list
        return all_optional_keys_position_Combinations
    
    def find_all_Combinations_Possible_Positions(self,all_optional_keys_position_Combinations):
        final_Combinations=[]
        all_Combinations_Possible_Positions=all_optional_keys_position_Combinations
        for i in range(len(all_optional_keys_position_Combinations)):
            for j in range(len(self.compulsary_Keys_Position)):
                all_Combinations_Possible_Positions[i].append(self.compulsary_Keys_Position[j])
            all_Combinations_Possible_Positions[i].sort()
        for i in range(len(all_Combinations_Possible_Positions)):
            kin=[]
            for j in range(len(all_Combinations_Possible_Positions[i])):
                kin.append(self.Grammar_Definition_Values[self.Total_Grammar_keys_Position[all_Combinations_Possible_Positions[i][j]]])
            final_Combinations.append(kin)
        return final_Combinations

    def find_Number_Of_Combinations_possible(self,final_Combinations):
        ans=0
        for t in range(len(final_Combinations)):
            combi=1
            for i in range(len(final_Combinations[t])):
                combi=combi*len(final_Combinations[t][i])
            ans=ans+combi
        return ans
    
    def product(self,*args, repeat=1):
        pools = [list(pool) for pool in args] * repeat
        result = [[]]
        count=0
        for pool in pools:
            result = [x+[y] for x in result for y in pool]
        count=1
        for prod in result:
            tempo=""
            for i in prod:
                tempo=tempo+i
            yield tempo
            print(tempo)
    
    def productL(self,*args, repeat=1):
        pools = [list(pool) for pool in args] * repeat
        result = [[]]
        count=0
        for pool in pools:
            result = [x+[y] for x in result for y in pool]
        count=1
        for prod in result:
            yield prod
    
    def find_final_Combinations(self,final_Combinations):
        res_Strings=[]
        res_Lists=[]
        for i in range(len(final_Combinations)):
            ter=final_Combinations[i]
            res_Strings= res_Strings+(list(self.product(*ter)))
            res_Lists=res_Lists+(list(self.productL(*ter)))
        return res_Strings,res_Lists

    def grammarFuzzer(self):
        #self.getInput()
        all_optional_keys_position_Combinations=self.find_all_optional_keys_position_Combinations()
        final_Combinations=self.find_all_Combinations_Possible_Positions(all_optional_keys_position_Combinations)
        #print("Number of combinations possible:",end="")
        ans=self.find_Number_Of_Combinations_possible(final_Combinations)
        #print(ans)
        res_Strings,res_Lists=self.find_final_Combinations(final_Combinations)
        #print(res_Lists)
        #print(res_Strings)
