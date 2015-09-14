


$(function(){
    if(deployment_pending){

        var scroll_iframe_ticker = setInterval(function(){
            var $contents = $('#deployment_output').contents();

            $contents.scrollTop($contents.height());
            if($contents.find('#finished').length > 0){
                status = $contents.find('#finished').html();
                if(status == 'failed'){
                    $('#status_section legend').html('Status: Failed!');
                    $('#status_section .glyphicon').attr('class', '').addClass('glyphicon').addClass('glyphicon-warning-sign').addClass('text-danger');
                }else if(status == 'success') {
                    $('#status_section legend').html('Status: Success!');
                    $('#status_section .glyphicon').attr('class', '').addClass('glyphicon').addClass('glyphicon-ok').addClass('text-success');
                }

                clearInterval(scroll_iframe_ticker);
            }
        }, 100);


    }else{
        $('#deployment_output .output').scrollTop($('#deployment_output .output')[0].scrollHeight);
    }
});
