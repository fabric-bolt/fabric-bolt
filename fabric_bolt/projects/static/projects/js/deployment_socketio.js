


$(function(){
    if(deployment_pending){

        var socket = io.connect("/deployment");

        socket.on('connect', function () {
            socket.emit('join', deployment_id);
        });

        socket.on('output', function (data) {
            if(data.status == 'pending'){
                $('#deployment_output .output').append(data.lines).scrollTop($('#deployment_output .output')[0].scrollHeight);
            }else{
                socket.disconnect();
                if(data.status == 'failed'){
                    $('#status_section legend').html('Status: Failed!');
                    $('#status_section .glyphicon').attr('class', '').addClass('glyphicon').addClass('glyphicon-warning-sign').addClass('text-danger');
                }else if(data.status == 'success') {
                    $('#status_section legend').html('Status: Success!');
                    $('#status_section .glyphicon').attr('class', '').addClass('glyphicon').addClass('glyphicon-ok').addClass('text-success');
                }
            }

        });

        $('#deployment_input').keyup(function(e){
            if(e.which == 13){
                var text = $(this).val();
                $(this).val('');
                socket.emit('input', text);
                $('#deployment_output .output').append('\n');
            }
        });


    }else{
        $('#deployment_output .output').scrollTop($('#deployment_output .output')[0].scrollHeight);
    }
});
