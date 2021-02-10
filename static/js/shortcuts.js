var initial = Cookies.get('toggle');
  
  if(initial=="true"){
    $('#customSwitches').attr("checked","true");
  }
  else if(initial==="false"){
    $('#customSwitches').attr("checkbox","false");
  }
  $("#customSwitches").on('change', function() {
    Cookies.remove('toggle', { path:'' });
    var val = $('#customSwitches').prop('checked');
    Cookies.set('toggle', val, { expires:700000 });
    console.log(Cookies.get('toggle'));
    location.reload();
    
  });

  // if(Cookies.get('toggle')=="false"){
      
  //   }


  if(Cookies.get('toggle')=="true"){
    
  function openLink1(){
    var url = "{% url 'HR_inventory:HR_inventory-home' %}";
    window.open(url,"_self");
  }

  function openLink2(){
    var url = "{% url 'HR_tasks:dashboard' %}";
    window.open(url,"_self");
  }

  function openLink3(){
    var url = "{% url 'create-leave' %}";
    window.open(url,'_self');
  }

  function openLink4(){
    window.open("{% url 'HR_tasks:admin' %}",'_self')
  }

  function doc_keyUp(e) {

  if (e.ctrlKey && e.keyCode == 73) {
      openLink1();
  }
  if (e.keyCode == 68) {
      openLink2();
  }
  if (e.keyCode == 76) {
      openLink3();
  }
  if(e.keyCode == 83){
    openLink4();
  }
  }
  document.addEventListener('keyup', doc_keyUp, false);
  
}