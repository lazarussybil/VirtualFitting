import os
import time
import cv2

from PIL import Image

# Module API
from remove_api import remove_inference, remove_inference_opencv
from parser.inference_single import inference  as parse_inference
from parser.inference_single import init_model
from vton.inference import inference as vton_inference

class opt():
    def __init__(self, name, stage, data_path, imname, cname, result_dir, checkpoint):
        self.name = name
        self.gpu_ids = ""
        self.workers = 1
        self.batch_size = 4
        self.data_path = data_path
        self.stage = stage
        self.imname = imname
        self.cname = cname
        self.fine_width = 192
        self.fine_height = 256
        self.radius = 5
        self.grid_size = 5
        self.grid_image = 'vton/grid.png'
        self.result_dir = result_dir
        self.checkpoint = checkpoint
        self.shuffle = False

def upload_cloth_api(cloth_image: Image):
    cloth_image = cloth_image.resize((192, 256)).convert('RGB')
    ti = time.localtime()
    ti = '%d-%d-%d-%d' % (ti[2], ti[3], ti[4], ti[5])
    temp_path = "./Database/val/temp/"+ti+"_1.jpg"
    cloth_image.save(temp_path)
    result_cloth, mask = remove_inference_opencv(temp_path)
    result = cv2.cvtColor(result_cloth, cv2.COLOR_BGR2RGB)
    return Image.fromarray(result_cloth), Image.fromarray(mask)

def init_model_api(parsing_model_path="./models/LIP_best.pth"):
    return init_model(parsing_model_path)

def tryon_cloth_api(parsing_model, cloth_image: Image, human_image: Image, cloth_mask: Image):
    ti = time.localtime()
    ti = '%d-%d-%d-%d' % (ti[2], ti[3], ti[4], ti[5])

    # First stage - parsing
    im_path = "./Database/temp/image/"+ti+"_1.jpg"
    human_image.save(im_path)
    parse_inference(parsing_model, im_path=im_path, save_dir="./Database/temp")
    human_name = ti + "_1.jpg"
    cloth_name = ti + "_1.jpg"
    cloth_image.save("./Database/temp/cloth/"+ti+"_1.jpg")
    cloth_mask.save("./Database/temp/cloth-mask/"+ti+"_1.jpg")

    # Second stage - tryon
    gmm_opt = opt(name="gmm_traintest_new", stage="GMM", data_path='./Database/temp', result_dir='./Database/temp', imname=human_name, cname=cloth_name, checkpoint='models/gmm_050000.pth')
    vton_inference(gmm_opt)
    tom_opt = opt(name="tom_test_new", stage="TOM", data_path='./Database/temp', result_dir='./Database/temp/output', imname=human_name, cname=cloth_name, checkpoint='models/tom_100000.pth')
    vton_inference(tom_opt)
    result = Image.open("./Database/temp/output/" + human_name)
    return result

if __name__ == "__main__":
    cloth_name = 'ali.jpg'
    human_name = 'lxgg.jpeg'

    # test upload cloth
    cloth_image = Image.open("./" + cloth_name) # Mock image upload
    result_cloth, cloth_mask = upload_cloth_api(cloth_image)
    result_cloth.save("./Database/test/cloth/" + cloth_name) # Mock cloth image save
    cloth_mask.save("./Database/test/cloth-mask/" + cloth_name) # Mock cloth mask save

    # initialize model
    parsing_model = init_model_api("./models/LIP_best.pth")

    # test tryon
    cloth_image = Image.open("./Database/test/cloth/" + cloth_name) # Mock cloth image load
    cloth_mask = Image.open("./Database/test/cloth-mask/" + cloth_name) # Mock cloth mask load
    human_image = Image.open("./Database/test/image/" + human_name) # Mock human image load
    tryon_result = tryon_cloth_api(parsing_model, cloth_image, human_image, cloth_mask)
    tryon_result.save("./output.jpg") # Mock tryon_result return