class FCGrammarChecker:
    # not using currently because of recursion; use SQLChecker.py instead
    Grammar_Definition_Values = {}
    optional_Keys_Position = []
    optional_Definition_Places_Values = {}
    compulsary_Keys_Position = []
    compulsary_Definition_Places_Values = {}
    Total_Grammar_keys_Position = {}
    Position = [0]
    grammarVals = []

    def Definition(self, name, values):
        self.Grammar_Definition_Values[name] = values
        self.grammarVals.append(values)

    def grammar_input_Parser(self, requirement, name):
        if requirement == 'O':
            self.optional_Keys_Position.append(self.Position[0])
            self.optional_Definition_Places_Values[self.Position[0]] = name
        else:
            self.compulsary_Keys_Position.append(self.Position[0])
            self.compulsary_Definition_Places_Values[self.Position[0]] = name
        self.Total_Grammar_keys_Position[self.Position[0]] = name
        self.Position[0] = self.Position[0] + 1

    def getInput(self):
        self.Definition("First_Name",
                        ["Alice", "Bob", "Charlie"])
        self.Definition("Last_Name", [".G", ".K", ".A"])
        self.Definition("@", ["@"])
        self.Definition("Mail", ["gmail", "outlook", "hotmail"])
        self.Definition("ending", [".com", ".in", ".ca"])
        self.Definition("Enter", ["--", "#", "/*"])
        self.grammar_input_Parser('C', "First_Name")
        self.grammar_input_Parser('O', "Last_Name")
        self.grammar_input_Parser('C', "@")
        self.grammar_input_Parser('C', "Mail")
        self.grammar_input_Parser('C', "ending")
        self.grammar_input_Parser('O', "Enter")

    def grammarChecker(self, stringAsList):
        self.getInput()
        grammarvalcount = 0
        temp = 0
        if len(self.compulsary_Keys_Position) <= len(stringAsList):
            for i in range(len(stringAsList)):
                if stringAsList[i] in self.grammarVals[grammarvalcount]:
                    grammarvalcount = grammarvalcount + 1
                elif stringAsList[i] not in self.grammarVals[grammarvalcount]:
                    if grammarvalcount in self.optional_Keys_Position:
                        continue
                    else:
                        temp = 1
                        break
        else:
            temp = 1
        if temp == 0:
            print("Grammar Parsed")
        else:
            print("Grammar not parsed")

