from matplotlib import pyplot 
import numpy 
from textwrap import wrap 
import matplotlib.ticker as ticker 

with open('settings.txt') as file:
    settings = [float(i) for i in file.read().split('\n')]

data = numpy.loadtxt('data.txt', dtype = int) * settings[1] 
data_t = numpy.array([i * settings[0] for i in range(data.size)]) 
fig, ax = pyplot.subplots(figsize = (16, 10), dpi = 500, linewidth = 2) 
ax.axis([data.min(), data_t.max() + 1, data.min(), data.max() + 0.1])

data1 = data.tolist()

index1 = data1.index(max(data1))
index2 = data_t[-1] - data_t[index1]

ax.text(18, 2, f'Время зарядки: {data_t[index1]}', fontsize = 20)
ax.text(18, 1.5, f'Время разрядки: {round(index2, 4)}', fontsize = 20)


ax.xaxis.set_major_locator(ticker.MultipleLocator(2)) 
ax.xaxis.set_minor_locator(ticker.MultipleLocator(0.5)) 


ax.yaxis.set_major_locator(ticker.MultipleLocator(0.5)) 
ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.1)) 

ax.set_ylabel("Напряжение, В", size = 20) 
ax.set_xlabel("Время, с", size = 20) 

ax.set_title('Процесс зарядки и разрядки конденсатора', size = 20, loc = 'center') 

ax.grid(which='major', color = 'k')
ax.minorticks_on() 
ax.grid(which='minor', color = '0.8', linestyle = ':') 

ax.plot(data_t, data, c ='m', linewidth = 1, label = 'V(t)') 
ax.scatter(data_t[0:data.size:20], data[0:data.size:20], marker = 's', c = 'm', s = 10) 
ax.legend(shadow = False, loc = 'upper right', fontsize = 30) 

fig.savefig('graph.png')
fig.savefig('graph.svg')
