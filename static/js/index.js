/**
 * selectのoptionタグを生成する
 */
function createOptionForElements(elem,val){
    let option = document.createElement('option');
    option.text = val;
    option.value = val;
    if (option.value == '1980') {
        option.setAttribute("selected", true);
    }
    elem.appendChild(option);
}

/**
 * 選択された年月に応じて日リストを変更する
 */
 function changeDays(){
    //日の要素をクリア
    birthDay.innerHTML = '';

    //選択された年月の最終日を取得
    let lastDayOfMonth = new Date(birthYear.value,birthMonth.value,0).getDate();

    //選択された年月の日リストを生成
    for(let i=1; i <=lastDayOfMonth; i++){
        createOptionForElements(birthDay,i);
    }
}

let birthYear = document.querySelector('#birth-year');
let birthMonth = document.querySelector('#birth-month');
let birthDay = document.querySelector('#birth-day');

console.log({birthYear});
console.log({birthMonth});
console.log({birthDay});

let dt = new Date();

//年の生成
for(let i=1900; i<=dt.getFullYear(); i++){
    createOptionForElements(birthYear,i);
}

//月の生成
for(let i=1; i<=12; i++){
    createOptionForElements(birthMonth,i);
}

//日の生成
for(let i=1; i<=31; i++){
    createOptionForElements(birthDay,i);
}

birthYear.addEventListener('change',function(){
    changeDays();
});

birthMonth.addEventListener('change',function(){
    changeDays();
});

//本命宿ごとのGoogleカレンダー埋め込みタグ
const CALENDAR_TAGS = {
    "尾":'<iframe src=\"https://calendar.google.com/calendar/embed?height=600&wkst=1&bgcolor=%23ffffff&ctz=Asia%2FTokyo&src=ZWxxNTM2OHNsZ3FkN2Z1ZGhwMzEwNm5yODhAZ3JvdXAuY2FsZW5kYXIuZ29vZ2xlLmNvbQ&color=%23EF6C00\" style=\"border:solid 1px #777\" width=\"600\" height=\"600\" frameborder=\"0\" scrolling=\"no\"></iframe>'
}

/** 宿曜占い */
$(function(){
    $('#get-honsyuku').bind('click', function(){
        $.ajax({
            type: 'POST',
            url: '/get_honsyuku',
            data: { 
                'birth_year': $('#birth-year').val(),
                'birth_month': $('#birth-month').val(),
                'birth_day': $('#birth-day').val(),
            },
            dataType : "json"
        }).done(function(data){
            let msg  = "あなたの本命宿は<span class=\'honsyuku\'>" + data.result + "宿</span>です";
            $("#result").html(msg);
            //本命宿に応じたカレンダーを表示する
            calendar_tag = CALENDAR_TAGS["尾"];
            $("#google-calendar").html(calendar_tag);
        }).fail(function(jqXHR,textStatus,errorThrown){
            let msg = `status=${jqXHR.status}, responseText=${jqXHR.responseText}, textStatus=${textStatus}, errorThrown=${errorThrown.message}`;
            $("#result").html(msg);
        });
    });
});

/** 動物占い */
$(function(){
    $('#get-doubutsu').bind('click', function(){
        $.ajax({
            type: 'POST',
            url: '/get_doubutsu',
            data: { 
                'birth_year': $('#birth-year').val(),
                'birth_month': $('#birth-month').val(),
                'birth_day': $('#birth-day').val(),
            },
            dataType : "json"
        }).done(function(data){
            let msg  = "あなたの動物は<span class=\'doubutsu\'>" + data.result + "</span>です";
            $("#result").html(msg);
            //宿曜運勢カレンダーは非表示
            $("#google-calendar").html("");
        }).fail(function(jqXHR,textStatus,errorThrown){
            let msg = `status=${jqXHR.status}, responseText=${jqXHR.responseText}, textStatus=${textStatus}, errorThrown=${errorThrown.message}`;
            $("#result").html(msg);
        });
    });
});

/** 宿曜＆動物占い */
$(function(){
    $('#get-honsyuku-doubutsu').bind('click', function(){
        $.ajax({
            type: 'POST',
            url: '/get_honsyuku_doubutsu',
            data: { 
                'birth_year': $('#birth-year').val(),
                'birth_month': $('#birth-month').val(),
                'birth_day': $('#birth-day').val(),
            },
            dataType : "json"
        }).done(function(data){
            let msg_honsyuku  = "<div>あなたの本命宿は<span class=\'honsyuku\'>" + data.result_honsyuku + "宿</span>です</div>";
            let msg_doubutsu  = "<div>あなたの動物は<span class=\'doubutsu\'>" + data.result_doubutsu + "</span>です</div>";
            $("#result").html(msg_honsyuku + msg_doubutsu);
            //本命宿に応じたカレンダーを取得する
            calendar_tag = CALENDAR_TAGS["尾"];
            $("#google-calendar").html(calendar_tag);
        }).fail(function(jqXHR,textStatus,errorThrown){
            let msg = `status=${jqXHR.status}, responseText=${jqXHR.responseText}, textStatus=${textStatus}, errorThrown=${errorThrown.message}`;
            $("#result").html(msg);
        });
    });
});

