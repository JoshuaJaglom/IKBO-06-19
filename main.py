from tkinter import *
from tkinter.ttk import Notebook, Frame, Combobox
import urllib.request
import xml.dom.minidom
import datetime
import matplotlib
import matplotlib.pyplot as plt
def btn1_click():
    number = float(input_number.get())
    val1 = value1.get()
    val2 = value2.get()
    if (val1 == val2):
        res_of_convert.configure(text=number)
    else:
        bad_cour1 = value[val1].split(',')                        #Замена запятой в числе на точку, с целью перевода этого числа во float#
        bad_cour2 = value[val2].split(',')
        course1 = bad_cour1[0] + '.' + bad_cour1[1]
        course2 = bad_cour2[0] + '.' + bad_cour2[1]
        nom1 = nominal[val1]
        nom2 = nominal[val2]
        res = ((float(course1) / float(nom1)) / (float(course2) / float(nom2))) * number
        res_of_convert.configure(text=res)
def btn2_click():
    month1 = list_of_month.get()
    val1 = value3.get()
    num = 0
    value_for_graph = []
    day_for_graph = []
    while month1 != month[num]:  #Вычисление номера месяца для подстановки в адрес#
        num += 1
    num = num + 1
    if num < 10:                   #Из-за особенности ссылки, где дни на конце пишутся так: если это число меньше 10 спереди подставляется 0#
        num1 = '0'+str(num)
    else:
        num1 = str(num)
    number_of_day = int(month_with_date[month1])
    for i in range(1, number_of_day + 1):
        day_for_graph.append(i)
        if i < 10:
            Url_button = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=0" + str(i) + '/' + num1 + '/' + '2019'
        else:                                   #Из-за особенности ссылки, где меcяцы на конце пишутся так: если это число меньше 10 спереди подставляется 0#
            Url_button = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=" + str(i) + '/' + num1 + '/' + '2019'

        response1 = urllib.request.urlopen(Url_button)
        dom = xml.dom.minidom.parse(response1)
        nodeArray = dom.getElementsByTagName("Valute")
        for node in nodeArray:
            childList = node.childNodes
            for child in childList:
                if child.childNodes[0].nodeValue == val1:
                    nom = childList[2]
                    val = childList[4]                          #При нахождении названия валюты, в этом же блоке я вызываю курс валюты как элемент массива под индексом 4(0 - Numcode, 1 - charcode, 2 - Nominal, 3 - Name, 4 - Value#
                    bad_val = val.childNodes[0].nodeValue.split(',')
                    nom1 = nom.childNodes[0].nodeValue
                    val = bad_val[0]+'.'+bad_val[1]
                    res = float(val)/float(nom1)
                    value_for_graph.append(res)

    matplotlib.use('TkAgg')
    fig = plt.figure()
    canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=tab2)
    plot_widget = canvas.get_tk_widget()
    fig.clear()
    plt.plot(day_for_graph, value_for_graph)
    plt.grid()
    plot_widget.place(height = 565, width = 500, x = 275, y = 4)
def btn3_click():       #Третья кнопка для получения актуальных названия валют#
    allActualName = []
    value3.configure(state = NORMAL)
    month1 = list_of_month.get()
    num = 0
    while month1 != month[num]:
        num += 1
    num = num + 1
    if num < 10:
        num1 = '0'+str(num)
    else:
        num1 = str(num)
    Url_button1 = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=01/" + num1 + '/' + '2019'
    response2 = urllib.request.urlopen(Url_button1)
    dom = xml.dom.minidom.parse(response2)
    nodeArray = dom.getElementsByTagName("Valute")
    for node in nodeArray:
        childList = node.childNodes
        for child in childList:
            if (child.nodeName == "Name"):
                allActualName.append(child.childNodes[0].nodeValue)
    value3["values"] = allActualName


d1 = datetime.datetime.now()
c=""
c += d1.strftime("%d/%m/%Y")
URL = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=" +c
response = urllib.request.urlopen(URL)
dom = xml.dom.minidom.parse(response)
nodeArray = dom.getElementsByTagName("Valute")
window = Tk()
window.title("Конвертер валют")
window.geometry("800x600")
tab_control = Notebook(window)
tab1 = Frame(tab_control)
tab_control.add(tab1, text = "Курсы валют")
tab2 = Frame(tab_control)
tab_control.add(tab2, text = "График")
tab_control.pack(expand = True, fill = BOTH)
allName = []
nominal = {}
value = {}
Nominal = ""
Name = ""
for node in nodeArray:
    childList = node.childNodes
    for child in childList:
        if(child.nodeName=="Nominal"):
            Nominal = child.childNodes[0].nodeValue
        if(child.nodeName=="Name"):
            Name = child.childNodes[0].nodeValue
            allName.append(Name)
            nominal[Name] = Nominal
        if (child.nodeName == "Value"):
            value[Name] = child.childNodes[0].nodeValue

value3 = Combobox(tab2, state = DISABLED)
value3.place(height = 20, width = 230, x = 2, y = 60)
allName.append("Русский рубль")
value["Русский рубль"] = '1,0'
nominal["Русский рубль"] ='1'
value1 = Combobox(tab1, values = allName)
value2 = Combobox(tab1, values = allName)
value1.place(height = 20, width = 150, x = 2, y = 4)
value2.place(height = 20, width = 150, x = 160, y = 4)
input_number = Entry(tab1, text = "")
input_number.place(height = 20, width = 150, x = 2, y = 40)
res_of_convert = Label(tab1, text = "")
res_of_convert.place(height = 20, width = 150, x = 160, y = 40)
button1 = Button(tab1, text = "Конвертировать", command = btn1_click)
button1.place(height = 20, width = 150, x = 320, y = 4)
month_with_date = {'Январь 2019':'31','Февраль 2019':'28','Март 2019':'31','Апрель 2019':'30','Май 2019':'31','Июнь 2019':'30','Июль 2019':'31','Август 2019':'31','Сентябрь 2019':'30','Октябрь 2019':'31','Ноябрь 2019':'30','Декабрь 2019':'31'}
month= []
for key in month_with_date:
    month.append(key)
list_of_month = Combobox(tab2, values = month)
list_of_month.place(height = 20, width = 230, x = 2, y = 4)
button2 = Button(tab2, text = "График", command = btn2_click)
button2.place(height = 20, width = 230, x = 2, y = 90)
button3 = Button(tab2, text = "Получить актуальные названия валют", command = btn3_click)
button3.place(height = 20, width = 230, x = 2, y = 30)
window.mainloop()
