var count = false;
$(function() {
            $('#chatbot-form-btn').click(function(e) {
                e.preventDefault();
                $('#chatbot-form').submit();
            });

            $('#chatbot-form').submit(function(e) {
                e.preventDefault();
                var bot_name= "Bot:"

                var message = $('#messageText').val();
                if(message!=""){
                $(".media-list").append('<li class="media"><div class="media-body"><div class="media"><div class="media-body">' + message + '<hr/></div></div></div></li>');

                    $.ajax({
                    type: "POST",
                    url: "/name",
                    data: $(this).serialize(),
                    success: function(response) {

                        $('#messageText').val('');

                        var answer = response.answer;

                        var chatPanel = document.getElementById("chatPanel");

                        $(".media-list").append('<li class="media"><div class="media-body"><div class="media"><div class="media-body">'  + bot_name.concat(answer) + '<hr/></div></div></div></li>');

                        DivElmnt = document.getElementById('MyDivName');
                        DivElmnt.scrollTop=DivElmnt.scrollHeight;
                    },
                    error: function(error) {
                        console.log(error);
                    },

                    redirection: function(response) {
                    $('#messageText').val('');

                        var answer = response.answer;

                        var chatPanel = document.getElementById("chatPanel");

                        $(".media-list").append('<li class="media"><div class="media-body"><div class="media"><div class="media-body">'  + bot_name.concat(answer) + '<hr/></div></div></div></li>');
                        $("#messageText").prop('disabled', true);
                    }
                });
            }
            });
        });
