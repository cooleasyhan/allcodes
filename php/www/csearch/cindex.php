<?php
# action list
# action index
#
#
#
ini_set('display_errors', 'On');
error_reporting(E_ALL);
ini_set( 'display_errors', 'On' );



class Cindex
{

    private $_cmd = "export CSEARCHINDEX=/u01/data/csearch/.csearchindex; /usr/bin/cindex ";



    public function __construct() {

    }

    public function do_list()
    {
        $cmd = $this->_cmd." -list";
        return $this->run($cmd);
    }

    public function reset()
    {
        $cmd = $this->_cmd." -reset";
        return $this->run($cmd);
    }

    public function index($folders)
    {
        $cmd = $this->_cmd;
        foreach($folders as $folder)
        {
            $_arg = escapeshellarg($folder);
            $cmd = $cmd." $_arg";
        }
        return $this->run($cmd);
    }

    private function run($cmd)
    {
        return shell_exec("$cmd 0>&1 1>&1 2>&1");
    }

}

$action = $_REQUEST["action"];

$cindex = new Cindex();
if ($action == "list")
{
    echo $cindex->do_list();
}
elseif($action == "reset")
{
    echo $cindex->reset();
}
elseif ($action == "index")
{
    $folders = $_REQUEST["folders"];
    $folder_array = json_decode($folders, true);
    echo $cindex->index($folder_array);
}
?>
