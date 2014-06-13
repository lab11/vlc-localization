import test
from test import run_test
from test import Picture

def sample_test(error_list):
        error_list.append(Picture(run_test("./samples/x_0_y_1.27.jpg",False),
                                  "./samples/x_0_y_1.27.jpg",
                                  "Normal 5 Light",
                                  0))
	error_list.append(Picture(run_test("./samples/small_blob.jpg",False),
                           "./samples/small_blob.jpg",
                           "Normal 5 Light",
                           0))
	error_list.append(Picture(run_test("./samples/2014-02-27--18-15-03-62.jpg",False),
                           "./samples/2014-02-27--18-15-03-62.jpg",
                           "Normal 5 Light",
                           0))
	error_list.append(Picture(run_test("./samples/2014-02-27--18-16-34-97.jpg",False),
                           "./samples/2014-02-27--18-16-34-97.jpg",
                           "Normal 5 Light",
                           0))
	error_list.append(Picture(run_test("./samples/4908_CBAD.jpg",False),
                           "./samples/4908_CBAD.jpg",
                           "Normal 5 Light",
                           0))
	error_list.append(Picture(run_test("./samples/mirror1.jpg",False),
                           "./samples/mirror1.jpg",
                           "Normal 5 Light",
                           0))
	error_list.append(Picture(run_test("./samples/mirror2.jpg",False),
                           "./samples/mirror2.jpg",
                           "Normal 5 Light",
                           0))
	error_list.append(Picture(run_test("./samples/mirror3.jpg",False),
                           "./samples/mirror3.jpg",
                           "Normal 5 Light",
                           0))
#	freq_list.append(Picture(0,run_test("./samples/4908_IFJE.jpg",True)))
#  freq_list.append(Picture(0,run_test("./samples/4908_ADGH.jpg",True)))
#  freq_list.append(Picture(error= run_test("./samples/1K_1.jpg",True)))
#  freq_list.append(Picture(error= run_test("./samples/4908_SKQP",True)))
#  freq_list.append(Picture(0,run_test("./samples/compressed.jpg",True)))
	return error_list

def dist_TX3K_test(freq_list,path):
	init_len = len(freq_list)
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/0.5m/0.5m_1.jpg",
                           "TX3K, .5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/0.5m/0.5m_1.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/0.5m/0.5m_2.jpg",
                           "TX3K, .5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/0.5m/0.5m_2.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/0.5m/0.5m_3.jpg",
                           "TX3K, .5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/0.5m/0.5m_3.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/0.5m/0.5m_4.jpg",
                           "TX3K, .5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/0.5m/0.5m_4.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/0.5m/0.5m_5.jpg",
                           "TX3K, .5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/0.5m/0.5m_5.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/0.5m/0.5m_6.jpg",
                           "TX3K, .5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/0.5m/0.5m_6.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/0.5m/0.5m_7.jpg",
                           "TX3K, .5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/0.5m/0.5m_7.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/0.5m/0.5m_8.jpg",
                           "TX3K, .5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/0.5m/0.5m_8.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/0.5m/0.5m_9.jpg",
                           "TX3K, .5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/0.5m/0.5m_9.jpg",True)))
	
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/1m/1m_1.jpg",
                           "TX3K, 1m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/1m/1m_1.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/1m/1m_2.jpg",
                           "TX3K, 1m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/1m/1m_2.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/1m/1m_3.jpg",
                           "TX3K, 1m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/1m/1m_3.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/1m/1m_4.jpg",
                           "TX3K, 1m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/1m/1m_4.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/1m/1m_5.jpg",
                           "TX3K, 1m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/1m/1m_5.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/1m/1m_6.jpg",
                           "TX3K, 1m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/1m/1m_6.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/1m/1m_7.jpg",
                           "TX3K, 1m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/1m/1m_7.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/1m/1m_8.jpg",
                           "TX3K, 1m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/1m/1m_8.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/1m/1m_9.jpg",
                           "TX3K, 1m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/1m/1m_9.jpg",True)))

	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/1.5m/1.5m_1.jpg",
                           "TX3K, 1.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/1.5m/1.5m_1.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/1.5m/1.5m_2.jpg",
                           "TX3K, 1.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/1.5m/1.5m_2.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/1.5m/1.5m_3.jpg",
                           "TX3K, 1.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/1.5m/1.5m_3.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/1.5m/1.5m_4.jpg",
                           "TX3K, 1.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/1.5m/1.5m_4.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/1.5m/1.5m_5.jpg",
                           "TX3K, 1.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/1.5m/1.5m_5.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/1.5m/1.5m_6.jpg",
                           "TX3K, 1.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/1.5m/1.5m_6.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/1.5m/1.5m_7.jpg",
                           "TX3K, 1.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/1.5m/1.5m_7.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/1.5m/1.5m_8.jpg",
                           "TX3K, 1.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/1.5m/1.5m_8.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/1.5m/1.5m_9.jpg",
                           "TX3K, 1.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/1.5m/1.5m_9.jpg",True)))

	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/2m/2m_1.jpg",
                           "TX3K, 2m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/2m/2m_1.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/2m/2m_2.jpg",
                           "TX3K, 2m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/2m/2m_2.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/2m/2m_3.jpg",
                           "TX3K, 2m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/2m/2m_3.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/2m/2m_4.jpg",
                           "TX3K, 2m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/2m/2m_4.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/2m/2m_5.jpg",
                           "TX3K, 2m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/2m/2m_5.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/2m/2m_6.jpg",
                           "TX3K, 2m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/2m/2m_6.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/2m/2m_7.jpg",
                           "TX3K, 2m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/2m/2m_7.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/2m/2m_8.jpg",
                           "TX3K, 2m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/2m/2m_8.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/2m/2m_9.jpg",
                           "TX3K, 2m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/2m/2m_9.jpg",True)))

	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/2.5m/2.5m_1.jpg",
                           "TX3K, 2.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/2.5m/2.5m_1.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/2.5m/2.5m_2.jpg",
                           "TX3K, 2.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/2.5m/2.5m_2.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/2.5m/2.5m_3.jpg",
                           "TX3K, 2.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/2.5m/2.5m_3.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/2.5m/2.5m_4.jpg",
                           "TX3K, 2.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/2.5m/2.5m_4.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/2.5m/2.5m_5.jpg",
                           "TX3K, 2.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/2.5m/2.5m_5.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/2.5m/2.5m_6.jpg",
                           "TX3K, 2.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/2.5m/2.5m_6.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/2.5m/2.5m_7.jpg",
                           "TX3K, 2.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/2.5m/2.5m_7.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/2.5m/2.5m_8.jpg",
                           "TX3K, 2.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/2.5m/2.5m_8.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/2.5m/2.5m_9.jpg",
                           "TX3K, 2.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/2.5m/2.5m_9.jpg",True)))

	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/3m/3m_1.jpg",
                           "TX3K, 3m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/3m/3m_1.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/3m/3m_2.jpg",
                           "TX3K, 3m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/3m/3m_2.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/3m/3m_3.jpg",
                           "TX3K, 3m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/3m/3m_3.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/3m/3m_4.jpg",
                           "TX3K, 3m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/3m/3m_4.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/3m/3m_5.jpg",
                           "TX3K, 3m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/3m/3m_5.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/3m/3m_6.jpg",
                           "TX3K, 3m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/3m/3m_6.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/3m/3m_7.jpg",
                           "TX3K, 3m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/3m/3m_7.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/3m/3m_8.jpg",
                           "TX3K, 3m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/3m/3m_8.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/3m/3m_9.jpg",
                           "TX3K, 3m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/3m/3m_9.jpg",True)))

	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/3.5m/3.5m_1.jpg",
                           "TX3K, 3.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/3.5m/3.5m_1.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/3.5m/3.5m_2.jpg",
                           "TX3K, 3.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/3.5m/3.5m_2.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/3.5m/3.5m_3.jpg",
                           "TX3K, 3.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/3.5m/3.5m_3.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/3.5m/3.5m_4.jpg",
                           "TX3K, 3.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/3.5m/3.5m_4.jpg",True)))
#	freq_list.append(Picture(0,run_test(path + "/vlc/back_camera/distance/TX3K/3.5m/3.5m_5.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/3.5m/3.5m_6.jpg",
                           "TX3K, 3.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/3.5m/3.5m_6.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/3.5m/3.5m_7.jpg",
                           "TX3K, 3.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/3.5m/3.5m_7.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/3.5m/3.5m_8.jpg",
                           "TX3K, 3.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/3.5m/3.5m_8.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/3.5m/3.5m_9.jpg",
                           "TX3K, 3.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/3.5m/3.5m_9.jpg",True)))

	i = init_len
	while i < len(freq_list):
		freq_list[i].freq_diff = freq_list[i].freq_diff - 3000
		i = i + 1
	return freq_list
               
def dist_TX1K_test(freq_list,path):
	init_len = len(freq_list)

	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/0.5m/0.5m_1.jpg",
                           "TX1K, .5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/0.5m/0.5m_1.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/0.5m/0.5m_2.jpg",
                           "TX1K, .5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/0.5m/0.5m_2.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/0.5m/0.5m_3.jpg",
                           "TX1K, .5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/0.5m/0.5m_3.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/0.5m/0.5m_4.jpg",
                           "TX1K, .5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/0.5m/0.5m_4.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/0.5m/0.5m_5.jpg",
                           "TX1K, .5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/0.5m/0.5m_5.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/0.5m/0.5m_6.jpg",
                           "TX1K, .5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/0.5m/0.5m_6.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/0.5m/0.5m_7.jpg",
                           "TX1K, .5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/0.5m/0.5m_7.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/0.5m/0.5m_8.jpg",
                           "TX1K, .5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/0.5m/0.5m_8.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/0.5m/0.5m_9.jpg",
                           "TX1K, .5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/0.5m/0.5m_9.jpg",True)))
	
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/1m/1m_1.jpg",
                           "TX1K, 1m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/1m/1m_1.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/1m/1m_2.jpg",
                           "TX1K, 1m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/1m/1m_2.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/1m/1m_3.jpg",
                           "TX1K, 1m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/1m/1m_3.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/1m/1m_4.jpg",
                           "TX1K, 1m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/1m/1m_4.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/1m/1m_5.jpg",
                           "TX1K, 1m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/1m/1m_5.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/1m/1m_6.jpg",
                           "TX1K, 1m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/1m/1m_6.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/1m/1m_7.jpg",
                           "TX1K, 1m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/1m/1m_7.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/1m/1m_8.jpg",
                           "TX1K, 1m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/1m/1m_8.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/1m/1m_9.jpg",
                           "TX1K, 1m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/1m/1m_9.jpg",True)))

	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/1.5m/1.5m_1.jpg",
                           "TX1K, 1.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/1.5m/1.5m_1.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/1.5m/1.5m_2.jpg",
                           "TX1K, 1.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/1.5m/1.5m_2.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/1.5m/1.5m_3.jpg",
                           "TX1K, 1.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/1.5m/1.5m_3.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/1.5m/1.5m_4.jpg",
                           "TX1K, 1.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/1.5m/1.5m_4.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/1.5m/1.5m_5.jpg",
                           "TX1K, 1.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/1.5m/1.5m_5.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/1.5m/1.5m_6.jpg",
                           "TX1K, 1.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/1.5m/1.5m_6.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/1.5m/1.5m_7.jpg",
                           "TX1K, 1.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/1.5m/1.5m_7.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/1.5m/1.5m_8.jpg",
                           "TX1K, 1.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/1.5m/1.5m_8.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/1.5m/1.5m_9.jpg",
                           "TX1K, 1.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/1.5m/1.5m_9.jpg",True)))

	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/2m/2m_1.jpg",
                           "TX1K, 2m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/2m/2m_1.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/2m/2m_2.jpg",
                           "TX1K, 2m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/2m/2m_2.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/2m/2m_3.jpg",
                           "TX1K, 2m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/2m/2m_3.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/2m/2m_4.jpg",
                           "TX1K, 2m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/2m/2m_4.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/2m/2m_5.jpg",
                           "TX1K, 2m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/2m/2m_5.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/2m/2m_6.jpg",
                           "TX1K, 2m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/2m/2m_6.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/2m/2m_7.jpg",
                           "TX1K, 2m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/2m/2m_7.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/2m/2m_8.jpg",
                           "TX1K, 2m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/2m/2m_8.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/2m/2m_9.jpg",
                           "TX1K, 2m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/2m/2m_9.jpg",True)))

	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/2.5m/2.5m_1.jpg",
                           "TX1K, 2.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/2.5m/2.5m_1.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/2.5m/2.5m_2.jpg",
                           "TX1K, 2.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/2.5m/2.5m_2.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/2.5m/2.5m_3.jpg",
                           "TX1K, 2.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/2.5m/2.5m_3.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/2.5m/2.5m_4.jpg",
                           "TX1K, 2.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/2.5m/2.5m_4.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/2.5m/2.5m_5.jpg",
                           "TX1K, 2.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/2.5m/2.5m_5.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/2.5m/2.5m_6.jpg",
                           "TX1K, 2.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/2.5m/2.5m_6.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/2.5m/2.5m_7.jpg",
                           "TX1K, 2.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/2.5m/2.5m_7.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/2.5m/2.5m_8.jpg",
                           "TX1K, 2.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/2.5m/2.5m_8.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/2.5m/2.5m_9.jpg",
                           "TX1K, 2.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/2.5m/2.5m_9.jpg",True)))

	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/3m/3m_1.jpg",
                           "TX1K, 3m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/3m/3m_1.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/3m/3m_2.jpg",
                           "TX1K, 3m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/3m/3m_2.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/3m/3m_3.jpg",
                           "TX1K, 3m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/3m/3m_3.jpg",True)))
#	freq_list.append(Picture(0,
#                           path + "/vlc/back_camera/distance/TX1K/3m/3m_4.jpg",
#                           "TX1K, 3m, 1 Light Source",
#                           run_test(path + "/vlc/back_camera/distance/TX1K/3m/3m_4.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/3m/3m_5.jpg",
                           "TX1K, 3m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/3m/3m_5.jpg",True)))
#	freq_list.append(Picture(0,
#                           path + "/vlc/back_camera/distance/TX1K/3m/3m_6.jpg",
#                           "TX1K, 3m, 1 Light Source",
#                           run_test(path + "/vlc/back_camera/distance/TX1K/3m/3m_6.jpg",True)))
#	freq_list.append(Picture(0,
#                           path + "/vlc/back_camera/distance/TX1K/3m/3m_7.jpg",
#                           "TX1K, 3m, 1 Light Source",
#                           run_test(path + "/vlc/back_camera/distance/TX1K/3m/3m_7.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/3m/3m_8.jpg",
                           "TX1K, 3m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/3m/3m_8.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/3m/3m_9.jpg",
                           "TX1K, 3m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/3m/3m_9.jpg",True)))

	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/3.5m/3.5m_1.jpg",
                           "TX1K, 3.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/3.5m/3.5m_1.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/3.5m/3.5m_2.jpg",
                           "TX1K, 3.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/3.5m/3.5m_2.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/3.5m/3.5m_3.jpg",
                           "TX1K, 3.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/3.5m/3.5m_3.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/3.5m/3.5m_4.jpg",
                           "TX1K, 3.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/3.5m/3.5m_4.jpg",True)))
#	freq_list.append(Picture(0,run_test(path + "/vlc/back_camera/distance/TX3K/3.5m/3.5m_5.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/3.5m/3.5m_6.jpg",
                           "TX1K, 3.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/3.5m/3.5m_6.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/3.5m/3.5m_7.jpg",
                           "TX1K, 3.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/3.5m/3.5m_7.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/3.5m/3.5m_8.jpg",
                           "TX1K, 3.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/3.5m/3.5m_8.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/3.5m/3.5m_9.jpg",
                           "TX1K, 3.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/3.5m/3.5m_9.jpg",True)))

	i = init_len
	while i < len(freq_list):
		freq_list[i].freq_diff = freq_list[i].freq_diff - 1000
		i = i + 1
	return freq_list
             
def   angle_x_test(error_list,path):
   	error_list.append(Picture(run_test(path + "/vlc/angled/x_axis/-18.jpg",False),
                        path + "/vlc/angled/x_axis/-18.jpg",
                        "-18 deg x axis Rotation, 5 Light Source",
                        0))
   	error_list.append(Picture(run_test(path + "/vlc/angled/x_axis/-9.jpg",False),
                        path + "/vlc/angled/x_axis/-9.jpg",
                        "-9 deg x axis Rotation, 5 Light Source",
                        0))
   	error_list.append(Picture(run_test(path + "/vlc/angled/x_axis/0.jpg",False),
                        path + "/vlc/angled/x_axis/0.jpg",
                        "0 deg x axis Rotation, 5 Light Source",
                        0))
   	error_list.append(Picture(run_test(path + "/vlc/angled/x_axis/9.jpg",False),
                        path + "/vlc/angled/x_axis/9.jpg",
                        "9 deg x axis Rotation, 5 Light Source",
                        0))
   	error_list.append(Picture(run_test(path + "/vlc/angled/x_axis/18.jpg",False),
                        path + "/vlc/angled/x_axis/18.jpg",
                        "18 deg x axis Rotation, 5 Light Source",
                        0))
	return error_list


def   angle_y_test(error_list,path):
   	error_list.append(Picture(run_test(path + "/vlc/angled/y_axis/-27.jpg",False),
                        path + "/vlc/angled/y_axis/-27.jpg",
                        "-27 deg y axis Rotation, 5 Light Source",
                        0))
   	error_list.append(Picture(run_test(path + "/vlc/angled/y_axis/-18.jpg",False),
                        path + "/vlc/angled/y_axis/-18.jpg",
                        "-18 deg y axis Rotation, 5 Light Source",
                        0))
   	error_list.append(Picture(run_test(path + "/vlc/angled/y_axis/-9.jpg",False),
                        path + "/vlc/angled/y_axis/-9.jpg",
                        "-9 deg y axis Rotation, 5 Light Source",
                        0))
   	error_list.append(Picture(run_test(path + "/vlc/angled/y_axis/0.jpg",False),
                        path + "/vlc/angled/y_axis/0.jpg",
                        "0 deg y axis Rotation, 5 Light Source",
                        0))
   	error_list.append(Picture(run_test(path + "/vlc/angled/y_axis/9.jpg",False),
                        path + "/vlc/angled/y_axis/9.jpg",
                        "9 deg y axis Rotation, 5 Light Source",
                        0))
   	error_list.append(Picture(run_test(path + "/vlc/angled/y_axis/18.jpg",False),
                        path + "/vlc/angled/y_axis/18.jpg",
                        "18 deg y axis Rotation, 5 Light Source",
                        0))
   	error_list.append(Picture(run_test(path + "/vlc/angled/y_axis/27.jpg",False),
                        path + "/vlc/angled/y_axis/27.jpg",
                        "27 deg y axis Rotation, 5 Light Source",
                        0))
   	return error_list

def   angle_z_test(error_list,path):
   	error_list.append(Picture(run_test(path + "/vlc/angled/z_axis/0.jpg",False),
                        path + "/vlc/angled/z_axis/0.jpg",
                        "0 deg y axis Rotation, 5 Light Source",
                        0))
   	error_list.append(Picture(run_test(path + "/vlc/angled/z_axis/45.jpg",False),
                        path + "/vlc/angled/z_axis/45.jpg",
                        "45 deg y axis Rotation, 5 Light Source",
                        0))
        error_list.append(Picture(run_test(path + "/vlc/angled/z_axis/90.jpg",False),
                        path + "/vlc/angled/z_axis/90.jpg",
                        "90 deg y axis Rotation, 5 Light Source",
                        0))
   	error_list.append(Picture(run_test(path + "/vlc/angled/z_axis/135.jpg",False),
                        path + "/vlc/angled/z_axis/135.jpg",
                        "135 deg y axis Rotation, 5 Light Source",
                        0))
   	error_list.append(Picture(run_test(path + "/vlc/angled/z_axis/180.jpg",False),
                        path + "/vlc/angled/z_axis/180.jpg",
                        "180 deg y axis Rotation, 5 Light Source",
                        0))
   	error_list.append(Picture(run_test(path + "/vlc/angled/z_axis/225.jpg",False),
                        path + "/vlc/angled/z_axis/225.jpg",
                        "225 deg y axis Rotation, 5 Light Source",
                        0))
   	error_list.append(Picture(run_test(path + "/vlc/angled/z_axis/270.jpg",False),
                        path + "/vlc/angled/z_axis/270.jpg",
                        "270 deg y axis Rotation, 5 Light Source",
                        0))
   	error_list.append(Picture(run_test(path + "/vlc/angled/z_axis/315.jpg",False),
                        path + "/vlc/angled/z_axis/315.jpg",
                        "315 deg y axis Rotation, 5 Light Source",
                        0))
   	error_list.append(Picture(run_test(path + "/vlc/angled/z_axis/0.jpg",False),
                        path + "/vlc/angled/z_axis/0.jpg",
                        "0 deg y axis Rotation, 5 Light Source",
                        0))
	return error_list

