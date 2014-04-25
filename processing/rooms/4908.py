origin = 'south-east'

# LTC6900
# f = 10 mHz * ( (20 k) / (N * Rset) )
# N = 100 [div pin tied to VCC]
# R1 = 2 M
# R2 = 1 M
# R3 = 800 K
# R4 = 500 K

def addR(R1, R2):
	if R1 == 0:
		return R2
	return 1.0 / ((1.0/R1) + (1.0/R2))

def dip2f(d1=False, d2=False, d3=False, d4=False):
	Rset = 0
	if d1:
		Rset = addR(Rset, 2e6)
	if d2:
		Rset = addR(Rset, 1e6)
	if d3:
		Rset = addR(Rset, 806e3)
	if d4:
		Rset = addR(Rset, 499e3)
	return 10e6 * ( (20e3) / (100 * Rset))

def dip2f_meas(d1, d2, d3, d4):
	MEASURED = {
			1 : 980,
			2 : 1.970e3,
			3 : 2.959e3,
			4 : 2.454e3,
			5 : 3.447e3,
			6 : 4.436e3,
			7 : 5.425e3,
			8 : 3.963e3,
			9 : 4.960e3,
			10: 5.945e3,
			11: 6.935e3,
			12: 6.430e3,
			13: 7.423e3,
			14: 8.414e3,
			15: 9.403e3,
			}

	d = bool(d1) | (bool(d2) << 1) | (bool(d3) << 2) | (bool(d4) << 3)
	return MEASURED[d]

LOWES = 'lowes'
T65 = 'T65'
T66 = 'T66'
T67 = 'T67'

DIP_SETTINGS = {
		'a': (1,0,1,1),
		'b': (1,1,0,0),
		'c': (0,0,1,0),
		'd': (0,1,0,1),
		'e': (1,0,1,0),
		'f': (0,0,1,1),
		'g': (1,1,1,1),
		'h': (1,0,1,1),
		'i': (0,1,1,0),
		'j': (0,1,0,0),
		'k': (1,1,0,1),
		'l': (0,1,1,1),
		'm': (0,0,0,1),
		'n': (1,0,0,1),
		'o': (0,1,0,1),
		'p': (0,1,0,1),
		'q': (0,0,1,0),
		#'r': (),
		's': (1,1,0,0),
		#'t': (),
		'u': (0,1,0,1),
		'v': (0,1,0,0),
		'w': (1,0,1,0),
		#'x': (),
		}

XY_COORDS = {
		'a': (7.637, 1.822+.752-.090),
		'b': (9.757, 1.552-.090),
		'c': (9.757, 2.604-.090),
		'd': (7.637, .906+.752-.090),
		'e': (0.158+1.665, 1.543),
		'f': (0.158+3.189, 1.513),
		'g': (6.093, 2.676-.090),
		'h': (6.093, 1.637-.090),
		'i': (3.350, 2.577),
		'j': (1.842, 2.585),
		'k': (3.350, 3.981),
		'p': (1.842, 3.975),
		'q': (1.842, 5.009),
		's': (3.350, 5.021),
		'u': (7.637, 3.220+.752-.090),
		'v': (9.757, 5.007-.090),
		'w': (7.637, 4.244+.752-.090),
		'x': (9.757, 3.970-.090),
		}

STYLES = {
		'a': LOWES,
		'b': T66,
		'c': T66,
		'd': T66,
		'e': T65,
		'f': T65,
		'g': T65,
		'h': T66,
		'i': T66,
		'j': T65,
		'k': T66,
		#'l': ,
		#'m': ,
		#'n': ,
		#'o': ,
		'p': T67,
		'q': T67,
		#'r': ,
		's': T67,
		#'t': ,
		'u': T67,
		'v': T67,
		'w': T67,
		'x': T67,
		}

Z_COORDS = {
		LOWES: 2.6, #FIXME: No measurement for this light
		T65 : (2.598+2.597)/2,
		T66 : 2.607,
		T67 : (2.646+2.653)/2,
		}

def coords(light):
	return (XY_COORDS[light][0], XY_COORDS[light][1], Z_COORDS[STYLES[light]])

transmitters = {}
for light in DIP_SETTINGS:
	f = dip2f_meas(*DIP_SETTINGS[light])
	try:
		c = coords(light)
	except KeyError:
		print("Skipping '{}', missing information".format(light))
		continue
	try:
		transmitters[f].append(c)
	except KeyError:
		transmitters[f] = [c,]

if __name__ == '__main__':
	for r4 in (0,1):
		for r3 in (0,1):
			for r2 in (0,1):
				for r1 in (0,1):
					if (r1+r2+r3+r4) == 0:
						continue
					print("{}{}{}{}: {: >4.1f} {: >4.1f} {:2.1f}%".format(
						r1,r2,r3,r4,
						dip2f(r1,r2,r3,r4),
						dip2f_meas(r1,r2,r3,r4),
						((dip2f(r1,r2,r3,r4) - dip2f_meas(r1,r2,r3,r4))/dip2f_meas(r1,r2,r3,r4))*100
						))

	print('')

	for k in sorted(DIP_SETTINGS.keys()):
		if dip2f(*DIP_SETTINGS[k]) > 7000:
			print("WARN: Light {} set to {:4.0f} which is not detectable".format(
				k, dip2f(*DIP_SETTINGS[k])))
		else:
			try:
				print("Light {} set to {:4.0f} ({:4.0f}) at {}".format(
					k, dip2f(*DIP_SETTINGS[k]), dip2f_meas(*DIP_SETTINGS[k]), coords(k)))
			except KeyError:
				print("Light {} set to {:4.0f} ({:4.0f})".format(
					k, dip2f(*DIP_SETTINGS[k]), dip2f_meas(*DIP_SETTINGS[k])))

	print('')
