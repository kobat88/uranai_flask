from flask import Flask, render_template,url_for,request,jsonify
from models.syukuyo import Syukuyo
from models.doubutsu_uranai import DoubutsuUranai
from models.g_calendar import GCalendar

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# 宿曜占い
@app.route('/get_honsyuku',methods=['GET','POST'])
def get_honsyuku():
    birth_year = request.form.get('birth_year', 0, type=int)     #GETの場合はrequest.args.get
    birth_month = request.form.get('birth_month', 0, type=int)
    birth_day = request.form.get('birth_day', 0, type=int)

    syukuyo = Syukuyo()
    honsyuku = syukuyo.get_honsyuku(birth_year,birth_month,birth_day)
    return jsonify({'result': honsyuku})

# 動物占い
@app.route('/get_doubutsu',methods=['GET','POST'])
def get_doubutsu():
    birth_year = request.form.get('birth_year', 0, type=int)     #GETの場合はrequest.args.get
    birth_month = request.form.get('birth_month', 0, type=int)
    birth_day = request.form.get('birth_day', 0, type=int)

    db_uranai = DoubutsuUranai()
    doubutsu = db_uranai.get_doubutsu(birth_year,birth_month,birth_day)
    return jsonify({'result': doubutsu})

# 宿曜占いと動物占い
@app.route('/get_honsyuku_doubutsu',methods=['GET','POST'])
def get_honsyuku_doubutsu():
    birth_year = request.form.get('birth_year', 0, type=int)     #GETの場合はrequest.args.get
    birth_month = request.form.get('birth_month', 0, type=int)
    birth_day = request.form.get('birth_day', 0, type=int)

    syukuyo = Syukuyo()
    honsyuku = syukuyo.get_honsyuku(birth_year,birth_month,birth_day)

    db_uranai = DoubutsuUranai()
    doubutsu = db_uranai.get_doubutsu(birth_year,birth_month,birth_day)
    return jsonify({'result_honsyuku': honsyuku, 'result_doubutsu':doubutsu})

@app.route('/maint_calendar')
def maint_calendar():
    return render_template('maint_calendar.html')
    

# 宿曜運勢をGoogleカレンダーへ書き込む
@app.route('/create_events',methods=['GET','POST'])
def create_events():
    honsyuku = request.form.get('honsyuku', '', type=str)
    months_num = request.form.get('months_num', '1', type=int)

    #except:で正常処理として明示的にreturnしないと、raiseしただけでは、ajaxのfailで処理はされるが、ここで指定したエラーメッセージが返らない
    if not((months_num) and (isinstance(months_num,int)) and (months_num >=1 and months_num <= 12)) :
        try:
            raise ValueError('月数は1ヵ月以上12ヵ月以下)を指定してください')
        except:
            return jsonify({'result':'月数は1ヵ月以上12ヵ月以下を指定してください'})

    syukuyo = Syukuyo()
    # honsyuku = syukuyo.get_honsyuku(birth_year,birth_month,birth_day)
    ft_list = syukuyo.get_fortune(honsyuku,months_num)

    g_calendar = GCalendar()
    resp = g_calendar.create_events(ft_list,honsyuku)
    return jsonify({'result':resp})

# Googleカレンダーの予定を削除する
@app.route('/delete_events',methods=['GET','POST'])
def delete_events():
    honsyuku = request.form.get('honsyuku', '', type=str)

    g_calendar = GCalendar()
    resp = g_calendar.delete_events(honsyuku)
    return jsonify({'result':resp})

if __name__ == '__main__':
    app.run(debug=True) 