

function myFunction(x) {
    $.getJSON($SCRIPT_ROOT + '/med_add', {
        post: x
        }, function(data) {
            var response = data.result;
            console.log(response);
            }
        });
}