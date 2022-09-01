# names_grammar.py
import gramfuzz
from gramfuzz.fields import *

class NRef(Ref):
    cat = "em_def"
class NDef(Def):
    cat = "em_def"

Def("email",
    NRef("user_name"),
    Opt(NRef("sub_dom")),
    NRef("domain"),
    NRef("suffix"),
cat="email", sep="")

NDef("user_name",
    String(min=4, max=8, charset=String.charset_alphanum), "@"
)

NDef("sub_dom",
    String(min=2, max=5, charset=String.charset_alpha_lower), "."
)

NDef("domain",
    String(min=2, max=5, charset=String.charset_alpha_lower), "."
)

NDef("suffix",
    Or("in", "com", "ca", "org", "edu", "ai", String(min=2, max=3, charset=String.charset_alpha_lower)), ""
)

