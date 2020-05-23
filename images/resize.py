from PIL import Image
img_name = 'password.png'
image = Image.open(img_name)
resize_image = image.resize((70, 70))
resize_image.save('new_pasword.png')
