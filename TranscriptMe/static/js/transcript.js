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
       let file_name = $('#file_name').val();   
      
       const insights = document.querySelectorAll(`input[name="insights"]:checked`);
       let values = [];

       var data = new FormData();

       insights.forEach((checkbox) => {
           values.push(checkbox.value);
           data.append(checkbox.value, checkbox.value)
       });
        data.append("file", file);
        data.append("file_name", file_name);
        data.append("csrfmiddlewaretoken", csrftoken);

        if(values.length > 0)
        {
            $('#download_link').html('<h4 class="my-3">Transcripting your file...</h4>');
            // sending form data
            $.ajax({
                type: "POST",
                url: URL,
                processData: false,
                contentType: false,
                mimeType: "multipart/form-data",
                dataType: "json",
                data: data,

                success: function (data) {
                    // alert(data.message);
                    console.log('success');
                    // console.log(data);

                    if(data){
                        let url = download_url.replace('0/1', `${data.job_id}/${data.conversation_id}`);
                        let download_link = `<h4 class="my-3">Download your file here!</h4>
                            <a href="${url}" type="button" class="btn btn-primary">Download Transcription</a>`;
                        $('#download_link').html(download_link);
                    }
                },
                
                failure: function (data) {
                    // alert(data.message);
                    console.log('fail');
                }
            });
        }
        else{
            alert('Please select atleast one insight!');
        }
        
    });


    // Audio form 
    $('#audio_submit_btn').on('click', function (e) {
       e.preventDefault(); 

       let file_props = $('#file').prop('files');   
       let file = file_props[0];
       const insights = document.querySelectorAll(`input[name="insights"]:checked`);
       let values = [];

       var data = new FormData();

       insights.forEach((checkbox) => {
           values.push(checkbox.value);
           data.append(checkbox.value, checkbox.value)
       });
        data.append("file", file);
        data.append("file_name", file_name);
        data.append("csrfmiddlewaretoken", csrftoken);

        if(values.length > 0)
        {
            $('#download_link').html('<h4 class="my-3">Transcripting your file...</h4>');
            // sending form data
            $.ajax({
                type: "POST",
                url: URL,
                processData: false,
                contentType: false,
                mimeType: "multipart/form-data",
                dataType: "json",
                data: data,

                success: function (data) {
                    // alert(data.message);
                    console.log('success');
                    // console.log(data);

                    if(data){
                        let url = download_url.replace('0/1', `${data.job_id}/${data.conversation_id}`);
                        let download_link = `<h4 class="my-3">Download your file here!</h4>
                            <a href="${url}" type="button" class="btn btn-primary">Download Transcription</a>`;
                        $('#download_link').html(download_link);
                    }
                },
                
                failure: function (data) {
                    // alert(data.message);
                    console.log('fail');
                }
            });
        }
        else{
            alert('Please select atleast one insight!');
        }
    });

});