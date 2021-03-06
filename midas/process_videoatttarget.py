import cv2
import torch
import urllib.request
import numpy as np
import os
import matplotlib.pyplot as plt

channel = 1
normalize = True
show = False
save = True

# path
home = os.path.expanduser("~")
load_dir = os.path.join(home, "exper/gaze/attention-target-detection/data/videoatttarget/images")
save_dir = os.path.join(home, "exper/gaze/attention-target-detection/data/videoatttarget/images_depth")

save_dir += "_" + str(channel)
save_dir += "_with_norm" if normalize else "_without_norm"

os.mkdir(save_dir)

# load model
model_type = "DPT_Large"     # MiDaS v3 - Large     (highest accuracy, slowest inference speed)
#model_type = "DPT_Hybrid"   # MiDaS v3 - Hybrid    (medium accuracy, medium inference speed)
#model_type = "MiDaS_small"  # MiDaS v2.1 - Small   (lowest accuracy, highest inference speed)

midas = torch.hub.load("intel-isl/MiDaS", model_type)

# gpu eval if available
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
midas.to(device)
midas.eval()

# transform
midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms")

if model_type == "DPT_Large" or model_type == "DPT_Hybrid":
    transform = midas_transforms.dpt_transform
else:
    transform = midas_transforms.small_transform

for foldername_first in os.listdir(load_dir):
    print("foldername_first: ", foldername_first)
    load_foldername_first = os.path.join(load_dir, foldername_first)
    save_foldername_first = os.path.join(save_dir, foldername_first)
    os.mkdir(save_foldername_first)
    for foldername_second in os.listdir(load_foldername_first):
        print("    foldername_second: ", foldername_second)
        load_foldername_second = os.path.join(load_foldername_first, foldername_second)
        save_foldername_second = os.path.join(save_foldername_first, foldername_second)
        os.mkdir(save_foldername_second)
        for filename in os.listdir(load_foldername_second):
            load_filename = os.path.join(load_foldername_second, filename)
            save_filename = os.path.join(save_foldername_second, filename)

            # load img
            img = cv2.imread(load_filename)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            input_batch = transform(img).to(device)

            # predict
            with torch.no_grad():
                prediction = midas(input_batch)

                prediction = torch.nn.functional.interpolate(
                    prediction.unsqueeze(1),
                    size=img.shape[:2],
                    mode="bicubic",
                    align_corners=False,
                ).squeeze()

            output = prediction.cpu().numpy()

            if channel == 3:
                if save:
                    plt.imsave(save_filename, output)
                if show:
                    plt.imshow(output)
                    plt.show()
            elif channel == 1:
                if normalize:
                    max_val = np.max(output)
                    min_val = np.min(output)
                    output = (output - min_val) / (max_val - min_val) * 255
                if save:
                    cv2.imwrite(save_filename, output)
                if show:
                    cv2.imshow(filename, output)
                    cv2.waitKey(0)