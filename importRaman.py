"""imports raman maps previously exported from l6m files"""

import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import matplotlib.pyplot as plt

def importFile(fileName):
    header = ""
    data = []
    with open(fileName, 'rt', encoding = 'latin') as file:
        for line in file:
            if line[0] == '#':
                header = header + line.replace('#','')
            elif line[0] == '\t':
                wavenumber = [float(ii) for ii in line.replace('\t\t','').replace(',','.').split('\t')]
            else:
                data.append([float(ii) for ii in line.replace(',','.').split('\t')])
        data = np.transpose(np.array(data))
        x = data[0]
        data = np.delete(data,0,0)
        y = data[0]
        data = np.delete(data,0,0)
        X = [ x[0] ]
        Y = []
        n = 0
        for ii in x:
            if ii != X[-1]:
                X.append(ii)
                n = n + 1
        for ii in y:
            if len(Y) and ii < Y[-1]:
                break
            Y.append(ii)
    return wavenumber, X, Y, data, header

class Raman(tk.Frame):
    def __init__(self, master=None):
        """Application initialization
            """
        tk.Frame.__init__(self, master)
        
        self.filename = tk.StringVar()
        self.filename.set('/Users/ramonbernardogavito/Box Sync/Raman/Marta/Marta_WS2_WSe2_29.txt')
        
        self.header = tk.StringVar()
        self.header.set('')

        self.point = tk.IntVar()
        self.point.set(0)
        
        self.xpoint = tk.IntVar()
        self.xpoint.set(40)
        self.ypoint = tk.IntVar()
        self.ypoint.set(40)
        
        self.importedData = []
        
        self.buttonsFrame = tk.Frame()
        self.filenameEntry = tk.Entry(textvariable = self.filename)
        self.filenameEntry.grid(row = 0, column = 0, sticky = tk.W+tk.E, padx = 5, pady = 5, in_ = self.buttonsFrame)
        self.importButton = tk.Button(self.buttonsFrame, text='Import', command=self.load_file) #self.importFile
        self.importButton.grid(row = 0, column = 1)
        self.buttonsFrame.grid(row = 0, column = 0, in_ = self)
        
        self.grid()

    def createWidgets(self):
        
        self.fig = plt.Figure(figsize=(5, 5), dpi=100)
        self.fig.suptitle("Raman Map")
        self.a = self.fig.add_subplot(111)
        self.fig2 = plt.Figure(figsize=(5, 5), dpi=100)
        self.fig2.suptitle("Raman Spectrum")
        self.b = self.fig2.add_subplot(111)
        
        self.buttonsFrame = tk.Frame()
        self.headerLabel = tk.Text(width = 40, highlightbackground="black", highlightcolor="black", highlightthickness=1)
        self.headerLabel.insert(tk.END, self.header.get())
        self.headerLabel.grid(row = 4, column = 0, columnspan = 2, padx = 5, pady = 5, in_ = self.buttonsFrame)
        self.pointEntry = tk.Entry(textvariable = self.point)
        self.pointEntry.grid(row = 0, column = 0, sticky = tk.W+tk.E, padx = 5, pady = 5, in_ = self.buttonsFrame)
        
        self.xEntry = tk.Entry(textvariable = self.xpoint)
        self.xEntry.grid(row = 2, column = 0, sticky = tk.W+tk.E, padx = 5, pady = 5, in_ = self.buttonsFrame)
        self.yEntry = tk.Entry(textvariable = self.ypoint)
        self.yEntry.grid(row = 3, column = 0, sticky = tk.W+tk.E, padx = 5, pady = 5, in_ = self.buttonsFrame)
        
        self.goButton = tk.Button(self.buttonsFrame, text='GO!', command=self.go)
        self.goButton.grid(row = 0, column = 1)
        self.buttonsFrame.grid(row = 1, columnspan = 1, rowspan = 3, column = 0, in_ = self)
        
        self.mapFrame = tk.Frame(bd = 2, bg = 'white', highlightbackground="black", highlightcolor="black", highlightthickness=1)
        self.plotFrame = tk.Frame(bd = 2, bg = 'white', highlightbackground="black", highlightcolor="black", highlightthickness=1)
        
        self.xScale = tk.Scale(self.mapFrame ,orient='vertical', from_=0, to=len(self.importedData[1])-1, resolution = 1, width = 15, length = 475, command=self.set_xvalue)
        self.xScale.grid(row = 1, column = 2)
        
        self.yScale = tk.Scale(self.mapFrame,orient='horizontal', from_=0, to=len(self.importedData[2])-1, resolution = 1, width = 15, length = 475, command=self.set_yvalue)
        self.yScale.grid(row = 2, column = 1)
        
        self.lambdaScale = tk.Scale(self.plotFrame,orient='horizontal', from_=0, to=1019, resolution = 1, width = 15, length = 475, command=self.set_value)
        self.lambdaScale.grid(row = 2, column = 3)
    
        self.figureCanvas = FigureCanvasTkAgg(self.fig, master=self.mapFrame)
        self.figureCanvas.get_tk_widget().grid(row = 1, column = 1, columnspan = 1, rowspan = 1, sticky = tk.N, in_ = self.mapFrame)
        self.mapFrame.grid(row = 1, column = 1, columnspan = 1, rowspan = 1, sticky = tk.N, padx = 20, pady = 20, in_ = self)
        
        self.figureCanvas2 = FigureCanvasTkAgg(self.fig2, master=self.plotFrame)
        self.figureCanvas2.get_tk_widget().grid(row = 1, column = 3, columnspan = 1, rowspan = 1, sticky = tk.N, in_ = self.plotFrame)
        self.plotFrame.grid(row = 1, column = 2, columnspan = 1, rowspan = 1, sticky = tk.N, padx = 20, pady = 20, in_ = self)
    
    def set_value(self, val):
        self.point.set(val)
        self.go()
    
    def set_xvalue(self, val):
        self.xpoint.set(val)
        self.go()
    
    def set_yvalue(self, val):
        self.ypoint.set(val)
        self.go()
    
    def importFile(self):
        self.importedData = importFile(self.filename.get())
        self.xpoint.set(len(self.importedData[1])-1)
        self.ypoint.set(len(self.importedData[2])-1)
        self.header.set(self.importedData[4])
        self.createWidgets()
    
    def go(self):
        self.showMap(self.importedData[1],self.importedData[2],self.importedData[3],self.point.get(),self.importedData[0])

    def showMap(self, x, y, data,p, l):
        self.a.cla()
        self.a.imshow(np.reshape(data[p], (len(x),len(y))))
        self.a.plot(range(0,len(y)),np.ones((len(y)))*self.xpoint.get(), color = 'red')
        self.a.plot(np.ones((len(x)))*self.ypoint.get(),range(0,len(x)), color = 'red')
        self.figureCanvas.show()
        self.b.cla()
        self.b.plot(l,np.transpose(data)[len(y)*self.xpoint.get()+self.ypoint.get()])
        self.b.plot([l[self.point.get()], l[self.point.get()]], [0, 100 + max(np.transpose(data)[len(y)*self.xpoint.get()+self.ypoint.get()])])
        self.b.axis([min(l), max(l), 0, 100 + max(np.transpose(data)[len(y)*self.xpoint.get()+self.ypoint.get()])])
        self.figureCanvas2.show()
        plt.pause(0.001)
        self.update()

    def load_file(self):
        fname = tkinter.filedialog.askopenfilename(filetypes=(("Text Files", "*.txt"),
                                           ("All files", "*.*") ))
        if fname:
           try:
               self.filename.set(fname)
               self.importFile()
           except:
               tkinter.messagebox.showerror("Open Source File", "Failed to read file\n'%s'" % fname)
               return




plt.ion()

root = tk.Tk()
root.title('Raman')

app = Raman(root)
app.mainloop()
