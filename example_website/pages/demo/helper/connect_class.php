<?php
/* 
Documentation

    Class:
    1. Connectors - used to encapsulate connection process.

    Data Members:
	
	- Connectors
	1. $dbname - used for storing database name.
	2. $username - used for storing database user name.
	3. $password - used for storing database password.
	
	Member Functions:
	
	- Connectors
    1. Connectors->phptodbconnector - connects mysql database with php pdo.
	
*/
Class Connectors{
	private $dbname="fuzzycrawler_test";
	private $username="root";
	private $password="fuzzycrawler@123";
	
	function phptodbconnector(){
		try{
			$db = new PDO('mysql:host=mysql-server;port=3306;dbname='.$this->dbname.';charset=utf8',$this->username,$this->password);
		}
		catch(Exception $e){
			return false;
		}
		return $db;
	}
}

class Auth{
    private $email="";
	private $fname="";
	private $lname="";
	private $errortxt="";
	private $status=false;

	public function authenticate($session,$db){
		if($db!=false){
			if(isset($session['fname'])&&isset($session['lname'])&&isset($session['email'])){
				$query=$db->prepare("SELECT * FROM user WHERE email=:email");
				$query->bindParam(":email",$session['email']);
				$query->execute();
				$row=$query->rowCount();
				if($row==0){
					$this->fname="";
					$this->lname="";
					$this->email="";
					$this->errortxt="Database Error: Cannot find user records.";
					$this->status=false;
					return false;
				}
				$this->fname=$session["fname"];
				$this->lname=$session["lname"];
				$this->email=$session["email"];

				$this->errortxt="";
				$this->status=true;
				return true;
			}else{
				$this->fname="";
				$this->lname="";
				$this->email="";
				$this->errortxt="";
				$this->status=false;
				return true;
			}
		}else{
			$this->fname="";
			$this->lname="";
			$this->email="";
			$this->errortxt="Database Connection: An Error Occured.";
			$this->status=false;
            return false;
        }
	}
	public function is_authenticated(){
		return $this->status;
	}
	public function getFirstName(){
        return htmlspecialchars($this->fname);
    }
    public function getLastName(){
        return htmlspecialchars($this->lname);
    }
    public function getEmail(){
        return htmlspecialchars($this->email);
    }
	public function getErrorTxt(){
        return htmlspecialchars($this->errortxt);
    }
}
?>