# BertRLFuzzer: A Grammar-preserving BERT-based Reinforcement Learning Fuzzer

We present a novel tool BertRLFuzzer, a grammar-preserving BERT-based Reinforcement Learning fuzzer aimed at finding security vulnerabilities, especially  SQL injection (SQLi) and Cross-site Scripting (XSS). Briefly, our method works as follows: given a list of grammar-adhering seed inputs, the fuzzer performs grammar-preserving and attack-provoking mutation operations on these seed inputs to generate candidate attack vectors. The core innovations of our tool is the combined use of two machine learning concepts. The first key idea is the use of a BERT-style Transformer model that enables the fuzzer to mutate strings in a grammar-preserving way without requiring the user to specify complex input grammars of victim applications, and the second is the use of a Proximal Policy Optimization (PPO)-based reinforcement learning (RL) technique that enables the fuzzer to automatically learn effective mutation operators. The ability of BERT-style models to learn grammars is key. This feature enables BertRLFuzzer to be grammar-preserving and learn attack vector patterns, and also enables BertRLFuzzer to be extensible, i.e., the user can extend to a variety of victim applications and attack vectors without explicitly modifying the fuzzer. Further, the mutation operators learnt via RL in BertRLFuzzer enable it to automatically search a space of attack vectors in a heuristic way that are specialized to a victim application. Finally, an additional advantage of using RL is that, unlike supervised learning based fuzzers, we don't need to create labeled training data.

### Running the example website

1) Make sure you have docker installed
2) Go to example_website/docker
3) On the CLI, execute `docker-compose up`

You will find the following two webpages: 
- http://localhost/demo/example_mysql_injection_login.php
- http://localhost/demo/example_mysql_injection_search_box.php

### Other benchmark SUTs

- [Classifieds](https://github.com/COLA-Laboratory/issta2020/blob/master/SUT/classifieds.war)
- [Employee](https://github.com/COLA-Laboratory/issta2020/blob/master/SUT/empldir.war)
- [Portal](https://github.com/COLA-Laboratory/issta2020/blob/master/SUT/portal.war)
- [Events](https://github.com/COLA-Laboratory/issta2020/blob/master/SUT/events.war)
- [Webchess](https://sourceforge.net/projects/webchess/)
- [Faqforge](https://sourceforge.net/projects/faqforge/files/faqforge/1.3.2/)
- [geccBBlite](https://sourceforge.net/projects/geccnuke/files/geccBB/geccBBlite/)
- [SchoolMate](https://sourceforge.net/projects/schoolmate/files/SchoolMate/SchoolMate%20V1.5.4/)

### Running the tool 

1) Setup the environment using requirements.txt
2) python attention_fuzzer/main.py --expt_tag <suitable_tag_for_future_ref> --model_variant "BERT" --logging "normal"
