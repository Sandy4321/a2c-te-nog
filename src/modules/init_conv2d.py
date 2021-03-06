import torch
import math

class InitConv2d(torch.nn.Conv2d):
    def __init__(self, *args, mode="kaiming", nonlinearity="leaky_relu", **kwargs):
        super(InitConv2d, self).__init__(*args, **kwargs)
        if mode == "orthogonal":
            gain = torch.nn.init.calculate_gain(nonlinearity)
            torch.nn.init.orthogonal_(self.weight.data, gain=gain)
            torch.nn.init.constant_(self.bias.data, 0.0)
        elif mode == "kaiming":
            torch.nn.init.kaiming_uniform_(self.weight, a=math.sqrt(5), nonlinearity=nonlinearity)
            fan_in, _ = torch.nn.init._calculate_fan_in_and_fan_out(self.weight)
            bound = 1 / math.sqrt(fan_in)
            torch.nn.init.uniform_(self.bias, -bound, bound)
        else:
            raise Exception("Unknown init mode %s" % mode)