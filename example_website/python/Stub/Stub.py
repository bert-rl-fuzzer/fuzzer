import requests
from bs4 import BeautifulSoup as bs
import json


class StubSession:
    def __init__(self):
        self.reset_session()

    def reset_session(self):
        self.s = requests.Session()
        self.s.headers[
            'user-agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"

    def get_URL_Input(self):
        url = input("Enter URL : ")
        return url

    def get_JSON_Path(self):
        jsonFilePath = input("Enter JSON File Path : ")
        return jsonFilePath

    def extractResponseCode(self, k):
        val = ''
        for i in range(0, len(k)):
            if k[i] == '[':
                i = i + 1
                while k[i] != ']':
                    val = val + k[i]
                    i = i + 1
                break
        val = int(val)
        return val

    def get_all_forms(self, url):
        soup = bs(self.s.get(url).content, "html.parser")
        return soup.find_all("form")

    def get_form_details(self, form):
        details = {}
        try:
            action = form.attrs.get("action").lower()
        except:
            action = None
        method = form.attrs.get("method", "get").lower()
        inputs = []
        for input_tag in form.find_all("input"):
            input_type = input_tag.attrs.get("type", "text")
            input_name = input_tag.attrs.get("name")
            input_value = input_tag.attrs.get("value", "")
            inputs.append({"type": input_type, "name": input_name, "value": input_value})
        return inputs

    def form_input_extraction(self, input):
        keys = []
        for variable in input:
            if variable['type'] != 'submit':
                keys.append(variable['name'])
        return keys

    def preprocessing_Form_Fields(self, url):
        # Getting form details and its keys of given url
        form = self.get_all_forms(url)
        form_details = self.get_form_details(form[0])
        keys = self.form_input_extraction(form_details)
        # print(keys)
        return form_details, keys

    def get_Values(self, keys):
        # Getting values for the retrieved keys
        values = []
        for i in keys:
            print("Enter " + i + " :", end=" ")
            k = input()
            values.append(k)
        # To be modified by fuzzing inputs
        # values=["john.doe@example.com ( ' OR 1=1;-- )",'Doe@123']
        # values=["john.doe@example.com",'Doe@123']
        return values

    def form_input_feeding(self, keys, values, input):
        logindata = {}
        for i in range(len(keys)):
            logindata[keys[i]] = values[i]
        for variable in input:
            if variable['type'] == 'submit':
                logindata[variable['name']] = variable['value']
        return logindata

    def jsonReading(self, jsonFilePath):
        with open(jsonFilePath) as json_file:
            data = json.load(json_file)
            pass_Conditions = data['pass']
            fail_Conditions = data['fail']
            return pass_Conditions, fail_Conditions

    def defaultValidation(self, url, logindata, keys):
        receive = self.s.get(url)
        send = self.s.post(url, data=logindata)
        status = 1
        if receive.content == send.content:
            status = 0
            # Check for same content after post operation
            # print("Feeding Credentials Failed") 
        elif self.extractResponseCode(str(send)) >= 400 or (url == send.url):
            # Check for invalid response code or urls identity after post operation
            # print("Fuzzed Credentials Failed")
            status = 0
        else:
            # Checks if url is changed after post operation
            newform = self.get_all_forms(send.url)
            flag = 0
            if len(newform) != 0:
                flag = 0
                newkeys = self.form_input_extraction(self.get_form_details(newform[0]))
                for i in newkeys:
                    if i in keys:
                        flag = flag + 1
            if flag == 0:
                status = 1
        # if status == 0:
            # print("Fuzzed Credentials Failed")
        # else:
            # print("Fuzzed Credentials Passed")
        return status

    def isURLChanged(self, sendURL, recieveURL):
        if sendURL != recieveURL:
            return 1
        else:
            return 0

    def isContentChanged(self, sendURL, recieveURL):
        if recieveURL.content != sendURL.content:
            return 1
        else:
            return 0

    def isResponseCodeChanged(self, url, logindata, Response_Code):
        send = self.s.post(url, data=logindata)
        if self.extractResponseCode(str(send)) != Response_Code:
            return 1
        else:
            return 0

    def isSearchWordAvailable(self, textString, searchWord):
        encoding = 'utf-8'
        stri = str(textString, encoding)
        if (stri.find(searchWord) == -1):
            return 0
        else:
            return 1

    def PFValidations(self, url, logindata, keys, Conditions):
        receive = self.s.get(url)
        send = self.s.post(url, data=logindata)
        finalStatus = 1
        try:
            URL_Change = Conditions["URL-Change"]
            if self.isURLChanged(url, send.url) != URL_Change:
                finalStatus = 0
                return finalStatus
        except:
            pass
        try:
            Content_Change = Conditions["Content-Change"]
            if self.isContentChanged(receive, send) != Content_Change:
                finalStatus = 0
                return finalStatus
        except:
            pass
        try:
            Response_Code = Conditions["Response-Code"]
            if self.isResponseCodeChanged(url, logindata, Response_Code) == 1:
                finalStatus = 0
                return finalStatus
        except:
            pass
        try:
            Data_inputs = Conditions["Data-Inputs"]
            for i in range(len(Data_inputs)):
                if self.isSearchWordAvailable(send.content, Data_inputs[i]) == 0:
                    finalStatus = 0
                    return finalStatus
        except:
            pass
        return finalStatus

    def validation(self, url, logindata, keys, pass_Conditions, fail_Conditions):
        status = 0
        if len(pass_Conditions) == 0 and len(fail_Conditions) == 0:
            status = self.defaultValidation(url, logindata, keys)
        elif len(fail_Conditions) == 0:
            status = self.PFValidations(url, logindata, keys, pass_Conditions)
        elif len(pass_Conditions) == 0:
            status = self.PFValidations(url, logindata, keys, fail_Conditions)
        else:
            pcheck = self.PFValidations(url, logindata, keys, pass_Conditions)
            fcheck = self.PFValidations(url, logindata, keys, fail_Conditions)
            if pcheck == 1:
                status = 1
            elif fcheck == 1:
                status = 0
        return status

    def exceptionCatcher(self, url, logindata):
        send = self.s.post(url, data=logindata)
        textString = str(send.content)
        if textString.find('PDOException') == -1:
            return 0
        else:
            return 1


if __name__ == "__main__":
    s = StubSession()
    # url=s.get_URL_Input()
    # jsonFilePath=s.get_JSON_Path()
    url = "http://localhost/demo/example_mysql_injection_login.php"
    jsonFilePath = 'conditions.json'

    # url = "http://localhost/demo/example_mysql_injection_search_box.php" ---
    # jsonFilePath='conditions1.json' ---

    # Getting form details and its keys of given url
    form_details, keys = s.preprocessing_Form_Fields(url)
    # print("Form inputs in give url are : ")
    # for i in range(len(keys)):
    #    print(str(i+1)+")"+keys[i])
    # Getting values for the retrieved keys
    # values=get_Values(keys)
    print(keys)
    values=["john.doe@example.com ( ' OR 1=1;-- )",'Doe@123']
    # values = ["jai", 'Doe@123']
    # values=["' Hello"]
    # values=["  ')  UNION SELECT Null, email, pass, Null FROM user;-- "]
    # values=["  ' UNION "]
    # values = ["and"] ---

    # Creating the login data
    logindata = s.form_input_feeding(keys, values, form_details)
    pass_Conditions, fail_Conditions = s.jsonReading(jsonFilePath)
    print(pass_Conditions)
    print(fail_Conditions)
    # Checking for SQL injection
    # status_ex = s.exceptionCatcher(url, logindata) ---
    # print(status_ex) ---
    status = s.validation(url, logindata, keys, pass_Conditions, fail_Conditions)
    if status == 1:
        print("Fuzzing Credentials Passed")
    else:
        print("Fuzzing Credentials Failed")
