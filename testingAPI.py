import argparse
import io, os

from google.cloud import vision
from google.cloud.vision import types



def annotate(path):
    """Returns web annotations given the path to an image."""
    client = vision.ImageAnnotatorClient()

    if path.startswith('http') or path.startswith('gs:'):
        image = types.Image()
        image.source.image_uri = path

    else:
        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = types.Image(content=content)

    web_detection = client.web_detection(image=image).web_detection

    return web_detection


def report(annotations):
    result = ""
    if annotations.web_entities:
        counter = 0
        for entity in annotations.web_entities:

            #result = result + 'Score      : {} \n'.format(entity.score)
            result = result + str(counter) + '. {} \n'.format(entity.description)
            counter = counter + 1
    return result


def callAPI(imageURL):
    cwd = os.getcwd()
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = cwd + '/creds.json'
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    path_help = str('The image to detect, can be web URI, '
                    'Google Cloud Storage, or path to local file.')
    parser.add_argument('image_url', help=path_help)
    args = imageURL

    result = report(annotate(imageURL))
    return result

