# Dibuat oleh: Cahya Amalinadhi Putra
# 16 Desember 2018, 22:43
# Code ini dapat disebarluaskan untuk tujuan pendidikan

# ============================================ #
#               AIRFOIL GENERATOR
# ============================================ #
# Airfoil adalah bentuk penampang sayap pesawat.
# Ada banyak jenis airfoil, satu yang terkenal adalah NACA 4-Digit Airfoil
#
# Sistem penomoran airfoil ini adalah sebagai berikut:
#       NACA MPXX
#        contoh
#       NACA 2412
#
#           dengan
#           -> XX   ketebalan maksimum (maximum thickness), t/c, (% chord). Ketebalan
#                   maksimum terletak pada 30% chord dari Leading Edge (x/c = 30%)
#           -> P    tebal chamber maksimum terhadap chord dibagi 100, (range 0.00 - 1.00)
#           -> M    posisi chamber maksimum dari Leading Edge terhadap chord dibagi 10, 
#                   x/c, (range 0.0 - 1.0)
#
#   NACA 2412 adalah airfoil dengan:
#       -> ketebalan maksimum 12% chord, terletak pada 30% chord
#       -> memiliki tebal chamber maksimum 2% pada 40% chord

# REFERENSI
# An Introduction To Theoretical and Computational Aerodynamics, Jack Moran
# Computer Program To Obtain Ordinates for NACA Airfoils, NASA, Dec 1996
# http://airfoiltools.com/airfoil/naca4digit
# https://en.wikipedia.org/wiki/NACA_airfoil

# ============================================ #
# MEMBUAT COORDINAT AIRFOIL #

import numpy as np

# Masukan tipe NACA MPXX
XX = 30             # dalam %
P = 40              # dalam %
M = 5               # dalam %

# Masukan jumlah pasangan koordinat airfoil yang akan dibuat
n = 201

# Proses pembuatan airfoil
# ==>
if (n%2 == 0):
    X = np.zeros(int(n/2))     # mendefinisikan koordinat-x
else:
    X = np.zeros(int(n/2) + 1)

delX = 1.0/(len(X) - 1)
for i in range(len(X)):
    X[i] = i*delX

# ==>
Yc = np.zeros(len(X))        # mendefinisikan chamber line
GradYc = np.zeros(len(X))    # mendefinisikan gradien dari chamber line (dYc/dx)

percentXX = XX/100.0
percentP = P/100.0
percentM = M/100.0

for i in range(len(Yc)-1):
    if (X[i] < percentP):
        Yc[i] = (percentM/(percentP**2))*(2*percentP*X[i] - X[i]**2)
        GradYc[i] = (2.0*percentM/(percentP**2))*(percentP - X[i])
    else:
        Yc[i] = (percentM/(1 - percentP)**2)*(1 - 2*percentP + 2*percentP*X[i] - X[i]**2)
        GradYc[i] = (2*percentM/(1 - percentP)**2)*(percentP - X[i])

# ==>
Yt = np.zeros(len(X))        # mendefinisikan fungsi ketebalan
#a = [0.2969, -0.126, -0.3516, 0.2843, -0.1015]  # untuk trailing edge terbuka
a = [0.2969, -0.126, -0.3516, 0.2843, -0.1036]  # untuk trailing edge tertutup

for i in range(len(Yt)):
    for j in range(len(a)):
        if j > 0:
            Yt[i] = Yt[i] + a[j]*X[i]**j
        else:
            Yt[i] = Yt[i] + a[j]*X[i]**0.5
    Yt[i] = (percentXX/0.2)*Yt[i]

# ==>
import math

Xu = np.zeros(len(X))
Xl = np.zeros(n-len(X))
Yu = np.zeros(len(Xu))
Yl = np.zeros(len(Xl))
theta = np.zeros(len(GradYc))

for i in range(len(Xu)):
    Xu[i] = X[i] - Yt[i]*math.sin(theta[i])
    Yu[i] = Yc[i] + Yt[i]*math.cos(theta[i])

for i in range(len(Xl)):
    Xl[i] = X[i] + Yt[i]*math.sin(theta[i])
    Yl[i] = Yc[i] - Yt[i]*math.cos(theta[i])

# ============================================ #
# MENYIMPAN KOORDINAT AIRFOIL #
if (n%2 == 0):
    xCoor = np.zeros(n-1)
    yCoor = np.zeros(n-1)
    for i in range(len(xCoor)):
            if i < len(X):
                xCoor[i] = Xu[len(X)-1-i]
                yCoor[i] = Yu[len(X)-1-i]
            else:
                xCoor[i] = Xl[i+1-len(X)]
                yCoor[i] = Yl[i+1-len(X)]
else:
    xCoor = np.zeros(n)
    yCoor = np.zeros(n)
    for i in range(len(xCoor)):
        if i < len(X):
            xCoor[i] = Xu[len(X)-1-i]
            yCoor[i] = Yu[len(X)-1-i]
        elif (i>= len(X) and i < len(xCoor)-1):
            xCoor[i] = Xl[i+1-len(X)]
            yCoor[i] = Yl[i+1-len(X)]
        else:
            xCoor[i] = Xu[-1]
            yCoor[i] = Yu[-1]

namaFile = 'textfile.txt'
np.savetxt(namaFile, np.transpose([xCoor, yCoor]))

# ============================================ #
# MENGGAMBAR KOORDINAT AIRFOIL #
import matplotlib.pyplot as plt

plt.title('Airfoil NACA ' + str(M) + str(P/10) + str(XX))
plt.plot(Xu, Yu, 'r')
plt.scatter(Xu, Yu)
plt.plot(Xl, Yl, 'b')
plt.scatter(Xl, Yl)
plt.xlabel('x/c')
plt.ylabel('y/c')
plt.axis([0.0, 1.0, -0.3, 0.3])
plt.grid(True)
plt.show()
