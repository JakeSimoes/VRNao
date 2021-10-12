from naoqi import ALProxy
from PIL import Image
import time
import sys

"""
This file serves only to grab and save images from NAO when called.
"""


def showNaoImage(IP, PORT, id, calls):
    visionProxy = ALProxy("ALVideoDevice", "127.0.0.1", 9559)
    subscriberID = "bruh5"
    subscriberID = visionProxy.subscribeCamera(subscriberID, 0, 1, 11, 5)
    visionProxy.getImageRemote(subscriberID)
    """
    First get an image from Nao, then show it on the screen with PIL.
    """

    camProxy = ALProxy("ALVideoDevice", IP, PORT)
    resolution = 2  # VGA
    colorSpace = 11  # RGB

    videoClient = camProxy.subscribe("python_client", resolution, colorSpace, 5)

    t0 = time.time()

    # Get a camera image.
    # image[6] contains the image data passed as an array of ASCII chars.
    naoImage = camProxy.getImageRemote(videoClient)

    t1 = time.time()

    # Time the image transfer.

    camProxy.unsubscribe(videoClient)

    # Now we work with the image returned and save it as a PNG  using ImageDraw
    # package.

    # Get the image size and pixel array.
    imageWidth = naoImage[0]
    imageHeight = naoImage[1]
    array = naoImage[6]

    # Create a PIL Image from our pixel array.
    im = Image.frombytes("RGB", (imageWidth, imageHeight), array)

    # Save the image.
    im.save("{}camImage{}.png".format(id, str(calls)), "PNG")
    visionProxy.unsubscribe(subscriberID)


if __name__ == '__main__':
    _, id, call = sys.argv
    showNaoImage("127.0.0.1", 9559, id, call)
