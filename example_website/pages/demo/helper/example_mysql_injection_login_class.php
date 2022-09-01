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
Class LUser{
    private $email="";
    private $password="";
    private $errortxt="";

    public function validateFormRequest($post){
        if(isset($post["loginbtn"])&&isset($post["email"])&&isset($post["password"])){
            $this->email=$post["email"];
            $this->password=$post["password"];
            return true;
        }
        return false;
    }

    public function validateFormFields(){
        if($this->email==""){
            $this->errortxt="Enter Email";
            return false;
        }
        if($this->password==""){
            $this->errortxt="Enter Password";
            return false;
        }
        $this->errortxt="";
        return true;
    }

    public function loginUser($db){
        if($db!=false){
            //MYSQL Injection Susceptible Code **STARTS**
            $queryString="SELECT * FROM user WHERE email='";
            $queryString=$queryString.$this->email."' AND pass='".$this->password."'";
            $query=$db->prepare($queryString);
            $query->execute();
            $row=$query->rowCount();
            if($row==0){
                $this->errortxt="Invalid Credentials!";
                return false;
            }
            $result=$query->fetch(PDO::FETCH_ASSOC);
            $_SESSION["id"]=$result["id"];
            $_SESSION["email"]=$result["email"];
            $_SESSION["fname"]=$result["fname"];
            $_SESSION["lname"]=$result["lname"];
            //MYSQL Injection Susceptible Code **ENDS**
            $this->errortxt="";
            return true;
        }else{
            $this->errortxt="Database Connection: An Error Occured.";
            return false;
        }

    }

    public function getEmail(){
        return htmlspecialchars($this->email);
    }
    public function getErrorTxt(){
        return htmlspecialchars($this->errortxt);
    }
}
?>