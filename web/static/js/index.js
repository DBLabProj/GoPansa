function close_btn(target){
    $(".fileBox").remove();
    $("#file").val(null);
    $(".go_btn").hide();
}

$(window).on('load', function(){
    // 레이어팝업 시작
    $('.btn-example').click(function(){
        var $href = $(this).attr('href');
        layer_popup($href);
        
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

                var html = `<b>${data.data.no}</b><br>
                <p>측정일시: ${data.data.datetime}</p><br>
                <p>측정분류: ${data.data.meat_type}</p>`;

                $("#classify-info").html(html);
                
                html = `<span>${data.data.grade}</span><br>`;
                // <p style='position:absolute;top -160px;transform:translateX(-50%); color: white; font-size: 12px;'>등급</p>`;
                $("#grade-info").html(html);

                
                var html = `<p>측정상호명: ${data.data.main_store}</p><br>
                <p>상호주소: ${data.data.address}</p><br>`;

                $("#store_info").html(html);

                // html = `<p>${data.data.gra}</p>`
                
                // classify-info
                // grade-info
                // store_info
			},
			error: function (e) {
				// 전송 후 에러 발생 시 실행 코드
				console.log("ERROR : ", e);
			}
		});
    });
    function layer_popup(el){

        var $el = $(el);    //레이어의 id를 $el 변수에 저장
        var isDim = $el.prev().hasClass('dimBg'); //dimmed 레이어를 감지하기 위한 boolean 변수

        isDim ? $('.dim-layer').fadeIn() : $el.fadeIn();

        var $elWidth = ~~($el.outerWidth()),
            $elHeight = ~~($el.outerHeight()),
            docWidth = $(document).width(),
            docHeight = $(document).height();

        // 화면의 중앙에 레이어를 띄운다.
        // if ($elHeight < docHeight || $elWidth < docWidth) {
        //     $el.css({
        //         marginTop: -$elHeight /2,
        //         marginLeft: -$elWidth/2
        //     })
        // } else {
        //     $el.css({top: 0, left: 0});
        // }

        $el.find('#result-close').click(function(){
            isDim ? $('.dim-layer').fadeOut() : $el.fadeOut(); // 닫기 버튼을 클릭하면 레이어가 닫힌다.
            return false;
        });

        $('.layer .dimBg').click(function(){
            $('.dim-layer').fadeOut();
            return false;
        });

    }
    // 레이어팝업 끝



    $("#check_grade").click(function(){
        // $("#search_box").show("slow");
        $("#search_box").toggle("slow");
    });

    $("#search_btn").click(function search_label(){
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
				// console.log(data.data);
                var meat_type = "";
                
                if (data.data.meat_type=="1"){
                    meat_type = "소고기";
                }
                else if(data.data.meat_type=="2"){
                    meat_type = "돼지고기";
                }
                var html = `<b>${data.data.no}</b><br>
                <p>측정일시:${data.data.datetime}</p><br>
                <p>측정분류:${meat_type}</p>`;

                $("#classify-info").html(html);
                
                html = `${data.data.grade}`;
                $("#grade-info").html(html);

                // html = `<p>${data.data.gra}</p>`
                
                // classify-info
                // grade-info
                // store_info
			},
			error: function (e) {
				// 전송 후 에러 발생 시 실행 코드
				console.log("ERROR : ", e);
			}
		});
    });
});