 function default_op(){
    var sel = document.getElementById('id_name');
    var user_name = document.getElementById('id_user_name').innerHTML;
    
    var opts = sel.options;
    for (var opt, j = 0; opt = opts[j]; j++) {
        console.log(opt.innerHTML)
        if (opt.innerHTML == user_name) {
            sel.selectedIndex = j;
            break;
        }   
    }
    
 }
 window.onload = default_op;

    