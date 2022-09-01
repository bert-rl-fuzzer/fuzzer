class GCheckModifier:
    # convert our test case to valid SQL format
    def grammarchecker(self, testcase):
        bad_chars = ["'", ')', ']', '(', "[", "@", "$"]
        temp = ""
        for i in range(len(testcase)):
            if testcase[i] == "'":
                break
            temp = temp + testcase[i]
        # print ("Original String : " + testcase)
        for i in bad_chars:
            testcase = testcase.replace(i, '')
            temp = temp.replace(i, '')
        # print(temp)
        if len(temp) > 2:
            zen = testcase.replace(temp, "", 1)
            testcase = "SELECT * FROM abc where username=" + temp + zen
        else:
            testcase = "SELECT * FROM abc where username=def" + testcase
        # print ("Resultant list is : " + str(testcase))
        return testcase


if __name__ == "__main__":
    G = GCheckModifier()
    k = "Administrator';/"
    G.grammarchecker(k)
