import torch

x = torch.randn(3,1,5,4)
print(x)

conv = torch.nn.Conv2d(1,4,(2,2), 1, padding=(0,1))
res = conv(x)

print(res)
print(res.shape)    # torch.Size([3, 4, 4, 2])