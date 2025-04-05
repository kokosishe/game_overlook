from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QHBoxLayout, QVBoxLayout, QGroupBox, QRadioButton, QPushButton, QLabel, QButtonGroup)
from random import shuffle, randint

class Question():
    def __init__(self, question, right_answer, wrong1, wrong2, wrong3):
        #все строки надо задать при создании обьекта, они запоминаются в свойства 
        self.question = question
        self.right_answer = right_answer
        self.wrong1 = wrong1
        self.wrong2 = wrong2
        self.wrong3 = wrong3


question_list = []
question_list.append(Question('Государственный язык Бразилии', 'Португальский', 'Английский', 'Испанский', 'Бразильский'))
question_list.append(Question('Какого цвета нет на флаге России?', 'Зеленый', 'Красный', 'Белый', 'Синий'))
question_list.append(Question('Национальная хижина якутов', 'Ураса', 'Юрта', 'Иглу', 'Хата'))

app = QApplication([])

window = QWidget()
window.setWindowTitle('Memo Card')

#Интерфейс приложения Memory Card
btn_OK  = QPushButton('Ответить') #Кнопка ответвета
lb_Question = QLabel('В каком году была основана Москва?') #Текст вопроса

RadioGruopBox = QGroupBox("Варианты ответов") #Группа на экране для переключателей с ответами


rbtn_1 = QRadioButton('1147')
rbtn_2 = QRadioButton('1242')
rbtn_3 = QRadioButton('1861')
rbtn_4 = QRadioButton('1943')

RadioGruop = QButtonGroup() #это для группировки переключателей, чтобы управлять их поведением
RadioGruop.addButton(rbtn_1)
RadioGruop.addButton(rbtn_2)
RadioGruop.addButton(rbtn_3)
RadioGruop.addButton(rbtn_4)

layout_ans1 = QHBoxLayout()
layout_ans2 = QVBoxLayout() #Вертикальные будут внутри горизонтального
layout_ans3 = QVBoxLayout()
layout_ans2.addWidget(rbtn_1) #Два ответа в первый столбец
layout_ans2.addWidget(rbtn_2)
layout_ans3.addWidget(rbtn_3) #Два ответа во второй столбец
layout_ans3.addWidget(rbtn_4)

layout_ans1.addLayout(layout_ans2)
layout_ans1.addLayout(layout_ans3) #Разместили столбцы в одной строке

RadioGruopBox.setLayout(layout_ans1) #Готова "панель" с вариантами ответов

AnsGroupBox = QGroupBox('Результат теста')
lb_Result = QLabel('прав ты или нет?')
lb_Correct = QLabel('ответ будет тут!')

layout_res = QVBoxLayout()
layout_res.addWidget(lb_Result, alignment=(Qt.AlignLeft | Qt.AlignTop))
layout_res.addWidget(lb_Correct, alignment=Qt.AlignHCenter, stretch=2)
AnsGroupBox.setLayout(layout_res)
layout_line1 = QHBoxLayout() #вопрос
layout_line2 = QHBoxLayout() #варианты ответов или результат теста
layout_line3 = QHBoxLayout() #кнопка "Ответить"

layout_line1.addWidget(lb_Question, alignment=(Qt.AlignHCenter | Qt.AlignVCenter))
layout_line2.addWidget(RadioGruopBox)
layout_line2.addWidget(AnsGroupBox)
AnsGroupBox.hide() #скроем панель с ответом, сначала должна быть видна панель вопросов

layout_line3.addStretch(1)
layout_line3.addWidget(btn_OK, stretch=2) #Кнопка должна быть большой
layout_line3.addStretch(1)

#Теперь созданные строки разместим друг под другой:
layout_card = QVBoxLayout()

layout_card.addLayout(layout_line1, stretch=2)
layout_card.addLayout(layout_line2, stretch=8)
layout_card.addStretch(1)
layout_card.addLayout(layout_line3, stretch=1)
layout_card.addStretch(1)
layout_card.setSpacing(5) #Пробелы между содержимым

def show_result():
    '''показать панель ответов'''
    RadioGruopBox.hide()
    AnsGroupBox.show()
    btn_OK.setText('Следующий вопрос')

def show_question():
    '''показать панель вопросов'''
    RadioGruopBox.show()
    AnsGroupBox.hide()
    btn_OK.setText('Ответить')
    #сбросить выбранную радио-кнопку
    RadioGruop.setExclusive(False) # сняли ограничения,чтобы можно было сбросить выбор радиокнопки
    rbtn_1.setChecked(False)
    rbtn_2.setChecked(False)
    rbtn_3.setChecked(False)
    rbtn_4.setChecked(False)
    RadioGruop.setExclusive(True) #вернули ограничения, теперь только одна радиокнопка может быть выбрана

answers = [rbtn_1, rbtn_2, rbtn_3, rbtn_4]

def ask(q: Question):
    '''функция записывает значения вопроса и ответов в соответсвующие виджеты,при этом варианты ответов
    распределятся случайным образом'''
    shuffle(answers) #перемешали список из кнопок, теперь на первом месте списка какая-то непредсказуемая кнопка
    answers[0].setText(q.right_answer) #первый элемент списка заполним правильным ответом, отсальные - неверными
    answers[1].setText(q.wrong1)
    answers[2].setText(q.wrong2)
    answers[3].setText(q.wrong3)
    lb_Question.setText(q.question) #вопрос
    lb_Correct.setText(q.right_answer) #ответ
    show_question() #показываем панель вопросов

def show_correct(res):
    '''показать результат - установим переданный текст в надпись "результат" и покажем нужную панель'''
    lb_Result.setText(res)
    show_result()

def check_answer():
    '''ессли выбран какой-то вариант ответа,то надо проверить и показать панель ответов'''
    if answers[0].isChecked():
        #правильный ответ!
        show_correct('Правильно!')
        window.score += 1
        print('Статистика\n-Всего вопросов: ', window.total, '\n-Правильных ответов: ', window.score)
        print('Рейтинг: ', (window.score/window.total*100), '%')
    else:
        if answers[1].isChecked() or answers[2].isChecked() or answers[3].isChecked():
            # неправильный ответ!
            show_correct('Неверно!')
            print('Рейтинг: ', (window.score/window.total*100), '%')

def next_question():
    '''задает следующий вопрос из списка'''
    #в этой функции нужна переменная,в которой будет указываться номер текущего вопросов
    #эту переменную можно сделать глобальной, либо же сделать свойством "глобального обьекта" (app или window)
    #мы заведем (ниже) свойство window.cur_question.
    window.total += 1    #переходим к следующему вопросу
    print('Статистика\n-Всего вопросов: ', window.total, '\n-Правильных ответов: ', window.score)
    cur_question = randint(0, len(question_list) - 1) #нам не нужно старое значение,
                                                      # поэтому можно использовать локальную переменную!
          #случайно взяли вопрос в пределах списка
          #если внести около сотни слов, то редко будет повторяться
    q = question_list[cur_question] #взяли вопрос
    ask(q) #спросили
    
        
def click_OK():
    ''' определяет, надо ли показывать другой вопрос либо проверить ответ на этот '''
    if btn_OK.text() == 'Ответить':
        check_answer() #проверка ответа
    else:
        next_question() #следующий вопрос


window = QWidget()
window.setLayout(layout_card)
window.setWindowTitle('Memo Card')
#текущий вопрос из списка сделаем свойством обьекта "окно", так мы сможем спокойно менять его из функции:
window.cur_question = -1 #по-хорошему такие переменные должны быть свойствами,
                         # только надо писать класс,экземпляры которого получат таие свойства,
                         # но python позволяет создать свойство у отдельно взятого экземпляра


btn_OK.clicked.connect(click_OK) #по нажатии на кнопку выбираем, что конкретно происходит 

#все настроено, осталось задать вопрос и показать окно:
window.score = 0
window.total = 0
next_question()
window.resize(400,300)
window.show()
app.exec()
