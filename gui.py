import tkinter as tk
from tkinter import messagebox
import utilities
from matplotlib import pylab as plt
import smoothing
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)

#Clear window from all element in the interface
def clear_frame(window):
    list = window.pack_slaves()
    for l in list:
        l.destroy()

#Check if alpha is between 0 and 1
def check_alpha(textBox, window):
    str = textBox.get("1.0",'end-1c')
    try:
        alfa = float(str)
        if(alfa < 0 or alfa > 1):
            messagebox.showerror(title="Error", message="Alfa not valid")
            return -1
        else:
            return alfa
    except ValueError:
        messagebox.showerror(title="Error", message="Alfa  not valid")
        return -1

#Check if beta is between 0 and 1
def check_beta(textBox, window):
    str = textBox.get("1.0", 'end-1c')
    try:
        beta = float(str)
        if (beta < 0 or beta > 1):
            messagebox.showerror(title="Error", message="Beta not valid")
            return -1
        else:
            return beta
    except ValueError:
        messagebox.showerror(title="Error", message="Beta not valid")
        return -1

#Clear the page and put initial component on the window
def backInitialPage(window):
    clear_frame(window)
    setup_gui_input_source(window)

#Function that call single smoothing
def setup_plot(all_dates, all_times, dates, result, window, n_prediction):
    fig = Figure(figsize=(9, 5), dpi=100)
    plt_figure = fig.add_subplot(111)
    plt_figure.plot(all_dates, all_times, "-b", label="Original Data")
    if(n_prediction == 1):
        plt_figure.plot(dates, result, "-r", label="Single Smoothing")
    else:
        plt_figure.plot(dates, result, "-r", label="Double Smoothing")
    plt_figure.axvline(dates[int((len(all_dates)/ 4 * 3))-n_prediction], 0,c="g", label='Start predictions')
    plt_figure.legend(loc="upper right")
    canvas = FigureCanvasTkAgg(fig, master=window)  # A tk.DrawingArea.
    canvas.draw()
    list = window.pack_slaves()
    if (len(list) > 10):
        list[10].destroy()  #delete old canvas
        list[11].destroy()
        list[12].destroy()
    return canvas


def call_single_smoothing(data, window, options, list_metrics, textBox):
    alfa = check_alpha(textBox, window)
    if(alfa == -1):
        return
    index_metric = list_metrics.index(options.get(), 0, len(list_metrics)) #get index of metric in the array
    values = data['data']['result'][index_metric]['values'] #get values from data read
    all_dates = []
    all_times = []
    for timestamp, value in values:
        all_dates.append(timestamp) #inserisco i dati delle serie temporali in degli array rappresentanti gli assi cartesiani
        all_times.append(float(value))
    len_training = int(len(data['data']['result'][index_metric]['values']) / 4 * 3 ) # 2/3 dati di training
    dates = []
    times = []
    for i in range(len_training+1):
        dates.append(values[i][0])
        times.append(float(values[i][1]))
    dates.append(values[len_training][0])
    result = smoothing.exponential_smoothing(times, alfa)
    canvas = setup_plot(all_dates, all_times, dates, result, window, 1)
    canvas.get_tk_widget().pack()
    times.append(all_times[len(times)])
    SSE = smoothing.sse(times, result)
    sse_string = 'SSE: ' + str(SSE)
    label_sse = tk.Label(window, text=sse_string, width=25)
    label_sse.pack()
    buttonBack = tk.Button(window, height=1, width=20, text="Back", command=lambda: backInitialPage(window))
    buttonBack.pack();

#Function that call double smoothing
def call_double_smoothing(data, window, options, list_metrics, textBoxAlfa, textBoxBeta):
    alfa = check_alpha(textBoxAlfa, window)
    if(alfa == -1):
        return
    beta = check_beta(textBoxBeta, window)
    if(beta == -1):
        return
    index_metric = list_metrics.index(options.get(), 0, len(list_metrics))
    values = data['data']['result'][index_metric]['values']
    all_dates = []
    all_times = []
    for timestamp, value in values:
        all_dates.append(timestamp)  # inserisco i dati delle serie temporali in degli array rappresentanti gli assi cartesiani
        all_times.append(float(value))
    len_training = int(len(data['data']['result'][index_metric]['values']) / 4 * 3)  # 2/3 dati di training
    dates = []
    times = []
    for i in range(len_training + 1):
        dates.append(values[i][0])
        times.append(float(values[i][1]))
    plt.plot(all_dates, all_times)
    dates.append(values[len_training][0])
    dates.append(values[len_training+1][0])
    result = smoothing.double_exponential_smoothing(times, alfa, beta)
    canvas = setup_plot(all_dates, all_times, dates, result, window, 2)
    canvas.get_tk_widget().pack()
    times.append(all_times[len(times)])
    times.append(all_times[len(times)+1])
    SSE = smoothing.sse(times, result)
    sse_string = 'SSE: ' + str(SSE)
    label_sse = tk.Label(window, text=sse_string, width=25)
    label_sse.pack()
    buttonBack = tk.Button(window, height=1, width=20, text="Back", command=lambda: backInitialPage(window))
    buttonBack.pack();

#Function that setup component for the analysis interface
def setup_gui_input_analysis(window, data):
    list_metrics = utilities.get_metrics(data)
    window.geometry("950x800")  # Size of the window
    window.title("Smoothing Data Series")  # Adding a title
    options = tk.StringVar(window)
    options.set(list_metrics[0])  # default value
    label_input_metric = tk.Label(window, text='Metric', width=25)
    label_input_metric.pack()
    om1 = tk.OptionMenu(window, options, *list_metrics)
    om1.pack()
    label_input_alfasingle = tk.Label(window, text='Alfa', width=25)
    label_input_alfasingle.pack()
    textBoxAlfaSingle = tk.Text(window, height=1, width=20)
    textBoxAlfaSingle.pack()
    buttonSingle = tk.Button(window, height=1, width=20, text="Single Smoothing", command=lambda: call_single_smoothing(data, window, options, list_metrics, textBoxAlfaSingle))
    buttonSingle.pack()
    label_input_alfadouble = tk.Label(window, text='Alfa', width=25)
    label_input_alfadouble.pack()
    textBoxAlfaDouble= tk.Text(window, height=1, width=20)
    textBoxAlfaDouble.pack()
    label_input_betadouble = tk.Label(window, text='Beta', width=25)
    label_input_betadouble.pack()
    textBoxBetaDouble= tk.Text(window, height=1, width=20)
    textBoxBetaDouble.pack()
    buttonDouble = tk.Button(window, height=1, width=20, text="Double Smoothing", command=lambda: call_double_smoothing(data, window, options, list_metrics, textBoxAlfaDouble, textBoxBetaDouble))
    #buttonDouble.grid(row=2, column= 2)
    buttonDouble.pack()

#Function that read call read from json or prometheus
def retrieve_input_source(options, textBox, window):
    choice = options.get()
    if (choice == 'JSON'):
        filename = textBox.get("1.0",'end-1c')
        data = utilities.read_json_file(filename)
        if (data == []):
            messagebox.showerror(title="Error", message="File Name not valid")
        else:
            clear_frame(window)
            setup_gui_input_analysis(window, data)
    else:
        data = utilities.read_from_prometheus()
        if(data == []):
            messagebox.showerror(title="Error", message="Prometheus not launched")
        else:
            clear_frame(window)
            setup_gui_input_analysis(window, data)
    print(choice)

#Function that setup gui for the start page
def setup_gui_input_source(window):
    window.geometry("600x200")  # Size of the window
    window.title("Smoothing Data Series")  # Adding a title
    options = tk.StringVar(window)
    options.set("JSON")  # default value
    label_input_series = tk.Label(window, text='Input Data Series', width=25)
    label_input_series.pack()
    om1 = tk.OptionMenu(window, options, "JSON", "Prometheus")
    om1.pack()
    label_input_filename = tk.Label(window, text='Input File Name If JSON', width=15)
    label_input_filename.pack()
    textBox = tk.Text(window, height=1, width=20)
    textBox.pack()
    buttonCommit = tk.Button(window, height=1, width=20, text="Commit", command=lambda: retrieve_input_source(options, textBox, window))
    #buttonCommit.grid(row=3, column= 1)
    buttonCommit.pack()
    window.mainloop()

#Create the window
def create_window():
    window = tk.Tk()
    setup_gui_input_source(window)