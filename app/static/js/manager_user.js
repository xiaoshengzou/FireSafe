
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
