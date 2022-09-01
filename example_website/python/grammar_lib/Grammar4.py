from FuzzyCrawler_Grammar_Fuzzer import FCGFuzzer
G4=FCGFuzzer()
G4.Definition("opening_Bracket", ["(","["])
G4.Definition("single_Quote", ["' "])
G4.Definition("union_select", ["UNION select"])
G4.Definition("Null", ["NULL"])
G4.Definition("SNull", [",NULL"])
G4.Definition("Comma", [","])
G4.Definition("email", [",email"])
G4.Definition("pass", [",pass",",password"])
G4.Definition("apostrophe_OR_Space", [";"," "])
G4.Definition("Dual", [" from DUAL"," from user"])
G4.Definition("comment", [" --"," #"," /*"])
G4.Definition("closing_Bracket", [")"])
G4.Definition("Space",[" "])
G4.grammar_input_Parser('O',"opening_Bracket")
G4.grammar_input_Parser('C',"single_Quote"),
G4.grammar_input_Parser('O',"closing_Bracket")
G4.grammar_input_Parser('O',"Space")
G4.grammar_input_Parser('C',"union_select"),
G4.grammar_input_Parser('',"Space")
G4.grammar_input_Parser('C',"Null")
G4.grammar_input_Parser('O',"email")
G4.grammar_input_Parser('O',"pass")
G4.grammar_input_Parser('O',"SNull")
#Can be removed-------------------------
#------------------------------------------
G4.grammar_input_Parser('C',"Dual")
G4.grammar_input_Parser('O',"apostrophe_OR_Space")
G4.grammar_input_Parser('C',"comment"),
G4.grammar_input_Parser('O',"closing_Bracket")
G4.grammarFuzzer()