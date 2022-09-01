from FuzzyCrawler_Grammar_Fuzzer import FCGFuzzer

# run this py file to get grammar based generation test cases
G1 = FCGFuzzer()
G1.Definition("opening_Bracket", ["("])
G1.Definition("single_Quote", ["' "])
G1.Definition("or", ["OR "])
G1.Definition("condition", ["1=1", "'1'='1'"])
G1.Definition("apostrophe_OR_Space", [";", " "])
G1.Definition("comment", [" --", " #", " /*"])
G1.Definition("closing_Bracket", [")"])
G1.grammar_input_Parser('O', "opening_Bracket")
G1.grammar_input_Parser('C', "single_Quote")
G1.grammar_input_Parser('C', "or")
G1.grammar_input_Parser('C', "condition")
G1.grammar_input_Parser('O', "apostrophe_OR_Space")
G1.grammar_input_Parser('C', "comment")
G1.grammar_input_Parser('O', "closing_Bracket")
G1.grammarFuzzer()
