import cv2, numpy

def preprocess(filename):        
    img=[]
    n = numpy.fromfile(filename, numpy.uint8)
    #n = numpy.array(image)
    _img = cv2.imdecode(n, cv2.IMREAD_COLOR)
    _img = cv2.cvtColor(_img, cv2.COLOR_BGR2RGB)
    _img = cv2.resize(_img, (224, 224))
    _img = cv2.cvtColor(_img, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(_img)
    assert(len(l.shape)==2)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))      # Create CLAHE Object
    clahe_image = numpy.empty(l.shape, dtype='uint8')
    l = clahe.apply(numpy.array(l, dtype='uint8'))
    processed_image = cv2.merge((l, a, b))
    processed_image = cv2.cvtColor(processed_image, cv2.COLOR_LAB2RGB)

    img.append(processed_image)
    img = numpy.array(img, dtype="uint8")
    return img