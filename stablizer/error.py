import numpy as np
import matplotlib.pyplot as plt
plt.tight_layout()

x = np.array([8,22,29,35,45,54,66])
y = np.array([980,2850,3690,4400,5680,7030,8890])/126.4
plt.figure(1,figsize=(5,4))
plt.scatter(x,y)
plt.plot(x,x)
plt.xlabel('measured length / cm')
plt.ylabel('calculated length / cm')
plt.savefig('output/expect.png')


plt.figure(2,figsize=(5,4))
plt.plot(x,np.abs(x-y))
plt.xlabel('measured length / cm')
plt.ylabel('absolute deviation / cm')
plt.savefig('output/deviation.png')
