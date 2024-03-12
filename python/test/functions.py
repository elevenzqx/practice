import torch.nn as nn
import torch
import numpy as np
import matplotlib.pyplot as plt

Tanh = nn.Tanh()
x = torch.from_numpy(np.linspace(-5,5,100))
value = Tanh(x)
plt.plot(x, value)
plt.savefig('Tanh.jpg')
