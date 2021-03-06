import torch
import time
import torchvision.transforms as transforms


from options.options import Options
import util.dataloader as dl
from models.visual_models import *
import models.audio_models
from torchsummary import summary
from PIL import Image

# this is a file i'm using to test changes, feel free to ignore


opt = Options()
opt.batch_size = 1

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

datas = dl.DataLoader(opt, transform_mode = "resize only")

model = VisAutoEncoder(opt.visual_aa,
                           **opt.visual_aa_args)

model.load_state_dict(torch.load("ckpts/default_model.pt"))
model.train(mode=False)

model = model.to(device)

# silly but simple way to get a single image from the dataset
for i, data in enumerate(datas):

    ins = ""
    while ins != "q":
        plt.imshow(data.detach()[0].permute(1, 2, 0))
        plt.show()
        data = data
        data_out = model.forward(data.to(device))
        ins = input("type n to see images, q to go to next image set...\n")
        print(f"\n you entered {ins}")
        plt.imshow(data_out.cpu().detach()[0].permute(1, 2, 0))
        plt.show()


#summary(model, (3, 512, 512))