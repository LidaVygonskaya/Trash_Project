import matplotlib.pyplot as plt

x = [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0]
y = [5.6733807131717845e+19, 3.993437168524554e+18, 7.114052055723335e+18, 7.161235510384579e+18, 6.072769680720276e+18, 3.7183783711463547e+18, 3.3901814859639726e+18, 2.6276305384339195e+18, 3.053191092644248e+18, 5.941561529646444e+18, 3.042236699888916e+18, 2.1732772630696061e+18, 2.1111982021404257e+18, 2.223147916446823e+18, 2.422710939128776e+18, 2.0605244064166828e+18, 2.025200832931742e+18, 1.776346334439523e+18]
y2 = [2.6708969930429776e+19, 2.6927198730495275e+19, 1.3676893409524824e+19, 1.1654234826488089e+19, 1.2179496101991027e+19, 1.0108425926489725e+19, 1.0748091671626684e+19, 8.275673898048184e+18, 8.571815871781185e+18, 7.281333042126683e+18, 7.300179290510597e+18, 7.120847397108894e+18, 7.803376206070102e+18, 5.836202540369682e+18, 6.420116756678779e+18, 5.433258837236825e+18, 5.488760100536883e+18, 4.89465989644673e+18]

#Count divided_residuals
def divided_residuals(x_list, y_list):
    step = 1
    f = [[] for a in range(len(x_list) - 1)]
    for element in f:
        if f.index(element) == 0:
            for i in range(1, len(x_list)):
                f1 = (y_list[i] - y_list[i - step]) / (x_list[i] - x_list[i - step])
                element.append(f1)

        else:
            f_last = f[f.index(element) - 1]
            m = 0
            for i in range(1, len(f_last)):
                f1 = (f_last[i] - f_last[i - 1]) / (x_list[m + step] - x_list[m])
                element.append(f1)
                m += 1
        step += 1
    return f


#the value of Neutons polynom in point x_0
def polynomial_fitting(x_list, y_list, f, x_0):
    t = y_list[0]
    for element in f:
        z = 1
        for s in range(f.index(element) + 1):
            z = z * (x_0 - x_list[s])

        z = element[0] * z
        t += z
    return t


def derivative(x_list, y_list):
    der = []
    for j in range(1, len(x_list)):
        d = (y_list[j] - y_list[j - 1]) / (x_list[j] - x_list[j - 1])
        der.append(d)
    return der


x1 = [2.0 ,5.0 , -6.0 ,  7.0  , 4.0 , 3.0, 8.0  , 9.0  , 1.0 , -2.0]
y1 = [-1,	77, -297, 249, 33, 9 ,389, 573, -3 ,-21]

plt.plot(x, y2, 'o')
#
f_list = divided_residuals(x, y2)
t_list = []

for i in range(len(x)):
    t1 = polynomial_fitting(x, y2, f_list, x[i] + 0.75)
    t_list.append(t1)


#plt.plot(x[:-2], t_list[:-2], 'o')
print f_list
plt.show()


der_list = derivative(x, y)
print (der_list)
plt.plot(x[:-1], der_list)
plt.show()