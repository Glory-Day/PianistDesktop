class Option:
    def __init__(self):
        self.__dict__['weights'] = 'models/besk.pt'
        self.__dict__['source'] = 'models/data/images'
        self.__dict__['img_size'] = 2048
        self.__dict__['conf_thres'] = 0.8
        self.__dict__['iou_thres'] = 0.5
        self.__dict__['device'] = ''
        self.__dict__['view_img'] = False
        self.__dict__['save_txt'] = True
        self.__dict__['save_conf'] = True
        self.__dict__['save_crop'] = True
        self.__dict__['nosave'] = False
        self.__dict__['classes'] = None
        self.__dict__['agnostic_nms'] = False
        self.__dict__['augment'] = False
        self.__dict__['update'] = False
        self.__dict__['project'] = '/runs/detect'
        self.__dict__['name'] = 'exp'
        self.__dict__['exist_ok'] = False
        self.__dict__['line_thickness'] = 1
        self.__dict__['hide_labels'] = False
        self.__dict__['hide_conf'] = False
