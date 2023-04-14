import torch
import torch.nn as nn
import torchvision.transforms as T
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
from torch import channels_last, float16
from torchvision.models import resnet18


def to_real_price(price):
    return torch.clamp((torch.exp(price) - 1) * 1000, 500, 30000).item()


class Predictor:
    def __init__(self):
        self.model = resnet18()
        self.model.fc = nn.Sequential(
            nn.Linear(512, 256),
            nn.LeakyReLU(),
            nn.Linear(256, 1)
        )

        self.model.load_state_dict(torch.load("weights.pth", map_location="cpu"))

        self.transforms = T.Compose(
            [
                T.Resize((224, 224)),
                T.ToTensor(),
                T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ]
        )

        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

        self.model.to(self.device)
        self.model.eval()

    @torch.inference_mode()
    def predict(self, image) -> float:
        image = self.transforms(image).unsqueeze(0).to(self.device)

        return to_real_price(self.model(image))


class ImageVariation:
    def __init__(self):
        self.pipeline = DiffusionPipeline.from_pretrained(
            "stabilityai/stable-diffusion-2-1-unclip-small",
            torch_dtype=float16
        )
        self.pipeline.enable_xformers_memory_efficient_attention()
        self.pipeline.unet.to(memory_format=channels_last)
        self.pipeline.scheduler = DPMSolverMultistepScheduler.from_config(self.pipeline.scheduler.config)

        self.pipeline.to(torch.device('cuda:0' if torch.cuda.is_available() else 'cpu'))

    @torch.inference_mode()
    def predict(self, image):
        return self.pipeline(image.resize((512, 512)), num_images_per_prompt=5).images
