function onReady(callback) {
    var intervalId = window.setInterval(function () {
        if (document.getElementsByTagName('body')[0] !== undefined) {
            window.clearInterval(intervalId);
            callback.call(this);
        }
    }, 1000);
}

function setVisible(selector, visible) {
    document.querySelector(selector).style.display = visible ? 'block' : 'none';
}

onReady(function () {
    setVisible('.loader', false);
});

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
        let speakers = $('#speakers').val();
        let speakers_email = $('#speakers_email').val();
        let data = new FormData();

        data.append("speakers", speakers);
        data.append("speakers_email", speakers_email);
        data.append("file", file);
        data.append("file_name", file_name);
        data.append("request", "file_upload");
        data.append("csrfmiddlewaretoken", csrftoken);
        $('#file_upload_btn').prop('value', 'Uploading File...');
        $('#waiting').css('display', 'block');
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

                if (data) {
                    $('#waiting').css('display', 'none');
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

        if (values.length > 0) {
            $('#waiting').css('display', 'block');
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

                    if (data) {
                        let url = download_url.replace('0/1', `${data.conversation_id}/${data.job_id}`);
                        let download_link = `<h4 class="my-3">Download your file here!</h4>
                            <a href="${url}" type="button" class="btn btn-primary">Download Transcription</a>`;
                        $('#waiting').css('display', 'none');
                        $('#download_link').html(download_link);
                    }
                },

                failure: function (data) {
                    // alert(data.message);
                    console.log('fail');
                }
            });
        }
        else {
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

        if (values.length > 0) {
            $('#waiting').css('display', 'block');
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

                    if (data) {
                        let url = download_url.replace('0/1', `${data.conversation_id}/${data.job_id}`);
                        let download_link = `<h4 class="my-3">Download your file here!</h4>
                            <a href="${url}" type="button" class="btn btn-primary">Download Transcription</a>`;
                        $('#waiting').css('display', 'none');
                        $('#download_link').html(download_link);
                    }
                },

                failure: function (data) {
                    // alert(data.message);
                    console.log('fail');
                }
            });
        }
        else {
            alert('Please select atleast one insight!');
        }
    });


    /** ---------------------Uploading Video File----------------------- */
    $('#video_submit_btn').on('click', function (e) {
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

        if (values.length > 0) {
            $('#waiting').css('display', 'block');
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

                    if (data) {
                        let url = download_url.replace('0/1', `${data.conversation_id}/${data.job_id}`);
                        let download_link = `<h4 class="my-3">Download your file here!</h4>
                            <a href="${url}" type="button" class="btn btn-primary">Download Transcription</a>`;
                        $('#waiting').css('display', 'none');
                        $('#download_link').html(download_link);
                    }
                },

                failure: function (data) {
                    // alert(data.message);
                    console.log('fail');
                }
            });
        }
        else {
            alert('Please select atleast one insight!');
        }
    });



    /** ---------------------URL Upload Button----------------------- */
    $('#url_upload_btn').on('click', function (e) {
        e.preventDefault();
        let file_name = $('#file_name').val();
        let url = $('#url').val();
        let data = new FormData();
        let speakers = $('#speakers').val();
        let speakers_email = $('#speakers_email').val();

        data.append("speakers", speakers);
        data.append("speakers_email", speakers_email);
        data.append("url", url);
        data.append("file_name", file_name);
        data.append("request", "file_upload");
        data.append("csrfmiddlewaretoken", csrftoken);

        $('#url_upload_btn').prop('value', 'Processing...');
        $('#waiting').css('display', 'block');
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

                if (data) {
                    $('#waiting').css('display', 'none');
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

        if (values.length > 0) {
            $('#waiting').css('display', 'block');
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

                    if (data) {
                        let url = download_url.replace('0/1', `${data.conversation_id}/${data.job_id}`);
                        let download_link = `<h4 class="my-3">Download your file here!</h4>
                            <a href="${url}" type="button" class="btn btn-primary">Download Transcription</a>`;
                        $('#waiting').css('display', 'none');
                        $('#download_link').html(download_link);
                    }
                },

                failure: function (data) {
                    // alert(data.message);
                    console.log('fail');
                }
            });
        }
        else {
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

        if (values.length > 0) {
            $('#waiting').css('display', 'block');
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

                    if (data) {
                        let url = download_url.replace('0/1', `${data.conversation_id}/${data.job_id}`);
                        let download_link = `<h4 class="my-3">Download your file here!</h4>
                            <a href="${url}" type="button" class="btn btn-primary">Download Transcription</a>`;
                        $('#waiting').css('display', 'none');
                        $('#download_link').html(download_link);
                    }
                },

                failure: function (data) {
                    // alert(data.message);
                    console.log('fail');
                }
            });
        }
        else {
            alert('Please select atleast one insight!');
        }
    });



    /** ---------------------- Zoom Meeting Call ------------------------- */

    $('#zoom_submit_btn').on('click', function (e) {
        e.preventDefault();
        let file_name = $('#file_name').val();
        let email = $('#email').val();
        let meetingId = $('#meetingId').val();
        let password = $('#password').val();
        let phoneNumber = $('#phoneNumber').val();

        if (phoneNumber == ''){
            phoneNumber = '+13017158592'
        }
        var data = new FormData();

        data.append("file_name", file_name);
        data.append("email", email);
        data.append("meetingId", meetingId);
        data.append("password", password);
        data.append("phoneNumber", phoneNumber);
        data.append("csrfmiddlewaretoken", csrftoken);
        
        $('#waiting').css('display', 'block');
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
                if (data) {
                    console.log(data);
                    $('#waiting').css('display', 'none');
                    $('#info-box').css('display', 'block');
                    $('#zoom_form').css('display', 'none');
                }
            },

            failure: function (data) {
                // alert(data.message);
                console.log('fail');
            }
        });

    });


    /** ------------------------- Zoom call download button ------------------------------- */
    $('#tbody').on('click', '.select-insights', function (e) {
        e.preventDefault();
        let conversation_id = $(this).attr('data-conversation-id');
        // let myThis= this;

        const insights = document.querySelectorAll(`input[name="insights${conversation_id}"]:checked`);
        let values = [];
        // let conversation_id = $('#conversation_id').val();
        var data = new FormData();

        insights.forEach((checkbox) => {
            values.push(checkbox.value);
            data.append(checkbox.value, checkbox.value)
        });

        data.append("request_for", "insights");
        data.append("conversation_id", conversation_id);
        data.append("csrfmiddlewaretoken", csrftoken);
        let url = download_url.replace('0/1', `${conversation_id}`);
        
        $('#waiting').css('display', 'block');
        $('#zoomModal'+conversation_id).modal('hide')

        // sending form data
        $.ajax({
            type: "POST",
            url: url,
            processData: false,
            contentType: false,
            mimeType: "multipart/form-data",
            dataType: "json",
            data: data,

            success: function (data) {
                if (data) {
                    console.log(data);
                    let download_link = `<a href="${url}" type="button" class="btn btn-success">Download Transcription</a>`;
                    $('#waiting').css('display', 'none');
                    $('#download_link'+conversation_id).html(download_link);
                }
            },

            failure: function (data) {
                // alert(data.message);
                console.log('fail');
            }
        });

    });



    
    /** ---------------------- Google Meet ------------------------- */

    $('#google_meet_submit_btn').on('click', function (e) {
        e.preventDefault();
        let file_name = $('#file_name').val();
        let email = $('#email').val();
        let pin = $('#pin').val();
        let phoneNumber = $('#phoneNumber').val();

        if (phoneNumber == ''){
            phoneNumber = '+13017158592'
        }
        var data = new FormData();

        data.append("file_name", file_name);
        data.append("email", email);
        data.append("pin", pin);
        data.append("phoneNumber", phoneNumber);
        data.append("csrfmiddlewaretoken", csrftoken);
        
        $('#waiting').css('display', 'block');
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
                if (data) {
                    console.log(data);
                    $('#waiting').css('display', 'none');
                    $('#info-box').css('display', 'block');
                    $('#google_meet_form').css('display', 'none');
                }
            },

            failure: function (data) {
                // alert(data.message);
                console.log('fail');
            }
        });

    });


    /** ------------------------- Google Meet download button ------------------------------- */
    $('#tbody').on('click', '.select-insights', function (e) {
        e.preventDefault();
        let conversation_id = $(this).attr('data-conversation-id');
        // let myThis= this;

        const insights = document.querySelectorAll(`input[name="insights${conversation_id}"]:checked`);
        let values = [];
        // let conversation_id = $('#conversation_id').val();
        var data = new FormData();

        insights.forEach((checkbox) => {
            values.push(checkbox.value);
            data.append(checkbox.value, checkbox.value)
        });

        data.append("request_for", "insights");
        data.append("conversation_id", conversation_id);
        data.append("csrfmiddlewaretoken", csrftoken);
        let url = download_url.replace('0/1', `${conversation_id}`);
        
        $('#waiting').css('display', 'block');
        $('gooleMeetModal'+conversation_id).modal('hide')

        // sending form data
        $.ajax({
            type: "POST",
            url: url,
            processData: false,
            contentType: false,
            mimeType: "multipart/form-data",
            dataType: "json",
            data: data,

            success: function (data) {
                if (data) {
                    console.log(data);
                    let download_link = `<a href="${url}" type="button" class="btn btn-success">Download Transcription</a>`;
                    $('#waiting').css('display', 'none');
                    $('#download_link'+conversation_id).html(download_link);
                }
            },

            failure: function (data) {
                // alert(data.message);
                console.log('fail');
            }
        });

    });
});