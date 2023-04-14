import torch
import torch.nn as nn
import torchvision.transforms as T
from torchvision.models import resnet18


def to_real_price(price):
    return ((torch.exp(price) - 1) * 1000).item()


class Predictor:
    def __init__(self):
        self.model = resnet18()
        self.model.fc = nn.Sequential(
            nn.Linear(512, 512),
            nn.LeakyReLU(),
            nn.Linear(512, 1)
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
        image = self.transforms(image.convert("RGB")).unsqueeze(0).to(self.device)

        return to_real_price(self.model(image))
