import logging
import os
import random
import sqlite3

"""
For a UNION query to work, two key requirements must be met:
- The individual queries must return the same number of columns.
- The data types in each column must be compatible with the individual queries.

Content-based Blind SQL Injection:

- This returns TRUE, and the details of item with ID 34 are shown. This is a clear indication that the page is vulnerable.

- SELECT column_name, column_name_2 FROM table_name WHERE ID = 34 and 1=1

- SELECT name, description, price FROM Store_table WHERE ID = 34 and 1=1
"""

def define_expt_tag(EXPT_TAG):
    global expt_tag
    expt_tag = EXPT_TAG

# Sample table name and corresponding column name from the seed database

def get_sampled_table_and_col(preferred_main):
    conn = sqlite3.connect(f'database/{expt_tag}/test.db')
    fuzzing_success, exception_success = False, False

    cursor = conn.execute(f"SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    output = [row[0] for row in cursor]

    conn.close()

    all_table_names = [o_ for o_ in output if 'testfts' not in o_]

    selected_table_name = random.sample(all_table_names, 1)[0]

    if preferred_main and 'user' in all_table_names:
        selected_table_name = 'user'
    elif not preferred_main and 'faq' in all_table_names:
        selected_table_name = 'faq'

    conn = sqlite3.connect(f'database/{expt_tag}/test.db')

    cursor = conn.execute(f"SELECT name from PRAGMA_table_info('{selected_table_name}');")
    possible_columns = [row[0] for row in cursor]

    conn.close()

    return selected_table_name, possible_columns


# Creating seed database

def create_database(stop_random=False, test_mode=False):
    choose_col1 = random.choice([True, False])
    choose_col2 = random.choice([True, False])
    choose_col3 = random.choice([True, False])
    choose_col4 = random.choice([True, False])
    choose_col5 = random.choice([True, False])
    choice_escape_seq = random.choice([True, False])
    choose_new_table = random.choice([True, False])

    if test_mode:
        choose_col1, choose_col2, choose_col3, choose_col4, choose_col5, choose_new_table = [True] * 6

    if stop_random:
        choose_col1, choose_col2, choose_col3, choose_col4, choose_col5, choose_new_table = [False] * 6

    logging.info(f"Create database: choose_col1={choose_col1}, choose_col2={choose_col2}, choose_new_table={choose_new_table}")

    table_name1 = "user"
    table_name2 = "faq"
    new_col1_create, new_col2_create, new_col3_create, new_col4_create, new_col5_create = [""] * 5
    col1_insert_into, col2_insert_into, col3_insert_into, col4_insert_into, col5_insert_into = [("", "")] * 5

    if choose_col1: new_col1_create = "col1 varchar(255) NOT NULL,\n"
    if choose_col2: new_col2_create = "col2 varchar(255) NOT NULL,\n"

    sql1 = f""" CREATE TABLE {table_name1}
    (
      id integer NOT NULL PRIMARY KEY,
      {new_col1_create}{new_col2_create}
      fname varchar(255) NOT NULL,
      lname varchar(255) NOT NULL,
      email varchar(400) NOT NULL,
      pass varchar(255) NOT NULL
    ) """

    if choose_col1: col1_insert_into = ("col1,", "'C1',")
    if choose_col2: col2_insert_into = ("col2,", "'C2',")

    sql2 = f""" INSERT INTO {table_name1}
      (fname,lname,{col1_insert_into[0]}{col2_insert_into[0]}
      email,pass) VALUES
    ('John','Doe',{col1_insert_into[1]}{col2_insert_into[1]}'john.doe@example.com','Doe@123');"""

    #     if choice_escape_seq:
    #         sql2 = f''' INSERT INTO {table_name1}
    #           (fname,lname,{col1_insert_into[0]}{col2_insert_into[0]}
    #           email,pass) VALUES
    #         ("John","Doe",{col1_insert_into[1]}{col2_insert_into[1]}"john.doe@example.com","Doe@123");'''

    sql3 = f""" CREATE TABLE {table_name2} (
      id integer NOT NULL PRIMARY KEY,
      {new_col1_create}{new_col2_create}
      question varchar(500) NOT NULL,
      answer text NOT NULL,
      date datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
    ) """

    sql4 = f""" INSERT INTO {table_name2} (id, {col1_insert_into[0]}{col2_insert_into[0]} question, answer, date) VALUES
    (1, {col1_insert_into[1]}{col2_insert_into[1]}'Is FuzzyCrawler Free to Use', 'Yes, FuzzyCrawler is an open-source tool that is licenced under the standard MIT licence. ', '2021-07-03 00:33:34'),
    (2, {col1_insert_into[1]}{col2_insert_into[1]}'Can I Use FuzzyCrawler For Commercial Purposes', 'Yes, the FuzzyCrawler tool was designed to offer modern fuzzing methods for various applications and therefore is very easy to integrate through modern testing workflows such as those implemented through CI/CD Pipelines. It can also be used with existing projects to detect vulnerabilities in existing software.', '2021-07-03 00:33:34'),
    (3, {col1_insert_into[1]}{col2_insert_into[1]}'Which is the best Fuzzing method', 'Every Application has different needs and use-case scenarios which means that no one technique can be considered better than others in general. Thus since each software needs is different, FuzzyCrawler offers multiple techniques to support a wider spectrum for testing.', '2021-07-03 00:43:46'),
    (4, {col1_insert_into[1]}{col2_insert_into[1]}'I need multiple types of fuzzers for my project, do I need to download from multiple GitHub repo', 'No, FuzzyCrawler offers a single Github repo that can easily integrate with your project and offer the various types of fuzzers supported by FuzzyCrawler in a single package. ', '2021-07-03 00:43:46');
    """

    if choose_new_table:
        sql5 = f""" CREATE TABLE new_table3
        (
          id integer NOT NULL PRIMARY KEY,
          newcol1 varchar(255) NOT NULL,
          newcol2 varchar(255) NOT NULL,
          newcol3 varchar(400) NOT NULL,
          newcol4 varchar(255) NOT NULL
        ) """
    else:
        sql5 = ""

    if os.path.isfile(f'database/{expt_tag}/test.db'):
        os.remove(f'database/{expt_tag}/test.db')
        logging.info("Deleted old DB successfully")
    print(f'database/{expt_tag}/test.db')
    if not os.path.exists(f'database/{expt_tag}'):
        os.makedirs(f'database/{expt_tag}')
    conn = sqlite3.connect(f'database/{expt_tag}/test.db')
    logging.info("Opened database successfully")

    for sql_st in [sql1, sql2, sql3, sql4]:
        conn.execute(sql_st)

    if sql5:
        conn.execute(sql5)

    conn.commit()
    logging.info("Records created successfully")
    conn.close()


def attack_search_box(attack_string, table_name="faq"):
    conn = sqlite3.connect(f'database/{expt_tag}/test.db')
    fuzzing_success, exception_success = False, False

    #     test_string = "' UNION SELECT Null, email, pass, Null FROM user;--"
    #     test_string = "'Is FuzzyCrawler Free to Use'"
    #     test_string = "Is FuzzyCrawler Free to Use"

    try:
        cursor = conn.execute(f"SELECT * FROM {table_name} WHERE question='{attack_string}';")
        #         cursor = conn.execute(f'SELECT * FROM {table_name} WHERE question="{attack_string}";')
        output = [row for row in cursor]
        if len(output) > 0:
            fuzzing_success = True

    except sqlite3.OperationalError:
        exception_success = True

    except sqlite3.Warning:
        pass

    conn.close()

    return fuzzing_success, exception_success


def attack_login_page(email, password, table_name="user"):
    conn = sqlite3.connect(f'database/{expt_tag}/test.db')
    fuzzing_success, exception_success = False, False

    try:
        cursor = conn.execute(f"SELECT * FROM {table_name} WHERE email='{email}' AND pass='{password}';")
        #         cursor = conn.execute(f'SELECT * FROM {table_name} WHERE email="{email}" AND pass="{password}";')
        output = [row for row in cursor]
        if len(output) > 0:
            fuzzing_success = True

    except sqlite3.OperationalError:
        exception_success = True

    except sqlite3.Warning:
        pass

    conn.close()

    return fuzzing_success, exception_success


def column_count():  # getting the number of columns using ORDER BY query
    for i in range(1, 12):
        _, status_chk = attack_search_box(f" ' ORDER BY {i} --  ")
        #         _, status_chk = attack_search_box(f' " ORDER BY {i} --  ')
        if status_chk:
            return i-1

# expt_tag = "test"
#
# create_database(stop_random=True)
#
# conn = sqlite3.connect(f'database/{expt_tag}/test.db')
# cursor = conn.execute("SELECT * from user")
# for row in cursor:
#     print(row)
#
# cursor = conn.execute("SELECT * from faq")
# for row in cursor:
#     print(row)
# conn.close()
#
# conn.close()
#
# # some test strings
#
# print(attack_search_box(" ' UNION SELECT Null, email, pass, Null FROM user;-- ")) # (True, False)
# print(attack_search_box(' " UNION SELECT Null, email, pass, Null FROM user;-- ')) # (False, False)
# print(attack_search_box(" ' ")) # (False, True)
# print(attack_login_page("john.doe@example.com ( ' OR 1=1;-- )", "blahblah")) # (True, False)
# print(attack_login_page("'john.doe@example.com ( ' OR 1=1;-- )", "blahblah")) # (False, True)
# print(attack_login_page("john.doe@example.com", "blahblah")) # (False, False)
# print(attack_login_page("( ' OR 1=1;-- )", "blahblah")) # (True, False)
# print(attack_login_page('john.doe@example.com" AND 1=1;-- )', "blahblah")) # (False, False)
# print(attack_search_box(" ' ORDER BY 5 --  ")) # to find no. of columns # (False, True)
# print(attack_search_box(" ' ORDER BY 3 --  ")) # to find no. of columns # (False, False)
# print(attack_login_page("' OR 1=1;-- )", "blahblah")) # (True, False)
# print("NEW -----")
# print(attack_login_page("' OR 1=1;", "blahblah")) #FF
# print(attack_login_page(" dsvgd g ' OR 1=1;", "blahblah")) #FF
# print(attack_login_page("' OR 1=1 --", "blahblah")) # TF
# print(attack_login_page("cvsscvfdz vf ' OR 1=1 ; --", "blahblah")) # TF
# print(attack_search_box(" ' UNION SELECT email, pass, Null FROM user;-- ")) # FT
# print(attack_search_box(" ' UNION SELECT email, pass, Null, Null FROM user;-- ")) # TF
# print(attack_search_box(" ' UNION SELECT email, Null, pass, Null FROM user;-- ")) # TF
# print(attack_search_box(" ' UNION SELECT Null, Null, Null, email FROM user;-- ")) # TF
# print(attack_search_box(" ' UNION SELECT Null, Null, Null, Null FROM user;-- ")) # TF
# print(attack_search_box(" ' SELECT Null, Null, Null, Null FROM user;-- ")) # FT
# print(attack_search_box(" ' SELECT Null, Null, Null, Null FROM user; ")) # FT
# print(attack_search_box(" ' UNION SELECT Null, Null, Null, Null FROM user; ")) # FF
# print(attack_search_box("' UNION SELECT Null, Null, Null, Null FROM user; --")) # TF
# print(attack_search_box("' UNION SELECT Null, Null, Null, Null FROM user --")) # TF
# print(attack_login_page("' OR 1=1 #", "blahblah")) # FT
# print(attack_search_box("' ) UNION SELECT Null, Null, Null, Null FROM user --")) # FT
#
# conn = sqlite3.connect(f'database/{expt_tag}/test.db')
# cursor = conn.execute("SELECT * from faq")
# for row in cursor:
#     assert column_count() == len(row)


# # To test new custom_seed
#
# seed_file = open('custom_seed', 'r')
# lines = seed_file.readlines()
# arr = []
# for line in lines:
#     if len(line) > 1:
#         line = line.strip()
#         arr.append(line)
# all_grammar_inputs_handpicked = list(set(arr))
#
# total = len(all_grammar_inputs_handpicked)
# count_succ, count_ex = 0, 0
# for seed in all_grammar_inputs_handpicked:
#     succ1, ex1 = attack_login_page(seed, "blahblah")
#     succ2, ex2 = attack_search_box(seed)
#     if succ1 or succ2:
#         print(seed)
#     count_succ += int(succ1 or succ2)
#     count_ex += int(ex1 or ex2)
# print(count_succ, count_ex, total)
