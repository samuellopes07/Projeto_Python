import sqlite3
import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image


def conectar():
    conn = sqlite3.connect('Louvores_BDDS.db')
    return conn

def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
       CREATE TABLE IF NOT EXISTS usuarios(
       id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        nome_lider TEXT NOT NULL,
        nome_regente NOT NULL,
        nome_louvor TEXT NOT NULL,
        data_louvor INTEGER                                          
       )  
   ''')
    conn.commit()
    conn.close()

def inserir_usuarios():
    nome  = entry_nome.get()
    data = entry_data.get()
    entr_regente = entry_regente.get()
    lider = entry_lider.get()
    
    

    if nome and data and entr_regente and lider:
        conn = conectar()
        c = conn.cursor()    
        c.execute('INSERT INTO usuarios (data_louvor, nome_louvor, nome_regente, nome_lider) VALUES (?,?,?,?) ', (data, nome, entr_regente, lider ))
        conn.commit()
        conn.close()
        messagebox.showinfo('Sucesso', 'Dados inseridos!')
        entry_nome.delete(0,'end')
        entry_data.delete(0,'end')
        entry_regente.delete(0,'end')
        entry_lider.delete(0,'end') 
        mostrar_usuarios()
    else:
        messagebox.showerror('Erro','Preencha corretamente!')    

def mostrar_usuarios():
    for row in tree.get_children():
        tree.delete(row)
    conn = conectar()
    c = conn.cursor()
    c.execute('SELECT * FROM usuarios')
    usuarios  =  c.fetchall()
    for usuario in usuarios:
        tree.insert("","end", values = (usuario[0], usuario[1], usuario[2], usuario[3],usuario[4],))
    conn.close()        


def eliminar_():
    selecao = tree.selection()
    if selecao:
        user_id = tree.item(selecao)['values'][0]
        conn = conectar()
        c = conn.cursor()
        c.execute('DELETE FROM usuarios WHERE id = ? ', (user_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo('Efetuado', 'Dados deletados!')
        mostrar_usuarios()
    else:
        messagebox.showinfo('Erro', 'Selecione corretamente')    

def atualizar():
    selecao = tree.selection()
    if selecao:
        user_id = tree.item(selecao)['values'][0]
        data = entry_data.get()
        nome = entry_nome.get()
        entr_regente = entry_regente.get()
        nome_lider = entry_lider.get()
        entry_data.delete(0,'end')
        entry_nome.delete(0,'end')
        entry_regente.delete(0,'end')
        entry_lider.delete(0,'end')        
       

        if data and nome and entr_regente and nome_lider:
          conn = conectar()
          c = conn.cursor()    
          c.execute('UPDATE usuarios SET  nome_louvor = ?, data_louvor =? , nome_regente = ?, nome_lider = ? WHERE id = ?',(nome, data, entr_regente ,nome_lider,user_id))
          conn.commit()
          conn.close()
          messagebox.showinfo('Dados', 'Atualização funcionou!')
          mostrar_usuarios()
        else:
           messagebox.showerror('Erro', 'Dados não foram atualizados!') 
    else:
        messagebox.showwarning('Atenção', 'Selecione corretamente') 





janela = ctk.CTk()
icon_salvar = ctk.CTkImage(light_image=Image.open("icon/salvar.png"), size=(20, 20))
icon_deletar = ctk.CTkImage(light_image=Image.open("icon/deletar.png"), size=(20, 20))
icon_atualizar = ctk.CTkImage(light_image=Image.open("icon/atualizar.png"), size=(20, 20))
janela.title('Banco de Dados')
janela.geometry('700x600')
janela.configure(fg_color ='black')



text_label = ctk.CTkLabel(janela, text='BANCO DE DADOS MINISTÉRIO DE LOUVOR', text_color='White', font=('arial', 26,'bold'))
text_label.pack(padx=20, pady=(10, 10), anchor='s',)

entry_frame = ctk.CTkFrame(janela, fg_color='blue', corner_radius=10, )
entry_frame.pack(pady=20)

label_data = ctk.CTkLabel(entry_frame, text = 'Data Louvor' )
label_data.grid(row=0, column=0, padx=10, pady=5, sticky='e')

entry_data = ctk.CTkEntry(entry_frame, placeholder_text='data do louvor...')
entry_data.grid(row=0, column=1, padx=10, pady=5)


label_nome = ctk.CTkLabel(entry_frame, text = 'Nome Louvor', )
label_nome.grid(row=1, column=0, padx=10, pady=5, sticky='e')

entry_nome = ctk.CTkEntry(entry_frame, placeholder_text='nome do louvor...')
entry_nome.grid(row=1, column=1, padx=10, pady=5)


label_regente = ctk.CTkLabel(entry_frame, text = 'Nome regente')
label_regente.grid(row=2,column=0, padx=10,pady=5)

entry_regente = ctk.CTkEntry(entry_frame,placeholder_text='Nome do regente... ')
entry_regente.grid(row=2,column=1, padx=10,pady=5)

label_lider = ctk.CTkLabel(entry_frame, text = 'nome lider')
label_lider.grid(row=3, column=0, padx=10, pady=5, sticky='e')

entry_lider = ctk.CTkEntry(entry_frame, placeholder_text='Nome Lider...')
entry_lider.grid(row=3, column=1, padx=10, pady=5)

btn_frame = ctk.CTkFrame(janela, fg_color='black')
btn_frame.pack(pady=10)

btn_salvar = ctk.CTkButton(btn_frame, text='SALVAR',  command=inserir_usuarios, image=icon_salvar, compound="left",fg_color='blue', font=('Arial', 11,'bold') )
btn_salvar.grid(row=0, column=0, padx=10, )



btn_deletar = ctk.CTkButton(btn_frame, text='DELETAR',  command=eliminar_, text_color='black', fg_color='red',image=icon_deletar, compound="left", font=('Arial', 11,'bold'))
btn_deletar.grid(row=0, column=1, padx=10,)


btn_atualizar = ctk.CTkButton(btn_frame, text='ATUALIZAR',  command=atualizar,text_color='white', image=icon_atualizar, compound="left", fg_color='blue', font=('Arial', 11,'bold'))
btn_atualizar.grid(row=0, column=2, padx=10, )


tree_frame = ctk.CTkFrame(janela, corner_radius=15, fg_color='blue')
tree_frame.pack(pady=10, fill='both', expand=True)

collumns = ('ID','NOME LIDER','NOME REGENTE', 'NOME LOUVOR', 'DATA LOUVOR')

tree = ttk.Treeview(tree_frame, columns= collumns, show='headings')
tree.pack(fill='both', expand=True, padx=10, pady=10)

for col in collumns:
    tree.heading(col, text=col, anchor='center')
    tree.column(col, width=150, anchor='center')

style = ttk.Style()
style.theme_use("default")
style.configure("Treeview", font=("Arial", 12), rowheight=25)
style.configure("Treeview.Heading", font=("Arial", 13, "bold"))

criar_tabela()
mostrar_usuarios()


janela.mainloop()