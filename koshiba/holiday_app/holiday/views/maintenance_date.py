from flask import request, redirect, url_for, render_template, flash, session
from holiday import app
from holiday import db
from holiday.models.mst_holiday import Holiday
import re

@app.route('/result', methods=['GET', 'POST'])
def m_result():
    if request.method == 'POST':
            # 日付またはテキストが空欄の場合、エラーメッセージを表示
            if not request.form['holiday'] or not request.form['holiday_text']:
                  if not request.form['holiday'] and not request.form['holiday_text']:
                        error_input = '日付とテキスト'
                  elif not request.form['holiday']:
                        error_input = '日付'
                  elif not request.form['holiday_text']:
                        error_input = 'テキスト'
                  flash(f'{error_input}が空欄です。正しい情報を入力してください。')
                  return render_template('input.html')
            
            # 20文字を超えている場合、エラーメッセージを表示
            elif len(request.form['holiday_text']) > 20:
                  error_input = request.form['holiday_text']
                  flash(f'{error_input}は文字数制限を超えています。20文字以内で入力してください。')
                  return render_template('input.html')
            
            # 絵文字を含む場合、エラーメッセージを表示
            elif re.search('[\U00010000-\U0010ffff]|[\U000000A9-\U00003299]', request.form['holiday_text']):
                  error_input = request.form['holiday_text']
                  flash(f'{error_input}に無効な絵文字が含まれるため、登録できません。絵文字なしで入力してください。')
                  return render_template('input.html')
            
            else:
                  # 登録、更新、削除のデータベース処理、valueによって条件分岐を行う
                  # 登録・更新の場合
                  if request.form["button"] == "insert_update":
                        judge = Holiday.query.get(request.form['holiday'])
                        if judge == None:
                              message_type = "登録"
                        else:
                              message_type = "更新"
                        # データベースにデータを挿入
                        holiday = Holiday(
                                    holi_date=request.form['holiday'],
                                    holi_text=request.form['holiday_text']
                                    )
                        db.session.merge(holiday)
                        db.session.commit()
                        return render_template('result.html', holi_date=request.form['holiday'], holi_text=request.form['holiday_text'], message_type=message_type)

                  # 削除の場合
                  elif request.form["button"] == "delete":
                        message_type = "削除"
                        holiday = Holiday.query.get(request.form['holiday']) # blogではid、カラムで設定した名前
                        if holiday != None:
                              holiday_text = holiday.holi_text
                              # 正常な場合の動作
                              if request.form['holiday_text'] == holiday_text:
                                    db.session.delete(holiday)
                                    db.session.commit()
                                    return render_template('result.html', holi_date=request.form['holiday'], holi_text=holiday_text, message_type=message_type)
                              # データベースのholi_textとholiday_text(入力値)が異なる場合、エラーメッセージを表示
                              else:
                                    error_day = request.form['holiday']
                                    error_input = request.form['holiday_text']
                                    flash(f'{error_day} ({error_input})は、異なるテキストで登録されています。祝日一覧で確認してください。')
                                    return render_template('input.html')
                        # holiday(入力値)がデータベースに存在しない場合、エラーメッセージを表示
                        else:
                              error_day = request.form['holiday']
                              flash(f'{error_day}は、祝日マスタに登録されていません')
                              return render_template('input.html')



          
        
    





