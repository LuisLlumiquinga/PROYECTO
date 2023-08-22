from tkinter import *
import ttkthemes
from tkinter import ttk, messagebox, filedialog
import time
import pymysql
import pandas

#funtionality Part

def iexit():
    result=messagebox.askyesno('CONFIRMACION', 'Desea salir?')
    if result:
        root.destroy()
    else:
        pass
def export_data():
    url=filedialog.asksaveasfilename(defaultextension='.csv')
    indexing=studenTable.get_children()
    newlist=[]
    for index in indexing:
        content=studenTable.item(index)
        datalist=content['values']
        newlist.append(datalist)

    table=pandas.DataFrame(newlist, columns=['Id', 'Nombre', 'Teléfono', 'Email', 'Dirección', 'Género', 'Compleaños', 'Fecha Agregado', 'Hora Agregado'])
    table.to_csv(url, index=False)
    messagebox.showinfo('NOTIFICACION', 'Datos exportados')

def toplevel_data(tittle, button_text, command):
    global idEntry, phoneEntry, nameEntry, emailEntry, addressEntry, genderEntry, dobEntry, screen
    screen = Toplevel()
    screen.title(tittle)
    screen.resizable(False, False)

    idLabel = Label(screen, text='Id', font=('times new roman', 20, 'bold'))
    idLabel.grid(row=0, column=0, padx=30, pady=15, sticky=W)
    idEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    idEntry.grid(row=0, column=1, pady=15, padx=10)

    nameLabel = Label(screen, text='Nombre', font=('times new roman', 20, 'bold'))
    nameLabel.grid(row=1, column=0, padx=30, pady=15, sticky=W)
    nameEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    nameEntry.grid(row=1, column=1, pady=15, padx=10)

    phoneLabel = Label(screen, text='Teléfono', font=('times new roman', 20, 'bold'))
    phoneLabel.grid(row=2, column=0, padx=30, pady=15, sticky=W)
    phoneEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    phoneEntry.grid(row=2, column=1, pady=15, padx=10)

    emailLabel = Label(screen, text='Email', font=('times new roman', 20, 'bold'))
    emailLabel.grid(row=3, column=0, padx=30, pady=15, sticky=W)
    emailEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    emailEntry.grid(row=3, column=1, pady=15, padx=10)

    addressLabel = Label(screen, text='Dirección', font=('times new roman', 20, 'bold'))
    addressLabel.grid(row=4, column=0, padx=30, pady=15, sticky=W)
    addressEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    addressEntry.grid(row=4, column=1, pady=15, padx=10)

    genderLabel = Label(screen, text='Género', font=('times new roman', 20, 'bold'))
    genderLabel.grid(row=5, column=0, padx=30, pady=15, sticky=W)
    genderEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    genderEntry.grid(row=5, column=1, pady=15, padx=10)

    dobLabel = Label(screen, text='Fecha de cumpleaños', font=('times new roman', 20, 'bold'))
    dobLabel.grid(row=6, column=0, padx=30, pady=15, sticky=W)
    dobEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    dobEntry.grid(row=6, column=1, pady=15, padx=10)

    student_button = ttk.Button(screen, text=button_text, command=command)
    student_button.grid(row=7, columnspan=2, pady=15)

    if tittle=='Actualizar Estudiante':
        indexing = studenTable.focus()
        content = studenTable.item(indexing)
        listdata = content['values']
        idEntry.insert(0, listdata[0])
        nameEntry.insert(0, listdata[1])
        phoneEntry.insert(0, listdata[2])
        emailEntry.insert(0, listdata[3])
        addressEntry.insert(0, listdata[4])
        genderEntry.insert(0, listdata[5])
        dobEntry.insert(0, listdata[6])

def update_data():
    query='update student set name=%s, mobile=%s, email=%s, address=%s, gender=%s, dob=%s, date=%s, time=%s where id=%s'
    mycursor.execute(query,(nameEntry.get(), phoneEntry.get(), emailEntry.get(), addressEntry.get(), genderEntry.get(), dobEntry.get(), date, currenttime, idEntry.get()))
    con.commit()
    messagebox.showinfo('ADVERTENCIA', f'Estudiante {idEntry.get()} fue actualizado', parent= screen)
    screen.destroy()
    show_student()




def show_student():
    query = 'select * from student'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    studenTable.delete(*studenTable.get_children())
    for data in fetched_data:
        studenTable.insert('', END, values=data)




def delete_student():
    indexing=studenTable.focus()
    content=studenTable.item(indexing)
    content_id=content['values'][0]
    query='delete from student where id=%s'
    mycursor.execute(query, content_id)
    con.commit()
    messagebox.showinfo('ELIMINAR', f'Estudiante {content_id} eliminado')
    query='select * from student'
    mycursor.execute(query)
    fetched_data=mycursor.fetchall()
    studenTable.delete(*studenTable.get_children())
    for data in fetched_data:
        studenTable.insert('', END, values=data)


def search_data():
    query='select *from student where id=%s or name=%s or email=%s or mobile=%s or address=%s or gender=%s or dob=%s'
    mycursor.execute(query, (idEntry.get(), nameEntry.get(), emailEntry.get(), phoneEntry.get(), addressEntry.get(), genderEntry.get(), dobEntry.get()))
    studenTable.delete(*studenTable.get_children())
    fetched_data=mycursor.fetchall()
    for data in fetched_data:
        studenTable.insert('', END, values=data)





def add_data():
    if idEntry.get()=='' or nameEntry.get()=='' or phoneEntry.get()=='' or emailEntry.get()=='' or addressEntry.get()=='' or genderEntry.get()=='' or dobEntry.get()=='':
        messagebox.showerror('ADVERTENCIA', 'Los campos son necesarios', parent=screen)
    else:
        try:
            query='insert into student values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mycursor.execute(query, (idEntry.get(), nameEntry.get(), phoneEntry.get(), emailEntry.get(), addressEntry.get(), genderEntry.get(), dobEntry.get(), date, currenttime))
            con.commit()
            result=messagebox.askyesno('ADVERTENCIA', 'Estudiante agregado con éxito. Desea limpiar el formulario?', parent=screen)
            if result:
                idEntry.delete(0, END)
                nameEntry.delete(0, END)
                phoneEntry.delete(0, END)
                emailEntry.delete(0, END)
                addressEntry.delete(0, END)
                genderEntry.delete(0, END)
                dobEntry.delete(0, END)
            else:
                pass

        except:
            messagebox.showerror('ADVERTENCIA', 'Id repetida', parent=screen)
            return

        query='select *from student'
        mycursor.execute(query)
        fetched_data=mycursor.fetchall()
        studenTable.delete(*studenTable.get_children())

        for data in fetched_data:
            studenTable.insert('', END, values=data)


def connect_database():
    def connect():
        global mycursor, con
        try:
            con=pymysql.connect(host='localhost', user='root', password='4189')
            mycursor=con.cursor()

        except:
            messagebox.showerror('Error', 'Datos invalidos', parent=connectWindow)
            return
        try:
            query='create database gestion_estudiantes'
            mycursor.execute(query)
            query='use gestion_estudiantes'
            mycursor.execute(query)
            query='create table student(id int not null primary key, name varchar(30), mobile varchar(10), email varchar(30), address varchar(100), gender varchar(20), dob varchar(20), date varchar(50), time varchar(50))'
            mycursor.execute(query)
        except:
            query='use gestion_estudiantes'
            mycursor.execute(query)
        messagebox.showinfo('Exito', 'Conexion exitosa', parent=connectWindow)
        connectWindow.destroy()
        addstudentsButton.config(state=NORMAL)
        searchstudentsButton.config(state=NORMAL)
        updatestudentsButton.config(state=NORMAL)
        showstudentsButton.config(state=NORMAL)
        exportstudentsButton.config(state=NORMAL)
        deletestudentsButton.config(state=NORMAL)

    connectWindow=Toplevel()
    connectWindow.grab_set()
    connectWindow.geometry('470x250+730+230')
    connectWindow.title('Conexión a la Base de Datos')
    connectWindow.resizable(0,0)

    hostnameLabel=Label(connectWindow, text='Host Name', font=('arial', 20, 'bold'))
    hostnameLabel.grid(row=0, column=0, padx=20)

    hostEntry=Entry(connectWindow, font=('roman', 15, 'bold'), bd=2)
    hostEntry.grid(row=0, column=1, padx=40, pady=20)

    usernameLabel = Label(connectWindow, text='User Name', font=('arial', 20, 'bold'))
    usernameLabel.grid(row=1, column=0, padx=20)

    usernameEntry = Entry(connectWindow, font=('roman', 15, 'bold'), bd=2)
    usernameEntry.grid(row=1, column=1, padx=40, pady=20)

    passwordLabel = Label(connectWindow, text='Password', font=('arial', 20, 'bold'))
    passwordLabel.grid(row=2, column=0, padx=20)

    passwordEntry = Entry(connectWindow, font=('roman', 15, 'bold'), bd=2)
    passwordEntry.grid(row=2, column=1, padx=40, pady=20)

    connectButton=ttk.Button(connectWindow, text='CONECTAR', command=connect)
    connectButton.grid(row=3, columnspan=2)


count=0
text=''
def slider():
    global text, count
    if count==len(s):
        count=0
        text=''
    text=text+s[count] #s
    sliderLabel.config(text=text)
    count+=1
    sliderLabel.after(300, slider)


def clock():
    global date, currenttime
    date=time.strftime('%d/%m/%Y')
    currenttime=time.strftime('%H:%M:%S')
    datetimeLabel.config(text=f'     Fecha: {date}\nHora: {currenttime}')
    datetimeLabel.after(1000, clock)

#GUI part
root=ttkthemes.ThemedTk()

root.get_themes()

root.get_themes()

root.set_theme('radiance')

root.geometry('1174x680+0+0')
root.resizable(0,0)
root.title('Gestión de Estudiantes')

datetimeLabel=Label(root, font=('times new roman', 18, 'bold'))
datetimeLabel.place(x=5, y=5)
clock()
s='Sistema de Gestion de Estudiantes'
sliderLabel=Label(root, font=('arial', 28, 'italic bold'), width=40)
sliderLabel.place(x=200, y=0)
slider()

connectButton=ttk.Button(root, text='Base de Datos', command=connect_database)
connectButton.place(x=1000, y=10)

leftFrame=Frame(root)
leftFrame.place(x=50, y=80, width=300, height=600)

logo_image=PhotoImage(file='student.png')
logo_Label=Label(leftFrame, image=logo_image)
logo_Label.grid(row=0, column=0)

addstudentsButton=ttk.Button(leftFrame, text='Agregar Estudiante', width=25, state=DISABLED, command=lambda :toplevel_data('Agregar Estudiante', 'AGREGAR', add_data))
addstudentsButton.grid(row=1, column=0, pady=20)

searchstudentsButton=ttk.Button(leftFrame, text='Buscar Estudiante', width=25, state=DISABLED, command=lambda :toplevel_data('Buscar Estudiante', 'BUSCAR', search_data))
searchstudentsButton.grid(row=2, column=0, pady=20)

deletestudentsButton=ttk.Button(leftFrame, text='Eliminar Estudiante', width=25, state=DISABLED, command=delete_student)
deletestudentsButton.grid(row=3, column=0, pady=20)

updatestudentsButton=ttk.Button(leftFrame, text='Actualizar Estudiante', width=25, state=DISABLED, command=lambda :toplevel_data('Actualizar Estudiante', 'ACTUALIZAR', update_data))
updatestudentsButton.grid(row=4, column=0, pady=20)

showstudentsButton=ttk.Button(leftFrame, text='Ver Estudiante', width=25, state=DISABLED, command=show_student)
showstudentsButton.grid(row=5, column=0, pady=20)

exportstudentsButton=ttk.Button(leftFrame, text='Exportar Datos', width=25, state=DISABLED, command=export_data)
exportstudentsButton.grid(row=6, column=0, pady=20)

exitstudentsButton=ttk.Button(leftFrame, text='SALIR', width=25, command=iexit)
exitstudentsButton.grid(row=7, column=0, pady=20)

rightFrame=Frame(root)
rightFrame.place(x=350, y=80, width=820, height=600)

scrollBarX=Scrollbar(rightFrame, orient=HORIZONTAL)
scrollBarY=Scrollbar(rightFrame, orient=VERTICAL)

studenTable=ttk.Treeview(rightFrame, columns=('Id', 'Name', 'Mobile', 'Email', 'Address', 'Gender', 'DOB', 'Added Date', 'Added Time'), xscrollcommand=scrollBarX.set, yscrollcommand=scrollBarY.set)

scrollBarX.config(command=studenTable.xview)
scrollBarY.config(command=studenTable.yview)

scrollBarX.pack(side=BOTTOM, fill=X)
scrollBarY.pack(side=RIGHT, fill=Y)

studenTable.pack(fill=BOTH, expand=1)

studenTable.heading('Id', text='Id')
studenTable.heading('Name', text='Nombre')
studenTable.heading('Mobile', text='Teléfono')
studenTable.heading('Email', text='Email')
studenTable.heading('Address', text='Dirección')
studenTable.heading('Gender', text='Género')
studenTable.heading('DOB', text='Cumpleaños')
studenTable.heading('Added Date', text='Fecha de agregación')
studenTable.heading('Added Time', text='Hora de agregación')

studenTable.column('Id', width=50, anchor=CENTER)
studenTable.column('Name', width=300, anchor=CENTER)
studenTable.column('Email', width=300, anchor=CENTER)
studenTable.column('Mobile', width=200, anchor=CENTER)
studenTable.column('Address', width=300, anchor=CENTER)
studenTable.column('Gender', width=100, anchor=CENTER)
studenTable.column('DOB', width=100, anchor=CENTER)
studenTable.column('Added Date', width=200, anchor=CENTER)
studenTable.column('Added Time', width=200, anchor=CENTER)

style=ttk.Style()

style.configure('Treeview', rowheight=40, font=('arial', 15, 'bold'), background='white', fielbackground='white')
style.configure('Treeview.Heading', font=('arial', 14, 'bold'), foreground='red')

studenTable.config(show='headings')

root.mainloop()
