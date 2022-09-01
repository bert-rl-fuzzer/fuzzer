import sys
from pyparsing import *


class parser:
    ParserElement.enablePackrat()

    LPAR, RPAR, COMMA = map(Suppress, "(),")
    DOT, STAR = map(Literal, ".*")
    select_stmt = Forward().setName("select statement")

    # keywords
    keywords = {
        k: CaselessKeyword(k)
        for k in """\
        UNION ALL AND OR INTERSECT EXCEPT COLLATE ASC DESC ON USING NATURAL INNER CROSS LEFT OUTER JOIN AS INDEXED NOT
        SELECT DISTINCT FROM WHERE GROUP BY HAVING ORDER LIMIT OFFSET OR CAST ISNULL NOTNULL NULL IS BETWEEN ELSE END
        CASE WHEN THEN EXISTS IN LIKE GLOB REGEXP MATCH ESCAPE CURRENT_TIME CURRENT_DATE CURRENT_TIMESTAMP TRUE FALSE
        """.split()
    }
    vars().update(keywords)

    any_keyword = MatchFirst(keywords.values())

    quoted_identifier = QuotedString('"', escQuote='""')
    identifier = (~any_keyword + Word(alphas, alphanums + "_")).setParseAction(
        pyparsing_common.downcaseTokens
    ) | quoted_identifier
    collation_name = identifier.copy()
    column_name = identifier.copy()
    column_alias = identifier.copy()
    table_name = identifier.copy()
    table_alias = identifier.copy()
    index_name = identifier.copy()
    function_name = identifier.copy()
    parameter_name = identifier.copy()
    database_name = identifier.copy()

    comment = "--" + restOfLine
    comment1 = "/*" + restOfLine
    comment2 = "#" + restOfLine
    eofstatement = ";" + restOfLine
    # expression
    expr = Forward().setName("expression")

    numeric_literal = pyparsing_common.number
    string_literal = QuotedString("'", escQuote="''")
    blob_literal = Regex(r"[xX]'[0-9A-Fa-f]+[@$]'")
    literal_value = (
            numeric_literal
            | string_literal
            | blob_literal
            | TRUE
            | FALSE
            | NULL
            | CURRENT_TIME
            | CURRENT_DATE
            | CURRENT_TIMESTAMP
    )
    bind_parameter = Word("?", nums) | Combine(oneOf(": @ $") + parameter_name)
    type_name = oneOf("TEXT REAL INTEGER BLOB NULL")

    expr_term = (
            CAST + LPAR + expr + AS + type_name + RPAR
            | EXISTS + LPAR + select_stmt + RPAR
            | function_name.setName("function_name")
            + LPAR
            + Optional(STAR | delimitedList(expr))
            + RPAR
            | literal_value
            | bind_parameter
            | Group(
        identifier("col_db") + DOT + identifier("col_tab") + DOT + identifier("col")
    )
            | Group(identifier("col_tab") + DOT + identifier("col"))
            | Group(identifier("col"))
    )

    NOT_NULL = Group(NOT + NULL)
    NOT_BETWEEN = Group(NOT + BETWEEN)
    NOT_IN = Group(NOT + IN)
    NOT_LIKE = Group(NOT + LIKE)
    NOT_MATCH = Group(NOT + MATCH)
    NOT_GLOB = Group(NOT + GLOB)
    NOT_REGEXP = Group(NOT + REGEXP)

    UNARY, BINARY, TERNARY = 1, 2, 3
    expr << infixNotation(
        expr_term,
        [
            (oneOf("- + ~") | NOT, UNARY, opAssoc.RIGHT),
            (ISNULL | NOTNULL | NOT_NULL, UNARY, opAssoc.LEFT),
            ("||", BINARY, opAssoc.LEFT),
            (oneOf("* / %"), BINARY, opAssoc.LEFT),
            (oneOf("+ -"), BINARY, opAssoc.LEFT),
            (oneOf("<< >> & |"), BINARY, opAssoc.LEFT),
            (oneOf("< <= > >="), BINARY, opAssoc.LEFT),
            (
                oneOf("= == != <>")
                | IS
                | IN
                | LIKE
                | GLOB
                | MATCH
                | REGEXP
                | NOT_IN
                | NOT_LIKE
                | NOT_GLOB
                | NOT_MATCH
                | NOT_REGEXP,
                BINARY,
                opAssoc.LEFT,
            ),
            ((BETWEEN | NOT_BETWEEN, AND), TERNARY, opAssoc.LEFT),
            (
                (IN | NOT_IN) + LPAR + Group(select_stmt | delimitedList(expr)) + RPAR,
                UNARY,
                opAssoc.LEFT,
            ),
            (AND, BINARY, opAssoc.LEFT),
            (OR, BINARY, opAssoc.LEFT),
        ],
    )

    compound_operator = UNION + Optional(ALL) | INTERSECT | EXCEPT

    ordering_term = Group(
        expr("order_key")
        + Optional(COLLATE + collation_name("collate"))
        + Optional(ASC | DESC)("direction")
    )

    join_constraint = Group(
        Optional(ON + expr | USING + LPAR + Group(delimitedList(column_name)) + RPAR)
    )

    join_op = COMMA | Group(
        Optional(NATURAL) + Optional(INNER | CROSS | LEFT + OUTER | LEFT | OUTER) + JOIN
    )

    join_source = Forward()
    single_source = (
            Group(database_name("database") + DOT + table_name("table*") | table_name("table*"))
            + Optional(Optional(AS) + table_alias("table_alias*"))
            + Optional(INDEXED + BY + index_name("name") | NOT + INDEXED)("index")
            | (LPAR + select_stmt + RPAR + Optional(Optional(AS) + table_alias))
            | (LPAR + join_source + RPAR)
    )

    join_source <<= (
            Group(single_source + OneOrMore(join_op + single_source + join_constraint))
            | single_source
    )

    # result_column = "*" | table_name + "." + "*" | Group(expr + Optional(Optional(AS) + column_alias))
    result_column = Group(
        STAR("col")
        | table_name("col_table") + DOT + STAR("col")
        | expr("col") + Optional(Optional(AS) + column_alias("alias"))
    )

    select_core = (
            SELECT
            + Optional(DISTINCT | ALL)
            + Group(delimitedList(result_column))("columns")
            + Optional(FROM + join_source("from*"))
            + Optional(WHERE + expr("where_expr"))
            + Optional(
        GROUP
        + BY
        + Group(delimitedList(ordering_term))("group_by_terms")
        + Optional(HAVING + expr("having_expr"))
    )
    )

    select_stmt << (
            select_core
            + ZeroOrMore(compound_operator + select_core)
            + Optional(ORDER + BY + Group(delimitedList(ordering_term))("order_by_terms"))
            + Optional(
        LIMIT
        + (Group(expr + OFFSET + expr) | Group(expr + COMMA + expr) | expr)("limit")
    )
    )

    select_stmt.ignore(comment)
    select_stmt.ignore(comment1)
    select_stmt.ignore(comment2)
    select_stmt.ignore(eofstatement)

    def main(self, testString):
        success, _ = self.select_stmt.runTests(testString, printResults=False)
        # print("\n{}".format("OK" if success else "FAIL"))
        return 0 if success else 1


if __name__ == "__main__":
    p = parser()
    status = p.main(
        "SELECT * FROM abc where username=def  UNION select passwrd email from DUAL #")  # from GCheckModifier
    if status == 1:
        print("failed")
    else:
        print("pass")
    # SELECT * FROM abc where username=def UNION select version FROM v$instance--
    # "SELECT * FROM abcd UNION SELECT Null,email,pass,Null FROM user--"
    # "SELECT * FROM abcd UNION SELECT Null,email,pass,Null FROM user#"
    # "SELECT * FROM abcd UNION SELECT Null,email,pass,Null FROM user/*"
