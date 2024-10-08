#!/usr/bin/env python3

"""Image transformations."""
import torchvision as tv
from data_utils.autoaugment import AutoAugImageNetPolicy

def get_transforms(split, size, pretrained_model, args):
    # if using clip backbones, we adopt clip official normalization.
    if pretrained_model.startswith("clip-"):
        normalize = tv.transforms.Normalize(
            mean=(0.48145466, 0.4578275, 0.40821073), std=(0.26862954, 0.26130258, 0.27577711)
        )
    # elif pretrained_model in ["vit-b-22k", "beit-b-1k", "peco-b-1k"]:
    #     normalize = tv.transforms.Normalize(
    #         mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5)
    #     )
    else:
        normalize = tv.transforms.Normalize(
            mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
        )

    # define the sizes used for resizing and cropping
    if size == 448:
        resize_dim = 512
        crop_dim = 448
    elif size == 224:
        # resize_dim = 270
        resize_dim = args.resize_dim
        # resize_dim = 256
        crop_dim = 224
    elif size == 384:
        resize_dim = 438
        crop_dim = 384
        

    # applying different tranforms for training and test
    if split == "train":
        if args.dataset == 'stanford_cars':
            print('using autoaugment')
            transform = tv.transforms.Compose(
            [
                tv.transforms.Resize(resize_dim),
                tv.transforms.RandomCrop(crop_dim),
                tv.transforms.RandomHorizontalFlip(0.5),
                AutoAugImageNetPolicy(),
                tv.transforms.ToTensor(),
                normalize,
            ]
        )
        else:  
            transform = tv.transforms.Compose(
                [
                    tv.transforms.Resize(resize_dim),
                    tv.transforms.RandomCrop(crop_dim),
                    tv.transforms.RandomHorizontalFlip(0.5),
                    tv.transforms.ToTensor(),
                    normalize,
                ]
            )
    else:
        transform = tv.transforms.Compose(
            [
                # tv.transforms.Resize(args.test_resize_dim),
                tv.transforms.Resize(resize_dim),
                tv.transforms.CenterCrop(crop_dim),
                tv.transforms.ToTensor(),
                normalize,
            ]
        )
        
    # applying different tranforms for training and test
    # if split == "train":
    #     transform = tv.transforms.Compose(
    #         [
    #             tv.transforms.Resize(224),
    #             tv.transforms.RandomCrop(224),
    #             tv.transforms.RandomHorizontalFlip(0.5),
    #             tv.transforms.ToTensor(),
    #             normalize,
    #         ]
    #     )
    # else:
    #     transform = tv.transforms.Compose(
    #         [
    #             tv.transforms.Resize(224),
    #             tv.transforms.CenterCrop(224),
    #             tv.transforms.ToTensor(),
    #             normalize,
    #         ]
    #     )
    return transform
