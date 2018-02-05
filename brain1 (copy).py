
from PIL import Image, ImageDraw

import multiprocessing

print("Enter image filename (for example \"test.jpg\")")
picture = input()
#picture = "test2.jpg"

image = Image.open(picture)

pixel = image.load()

height = image.size[1]
width = image.size[0]

number_of_clusters = 3

centers = []
points = []

for i in range(number_of_clusters**2):
	centers.append([0, 0, 0, 0, 0])
	
for i in range(width):
	for j in range(height):
		points.append([0, 0, 0])

for i in range(number_of_clusters):
	for j in range(number_of_clusters):
		centers[number_of_clusters * i + j][0] = width / number_of_clusters * i
		centers[number_of_clusters * i + j][1] = height / number_of_clusters * j
		centers[number_of_clusters * i + j][2] = pixel[width / number_of_clusters * i, height / number_of_clusters * j][0]
		centers[number_of_clusters * i + j][3] = pixel[width / number_of_clusters * i, height / number_of_clusters * j][1]
		centers[number_of_clusters * i + j][4] = pixel[width / number_of_clusters * i, height / number_of_clusters * j][2]		


for i in range(width):
	for j in range(height):
		minimum = 1000000000
		curr = 0
		for k in centers:
			distance = ((k[0] - i)**2 + (k[1] - j)**2 + ((k[2] - pixel[i, j][0])**2 + (k[3] - pixel[i, j][1])**2 + (k[4] - pixel[i, j][2])**2))
			if distance < minimum:
				points[i * height + j][0] = i
				points[i * height + j][1] = j
				points[i * height + j][2] = curr
				minimum = distance 
			curr = curr + 1
		
print("zero")

flag = 1
kill = 0

while (flag) & (kill < 5):
	curr = 0
	for k in centers:
		#print(k)
		#su = input()
		new_center = [0, 0, 0, 0, 0]
		num = 0
		for p in points:
			if p[2] == curr:
				new_center[0] = new_center[0] + p[0]
				new_center[1] = new_center[1] + p[1]
				new_center[2] = new_center[2] + pixel[p[0], p[1]][0]
				new_center[3] = new_center[3] + pixel[p[0], p[1]][1]
				new_center[4] = new_center[4] + pixel[p[0], p[1]][2]
				num = num + 1
		new_center[0] = new_center[0] / num
		new_center[1] = new_center[1] / num
		new_center[2] = new_center[2] / num
		new_center[3] = new_center[3] / num
		new_center[4] = new_center[4] / num
		#print(new_center)
		#su = input()
		if (new_center[0] == k[0]) & (new_center[1] == k[1]) & (new_center[2] == k[2]) & (new_center[3] == k[3]) & (new_center[4] == k[4]):
			flag = 0
		else:
			flag = 1
			centers[curr][0] = new_center[0]
			centers[curr][1] = new_center[1]
			centers[curr][2] = new_center[2]
			centers[curr][3] = new_center[3]
			centers[curr][4] = new_center[4]
		curr = curr + 1
		
		for i in range(width):
			for j in range(height):
				minimum = 1000000000
				true_curr = 0
				for k in centers:
					distance = ((k[0] - i)**2 + (k[1] - j)**2 + ((k[2] - pixel[i, j][0])**2 + (k[3] - pixel[i, j][1])**2 + (k[4] - pixel[i, j][2])**2))
					if distance < minimum:
						#points[i * height + j][0] = i
						#points[i * height + j][1] = j
						points[i * height + j][2] = true_curr
						minimum = distance 
					true_curr = true_curr + 1
	print("one")
	kill = kill + 1
	
print("haha")
	
curr = 0		

for k in centers:
	
	cluster_name = "cluster_" + str(curr) + ".jpg"
	
	cluster = Image.open(picture)
	draw = ImageDraw.Draw(cluster)
	
	for p in points:
		if p[2] != curr:
			draw.point((p[0], p[1]), (255, 255, 255))
			
	cluster.save(cluster_name)
	
	curr = curr + 1
	
















