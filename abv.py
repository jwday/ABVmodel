import numpy as np
import matplotlib.pyplot as plt

# Inputs
abv = 0.05				# ABV of beverage
vol = 16				# Volume of single beverage [fl. oz.]
n = 1					# Number of beverages consumed
# rest = 0				# Time between finishing one drink and starting the next [min] (NOT IMPLEMENTED)
r = 20					# Time to consume each beverage at constant rate [min]
weight = 68				# Weight (mass) [kg]
hydration = 0.58		# What percentage of water are you?
k1 = 0.109456			# Rate at which alcohol in stomach is transferred to bloodstream [Emperical]
k2 = 0.017727			# Rate at which alcohol in bloodstream is processed by liver [Emperical]

# Constants
rho_alc = 789.45		# Density of pure alcohol [g/L]
vol_blood = 4.5			# Volume of blood in human body [L]

# Calculations and Converstions
h2o = weight*hydration	# Volume of water in body [L]
vol*= 29.5735/1000		# Convert volume of beverage [L]
tot = n*vol*abv			# Volume of pure alcohol consumed [L]
m = 1000*rho_alc*tot	# Mass of pure alcohol consumed [mg]



# Stomach Alcohol Content [mg/L]
def A_func(A0, t, d):
	if d == 1:
		foo = ((m/h2o)/r)
		A = -(foo/k1)*np.exp(-k1*t) + foo/k1
	else:
		A = a[r]*np.exp(-k1*(t-r))
	return A

# Blood Alcohol Content [mg/L]
def BAC(a, t):
	if d == 1:
		foo = ((m/h2o)/r)
		c1 = -foo/(k1-k2) - foo/k2
		B = c1*np.exp(-k2*t) + (foo/(k1-k2))*np.exp(-k1*t) + foo/k2
	else:
		B = a[t]*k1/(k2-k1) + (b[r] - a[r]*k1/(k2-k1))*np.exp(-k2*(t-r))
	return B

# Blood Alcohol Content [%]
def BAC_P(b, rho_alc):
	# return 100*b/(rho_alc*1000)
	return b/10000

# Estimated BAC (Widmark Formula)
def EBAC(t):
	ebac = 100*(m/(h2o*10**6)) - k2*(t/60)
	if ebac < 0:
		ebac = 0
	return ebac

a = []
b = []
p = []
ebac = []
time = range(100)

for t, i in enumerate(time):
	if t <= r:
		d = 1
	else:
		d = 0
	a.append(A_func(0, t, d))
	b.append(BAC(a, t))
	p.append(BAC_P(b[i], rho_alc))
	ebac.append(EBAC(t))

print('Total alcohol volume: {} fl. oz.'.format(tot))
print('Alcohol leaves the body at an average rate of 0.015 g/100mL/hour')

fig, (ax1, ax2, ax3) = plt.subplots(1,3, figsize=(15,5), constrained_layout=True)

ax1.plot(time, a)
ax1.set_title(r'Stomach Alcohol Concentration')
ax1.set_xlabel(r'Time $[min]$')
ax1.set_ylabel(r'SAC $[mg/L]$')
ax1.grid()

ax2.plot(time, b)
ax2.set_title(r'Blood Alcohol Concentration')
ax2.set_xlabel(r'Time $[min]$')
ax2.set_ylabel(r'BAC $[mg/L]$')
ax2.grid()

ax3.plot(time, p, label='Analytical')
ax3.plot(time, ebac, label='Widmark Formula')
ax3.set_title(r'Blood Alcohol Percentage')
ax3.set_xlabel(r'Time $[min]$')
ax3.set_ylabel(r'BAC (%) $[g/100 mL]$')
ax3.legend()
ax3.grid()

fig.suptitle(r'{}x {} fl. oz. Serving of a {}% ABV Beverage Consumed in {} minutes'.format(n, round(vol*1000/29.5735), round(abv*100), r), fontsize=16)

plt.show()