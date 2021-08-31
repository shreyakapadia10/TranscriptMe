const csrftoken = getCookie('csrftoken');

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function () {
    
    // Text form 
    $('#text_submit_btn').on('click', function (e) {
       e.preventDefault(); 

       let file_props = $('#file').prop('files');   
       let file = file_props[0];
       console.log(file_props);
       let messages = $('#messages').val();   
       let action_items = $('#action_items').val();      
       let questions = $('#questions').val();
       let topics = $('#topics').val();
       let follow_ups = $('#follow_ups').val();
       let members = $('#members').val();

        // Sending form data

        var data = new FormData();

        data.append("file", file);
        data.append("messages", messages);
        data.append("action_items", action_items);
        data.append("questions", questions);
        data.append("topics", topics);
        data.append("follow_ups", follow_ups);
        data.append("members", members);
        data.append("csrfmiddlewaretoken", csrftoken);

        $.ajax({
            type: "POST",
            url: URL,
            processData: false,
            contentType: false,
            mimeType: "multipart/form-data",
            data: data,

            success: function (data) {
                // alert(data.message);
                console.log('success');
            },
            
            failure: function (data) {
                // alert(data.message);
                console.log('fail');
            }
        });
    });


    // Audio form 
    $('#audio_submit_btn').on('click', function (e) {
       e.preventDefault(); 

       let file_props = $('#file').prop('files');   
       let file = file_props[0];
       let messages = $('#messages').val();   
       let action_items = $('#action_items').val();      
       let questions = $('#questions').val();
       let topics = $('#topics').val();
       let follow_ups = $('#follow_ups').val();
       let members = $('#members').val();

        // Sending form data

        var data = new FormData();

        data.append("file", file);
        data.append("messages", messages);
        data.append("action_items", action_items);
        data.append("questions", questions);
        data.append("topics", topics);
        data.append("follow_ups", follow_ups);
        data.append("members", members);
        data.append("csrfmiddlewaretoken", csrftoken);

        $.ajax({
            type: "POST",
            url: URL,
            processData: false,
            contentType: false,
            mimeType: "multipart/form-data",
            data: data,

            success: function (data) {
                // alert(data.message);
                console.log('success');
            },
            
            failure: function (data) {
                // alert(data.message);
                console.log('fail');
            }
        });
    });

});