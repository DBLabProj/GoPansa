function close_btn(target){
    $(".fileBox").remove();
    $("#file").val(null);
    $(".go_btn").hide();
}

$(window).on('load', function(){
    $("#check_grade").click(function(){
        // $("#search_box").show("slow");
        $("#search_box").toggle("slow");
    });

    $("#search_btn").click(function(){
		// Get form
		var form = $('#label_form')[0];

		// Create an FormData object 
		var data = new FormData(form);

        
		$.ajax({
			type: "POST",
			enctype: 'multipart/form-data',
			url: '/check_label',	// form을 전송할 실제 파일경로
			data: data,
			processData: false,
			contentType: false,
			cache: false,
			timeout: 600000,
			beforeSend : function() {
				// 전송 전 실행 코드
			},
			success: function (data) {
				// 전송 후 성공 시 실행 코드
				console.log(data);
			},
			error: function (e) {
				// 전송 후 에러 발생 시 실행 코드
				console.log("ERROR : ", e);
			}
		});
    });

    
    $('.zone').on("dragover", dragOver).on("drop", uploadFiles);
                
    $("#file").change(function(e){
        uploadFiles(e);
    });

    function dragOver(e) {
        if($(e.target).get(0) != $('#file').get(0)){
            e.stopPropagation();
            e.preventDefault();
        }

        var dropZone = $('.zone'),
            timeout = window.dropZoneTimeout;
        if (!timeout) {
            dropZone.addClass('in');
        }
        else {
            clearTimeout(timeout);
        }
        var found = false,
            node = e.target;

        do {
            if (node === dropZone[0]) {
                found = true;
                break;
            }
            node = node.parentNode;
        } while (node != null);

        if (found) {
            dropZone.addClass('hover');
        }
        else {
            dropZone.removeClass('hover');
        }
        window.dropZoneTimeout = setTimeout(function () {
            window.dropZoneTimeout = null;
            dropZone.removeClass('in hover');
        }, 100);
    }

    function uploadFiles(e) {
        if($(e.target).get(0) != $('#file').get(0)){
            e.stopPropagation();
            e.preventDefault();
            dragOver(e);
        }
        
        e.dataTransfer = e.originalEvent.dataTransfer;
        var files = e.target.files || e.dataTransfer.files;

        selectFile(files, e);
    }

    
    function selectFile(fileObject, e){
        var files = null;

        if(fileObject == undefined){

        }

        if(fileObject != null){
            files = fileObject;
        }
        else{
            files = $("#file").files;
        }

        if(files != null && files[0] != undefined){
            if (files.length > 1 || $("#dropZ .fileBox").length>0 ){
                alert('파일은 1개만 업로드할 수 있습니다.');
                return;
            }

            if (files[0].type==='image/jpeg' || files[0].type==='image/png') {
                $(".go_btn").show();
                $(".view_image_box").hide();
                $(".btn_box").hide();



                $(".zone").css({"outline": "none"});

                $('.view_image_box,.view_image_box').hide();

                var tag = '';
                var f = files[0];
                var fileName = f.name;
                var fileSize = f.size / 1024 / 1024;
                fileSize = fileSize < 1 ? fileSize.toFixed(3) : fileSize.toFixed(1);

                tag += 
                    "<div class='fileBox'>" +
                        "<image id='thumbnail'>" +
                        "<span class='x_btn' onclick='close_btn(this);'>x</span>" +
                        "<div class='filename_text'>"+fileName+"<br>"+fileSize+" MB</div>" +
                    "</div>";

                $("#non-upload-box").css("display", "none");
                $("#dropZ").append(tag);

                $('html,body').animate({ scrollTop: 9999 }, 'slow');

                var reader = new FileReader();
                reader.onload = function(e){
                    $("#thumbnail").attr("src", e.target.result);
                }
                reader.readAsDataURL(f);

                $('.go_btn').click(function(){
                    var formData = new FormData();
                    formData.append("file", f);
                    ori_image_path = '../static/org_image/'+fileName;
                    ren_image_path = '../static/render_image/'+fileName;

                    $.ajax({
                        type: 'POST',
                        url: '/uploadIMG',
                        processData: false,
                        contentType: false,
                        xhrFields: {
                            withCredentials: true
                        },
                        data: formData,
                        success: function (data) {
                            do_image_job("start", "#reduce_btn", ori_image_path);
                            $("#reduce_box").show();
                            $(".download_btn").eq(0).attr("href", ori_image_path);
                        },
                        error: function (error) {
                            console.error(error);
                        }
                    });
                });
            }
            else{
                alert('이미지 파일만 업로드할 수 있습니다.');
                $("#file").val(null);
                return;
            }
        }
    }
});