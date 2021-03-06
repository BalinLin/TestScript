#! /usr/bin/env python3
# coding=utf-8

import cv2, torch
import os
import numpy as np
import matplotlib.pyplot as plt
import time
from collections import Counter
import torchvision.models as models


if __name__ == "__main__":
    a = torch.randn(2,3,4)
    print("a: ", a)
    b = torch.randn(2,3,4)
    print("b: ", b)
    c = a + b
    print("c: ", c)
    c = c + 1
    print("c: ", c)
    d = a * b
    print("d: ", d)

    a = torch.randn(10,1,2,2)
    print("a: ", a)
    b = torch.randn(10,1,1,1)
    print("b: ", b)
    c = a * b
    print("c: ", c)
