import matplotlib.pyplot as plt
import numpy as np
import csv


## CSV file name
data_file = 'exp1psnr.csv'
#data_file = 'exp2psnr.csv'


## Read data
with open(data_file,'r') as csvfile:
  plots = csv.reader(csvfile, delimiter=',')
  next(plots)
  data = np.array([[float(val) for val in row] for row in plots])


## Swap axes
data = np.swapaxes(data, 0, 1)


## Make plot
t = [i / 25 for i in range(len(data[0]))]
for i, series in enumerate(data):
  plt.plot(t, series, label='Layer %d' % i)


## y axis
plt.ylabel('PSNR', fontsize=18)
plt.ylim([10, 50])


## x axis
plt.xlabel('Seconds of video', fontsize=18)

plt.legend()
plt.show()