import argparse
import os.path
import time
from option import Option
from pathlib import Path

import cv2
import torch
import torch.backends.cudnn as cudnn
from numpy import random

from models.experimental import attempt_load
from utils.datasets import LoadImages
from utils.general import check_img_size, check_requirements, non_max_suppression
from utils.general import scale_coords, xyxy2xywh, set_logging, increment_path, save_one_box
from utils.plots import colors, plot_one_box
from utils.torch_utils import select_device, time_synchronized


def detect(option: Option = Option()) -> str:
    source, weights, view_img = option.source, option.weights, option.view_img
    save_txt, img_size = option.save_txt, option.img_size
    # save inference images
    save_img = not option.nosave and not source.endswith('.txt')

    # Directories
    # increment run
    save_dir = increment_path(Path(option.project) / option.name, exist_ok=option.exist_ok)
    # make dir
    (save_dir / 'labels' if save_txt else save_dir).mkdir(parents=True, exist_ok=True)

    # Initialize
    set_logging()
    device = select_device(option.device)
    # half precision only supported on CUDA
    half = device.type != 'cpu'

    # Load model
    # load FP32 model
    model = attempt_load(weights, map_location=device)
    # model stride
    stride = int(model.stride.max())
    # check img_size
    img_size = check_img_size(img_size, s=stride)
    # get class names
    names = model.module.names if hasattr(model, 'module') else model.names
    if half:
        # to FP16
        model.half()

    # Set Dataloader
    dataset = LoadImages(source, img_size=img_size, stride=stride)

    # Run inference
    if device.type != 'cpu':
        # run once
        model(torch.zeros(1, 3, img_size, img_size).to(device).type_as(next(model.parameters())))
    t0 = time.time()
    for path, img, im0s, vid_cap in dataset:
        img = torch.from_numpy(img).to(device)
        # uint8 to fp16/32
        img = img.half() if half else img.float()
        # 0-255 to 0.0-1.0
        img /= 255.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # Inference
        t1 = time_synchronized()
        pred = model(img, augment=option.augment)[0]

        # Apply NMS
        pred = non_max_suppression(pred, option.conf_thres, option.iou_thres, classes=option.classes,
                                   agnostic=option.agnostic_nms)
        t2 = time_synchronized()

        # Process detections
        for det in pred:  # detections per image
            p, s, im0, frame = path, '', im0s.copy(), getattr(dataset, 'frame', 0)

            p = Path(p)  # to Path
            save_path = str(save_dir / p.name)  # img.jpg
            txt_path = str(save_dir / 'labels' / p.stem) + ('' if dataset.mode == 'image' else f'_{frame}')  # img.txt
            s += '%gx%g ' % img.shape[2:]  # print string
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                # Print results
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

                # Write results
                for *xyxy, conf, cls in reversed(det):
                    if save_txt:  # Write to file
                        xywh = (torch.tensor(xyxy).view(1, 4)).view(-1).tolist()  # normalized xywh
                        line = (cls, *xywh, conf) if option.save_conf else (cls, *xywh)  # label format
                        with open(txt_path + '.txt', 'a') as f:
                            f.write(('%g ' * len(line)).rstrip() % line + '\n')

                    if save_img or option.save_crop or view_img:  # Add bbox to image
                        c = int(cls)  # integer class
                        label = f'{names[c]} {conf:.2f}'

                        plot_one_box(xyxy, im0, label=label, color=colors(c, True),
                                     line_thickness=option.line_thickness)
                        if option.save_crop:
                            save_one_box(xyxy, im0s, file=save_dir / 'crops' / names[c] / f'{p.stem}.jpg', BGR=True)

            # Print time (inference + NMS)
            print(f'{s}Done. ({t2 - t1:.3f}s)')

            # Save results (image with detections)
            if save_img:
                if dataset.mode == 'image':
                    cv2.imwrite(save_path, im0)

    if save_txt or save_img:
        s = f"\n{len(list(save_dir.glob('labels/*.txt')))} labels saved to {save_dir / 'labels'}" if save_txt else ''
        print(f"Results saved to {save_dir}{s}")

    print(f'Done. ({time.time() - t0:.3f}s)')

    return os.path.abspath(save_dir)


if __name__ == '__main__':
    check_requirements(exclude=('tensorboard', 'pycocotools', 'thop'))

    with torch.no_grad():
        detect(option=Option())
