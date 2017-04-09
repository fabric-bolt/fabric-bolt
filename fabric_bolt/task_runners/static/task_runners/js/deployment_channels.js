$(function(){
    if(deployment_pending){

        socket = new WebSocket("ws://" + window.location.host + "/" + deployment_id);

        socket.onmessage = function(e)  {
            data = JSON.parse(e.data);

            $('#deployment_output .output').append(data.text).scrollTop($('#deployment_output .output')[0].scrollHeight);

            if(data.status != 'pending'){
                if(data.status == 'failed'){
                    $('#status_section legend').html('Status: Failed!');
                    $('#status_section .glyphicon').attr('class', '').addClass('glyphicon').addClass('glyphicon-warning-sign').addClass('text-danger');
                }else if(data.status == 'success') {
                    $('#status_section legend').html('Status: Success!');
                    $('#status_section .glyphicon').attr('class', '').addClass('glyphicon').addClass('glyphicon-ok').addClass('text-success');
                }
            }

        };
        //
        // $('#deployment_input').keyup(function(e){
        //     if(e.which == 13){
        //         var text = $(this).val();
        //         $(this).val('');
        //         socket.send(text);
        //         $('#deployment_output .output').append('\n');
        //     }
        // });

    }else{
        $('#deployment_output .output').scrollTop($('#deployment_output .output')[0].scrollHeight);
    }
});
