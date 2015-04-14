
origin = 'center'
units = 'm'
user_is = 'below'

# room wall: 17.0688 m
# bathroom:  49.0728 m
# meeting:   28.956 m
# arch:      17.3228 m
# arch2:     45.2628 m
# elevator:  21.336 m

# z measured, center measured, others calibrated
transmitters_measured = {
		# Chandelier 1
		# Second from bathroom
		# Center: x = 3.45 + meeting, y = bathroom wall - 14.00
		# camera -> -x
		#4650 : ((20.216,35.943, 3.021),),		# Bulb e
		4200 : ((21.740,34.743, 3.026),),		# Bule 5
		4050 : ((20.032,34.102, 2.993),),		# Bulb 2
		4300 : ((20.519,34.073, 3.000),),		# Bulb 7

		# Chandelier 2
		# glass room near glass
		# Center: x = 5.66, y = 10.05
		# camera -> -y
		4400 : (( 5.660,10.050, 3.305),),		# Bulb 9
		4350 : (( 5.962, 9.180, 3.312),),		# Bule 8
		4600 : (( 6.171,11.002, 3.304),),		# Bulb d
		4550 : (( 4.473,10.401, 3.315),),		# Bulb c

		# Chandelier 3
		# big room triangle point
		# Center: x = 11.87 + wall, y = 12.39
		# camera -> -y
		4450 : ((29.838,12.579, 3.457),),		# Bulb 0a
		4500 : ((28.939,12.390, 3.407),),		# Bule 0b
		4250 : ((28.452,11.234, 3.375),),		# Bulb 06
		4150 : ((28.038,13.001, 3.388),),		# Bulb 04

		# Chandelier 4
		# third from bathroom
		# Center: x = 3.87 + meeting, y = 8.41 + arch
		# camera -> -x
		4950 : ((33.180,26.676, 3.010),),		# Bulb 14
		5050 : ((31.713,25.611, 2.925),),		# Bule 16
		4850 : ((33.450,24.859, 2.962),),		# Bulb 12
		4750 : ((32.974,25.619, 2.964),),		# Bulb 10

		# Chandelier 5
		# big room middle of line
		# Center: x = 8.61 + Chandelier 9,  y = 5.74
		# camera -> -y
		5000 : ((33.001, 5.964, 3.297),),		# Bulb 15
		4100 : ((31.460, 6.902, 3.317),),		# Bule 03
		4000 : ((31.433, 4.971, 3.296),),		# Bulb 01
		4700 : ((31.939, 5.740, 3.307),),		# Bulb 0f


		# Chandelier 6
		# stub hallway light
		# Center: 3.80 + arch2, y = 1.95 + electric / elevator room (309)
		# camera -> +x
		4800 : ((49.061,22.221, 2.843),),		# Bulb 11
		5200 : ((50.282,23.507, 2.749),),		# Bule 1a
		4900 : ((48.399,23.929, 2.830),),		# Bulb 13
		5650 : ((49.063,23.286, 2.815),),		# Bulb 23


		# Chandelier 7
		# big stub solo
		# Center: x = 9.52 + Chandelier 5, y = 6.20
		# camera -> -x
		5350 : ((41.278, 7.265, 3.552),),		# Bulb 1d
		5250 : ((42.720, 6.164, 3.507),),		# Bule 1b
		5500 : ((40.918, 5.455, 3.586),),		# Bulb 20
		5750 : ((41.459, 6.200, 3.549),),		# Bulb 25

		# Chandelier 8
		# Nearest bathroom (end of food)
		# Center: x = 8.59 + meeting, y = bathroom - 5.89
		# camera -> -x
		5150 : ((38.285,43.962, 3.312),),		# Bulb 19
		5900 : ((37.546,43.183, 3.326),),		# Bule 29
		#4650 : ((36.634,43.176, 3.328),),		# Bulb 1c, NOTE: conf thought this should be 5300
		5100 : ((38.251,42.168, 3.320),),		# Bulb 18, estimated


		# Chandelier 9
		# big room nearest glass wall
		# Center: x = 6.26 + wall, y = 5.46
		# camera -> -y
		5450 : (( 23.892, 4.533, 3.386),),		# Bulb 1f
		5550 : (( 22.161, 5.028, 3.480),),		# Bule 21
		5400 : (( 23.561, 6.356, 3.430),),		# Bulb 1e
		5850 : (( 23.329, 5.46, 3.418),),		# Bulb 27

		# Chandelier 10
		# glass room near wall
		# x = 11.77, y = 3.95
		# camera -> -y
		5700 : ((11.768, 2.868, 3.222),),		# Bulb 24
		5600 : ((12.916, 4.274, 3.255),),		# Bule 22
		5800 : ((11.104, 4.685, 3.216),),		# Bulb 26
		5950 : ((11.836, 4.117, 3.215),),		# Bulb 2a



		}

#transmitters_calibration = {
#		# Chandelier 1
#
#		4000 : (( 3.761, 4.627, 3.382),),		# Bulb 5
#		4500 : (( 4.839, 6.236, 3.500),),		# Bule e
#		5000 : (( 3.003, 6.297, 3.400),),		# Bulb 2
#		5500 : (( 4.005, 5.877, 3.430),),		# Bulb 7
#		}

transmitters = transmitters_measured
#transmitters = transmitters_calibration
