import boto3
import csv
from PIL import Image, ImageDraw, ImageFont
import io 

with open('credentials.csv', 'r') as file:
    next(file)
    reader = csv.reader(file)

    for line in reader:
        access_key_id=line[0]
        secret_access_key = line[1]

client =  boto3.client('rekognition', region_name='us-west-2',
                        aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)

photo = 'photos/puppy.jpeg'

with open(photo, 'rb') as image_file:
    source_bytes = image_file.read()

detect_objects = client.detect_labels(Image={'Bytes': source_bytes})
# print(detect_objects)

image = Image.open(io.BytesIO(source_bytes))
draw = ImageDraw.Draw(image)

for label in detect_objects['Labels']:
    print(label["Name"])
    print("Confidence:", label["Confidence"])

    for instances in label['Instances']:
        if 'BoundingBox' in instances:
            
            box = instances["BoundingBox"]

            left = image.width * box['Left']
            top = image.width * box['Top']
            width = image.width * box['Width']
            height = image.width * box['Height']

            points = (
                (left, top),
                (left+width, top),
                (left+width, top+height),
                (left, top+height),
                (left,top)
            )
            draw.line(points, width=5, fill="#df3eed")

            shape = [(left -2, top-35), (width+2 +left,top)]
            draw.rectangle(shape, fill="#df3eed")

            font=ImageFont.truetype('Rudolph.ttf', 20)
            draw.text((left+10, top-30), label["Name"], font=font, fill="#ffffff")

image.show()