


fuzzer.load_grammar("email_grammar.py")
names = fuzzer.gen(cat="email", num=10)
print(names)