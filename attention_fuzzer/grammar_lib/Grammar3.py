from FuzzyCrawler_Grammar_Fuzzer import FCGFuzzer
G3=FCGFuzzer()
G3.Definition("opening_Bracket", ["("])
G3.Definition("single_Quote", ["' "])
G3.Definition("orderby", ["ORDER BY "])
G3.Definition("Number", ["0","1","2","3","4","5","6","7","8","9"])
G3.Definition("apostrophe_OR_Space", [";"," "])
G3.Definition("comment", [" --"," #"," /*"])
G3.Definition("closing_Bracket", [")"])
G3.grammar_input_Parser('O',"opening_Bracket")
G3.grammar_input_Parser('C',"single_Quote")
G3.grammar_input_Parser('C',"orderby")
G3.grammar_input_Parser('C',"Number")
# G3.grammar_input_Parser('O',"Number") # 2 digit
# G3.grammar_input_Parser('O',"Number") # 3 digit
# G3.grammar_input_Parser('O',"Number") # 4 digit
G3.grammar_input_Parser('O',"apostrophe_OR_Space")
G3.grammar_input_Parser('C',"comment")
G3.grammar_input_Parser('O',"closing_Bracket")
G3.grammarFuzzer()