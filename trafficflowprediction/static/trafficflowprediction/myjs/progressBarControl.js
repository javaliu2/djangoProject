$(function () {
    $("#btn").on('click', function () {
        console.log("come in ")
        var intelval = setInterval(function () {
            //执行ajax
            $.ajax({
                url: "{% url 'trafficflowprediction:upload' %}",
                data: {
                    getProgressNum: 1,
                },
                dataType: "text",
                type: "get",
                success: function (num_progress) {
                    $('.progress-bar').css('width', num_progress + '%');
                    $('.progress-bar').text(num_progress + '%');
                }
            })
        }, 10);

        //创建对象
        var formdata = new FormData();
        //这里FormData是一个jquery对象，用来绑定values对象，
        //也可以用来上传二进制文件，有了他就可以不用form表单来上传文件了

        var file_obj = $('[name=myfile]')[0].files[0];
        var csrf_data = $('[name=csrfmiddlewaretoken]').val();
        formdata.append('file_obj',file_obj);
        formdata.append('csrfmiddlewaretoken',csrf_data);

        $.ajax({
            url: '{% url "trafficflowprediction:upload" %}',
            type: 'post',
            data: formdata,
            processData: false,    // 不处理数据
            contentType: false,    // 不设置内容类型
            success: function (response) {
                console.log(response);
                $('.progress-bar').css('width', '100%');
                $('.progress-bar').text('100%');
                //清除Internal
                clearInterval(intelval);
                // alert('文件上传成功。');
                // window.location.href='../../../templates/trafficflowprediction/show.html';
            }
        })
    })
})
