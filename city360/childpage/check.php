<?php
error_reporting(E_ERROR); 
ini_set("display_errors","Off");



 	$A=$_POST['A'];
 	$B=$_POST['B'];
 	$C=$_POST['C'];
 	$D=$_POST['D'];
 	$E=$_POST['E'];
 	$F=$_POST['F'];
 	$G=$_POST['G'];
 	$H=$_POST['H'];

    $str=$A.$B.$C.$D.$E.$F.$G.$H;

    $str=$A.$B.$C.$D.$E.$F.$G.$H;
    if($A=="" || $B=="" || $C==""|| $D==""|| $E==""|| $F==""|| $G=="" || $H=="" ){
      $data['code']=1; $data['msg']="参数不完整";
      echo json_encode($data);exit;
    }


    $dir="pic";
  $file=scandir($dir);//遍历目录
  array_splice($file, 0, 2);//删除相关数据

   $list=array();

    foreach($file as $key=>$val){
 		//$file[$key]=str_replace(".jpg","",$val);
 		$list[$key]['pic']=str_replace(".jpg","",$val);
		similar_text($list[$key]['pic'], $str, $percent);
 		$list[$key]['num']=$percent;
 	}

//array_multisort(array_column($list,'num'),SORT_DESC,$list);

  foreach ($list as $key => $row) {
    $volume[$key]  = $row['num'];
  }
  array_multisort($volume, SORT_DESC, $list);

$data['code']=1;
$data['pic'][0]=$list[0];
$data['pic'][1]=$list[1];

echo json_encode($data);exit;



//print_r($list)

?>
