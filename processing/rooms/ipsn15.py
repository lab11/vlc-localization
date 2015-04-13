
origin = 'center'
units = 'm'
user_is = 'below'

transmitters_measured = {
		# Chandelier 1
		# Second from bathroom
		# Center: x = 3.45 + meeting, y = bathroom wall - 14.00
		# camera -> -x
		4650 : (( 0.000, 0.000, 3.021),),		# Bulb e
		4200 : (( 0.000, 0.000, 3.026),),		# Bule 5
		4050 : (( 0.000, 0.000, 2.993),),		# Bulb 2
		4300 : (( 0.000, 0.000, 3.000),),		# Bulb 7

		# Chandelier 2
		# glass room near glass
		# Center: x = 5.66, y = 10.05
		# camera -> -y
		4400 : (( 0.000, 0.000, 3.305),),		# Bulb 9
		4350 : (( 0.000, 0.000, 3.312),),		# Bule 8
		4600 : (( 0.000, 0.000, 3.304),),		# Bulb d
		4550 : (( 0.000, 0.000, 3.315),),		# Bulb c

		# Chandelier 3
		# big room triangle point
		# Center: x = 11.87 + wall, y = 12.39
		# camera -> -y
		4450 : (( 0.000, 0.000, 3.457),),		# Bulb 0a
		4500 : (( 0.000, 0.000, 3.407),),		# Bule 0b
		4250 : (( 0.000, 0.000, 3.375),),		# Bulb 06
		4150 : (( 0.000, 0.000, 3.388),),		# Bulb 04

		# Chandelier 4
		# third from bathroom
		# Center: x = 3.87 + meeting, y = 8.41 + arch
		# camera -> -x
		4950 : (( 0.000, 0.000, 3.010),),		# Bulb 14
		5050 : (( 0.000, 0.000, 2.925),),		# Bule 16
		4850 : (( 0.000, 0.000, 2.962),),		# Bulb 12
		4750 : (( 0.000, 0.000, 2.964),),		# Bulb 10

		# Chandelier 5
		# big room middle of line
		# Center: x = 8.61 + Chandelier 9,  y = 5.74
		# camera -> -y
		5000 : (( 0.000, 0.000, 3.297),),		# Bulb 15
		4100 : (( 0.000, 0.000, 3.317),),		# Bule 03
		4000 : (( 0.000, 0.000, 3.296),),		# Bulb 01
		4700 : (( 0.000, 0.000, 3.307),),		# Bulb 0f


		# Chandelier 6
		# stub hallway light
		# Center: 3.80 + arch, y = 1.95 + electric / elevator room (309)
		# camera -> +x
		4800 : (( 0.000, 0.000, 2.843),),		# Bulb 11
		5200 : (( 0.000, 0.000, 2.749),),		# Bule 1a
		4900 : (( 0.000, 0.000, 2.830),),		# Bulb 13
		5650 : (( 0.000, 0.000, 2.815),),		# Bulb 23


		# Chandelier 7
		# big stub solo
		# Center: x = 9.52 + Chandelier 5, y = 6.20
		# camera -> -x
		5350 : (( 0.000, 0.000, 3.552),),		# Bulb 1d
		5250 : (( 0.000, 0.000, 3.507),),		# Bule 1b
		5500 : (( 0.000, 0.000, 3.586),),		# Bulb 20
		5750 : (( 0.000, 0.000, 3.549),),		# Bulb 25

		# Chandelier 8
		# Nearest bathroom (end of food)
		# Center: x = 8.59 + meeting, y = bathroom - 5.89
		# camera -> -x
		5150 : (( 0.000, 0.000, 3.312),),		# Bulb 19
		5900 : (( 0.000, 0.000, 3.326),),		# Bule 29
		5300 : (( 0.000, 0.000, 3.328),),		# Bulb 1c
		5100 : (( 0.000, 0.000, 3.320),),		# Bulb 18, estimated


		# Chandelier 9
		# big room nearest glass wall
		# Center: x = 6.26 + wall, y = 5.46
		# camera -> -y
		5450 : (( 0.000, 0.000, 3.386),),		# Bulb 1f
		5550 : (( 0.000, 0.000, 3.480),),		# Bule 21
		5400 : (( 0.000, 0.000, 3.430),),		# Bulb 1e
		5850 : (( 0.000, 0.000, 3.418),),		# Bulb 27

		# Chandelier 10
		# glass room near wall
		# x = 11.77, y = 3.95
		# camera -> -y
		5700 : (( 0.000, 0.000, 3.222),),		# Bulb 24
		5600 : (( 0.000, 0.000, 3.255),),		# Bule 22
		5800 : (( 0.000, 0.000, 3.216),),		# Bulb 26
		5950 : (( 0.000, 0.000, 3.215),),		# Bulb 2a



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
