from tkinter import *
from tkinter import messagebox
import tkinter as tk
from PIL import ImageTk, Image
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import datetime
import json

class VentanaPrincipal(ttk.Frame):
    """Clase que muestra una receta especifica (RECETA DEL DIA)"""
    def __init__(self, parent, receta):
        super().__init__()
        self.parent = parent
        parent.title('RECETA DEL DIA')
        parent.geometry('400x500')
        parent.configure(bg='black')
        nombre = receta['nombre']
        title = f'{nombre} '
        label = ttk.Label(self.parent, text=title, justify='left', font='bold', bootstyle="inverse-dark")
        label.pack(pady=5)
        # imagen
        self.canvas = Canvas(self.parent, width=300, height=250)
        self.canvas.pack()
        if receta['imagen'] != "":
            imagen = Image.open(receta['imagen'])
            imagen = imagen.resize((300, 250))
            self.imagen_tk = ImageTk.PhotoImage(imagen)
            self.canvas.create_image(0, 0, anchor=NW, image=self.imagen_tk)
        else:
            #no contiene una imagen guardada
            ttk.Label(self.parent, text="No hay imagen para esta receta.", bootstyle="inverse-dark").pack()
        # buttons que abren otra ventana
        self.ingredientes = receta['ingredientes']
        btnIngreditnes = ttk.Button(self.parent, text="Ingredientes", bootstyle="info-outline", command=self.abrir_ventanaIng)
        btnIngreditnes.pack(pady=5)
        self.pasos = receta['preparacion']
        btnPreparacion = ttk.Button(self.parent, text="Pasos Preparacion",bootstyle="info-outline", command=self.abrir_ventanaPasos)
        btnPreparacion.pack(pady=5)
        # tiempo de coccion
        time_coccion = receta['tiempo_coccion']
        label = ttk.Label(self.parent, text=f"Tiempo de coccion: {time_coccion}", justify='left', bootstyle="inverse-dark")
        label.pack()
        # fecha de creacion
        fecha = receta['fecha_creacion']
        fecha_creacion = f'Fecha de creacion: {fecha}'
        label = ttk.Label(self.parent, text=fecha_creacion, justify='left', bootstyle="inverse-dark")
        label.pack()
        # tiempo de preparacion
        preparacion = receta['tiempo_preparacion']
        time_coccion = f'Tiempo de preparacion: {preparacion}'
        label = ttk.Label(self.parent, text=time_coccion, justify='left', bootstyle="inverse-dark")
        label.pack()
        # es favorita
        favorita = receta['favorita']
        label = ttk.Label(self.parent, text=f"Es favorita: {'Sí' if favorita else 'No'}", justify='left', bootstyle="inverse-dark")
        label.pack()
        
    def abrir_ventanaIng(self):
        """Abre una ventada para visualizar los ingredientes de cada receta"""
        if len(self.ingredientes) > 0:
            toplevel = Toplevel(self.parent)
            SecundariaIngredientes(toplevel, self.ingredientes).grid()
        else:
            messagebox.showwarning(message="No tiene ingredientes, no se puede preparar :c")
            
    def abrir_ventanaPasos(self):
        """Abre una ventada para visualizar los pasos de cada receta"""
        if len(self.pasos) > 0:
            toplevel = Toplevel(self.parent)
            SecundariaPasos(toplevel, self.pasos).grid()
        else:
            messagebox.showwarning(message="No tiene pasos, no se puede preparar :c")
        
class SecundariaIngredientes(ttk.Frame):
    """ABRE UNA VENTANA SECUNDARIA PARA LA VISUALIZACION DE INGREDIENTES DE UNA RECETA."""
    def __init__(self, parent, ingredientes):
        super().__init__(parent, padding=(20))
        self.parent = parent
        parent.configure(bg='black')
        parent.title("Ingredientes")
        parent.geometry("200x200")
        parent.resizable(False, False)
        self.mostrar_Ingredientes(ingredientes)
        
    def mostrar_Ingredientes(self, ingredientes):
        """funcion que muestra los ingredientes en la ventana"""
        for ingrediente in ingredientes:
            texto =f"•  {ingrediente['nombre']}: {ingrediente['cantidad']} {ingrediente['unidad']}"
            ttk.Label(self.parent, text = texto, bootstyle="inverse-dark", anchor=CENTER).grid(column=1, columnspan=2, pady=5)

class SecundariaPasos(ttk.Frame):
    """ABRE UNA VENTANA SECUNDARIA PARA LA VISUALIZACION DE LOS PASOS DE UNA RECETA."""
    def __init__(self, parent, pasos):
        super().__init__(parent, padding=(20))
        self.parent = parent
        parent.title("Pasos de Preparacion")
        parent.geometry("+180+100")
        parent.configure(bg='black')
        self.grid(sticky=(tk.N, tk.S, tk.E, tk.W))
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        
        self.mostrar_pasos(pasos)
        
    def mostrar_pasos(self, pasos):
        """Printea los pasos en la ventana."""
        tabla = ttk.Treeview(self.parent, columns=2)
        tabla.grid(padx=20, pady=20)
        tabla.column("#0", width=500, anchor=CENTER)
        tabla.column("#1", width=70 ,anchor=CENTER)
        
        tabla.heading("#0", text ="Descripcion", anchor=CENTER)
        tabla.heading("#1", text ="Pasos", anchor=CENTER)
        
        i = 1
        for paso in pasos:
            tabla.insert('', END, text=paso, values=i)
            i += 1