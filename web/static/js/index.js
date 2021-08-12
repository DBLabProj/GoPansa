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
        search_label();
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
        if ($elHeight < docHeight || $elWidth < docWidth) {
            $el.css({
                marginTop: -$elHeight /2,
                marginLeft: -$elWidth/2
            })
        } else {
            $el.css({top: 0, left: 0});
        }

        $el.find('a.btn-layerClose').click(function(){
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
				console.log(data);
			},
			error: function (e) {
				// 전송 후 에러 발생 시 실행 코드
				console.log("ERROR : ", e);
			}
		});
    });
});