<?php

function mail_tpl($from, $to, $template, $fields,$customheaders="") {
  global $errno,$er;
  //  $er->log(ERROR_LEVEL_FPUT,"mail_tpl",array("from"=>$from,"to"=>$to,"template"=>$template));
  //  echo "mailtpl : $from : $to : $template <br>\n";
  /* Envoi d'un mail avec substitution de patron */
  $f=@fopen($template,"rb");
  if ($f) {
    $subject=trim(fgets($f,1024));
    $text="";
    while (!feof($f)) {
      $text.=fgets($f,1024);
    }
    fclose($f);

    reset($fields);
    while (list($k,$v)=each($fields)) {
      $subject=str_replace("%%".$k."%%",$v,$subject);
      $text=str_replace("%%".$k."%%",$v,$text);
    }

    ini_set('sendmail_from', $from); //Suggested by "Some Guy"
    return mail($to,$subject,$text,"From: $from\nReply-to: $from".$customheaders);
  } else {
    return false;
  }
}




function startElement($parser, $name, $attrs) {
  global $pfend,$pfattrs,$pfelement;
  //  echo "start: $name \n";
  if ($name=="PEER") {
    $pfattrs=array();
    if ($attrs["IX"]) $pfattrs["IX"]=$attrs["IX"];
  }
  $pfelement="";
}

function endElement($parser, $name) {
  global $pfend,$pfattrs,$pfelement,$peers;
  //  echo "end: $name\n";
  if ($name=="PEER") {
    $peers[]=$pfattrs;
    echo  ".";
  } else {
    $pfattrs[$name]=$pfelement;
  }
}

function dataParser($parser,$data) {
  global $pfend,$pfattrs,$pfelement;
  //  echo "data:$data\n";
  $pfelement.=$data;
}

function parsehead($file) {
  global $pfend,$pfattrs,$pfelement;
  $pfend=false;
  $pfelement="";
  $pfattrs=array();
  $xml_parser = xml_parser_create("ISO-8859-1");
  xml_set_element_handler($xml_parser, "startElement", "endElement");
  xml_set_character_data_handler($xml_parser, "dataParser");
        
  if (!($fp = fopen($file, "r"))) {
    die("could not open XML input");
  }
        
  while (($data = fgets($fp, 4096))) {
    if (!xml_parse($xml_parser, $data, gzeof($fp))) {
      //                return false;
                  die(sprintf("XML error: %s at line %d",
                            xml_error_string(xml_get_error_code($xml_parser)),
                            xml_get_current_line_number($xml_parser)));
      }
  }
  fclose($fp);
  xml_parser_free($xml_parser);
  reset($pfattrs);
  return $pfattrs;        
}

echo "Parsing XML file "; flush();
parsehead("peers.xml");
echo " done \n";

echo "Searching for down hosts from file down.txt\n";
$f=fopen("down.txt","rb");
$down=array();
while ($s=fgets($f,1024)) {
  $s=trim($s);
  $down[$s]=$s;
}
fclose($f);
//print_r($down);

$IPS=array(
	   "freeix"=>"213.228.3.249",
	   "sfinx"=>"0",
	   "panap"=>"62.35.254.66",
	   );

foreach($peers as $p) {
  if ($down[$p["IP"]]  && trim($p["CONTACT"])!="") {
    echo "Sending mail to peer ".$p["IP"]." for IX ".$p["IX"]." named ".$p["NAME"]." at email ".$p["CONTACT"]."\n";
    $p["GITOYENIP"]=$IPS[$p["IX"]];
    mail_tpl("noc@gitoyen.net",$p["CONTACT"],"relance.mailtpl.txt",$p);
  }
}

?>