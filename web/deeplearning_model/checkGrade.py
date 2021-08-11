#
'''
21.08.11
소고기와 돼지고기 딥러닝 모델을 활용하는 class

'''
import torch
import torchvision.models as models
import torch.nn as nn
from torchvision import datasets, transforms
from torch.autograd import Variable
from PIL import Image
import PIL

class AIModel:
    def __init__(self):
        self.dir = "./"
        self.pig_model = "pig1"
        self.pig_class = 3
        self.cow_model = "cow1"
        self.cow_class = 5
        self.size = 128
        
        self.device = torch.device('cpu') 
        # 이미지 transformation
        # self.test_compose=transforms.Compose([
            # transforms.Resize((self.size,self.size)),
            # transforms.ToTensor()
        # ])
        self.loader = transforms.Compose(
                    [transforms.Scale(self.size), transforms.ToTensor()]
                )
        
        pass
    
    def getModel(self, classes, model_path):
        model=models.resnext50_32x4d(pretrained=False)
        model.fc=nn.Linear(model.fc.in_features, classes)
        checkpoint = torch.load(model_path+".pht", map_location=self.device)
        model.load_state_dict(checkpoint['state_dict'])
        model = model.eval()
        
        return model
    
    def getTensorImage(self, image_name):
        """load image, returns cuda tensor"""
        image = Image.open(image_name)
        image = self.loader(image).float()
        image = Variable(image, requires_grad=True)
        image = image.unsqueeze(0)  #this is for VGG, may not be needed for ResNet
        return image #.cuda()  #assumes that you're using GPU
    
    def pig(self, image_path):
        input = self.getTensorImage(image_path)
        model = self.getModel(self.pig_class, self.dir + self.pig_model)
        
        output = model(image)
        index = output.data.cpu().numpy().argmax()
        return output, index
        
    def cow(self, image_path):
        input = self.getTensorImage(image_path)
        model = self.getModel(self.cow_class, self.dir + self.cow_model)
        
        output = model(image)
        index = output.data.cpu().numpy().argmax()
        return output, index


if __name__ == "__main__":
    
    pass




        