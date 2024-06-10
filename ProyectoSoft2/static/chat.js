$(document).ready(function() {
    $('#send-button').click(function() {
        var userInput = $('#user-input').val();
        if (userInput) {
            $('#chat-log').append('<div><strong>Tú:</strong> ' + userInput + '</div>');
            $('#user-input').val('');
            $.ajax({
                url: '/get_response',
                method: 'POST',
                data: { message: userInput },
                success: function(response) {
                    $('#chat-log').append('<div><strong>Bot:</strong> ' + response.response + '</div>');
                }
            });
        }
    });

    $('#user-input').keypress(function(e) {
        if (e.which === 13) {
            $('#send-button').click();
        }
    });
});
