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
        self.dir = "deeplearning_model/"
        self.pig_model = "pig1"
        self.pig_class = 3
        self.cow_model = "cow1"
        self.cow_class = 5
        self.__size = 128
        
        self.__device = torch.device('cpu') 
        # 이미지 transformation
        # self.test_compose=transforms.Compose([
            # transforms.Resize((self.__size,self.__size)),
            # transforms.ToTensor()
        # ])
        self.__loader = transforms.Compose(
                    [transforms.Scale(self.__size), transforms.ToTensor()]
                )
        
        pass
    
    def __getModel(self, classes, model_path):
        model=models.resnext50_32x4d(pretrained=False)
        model.fc=nn.Linear(model.fc.in_features, classes)
        checkpoint = torch.load(model_path+".pht", map_location=self.__device)
        model.load_state_dict(checkpoint['state_dict'])
        model = model.eval()
        
        return model
    
    def __getTensorImage(self, image_name):
        """load image, returns cuda tensor"""
        image = Image.open(image_name)
        image = self.__loader(image).float()
        image = Variable(image, requires_grad=True)
        image = image.unsqueeze(0)  #this is for VGG, may not be needed for ResNet
        return image #.cuda()  #assumes that you're using GPU
    
    def pig(self, image_path):
        input = self.__getTensorImage(image_path)
        model = self.__getModel(self.pig_class, self.dir + self.pig_model)
        
        output = model(input)
        index = output.data.cpu().numpy().argmax()
        return output, index
        
    def cow(self, image_path):
        input = self.__getTensorImage(image_path)
        model = self.__getModel(self.cow_class, self.dir + self.cow_model)
        output = model(input)
        index = output.data.cpu().numpy().argmax()
        return output, index


if __name__ == "__main__":
    imdir = "./sample/cow/"
    impath = "1++-2"
    
    model = AIModel()
    output, index = model.cow( imdir + impath + '.jpg' )
    print("output>", output)
    print("index>", index)
    pass




        