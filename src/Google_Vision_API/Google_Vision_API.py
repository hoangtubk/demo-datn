"""
* Created by PyCharm.
* User: tuhoangbk
* Date: 05/10/2018
* Time: 23:28
*Have a nice day　:*)　:*)
"""
from google.cloud import vision
from google.cloud.vision import types
import io

def get_text_from_image(path_to_image):
    """Detects text in the file."""
    client = vision.ImageAnnotatorClient()
    # [START migration_text_detection]
    with io.open(path_to_image, 'rb') as image_file:
        content = image_file.read()
    image = types.Image(content=content)
    response = client.text_detection(image=image)
    res = 'None'
    texts = response.text_annotations
    try:
        res = texts[0].description
    except:
        print('error string at file: ' + path_to_image)

    return res

def detect_document(path):
    """Detects document features in an image."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.document_text_detection(image=image)
    arr_blocks = []
    boxes = []
    arr_bounding_box = []
    thresh_hold = 0.7
    for page in response.full_text_annotation.pages:#1
        for block in page.blocks:#3
            print('\nBlock confidence: {}\n'.format(block.confidence))

            for paragraph in block.paragraphs:#1
                print('Paragraph confidence: {}'.format(
                    paragraph.confidence))

                for word in paragraph.words:#1
                    word_text = ''.join([
                        symbol.text for symbol in word.symbols
                    ])
                    print('Word text: {} (confidence: {})'.format(
                        word_text, word.confidence))
                    if word.confidence > thresh_hold:
                        arr_blocks.append(word_text)
                        arr_bounding_box.append(paragraph.bounding_box)
                    for symbol in word.symbols:#3, 9, 9
                        print('\tSymbol: {} (confidence: {})'.format(
                            symbol.text, symbol.confidence))

    for box in arr_bounding_box:
        box_vertices = []
        for point in box.vertices:
            box_vertices.append(point.x)
            box_vertices.append(point.y)
        boxes.append(box_vertices)

    return arr_blocks, boxes

def detect_document_uri(uri):
    """Detects document features in the file located in Google Cloud
    Storage."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()
    image = vision.types.Image()
    image.source.image_uri = uri

    response = client.document_text_detection(image=image)

    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            print('\nBlock confidence: {}\n'.format(block.confidence))

            for paragraph in block.paragraphs:
                print('Paragraph confidence: {}'.format(
                    paragraph.confidence))

                for word in paragraph.words:
                    word_text = ''.join([
                        symbol.text for symbol in word.symbols
                    ])
                    print('Word text: {} (confidence: {})'.format(
                        word_text, word.confidence))

                    for symbol in word.symbols:
                        print('\tSymbol: {} (confidence: {})'.format(
                            symbol.text, symbol.confidence))