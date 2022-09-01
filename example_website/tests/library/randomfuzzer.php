<?php
class RandomFuzzer{

    protected function validateRequirements(){
        return false;
    }
    
    public function addField(){

    } 

    public function fuzzer(){
    if($this->validateRequirements()){

    }else{
        throw new Exception("I am crazy");
    }    
    }
}

$RandomFuzzer = new RandomFuzzer();
try{
    $RandomFuzzer.fuzzer();
}catch(Exception $e){
    die("LibError: ".$e);
}
?>