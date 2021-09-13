/** ---------------------Getting CSRF TOKEN START----------------------- */

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

/** ---------------------Getting CSRF TOKEN END----------------------- */
$(document).ready(function () {
    let my_response_data = []
    
    /** ---------------------FILE UPLOAD BUTTON----------------------- */
    $('#file_upload_btn').on('click', function (e) {
        e.preventDefault(); 
        let file_props = $('#file').prop('files');   
        let file = file_props[0];
        let file_name = $('#file_name').val();   
        let data = new FormData();

        data.append("file", file);
        data.append("file_name", file_name);
        data.append("request", "file_upload");
        data.append("csrfmiddlewaretoken", csrftoken);
        $('#file_upload_btn').prop('value', 'Uploading File...');
        // sending form data
        $.ajax({
            type: "POST",
            url: window.location.pathname,
            processData: false,
            contentType: false,
            mimeType: "multipart/form-data",
            dataType: "json",
            data: data,

            success: function (data) {
                // alert(data.message);
                // console.log('success');
                // console.log(data);
                
                if(data){
                    $('#file_upload_btn').prop('value', 'Uploaded');
                    $('#file_upload_btn').removeClass('btn btn-outline-secondary');
                    $('#file_upload_btn').addClass('btn btn-success');
                    $('#insights_div').css('display', 'block');
                    $('#transcription_btn_div').css('display', 'block');
                    my_response_data.push(data.job_id);
                    my_response_data.push(data.conversation_id);
                }
            },
            
            failure: function (data) {
                // alert(data.message);
                console.log('fail');
            }
        });

    });


    /** ---------------------Uploading Text File----------------------- */
    
    $('#text_submit_btn').on('click', function (e) {
        e.preventDefault(); 
        const insights = document.querySelectorAll(`input[name="insights"]:checked`);
        let values = [];

        var data = new FormData();

        insights.forEach((checkbox) => {
            values.push(checkbox.value);
            data.append(checkbox.value, checkbox.value)
        });
       
        data.append("job_id", my_response_data[0]);
        data.append("conversation_id", my_response_data[1]);
        data.append("request", "file_download");
        data.append("csrfmiddlewaretoken", csrftoken);

        if(values.length > 0)
        {
            $('#download_link').html('<img src="/static/images/misc/loading.gif" class="my-3">');
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
                    // console.log('success');
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


    /** ---------------------Uploading Audio File----------------------- */
    $('#audio_submit_btn').on('click', function (e) {
        e.preventDefault();   
        const insights = document.querySelectorAll(`input[name="insights"]:checked`);
        let values = [];

        var data = new FormData();

        insights.forEach((checkbox) => {
            values.push(checkbox.value);
            data.append(checkbox.value, checkbox.value)
        });
        data.append("job_id", my_response_data[0]);
        data.append("conversation_id", my_response_data[1]);
        data.append("request", "file_download");
        data.append("csrfmiddlewaretoken", csrftoken);

        if(values.length > 0)
        {
            $('#download_link').html('<img src="/static/images/misc/loading.gif" class="my-3">');
            // sending form data
            $.ajax({
                type: "POST",
                url: window.location.pathname,
                processData: false,
                contentType: false,
                mimeType: "multipart/form-data",
                dataType: "json",
                data: data,

                success: function (data) {
                    // alert(data.message);
                    // console.log('success');
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


    /** ---------------------URL Upload Button----------------------- */
    $('#url_upload_btn').on('click', function (e) {
        e.preventDefault(); 
        let file_name = $('#file_name').val();   
        let url = $('#url').val();   
        let data = new FormData();

        data.append("url", url);
        data.append("file_name", file_name);
        data.append("request", "file_upload");
        data.append("csrfmiddlewaretoken", csrftoken);
        
        $('#url_upload_btn').prop('value', 'Processing...');
        // sending form data
        $.ajax({
            type: "POST",
            url: window.location.pathname,
            processData: false,
            contentType: false,
            mimeType: "multipart/form-data",
            dataType: "json",
            data: data,

            success: function (data) {
                // alert(data.message);
                // console.log('success');
                // console.log(data);
                
                if(data){
                    $('#url_upload_btn').prop('value', 'Uploaded');
                    $('#url_upload_btn').removeClass('btn btn-outline-secondary');
                    $('#url_upload_btn').addClass('btn btn-success');
                    $('#insights_div').css('display', 'block');
                    $('#transcription_btn_div').css('display', 'block');
                    my_response_data.push(data.job_id);
                    my_response_data.push(data.conversation_id);
                }
            },
            
            failure: function (data) {
                // alert(data.message);
                console.log('fail');
            }
        });
    });



   
    /** ---------------------Audio URL----------------------- */

    $('#audio_url_submit_btn').on('click', function (e) {
        e.preventDefault();   
        const insights = document.querySelectorAll(`input[name="insights"]:checked`);
        let values = [];

        var data = new FormData();

        insights.forEach((checkbox) => {
            values.push(checkbox.value);
            data.append(checkbox.value, checkbox.value)
        });
        data.append("job_id", my_response_data[0]);
        data.append("conversation_id", my_response_data[1]);
        data.append("request", "file_download");
        data.append("csrfmiddlewaretoken", csrftoken);

        if(values.length > 0)
        {
            $('#download_link').html('<img src="/static/images/misc/loading.gif" class="my-3">');
            // sending form data
            $.ajax({
                type: "POST",
                url: window.location.pathname,
                processData: false,
                contentType: false,
                mimeType: "multipart/form-data",
                dataType: "json",
                data: data,

                success: function (data) {
                    // alert(data.message);
                    // console.log('success');
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


    /** ---------------------Video URL----------------------- */

    $('#video_url_submit_btn').on('click', function (e) {
        e.preventDefault();   
        const insights = document.querySelectorAll(`input[name="insights"]:checked`);
        let values = [];

        var data = new FormData();

        insights.forEach((checkbox) => {
            values.push(checkbox.value);
            data.append(checkbox.value, checkbox.value)
        });
        data.append("job_id", my_response_data[0]);
        data.append("conversation_id", my_response_data[1]);
        data.append("request", "file_download");
        data.append("csrfmiddlewaretoken", csrftoken);

        if(values.length > 0)
        {
            $('#download_link').html('<img src="/static/images/misc/loading.gif" class="my-3">');
            // sending form data
            $.ajax({
                type: "POST",
                url: window.location.pathname,
                processData: false,
                contentType: false,
                mimeType: "multipart/form-data",
                dataType: "json",
                data: data,

                success: function (data) {
                    // alert(data.message);
                    // console.log('success');
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