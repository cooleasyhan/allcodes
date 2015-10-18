<?php
# action list
# action index
#
#
#
ini_set('display_errors', 'On');
error_reporting(E_ALL);
ini_set( 'display_errors', 'On' );



class Csearch
{

    private $_cmd = "export CSEARCHINDEX=/u01/data/csearch/.csearchindex; /usr/bin/csearch ";



    public function __construct() {

    }


    public function do_search($file_regexp,$regexp)
    {
        $cmd = $this->_cmd;
        if (!empty($file_regexp))
        {
            $arg = escapeshellarg($file_regexp);
            $cmd = $cmd." -f ".$arg." ";
        }

        $cmd = $cmd.$regexp;
        return $this->run($cmd);
    }



    private function run($cmd)
    {
        return shell_exec("$cmd 0>&1 1>&1 2>&1");
    }

}

$action = $_REQUEST["action"];
$file_regexp = $_REQUEST["file_regexp"];
$regexp = $_REQUEST["regexp"];

$csearch = new Csearch();
if ($action == "search")
{
    echo $csearch->do_search($file_regexp,$regexp);
}
?>
