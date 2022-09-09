from flask import Flask, render_template,url_for,request,jsonify
from models.syukuyo import Syukuyo
from models.doubutsu_uranai import DoubutsuUranai
from models.syukuyo_calendar import SyukuyoCalendar
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
    birth_year = request.form.get('birth_year', 0, type=int)    
    birth_month = request.form.get('birth_month', 0, type=int)
    birth_day = request.form.get('birth_day', 0, type=int)

    db_uranai = DoubutsuUranai()
    doubutsu = db_uranai.get_doubutsu(birth_year,birth_month,birth_day)
    return jsonify({'result': doubutsu})

# 宿曜占いと動物占い
@app.route('/get_honsyuku_doubutsu',methods=['GET','POST'])
def get_honsyuku_doubutsu():
    birth_year = request.form.get('birth_year', 0, type=int)     
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
    y_from = request.form.get('year_from', 0, type=int)
    m_from = request.form.get('month_from', 0, type=int)
    y_to = request.form.get('year_to', 0, type=int)
    m_to = request.form.get('month_to', 0, type=int)

    scal = SyukuyoCalendar()
    resp = scal.create_events(honsyuku,y_from,m_from,y_to,m_to)
    return jsonify({'result':resp})

# Googleカレンダーの予定を削除する
@app.route('/delete_events',methods=['GET','POST'])
def delete_events():
    honsyuku = request.form.get('honsyuku', '', type=str)
    y_from = request.form.get('year_from', 0, type=int)
    m_from = request.form.get('month_from', 0, type=int)
    y_to = request.form.get('year_to', 0, type=int)
    m_to = request.form.get('month_to', 0, type=int)

    scal = SyukuyoCalendar()
    resp = scal.delete_events(honsyuku,y_from,m_from,y_to,m_to)
    return jsonify({'result':resp})


if __name__ == '__main__':
    app.run(debug=True) 