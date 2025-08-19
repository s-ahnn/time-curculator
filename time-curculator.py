from tkinter import *
import datetime
import tkinter.ttk
import pytz
import os
import sys

#검색 가능한 드롭다운 개체
class AutoCompleteCombobox(tkinter.ttk.Combobox):
    def setList(self, list):
        self.originList = sorted(list)
        self.configure(values=self.originList)
        self.bind('<KeyRelease>', self.findCountry)

    def findCountry(self, event):
        typed = self.get()
        if typed == '':
            self.configure(values=self.originList)
        else:
            findings = [item for item in self.originList if typed in item]
            self.configure(values=findings)

        # self.event_generate('<Down>')

def makeDict():
    countries = dict()
    
    if getattr(sys, 'frozen', False): 
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    file_path = os.path.join(base_path, 'timezone.txt')

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            key, value = line.strip().split(':')
            countries[key.strip()] = value.strip()

    return countries

countries = makeDict()
values = list(countries.keys())

#시차 계산 (시차 알리미용)
def calculate() :
    selected = selectCountry_diff.get()
    if selected in countries:
        resultMessege_diff.config(text=f'우리나라와 {selected}와(과)의 시차는?')
    elif selected not in countries:
        resultMessege_diff.config(text='해당 국가의 시간을 찾을 수 없습니다.')
        resultSpace_diff.configure(state='normal')
        resultSpace_diff.delete(1.0, "end")
        resultSpace_diff.configure(state='disabled')    


    korea = pytz.timezone('Asia/Seoul')
    target = pytz.timezone(countries[selected])

    # 한국과 대상국가의 현재 시각(aware datetime)
    now = datetime.datetime.now()
    now_korea = korea.localize(now)
    now_target = target.localize(now)

    # 각 타임존의 UTC 오프셋 구하기
    korea_offset = now_korea.utcoffset()
    target_offset = now_target.utcoffset()

    # 시차 계산 (초 단위 → 시간 단위)
    timeDifference = (target_offset - korea_offset).total_seconds() / 3600

    resultSpace_diff.configure(state='normal')
    resultSpace_diff.delete(1.0, "end")
    resultSpace_diff.insert(1.0, f'{int(timeDifference)}시간')
    resultSpace_diff.configure(state='disabled')

#메인에 현재 시간용
def mainNowTime():
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    nowPrint.configure(state='normal')
    nowPrint.delete(1.0, "end")
    nowPrint.insert(1.0, f'현재 우리나라 시간: {nowTime}')
    nowPrint.configure(state='disabled')
    mainScreen.after(1000, mainNowTime)

#현재 시간 변환용
def transNowTime():
    selected = selectCountry_now.get()
    if selected in countries:
        resultMessege_now.config(text=f'현재 {selected}의 시간은 ?')
    elif selected not in countries:
        resultMessege_now.config(text='해당 국가의 시간을 찾을 수 없습니다.')
        resultSpace_now.configure(state='normal')
        resultSpace_now.delete(1.0, "end")
        resultSpace_now.configure(state='disabled')    
    
    target = pytz.timezone(countries[selected])

    nowTime = datetime.datetime.now(target).strftime('%Y-%m-%d %H:%M:%S')
    resultSpace_now.configure(state='normal')
    resultSpace_now.delete(1.0, "end")
    resultSpace_now.insert(1.0, nowTime)
    resultSpace_now.configure(state='disabled')
    nowTimescreen.after(1000, transNowTime)

#지정 시간 변환용
def transSelectTime():
    selected = selectCountry.get()
    if selected in countries:
        resultMessege_select.config(text=f'설정한 시간은 {selected}에서는 ?')
    elif selected not in countries:
        resultMessege_select.config(text='해당 국가의 시간을 찾을 수 없습니다.')
        resultSpace_select.configure(state='normal')
        resultSpace_select.delete(1.0, "end")
        resultSpace_select.configure(state='disabled')  
        
    hour = int(setHour.get())
    minute = int(setMinute.get())
    second = int(setSecond.get())

    nowDate = datetime.date.today()
    today = datetime.datetime.combine(nowDate, datetime.time(hour, minute, second))

    korea = pytz.timezone('Asia/Seoul')
    koreaTime = korea.localize(today)  

    transCountry = pytz.timezone(countries[selected])

    timeTrans = koreaTime.astimezone(transCountry)
    resultSpace_select.configure(state='normal')
    resultSpace_select.delete(1.0, "end")
    resultSpace_select.insert(1.0, timeTrans.strftime('%Y-%m-%d %H:%M:%S'))
    resultSpace_select.configure(state='disabled')

#화면 기본 세팅
screen = Tk()
screen.title('시차 계산기')
screen.geometry('540x1080')

#현재 시간 변환 화면 생성
nowTimescreen = Frame(screen, width=540, height=1080, bg='white')
nowTimescreen.place(x=0, y=0)
#지정 시간 변환 화면 생성
selectTimescreen = Frame(screen, width=540, height=1080, bg='white')
selectTimescreen.place(x=0, y=0)
#시차 알리미 화면 생성
timeDiffscreen = Frame(screen, width=540, height=1080, bg='white')
timeDiffscreen.place(x=0, y=0)
#메인 화면 생성
mainScreen = Frame(screen, width=540, height=1080, bg='white')
mainScreen.place(x=0, y=0)

#메인 화면 (mainScreen)
subtitle = Label(mainScreen, text='한국 기준', font='프리텐다드 20', bg='white', fg='red')
subtitle.place(x=233, y=200)

title = Label(mainScreen, text='시차 계산기', font='프리텐다드 30', bg='white', fg='black')
title.place(x=200, y=250)
    #시차 알리미 버튼
timeDiffButt = Button(mainScreen, text='시차 알리미', width=40, height=2, command=timeDiffscreen.lift)
timeDiffButt.place(x=70, y=350)
    #지정 시간 변환 버튼
selectTimeButt = Button(mainScreen, text='지정 시간 변환', width=40, height=2, command=selectTimescreen.lift)
selectTimeButt.place(x=70, y=430)
    #현재 시간 변환 버튼
nowTimeButt = Button(mainScreen, text='현재 시간 변환', width=40, height=2, command=nowTimescreen.lift)
nowTimeButt.place(x=70, y=510)
    #현재 시간 출력
now = Label(mainScreen, text=f'현재 우리나라 시간은?', font='프리텐다드 20', bg='white', fg='black')
now.place(x=180, y=600)

nowPrint = Text(mainScreen, width=40, height=3, fg='black', bg='white')
nowPrint.place(x=130, y=650)
    #종료 버튼
quit_butt = Button(mainScreen, text='종료', width=40, height=2, command=screen.destroy)
quit_butt.place(x=70, y=750)

#시차 알리미 화면 (timeDiffscreen)
subtitle_diff = Label(timeDiffscreen, text='한국 기준', font='프리텐다드 20', bg='white', fg='red')
subtitle_diff.place(x=233, y=200)

timeDifftitle = Label(timeDiffscreen, text='시차 알리미', font='프리텐다드 30', bg='white', fg='black')
timeDifftitle.place(x=200, y=250)
    #드롭다운 스타일 지정
style_diff = tkinter.ttk.Style()
style_diff.theme_use('default')
style_diff.configure('White.TCombobox', fieldbackground='white', background='white', foreground='black')
    #드롭다운 생성
selectCountry_diff = AutoCompleteCombobox(timeDiffscreen, style='White.TCombobox')
selectCountry_diff.setList(values)
selectCountry_diff.place(x=150, y=350)
selectCountry_diff.set('국가를 선택하세요.')
    #변환 버튼 생성
transform_diff = tkinter.ttk.Button(timeDiffscreen, text='계산', width=3, style='TButton', command=calculate)
transform_diff.place(x=360, y=350)
    #결과 출력
resultMessege_diff = Label(timeDiffscreen, text=f'우리나라와 선택된 국가의 시차는 ?', font='프리텐다드 20', bg='white', fg='black')
resultMessege_diff.place(relx=0.5, y=430, anchor='center')

resultSpace_diff = Text(timeDiffscreen, width=40, height=3, fg='black', bg='white')
resultSpace_diff.place(x=130, y=450)
    #메인 화면 이동 버튼
mainButt_diff = Button(timeDiffscreen, text='메인 화면으로', width=40, height=2, command=mainScreen.lift)
mainButt_diff.place(x=70, y=750)

#지정 시간 변환 화면 (selectTimescreen)
subtitle_select = Label(selectTimescreen, text='한국 기준', font='프리텐다드 20', bg='white', fg='red')
subtitle_select.place(x=233, y=200)

selectTimetitle = Label(selectTimescreen, text='지정 시간 변환', font='프리텐다드 30', bg='white', fg='black')
selectTimetitle.place(x=190, y=250)
    #드롭다운 스타일 지정
style_select = tkinter.ttk.Style()
style_select.theme_use('default')
style_select.configure('White.TCombobox', fieldbackground='white', background='white', foreground='black')
    #드롭다운 생성
selectCountry = AutoCompleteCombobox(selectTimescreen, style='White.TCombobox')
selectCountry.setList(values)
selectCountry.place(x=150, y=350)
selectCountry.set('국가를 선택하세요.')
    #변환 버튼 생성
transform_select = tkinter.ttk.Button(selectTimescreen, text='계산', width=3, style='TButton', command=transSelectTime)
transform_select.place(x=360, y=350)
    #시간 설정(스핀박스)
setHour = Spinbox(selectTimescreen, to=23, bg='white', fg='black', width=3) #시
setHour.place(x=150, y=380)
setMinute = Spinbox(selectTimescreen, to=59, bg='white', fg='black', width=3) #분
setMinute.place(x=215, y=380)
setSecond = Spinbox(selectTimescreen, to=59, bg='white', fg='black', width=3) #초
setSecond.place(x=280, y=380)
    #결과 출력
resultMessege_select = Label(selectTimescreen, text=f'설정한 시간은 해당 나라에선 ?', font='프리텐다드 20', bg='white', fg='black')
resultMessege_select.place(relx=0.5, y=430, anchor='center')

resultSpace_select = Text(selectTimescreen, width=40, height=3, fg='black', bg='white')
resultSpace_select.place(x=130, y=450)
    #메인 화면 이동 버튼
mainButt_select = Button(selectTimescreen, text='메인 화면으로', width=40, height=2, command=mainScreen.lift)
mainButt_select.place(x=70, y=750)

#현재 시간 변환 화면 (nowTimescreen)
subtitle_now = Label(nowTimescreen, text='한국 기준', font='프리텐다드 20', bg='white', fg='red')
subtitle_now.place(x=233, y=200)

nowTimetitle = Label(nowTimescreen, text='현재 시간 변환', font='프리텐다드 30', bg='white', fg='black')
nowTimetitle.place(x=190, y=250)
    #드롭다운 스타일 지정
style_now = tkinter.ttk.Style()
style_now.theme_use('default')
style_now.configure('White.TCombobox', fieldbackground='white', background='white', foreground='black')
    #드롭다운 생성
selectCountry_now = AutoCompleteCombobox(nowTimescreen, style='White.TCombobox')
selectCountry_now.setList(values)
selectCountry_now.place(x=150, y=350)
selectCountry_now.set('국가를 선택하세요.')
    #변환 버튼 생성
transform_now = tkinter.ttk.Button(nowTimescreen, text='계산', width=3, style='TButton', command=transNowTime)
transform_now.place(x=360, y=350)
    #결과 출력
resultMessege_now = Label(nowTimescreen, text=f'선택된 나라의 현재 시간은 ?', font='프리텐다드 20', bg='white', fg='black')
resultMessege_now.place(relx=0.5, y=430, anchor='center')

resultSpace_now = Text(nowTimescreen, width=40, height=3, fg='black', bg='white')
resultSpace_now.place(x=130, y=450)
    #메인 화면 이동 버튼
mainButt_now = Button(nowTimescreen, text='메인 화면으로', width=40, height=2, command=mainScreen.lift)
mainButt_now.place(x=70, y=750)

mainNowTime()

screen.mainloop()