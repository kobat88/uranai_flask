//本宿ごとのGoogleカレンダー埋め込みタグリスト
const CALENDAR_TAGS = {
    '尾':'<iframe src=\"https://calendar.google.com/calendar/embed?height=600&wkst=1&bgcolor=%23ffffff&ctz=Asia%2FTokyo&src=ZWxxNTM2OHNsZ3FkN2Z1ZGhwMzEwNm5yODhAZ3JvdXAuY2FsZW5kYXIuZ29vZ2xlLmNvbQ&color=%23EF6C00\" style=\"border:solid 1px #777\" width=\"600\" height=\"600\" frameborder=\"0\" scrolling=\"no\"></iframe>'
}

/** Googleカレンダーを表示する */
$(function(){
    $('#show-events').bind('click', function(){
        let honsyuku_input =  $('#honsyuku-input').val();

        //入力された本宿の文字がCALENDAR_TAGSリストのkeyに存在すればカレンダーと本宿テキストを表示
        if(honsyuku_input in CALENDAR_TAGS){
            //本宿に応じたカレンダーを取得
            let calendar_tag = CALENDAR_TAGS['尾'];
            $("#google-calendar").html(calendar_tag);

            //本宿テキストをセット
            $("#honsyuku-text").text(honsyuku_input);

            $("#calendar-result").html("");

            //カレンダー書込みと削除ボタンを活性化する
            $('#create-events').prop("disabled",false);
            $('#delete-events').prop("disabled",false);
        } else {
            let msg  = '<div>入力文字が不正です</div>'
            $("#calendar-result").html(msg);
        }
    });
});


/** 宿曜運勢をGoogleカレンダーに書き込む */
$(function(){
    $('#create-events').bind('click', function(){
        //時間がかかるため、スピナーを表示
        $('#spinner-div').show();//Load button clicked show spinner
        $.ajax({
            type: 'POST',
            url: '/create_events',
            data: { 
                'honsyuku':  $('#honsyuku-text').text(),
                'months_num':  $('#months-num').val()
            },
            dataType : "json"
        }).done(function(data){
            $('#spinner-div').hide();//Request is complete so hide spinner
            let msg  = '<div>' + data.result + '</div>'
            $("#calendar-result").html(msg);
        }).fail(function(jqXHR,textStatus,errorThrown){
            let msg = '<p>status:' + jqXHR.stauts + ',' + textStatus + ',' + errorThrown.message + '</p>'
            //let msg = 'status=' + jqXHR.status + jqXHR.responseText 
            $("#calendar-result").html(msg);
        }).always(function(){
            //AJAXの結果が返ったら（成功でも失敗でも）スピナーを非表示
            $('#spinner-div').hide();//Request is complete so hide spinner
        });
    });
});


/** Googleカレンダーから予定を削除する */
$(function(){
    $('#delete-events').bind('click', function(){
        $('#spinner-div').show();//Load button clicked show spinner
        $.ajax({
            type: 'POST',
            url: '/delete_events',
            data: { 
                'honsyuku': $('#honsyuku-text').text()
            },
            dataType : "json"
        }).done(function(data){
            let msg  = '<div>' + data.result + '</div>'
            $("#calendar-result").html(msg);
        }).fail(function(jqXHR,textStatus,errorThrown){
            let msg = 'status=' + jqXHR.status + jqXHR.responseText;
            $("#calendar-result").html(msg);
        }).always(function(){
            $('#spinner-div').hide();//Request is complete so hide spinner
        });
    });
});

//本宿テキストがブランクの時（＝カレンダー未表示の時）、カレンダー書込みと削除ボタンを非活性にする
if ($('#honsyuku-text').text()==""){
    $('#create-events').prop("disabled",true);
    $('#delete-events').prop("disabled",true);
}