let dt = new Date();

/**
 * selectのoptionタグを生成する
 */
 function createOptionForElements(elem,val){
    let option = document.createElement('option');
    option.text = val;
    option.value = val;
    if (option.value == dt.getFullYear()) {
        option.setAttribute("selected", true);
    } else if (option.value == dt.getMonth()+1) {
        option.setAttribute("selected", true);
    }
    elem.appendChild(option);
}

let yearFrom = document.querySelector('#year-from');
let monthFrom = document.querySelector('#month-from');
let yearTo = document.querySelector('#year-to');
let monthTo = document.querySelector('#month-to');

//開始年の生成
for(let i=1900; i<=2050; i++){
    createOptionForElements(yearFrom,i);
}

//開始月の生成
for(let i=1; i<=12; i++){
    createOptionForElements(monthFrom,i);
}

//終了年の生成
for(let i=1900; i<=2050; i++){
    createOptionForElements(yearTo,i);
}

//終了月の生成
for(let i=1; i<=12; i++){
    createOptionForElements(monthTo,i);
}

//宿リスト
const syuku27 = ["室","壁","奎","婁","胃","昂","畢","觜","参","井","鬼","柳","星","張","翼","軫","角","亢","氐","房","心","尾","箕","斗","女","虚","危"]

let honsyukuSelect = document.querySelector('#honsyuku-select');

//本命宿選択リストの生成
for(let i=0; i<=syuku27.length-1; i++){
    createOptionForElements(honsyukuSelect,syuku27[i]);
}

//本命宿ごとのGoogleカレンダー埋め込みタグリスト
const CALENDAR_TAGS = {
    '尾':'<iframe src=\"https://calendar.google.com/calendar/embed?height=600&wkst=1&bgcolor=%23ffffff&ctz=Asia%2FTokyo&src=ZWxxNTM2OHNsZ3FkN2Z1ZGhwMzEwNm5yODhAZ3JvdXAuY2FsZW5kYXIuZ29vZ2xlLmNvbQ&color=%23EF6C00\" style=\"border:solid 1px #777\" width=\"600\" height=\"600\" frameborder=\"0\" scrolling=\"no\"></iframe>'
}

/** 指定された本命宿のGoogleカレンダーを表示する */
$(function(){
    $('#show-events').bind('click', function(){
        let honsyuku =  $('#honsyuku-select').val();
       
        //本命宿に応じたカレンダーを取得
        //let calendar_tag = CALENDAR_TAGS[honsyuku];
        let calendar_tag = CALENDAR_TAGS['尾'];
        $("#google-calendar").html(calendar_tag);

        //カレンダー操作結果メッセージは非表示
        $("#result").html("");

        //予定書込みと削除ボタンを活性化する
        $('#create-events').prop("disabled",false);
        $('#delete-events').prop("disabled",false);

        //本命宿選択リストを非活性化する
        $('#honsyuku-select').prop("disabled",true);
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
                'honsyuku':  $('#honsyuku-select').val(),
                'year_from':  $('#year-from').val(),
                'month_from':  $('#month-from').val(),
                'year_to':  $('#year-to').val(),
                'month_to':  $('#month-to').val()
            },
            dataType : "json"
        }).done(function(data){
            let msg  = '<div>' + data.result + '</div>'
            $("#result").html(msg);
        }).fail(function(jqXHR,textStatus,errorThrown){
            let msg = `status=${jqXHR.status}, responseText=${jqXHR.responseText}, textStatus=${textStatus}, errorThrown=${errorThrown.message}`;
            $("#result").html(msg);
        }).always(function(){
            //AJAXの結果が返ったら（成功でも失敗でも）スピナーを非表示
            $('#spinner-div').hide();   //Request is complete so hide spinner
        });
    });
});


/** Googleカレンダーから予定を削除する */
$(function(){
    $('#delete-events').bind('click', function(){
        $('#spinner-div').show();
        $.ajax({
            type: 'POST',
            url: '/delete_events',
            data: { 
                'honsyuku':  $('#honsyuku-select').val(),
                'year_from':  $('#year-from').val(),
                'month_from':  $('#month-from').val(),
                'year_to':  $('#year-to').val(),
                'month_to':  $('#month-to').val()
            },
            dataType : "json"
        }).done(function(data){
            let msg  = '<div>' + data.result + '</div>'
            $("#result").html(msg);
        }).fail(function(jqXHR,textStatus,errorThrown){
            let msg = `status=${jqXHR.status}, responseText=${jqXHR.responseText}, textStatus=${textStatus}, errorThrown=${errorThrown.message}`;
            $("#result").html(msg);
        }).always(function(){
            $('#spinner-div').hide();
        });
    });
});


//カレンダー未表示の時、カレンダー書込みと削除ボタンを非活性にする
if ($.trim($("#google-calendar").text())==""){
    $('#create-events').prop("disabled",true);
    $('#delete-events').prop("disabled",true);
}