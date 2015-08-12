$(function () {
    var outputElement = $('#deployment_output').find('pre');
    var legendElement = $('#status_section').find('legend');
    var iconElement = $('#status_section').find('.glyphicon');

    if (deployment_pending) {
        var output_updater = setInterval(function () {
            $.getJSON(deployment_url, function (deployment) {
                outputElement.text(deployment.output);
                if (deployment.is_finished) {
                    if (deployment.status == 'failed') {
                        legendElement.html('Status: Failed!');
                        iconElement.attr('class', '').addClass('glyphicon').addClass('glyphicon-warning-sign').addClass('text-danger');
                    } else if (deployment.status == 'success') {
                        legendElement.html('Status: Success!');
                        iconElement.attr('class', '').addClass('glyphicon').addClass('glyphicon-ok').addClass('text-success');
                    }
                    clearInterval(output_updater)
                } else {
                    var height = outputElement[0].scrollHeight;
                    outputElement.scrollTop(height);
                }
            });
        }, 500);
    } else {
        outputElement.scrollTop(outputElement[0].scrollHeight);
    }
});