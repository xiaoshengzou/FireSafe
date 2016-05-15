
function agreeOrfreezeOption(id,option) {
    $.post('/agreeOrFreeze',{'id':id, 'option':option},function(responce){
        if (responce == 'ok'){
            $('#tr-'+id).remove();
        }
    }); 
}

function disagreeOrdeleteOption(id) {
    $.post('/disagreeOrdelete', {'id':id}, function(responce){
        if (responce == 'ok'){
            $('#tr-'+id).remove();
        }
    }); 
}

function moveTopOrCancel(id) {
    var option = $('#movetop-'+id).text();
    var opCode = 0;     //1 代表Top 2代表Cancel
    if(option == 'Top') {
        opCode = 1;
    }else {
        opCode = 2;
    }
    $.post('/moveTopOrCancel',{'id':id, 'opCode':opCode}, function(responce){
        if(responce == 'ok') {
            if(option == 'Top') {
                $('#movetop-'+id).text("Cancel");
                $('#movetop-'+id).removeClass("btn btn-info btn-small");
                $('#movetop-'+id).addClass("btn btn-danger btn-small");
            }else {
                $('#movetop-'+id).text("Top");
                $('#movetop-'+id).removeClass("btn btn-danger btn-small");
                $('#movetop-'+id).addClass("btn btn-info btn-small");
            }
        }else {
            alert("置顶失败!");
        }
    });
}


function refreshLog() {
    $.post('/refreshLog',function(responce) {
        var list = eval(responce);
        for(var i=1; i<=list.slogs.length; i++) {
            $("#count").text(list.slogs[i-1].count);
            $("#name_" + i).text(list.slogs[i-1].name);
            $("#state_"+ i).text(list.slogs[i-1].state);
            $("#time_" + i).text(list.slogs[i-1].time);
        }
    });
}

