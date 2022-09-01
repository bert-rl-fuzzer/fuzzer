<?php
/*
Documentation

    Class:
    1. LUser - used to encapsulate login process.

    Data Members:
    1. $email - used for storing user's email.
    2. $password - used for storing user's password.
    3. $errortxt - used for storing error messages. 

    Member Functions:
    1. LUser->validateFormRequest() - Checks if form is submitted, stores submitted values in class variables. Requires form post object to 
    access form field data.
    2. LUser->validateFormFields() - Checks if submitted form fields are valid & updates the error string.
    3. LUser->loginUser() - Checks if the user credentials are valid and a database connection is available, if yes then logs in the user 
    otherwise updates the error string. Requires pdo object as function parameter for connecting to database. 
    4. LUser->getErrorTxt() - Returns error string which will be empty when no error is present.
    5. LUser->getEmail() - Returns the email of user incase form field validation fails, otherwise returns an empty string.

*/
Class FAQSearch{
    private $question = array();
    private $answer = array();
    private $number_of_questions = 0;
    private $errortxt = "";
    
    public function generateSearchResults($db,$SearchText){
        if($db!=false){
            if(isset($SearchText)&&$SearchText!=""){
                $queryString="SELECT * FROM faq WHERE MATCH(`question`) AGAINST ('".$SearchText."' IN NATURAL LANGUAGE MODE)";
                $query=$db->prepare($queryString);
                $query->execute();          
            }else{
                $queryString="SELECT * FROM faq";
                $query=$db->prepare($queryString);
                $query->execute();
            }
            while($result=$query->fetch(PDO::FETCH_ASSOC)){
                array_push($this->question, $result["question"]);
                array_push($this->answer, $result["answer"]);
                $this->number_of_questions=$this->number_of_questions+1;
            }
        }else{
            $this->errortxt="Database Connection: An Error Occured.";
            return False;
        }
        return True;
    }

    public function getAnswers(){
        return $this->answer;
    }

    public function getQuestions(){
        return $this->question;
    }

    public function getResultCount(){
        return $this->number_of_questions;
    }

    public function getErrorTxt(){
        return htmlspecialchars($this->errortxt);
    }
}
?>