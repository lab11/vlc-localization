import test
from test import run_test
from test import Picture

def sample_test(error_list):
        error_list.append(Picture(run_test("./samples/x_0_y_1.27.jpg",False,'test_rig'),
                                  "./samples/x_0_y_1.27.jpg",
                                  "Normal 5 Light",
                                  0))
	error_list.append(Picture(run_test("./samples/small_blob.jpg",False,'test_rig'),
                           "./samples/small_blob.jpg",
                           "Normal 5 Light",
                           0))
	error_list.append(Picture(run_test("./samples/2014-02-27--18-15-03-62.jpg",False,'test_rig'),
                           "./samples/2014-02-27--18-15-03-62.jpg",
                           "Normal 5 Light",
                           0))
	error_list.append(Picture(run_test("./samples/2014-02-27--18-16-34-97.jpg",False,'test_rig'),
                           "./samples/2014-02-27--18-16-34-97.jpg",
                           "Normal 5 Light",
                           0))
	error_list.append(Picture(run_test("./samples/4908_CBAD.jpg",False,'test_rig'),
                           "./samples/4908_CBAD.jpg",
                           "Normal 5 Light",
                           0))
	error_list.append(Picture(run_test("./samples/mirror1.jpg",False,'test_rig'),
                           "./samples/mirror1.jpg",
                           "Normal 5 Light",
                           0))
	error_list.append(Picture(run_test("./samples/mirror2.jpg",False,'test_rig'),
                           "./samples/mirror2.jpg",
                           "Normal 5 Light",
                           0))
	error_list.append(Picture(run_test("./samples/mirror3.jpg",False,'test_rig'),
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
                           run_test(path + "/vlc/back_camera/distance/TX3K/0.5m/0.5m_1.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/0.5m/0.5m_2.jpg",
                           "TX3K, .5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/0.5m/0.5m_2.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/0.5m/0.5m_3.jpg",
                           "TX3K, .5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/0.5m/0.5m_3.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/0.5m/0.5m_4.jpg",
                           "TX3K, .5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/0.5m/0.5m_4.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/0.5m/0.5m_5.jpg",
                           "TX3K, .5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/0.5m/0.5m_5.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/0.5m/0.5m_6.jpg",
                           "TX3K, .5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/0.5m/0.5m_6.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/0.5m/0.5m_7.jpg",
                           "TX3K, .5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/0.5m/0.5m_7.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/0.5m/0.5m_8.jpg",
                           "TX3K, .5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/0.5m/0.5m_8.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/0.5m/0.5m_9.jpg",
                           "TX3K, .5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/0.5m/0.5m_9.jpg",True,'test_rig')))
	
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/1m/1m_1.jpg",
                           "TX3K, 1m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/1m/1m_1.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/1m/1m_2.jpg",
                           "TX3K, 1m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/1m/1m_2.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/1m/1m_3.jpg",
                           "TX3K, 1m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/1m/1m_3.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/1m/1m_4.jpg",
                           "TX3K, 1m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/1m/1m_4.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/1m/1m_5.jpg",
                           "TX3K, 1m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/1m/1m_5.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/1m/1m_6.jpg",
                           "TX3K, 1m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/1m/1m_6.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/1m/1m_7.jpg",
                           "TX3K, 1m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/1m/1m_7.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/1m/1m_8.jpg",
                           "TX3K, 1m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/1m/1m_8.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/1m/1m_9.jpg",
                           "TX3K, 1m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/1m/1m_9.jpg",True,'test_rig')))

	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/1.5m/1.5m_1.jpg",
                           "TX3K, 1.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/1.5m/1.5m_1.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/1.5m/1.5m_2.jpg",
                           "TX3K, 1.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/1.5m/1.5m_2.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/1.5m/1.5m_3.jpg",
                           "TX3K, 1.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/1.5m/1.5m_3.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/1.5m/1.5m_4.jpg",
                           "TX3K, 1.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/1.5m/1.5m_4.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/1.5m/1.5m_5.jpg",
                           "TX3K, 1.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/1.5m/1.5m_5.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/1.5m/1.5m_6.jpg",
                           "TX3K, 1.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/1.5m/1.5m_6.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/1.5m/1.5m_7.jpg",
                           "TX3K, 1.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/1.5m/1.5m_7.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/1.5m/1.5m_8.jpg",
                           "TX3K, 1.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/1.5m/1.5m_8.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/1.5m/1.5m_9.jpg",
                           "TX3K, 1.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/1.5m/1.5m_9.jpg",True,'test_rig')))

	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/2m/2m_1.jpg",
                           "TX3K, 2m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/2m/2m_1.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/2m/2m_2.jpg",
                           "TX3K, 2m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/2m/2m_2.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/2m/2m_3.jpg",
                           "TX3K, 2m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/2m/2m_3.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/2m/2m_4.jpg",
                           "TX3K, 2m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/2m/2m_4.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/2m/2m_5.jpg",
                           "TX3K, 2m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/2m/2m_5.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/2m/2m_6.jpg",
                           "TX3K, 2m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/2m/2m_6.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/2m/2m_7.jpg",
                           "TX3K, 2m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/2m/2m_7.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/2m/2m_8.jpg",
                           "TX3K, 2m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/2m/2m_8.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/2m/2m_9.jpg",
                           "TX3K, 2m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/2m/2m_9.jpg",True,'test_rig')))

	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/2.5m/2.5m_1.jpg",
                           "TX3K, 2.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/2.5m/2.5m_1.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/2.5m/2.5m_2.jpg",
                           "TX3K, 2.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/2.5m/2.5m_2.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/2.5m/2.5m_3.jpg",
                           "TX3K, 2.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/2.5m/2.5m_3.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/2.5m/2.5m_4.jpg",
                           "TX3K, 2.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/2.5m/2.5m_4.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/2.5m/2.5m_5.jpg",
                           "TX3K, 2.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/2.5m/2.5m_5.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/2.5m/2.5m_6.jpg",
                           "TX3K, 2.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/2.5m/2.5m_6.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/2.5m/2.5m_7.jpg",
                           "TX3K, 2.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/2.5m/2.5m_7.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/2.5m/2.5m_8.jpg",
                           "TX3K, 2.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/2.5m/2.5m_8.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/2.5m/2.5m_9.jpg",
                           "TX3K, 2.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/2.5m/2.5m_9.jpg",True,'test_rig')))

	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/3m/3m_1.jpg",
                           "TX3K, 3m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/3m/3m_1.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/3m/3m_2.jpg",
                           "TX3K, 3m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/3m/3m_2.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/3m/3m_3.jpg",
                           "TX3K, 3m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/3m/3m_3.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/3m/3m_4.jpg",
                           "TX3K, 3m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/3m/3m_4.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/3m/3m_5.jpg",
                           "TX3K, 3m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/3m/3m_5.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/3m/3m_6.jpg",
                           "TX3K, 3m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/3m/3m_6.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/3m/3m_7.jpg",
                           "TX3K, 3m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/3m/3m_7.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/3m/3m_8.jpg",
                           "TX3K, 3m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/3m/3m_8.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/3m/3m_9.jpg",
                           "TX3K, 3m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/3m/3m_9.jpg",True,'test_rig')))

	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/3.5m/3.5m_1.jpg",
                           "TX3K, 3.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/3.5m/3.5m_1.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/3.5m/3.5m_2.jpg",
                           "TX3K, 3.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/3.5m/3.5m_2.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/3.5m/3.5m_3.jpg",
                           "TX3K, 3.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/3.5m/3.5m_3.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/3.5m/3.5m_4.jpg",
                           "TX3K, 3.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/3.5m/3.5m_4.jpg",True,'test_rig')))
#	freq_list.append(Picture(0,run_test(path + "/vlc/back_camera/distance/TX3K/3.5m/3.5m_5.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/3.5m/3.5m_6.jpg",
                           "TX3K, 3.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/3.5m/3.5m_6.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/3.5m/3.5m_7.jpg",
                           "TX3K, 3.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/3.5m/3.5m_7.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/3.5m/3.5m_8.jpg",
                           "TX3K, 3.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/3.5m/3.5m_8.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX3K/3.5m/3.5m_9.jpg",
                           "TX3K, 3.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX3K/3.5m/3.5m_9.jpg",True,'test_rig')))

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
                           run_test(path + "/vlc/back_camera/distance/TX1K/0.5m/0.5m_1.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/0.5m/0.5m_2.jpg",
                           "TX1K, .5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/0.5m/0.5m_2.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/0.5m/0.5m_3.jpg",
                           "TX1K, .5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/0.5m/0.5m_3.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/0.5m/0.5m_4.jpg",
                           "TX1K, .5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/0.5m/0.5m_4.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/0.5m/0.5m_5.jpg",
                           "TX1K, .5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/0.5m/0.5m_5.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/0.5m/0.5m_6.jpg",
                           "TX1K, .5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/0.5m/0.5m_6.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/0.5m/0.5m_7.jpg",
                           "TX1K, .5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/0.5m/0.5m_7.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/0.5m/0.5m_8.jpg",
                           "TX1K, .5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/0.5m/0.5m_8.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/0.5m/0.5m_9.jpg",
                           "TX1K, .5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/0.5m/0.5m_9.jpg",True,'test_rig')))
	
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/1m/1m_1.jpg",
                           "TX1K, 1m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/1m/1m_1.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/1m/1m_2.jpg",
                           "TX1K, 1m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/1m/1m_2.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/1m/1m_3.jpg",
                           "TX1K, 1m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/1m/1m_3.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/1m/1m_4.jpg",
                           "TX1K, 1m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/1m/1m_4.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/1m/1m_5.jpg",
                           "TX1K, 1m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/1m/1m_5.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/1m/1m_6.jpg",
                           "TX1K, 1m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/1m/1m_6.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/1m/1m_7.jpg",
                           "TX1K, 1m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/1m/1m_7.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/1m/1m_8.jpg",
                           "TX1K, 1m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/1m/1m_8.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/1m/1m_9.jpg",
                           "TX1K, 1m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/1m/1m_9.jpg",True,'test_rig')))

	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/1.5m/1.5m_1.jpg",
                           "TX1K, 1.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/1.5m/1.5m_1.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/1.5m/1.5m_2.jpg",
                           "TX1K, 1.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/1.5m/1.5m_2.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/1.5m/1.5m_3.jpg",
                           "TX1K, 1.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/1.5m/1.5m_3.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/1.5m/1.5m_4.jpg",
                           "TX1K, 1.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/1.5m/1.5m_4.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/1.5m/1.5m_5.jpg",
                           "TX1K, 1.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/1.5m/1.5m_5.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/1.5m/1.5m_6.jpg",
                           "TX1K, 1.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/1.5m/1.5m_6.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/1.5m/1.5m_7.jpg",
                           "TX1K, 1.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/1.5m/1.5m_7.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/1.5m/1.5m_8.jpg",
                           "TX1K, 1.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/1.5m/1.5m_8.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/1.5m/1.5m_9.jpg",
                           "TX1K, 1.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/1.5m/1.5m_9.jpg",True,'test_rig')))

	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/2m/2m_1.jpg",
                           "TX1K, 2m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/2m/2m_1.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/2m/2m_2.jpg",
                           "TX1K, 2m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/2m/2m_2.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/2m/2m_3.jpg",
                           "TX1K, 2m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/2m/2m_3.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/2m/2m_4.jpg",
                           "TX1K, 2m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/2m/2m_4.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/2m/2m_5.jpg",
                           "TX1K, 2m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/2m/2m_5.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/2m/2m_6.jpg",
                           "TX1K, 2m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/2m/2m_6.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/2m/2m_7.jpg",
                           "TX1K, 2m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/2m/2m_7.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/2m/2m_8.jpg",
                           "TX1K, 2m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/2m/2m_8.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/2m/2m_9.jpg",
                           "TX1K, 2m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/2m/2m_9.jpg",True,'test_rig')))

	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/2.5m/2.5m_1.jpg",
                           "TX1K, 2.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/2.5m/2.5m_1.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/2.5m/2.5m_2.jpg",
                           "TX1K, 2.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/2.5m/2.5m_2.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/2.5m/2.5m_3.jpg",
                           "TX1K, 2.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/2.5m/2.5m_3.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/2.5m/2.5m_4.jpg",
                           "TX1K, 2.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/2.5m/2.5m_4.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/2.5m/2.5m_5.jpg",
                           "TX1K, 2.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/2.5m/2.5m_5.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/2.5m/2.5m_6.jpg",
                           "TX1K, 2.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/2.5m/2.5m_6.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/2.5m/2.5m_7.jpg",
                           "TX1K, 2.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/2.5m/2.5m_7.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/2.5m/2.5m_8.jpg",
                           "TX1K, 2.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/2.5m/2.5m_8.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/2.5m/2.5m_9.jpg",
                           "TX1K, 2.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/2.5m/2.5m_9.jpg",True,'test_rig')))

	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/3m/3m_1.jpg",
                           "TX1K, 3m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/3m/3m_1.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/3m/3m_2.jpg",
                           "TX1K, 3m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/3m/3m_2.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/3m/3m_3.jpg",
                           "TX1K, 3m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/3m/3m_3.jpg",True,'test_rig')))
#	freq_list.append(Picture(0,
#                           path + "/vlc/back_camera/distance/TX1K/3m/3m_4.jpg",
#                           "TX1K, 3m, 1 Light Source",
#                           run_test(path + "/vlc/back_camera/distance/TX1K/3m/3m_4.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/3m/3m_5.jpg",
                           "TX1K, 3m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/3m/3m_5.jpg",True,'test_rig')))
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
                           run_test(path + "/vlc/back_camera/distance/TX1K/3m/3m_8.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/3m/3m_9.jpg",
                           "TX1K, 3m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/3m/3m_9.jpg",True,'test_rig')))

	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/3.5m/3.5m_1.jpg",
                           "TX1K, 3.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/3.5m/3.5m_1.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/3.5m/3.5m_2.jpg",
                           "TX1K, 3.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/3.5m/3.5m_2.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/3.5m/3.5m_3.jpg",
                           "TX1K, 3.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/3.5m/3.5m_3.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/3.5m/3.5m_4.jpg",
                           "TX1K, 3.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/3.5m/3.5m_4.jpg",True,'test_rig')))
#	freq_list.append(Picture(0,run_test(path + "/vlc/back_camera/distance/TX3K/3.5m/3.5m_5.jpg",True)))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/3.5m/3.5m_6.jpg",
                           "TX1K, 3.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/3.5m/3.5m_6.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/3.5m/3.5m_7.jpg",
                           "TX1K, 3.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/3.5m/3.5m_7.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/3.5m/3.5m_8.jpg",
                           "TX1K, 3.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/3.5m/3.5m_8.jpg",True,'test_rig')))
	freq_list.append(Picture(0,
                           path + "/vlc/back_camera/distance/TX1K/3.5m/3.5m_9.jpg",
                           "TX1K, 3.5m, 1 Light Source",
                           run_test(path + "/vlc/back_camera/distance/TX1K/3.5m/3.5m_9.jpg",True,'test_rig')))

	i = init_len
	while i < len(freq_list):
		freq_list[i].freq_diff = freq_list[i].freq_diff - 1000
		i = i + 1
	return freq_list
             
def   angle_x_test(error_list,path):
   	error_list.append(Picture(run_test(path + "/vlc/angled/x_axis/-18.jpg",False,'test_rig'),
                        path + "/vlc/angled/x_axis/-18.jpg",
                        "-18 deg x axis Rotation, 5 Light Source",
                        0))
   	error_list.append(Picture(run_test(path + "/vlc/angled/x_axis/-9.jpg",False,'test_rig'),
                        path + "/vlc/angled/x_axis/-9.jpg",
                        "-9 deg x axis Rotation, 5 Light Source",
                        0))
   	error_list.append(Picture(run_test(path + "/vlc/angled/x_axis/0.jpg",False,'test_rig'),
                        path + "/vlc/angled/x_axis/0.jpg",
                        "0 deg x axis Rotation, 5 Light Source",
                        0))
   	error_list.append(Picture(run_test(path + "/vlc/angled/x_axis/9.jpg",False,'test_rig'),
                        path + "/vlc/angled/x_axis/9.jpg",
                        "9 deg x axis Rotation, 5 Light Source",
                        0))
   	error_list.append(Picture(run_test(path + "/vlc/angled/x_axis/18.jpg",False,'test_rig'),
                        path + "/vlc/angled/x_axis/18.jpg",
                        "18 deg x axis Rotation, 5 Light Source",
                        0))
	return error_list


def   angle_y_test(error_list,path):
   	error_list.append(Picture(run_test(path + "/vlc/angled/y_axis/-27.jpg",False,'test_rig'),
                        path + "/vlc/angled/y_axis/-27.jpg",
                        "-27 deg y axis Rotation, 5 Light Source",
                        0))
   	error_list.append(Picture(run_test(path + "/vlc/angled/y_axis/-18.jpg",False,'test_rig'),
                        path + "/vlc/angled/y_axis/-18.jpg",
                        "-18 deg y axis Rotation, 5 Light Source",
                        0))
   	error_list.append(Picture(run_test(path + "/vlc/angled/y_axis/-9.jpg",False,'test_rig'),
                        path + "/vlc/angled/y_axis/-9.jpg",
                        "-9 deg y axis Rotation, 5 Light Source",
                        0))
   	error_list.append(Picture(run_test(path + "/vlc/angled/y_axis/0.jpg",False,'test_rig'),
                        path + "/vlc/angled/y_axis/0.jpg",
                        "0 deg y axis Rotation, 5 Light Source",
                        0))
   	error_list.append(Picture(run_test(path + "/vlc/angled/y_axis/9.jpg",False,'test_rig'),
                        path + "/vlc/angled/y_axis/9.jpg",
                        "9 deg y axis Rotation, 5 Light Source",
                        0))
   	error_list.append(Picture(run_test(path + "/vlc/angled/y_axis/18.jpg",False,'test_rig'),
                        path + "/vlc/angled/y_axis/18.jpg",
                        "18 deg y axis Rotation, 5 Light Source",
                        0))
   	error_list.append(Picture(run_test(path + "/vlc/angled/y_axis/27.jpg",False,'test_rig'),
                        path + "/vlc/angled/y_axis/27.jpg",
                        "27 deg y axis Rotation, 5 Light Source",
                        0))
   	return error_list

def   angle_z_test(error_list,path):
   	error_list.append(Picture(run_test(path + "/vlc/angled/z_axis/0.jpg",False,'test_rig'),
                        path + "/vlc/angled/z_axis/0.jpg",
                        "0 deg y axis Rotation, 5 Light Source",
                        0))
   	error_list.append(Picture(run_test(path + "/vlc/angled/z_axis/45.jpg",False,'test_rig'),
                        path + "/vlc/angled/z_axis/45.jpg",
                        "45 deg y axis Rotation, 5 Light Source",
                        0))
        error_list.append(Picture(run_test(path + "/vlc/angled/z_axis/90.jpg",False,'test_rig'),
                        path + "/vlc/angled/z_axis/90.jpg",
                        "90 deg y axis Rotation, 5 Light Source",
                        0))
   	error_list.append(Picture(run_test(path + "/vlc/angled/z_axis/135.jpg",False,'test_rig'),
                        path + "/vlc/angled/z_axis/135.jpg",
                        "135 deg y axis Rotation, 5 Light Source",
                        0))
   	error_list.append(Picture(run_test(path + "/vlc/angled/z_axis/180.jpg",False,'test_rig'),
                        path + "/vlc/angled/z_axis/180.jpg",
                        "180 deg y axis Rotation, 5 Light Source",
                        0))
   	error_list.append(Picture(run_test(path + "/vlc/angled/z_axis/225.jpg",False,'test_rig'),
                        path + "/vlc/angled/z_axis/225.jpg",
                        "225 deg y axis Rotation, 5 Light Source",
                        0))
   	error_list.append(Picture(run_test(path + "/vlc/angled/z_axis/270.jpg",False,'test_rig'),
                        path + "/vlc/angled/z_axis/270.jpg",
                        "270 deg y axis Rotation, 5 Light Source",
                        0))
   	error_list.append(Picture(run_test(path + "/vlc/angled/z_axis/315.jpg",False,'test_rig'),
                        path + "/vlc/angled/z_axis/315.jpg",
                        "315 deg y axis Rotation, 5 Light Source",
                        0))
   	error_list.append(Picture(run_test(path + "/vlc/angled/z_axis/0.jpg",False,'test_rig'),
                        path + "/vlc/angled/z_axis/0.jpg",
                        "0 deg y axis Rotation, 5 Light Source",
                        0))
	return error_list

def full_box_test(error_list):#add in testing suite of box test to shed-data
   error_list.append(Picture(run_test("/home/noah/lab/box_light/full/1.jpg",False,'box'),
                     "/home/noah/lab/box_light/full/1.jpg",
                     "full 4 light image close up 1,2,2.46,3 k freq",
                     0))
   error_list.append(Picture(run_test("/home/noah/lab/box_light/full/2.jpg",False,'box'),
                     "/home/noah/lab/box_light/full/2.jpg",
                     "full 4 light image close up 1,2,2.46,3 k freq",
                     0))
   error_list.append(Picture(run_test("/home/noah/lab/box_light/full/3.jpg",False,'box'),
                     "/home/noah/lab/box_light/full/3.jpg",
                     "full 4 light image close up 1,2,2.46,3 k freq",
                     0))
   error_list.append(Picture(run_test("/home/noah/lab/box_light/full/4.jpg",False,'box'),
                     "/home/noah/lab/box_light/full/4.jpg",
                     "full 4 light image close up 1,2,2.46,3 k freq",
                     0))
   error_list.append(Picture(run_test("/home/noah/lab/box_light/full/5.jpg",False,'box'),
                     "/home/noah/lab/box_light/full/5.jpg",
                     "full 4 light image close up 1,2,2.46,3 k freq",
                     0))
   error_list.append(Picture(run_test("/home/noah/lab/box_light/full/6.jpg",False,'box'),
                     "/home/noah/lab/box_light/full/6.jpg",
                     "full 4 light image close up 1,2,2.46,3 k freq",
                     0))
   error_list.append(Picture(run_test("/home/noah/lab/box_light/full/7.jpg",False,'box'),
                     "/home/noah/lab/box_light/full/7.jpg",
                     "full 4 light image close up 1,2,2.46,3 k freq",
                     0))
   error_list.append(Picture(run_test("/home/noah/lab/box_light/full/8.jpg",False,'box'),
                     "/home/noah/lab/box_light/full/8.jpg",
                     "full 4 light image close up 1,2,2.46,3 k freq",
                     0))
   error_list.append(Picture(run_test("/home/noah/lab/box_light/full/9.jpg",False,'box'),
                     "/home/noah/lab/box_light/full/9.jpg",
                     "full 4 light image close up 1,2,2.46,3 k freq",
                     0))
   error_list.append(Picture(run_test("/home/noah/lab/box_light/full/10.jpg",False,'box'),
                     "/home/noah/lab/box_light/full/10.jpg",
                     "full 4 light image close up 1,2,2.46,3 k freq",
                     0))
   error_list.append(Picture(run_test("/home/noah/lab/box_light/full/11.jpg",False,'box'),
                     "/home/noah/lab/box_light/full/11.jpg",
                     "full 4 light image close up 1,2,2.46,3 k freq",
                     0))
   error_list.append(Picture(run_test("/home/noah/lab/box_light/full/12.jpg",False,'box'),
                     "/home/noah/lab/box_light/full/12.jpg",
                     "full 4 light image close up 1,2,2.46,3 k freq",
                     0))
   error_list.append(Picture(run_test("/home/noah/lab/box_light/full/13.jpg",False,'box'),
                     "/home/noah/lab/box_light/full/13.jpg",
                     "full 4 light image close up 1,2,2.46,3 k freq",
                     0))
   error_list.append(Picture(run_test("/home/noah/lab/box_light/full/14.jpg",False,'box'),
                     "/home/noah/lab/box_light/full/14.jpg",
                     "full 4 light image close up 1,2,2.46,3 k freq",
                     0))
   error_list.append(Picture(run_test("/home/noah/lab/box_light/full/15.jpg",False,'box'),
                     "/home/noah/lab/box_light/full/15.jpg",
                     "full 4 light image close up 1,2,2.46,3 k freq",
                     0))
   error_list.append(Picture(run_test("/home/noah/lab/box_light/full/16.jpg",False,'box'),
                     "/home/noah/lab/box_light/full/16.jpg",
                     "full 4 light image close up 1,2,2.46,3 k freq",
                     0))
   error_list.append(Picture(run_test("/home/noah/lab/box_light/full/17.jpg",False,'box'),
                     "/home/noah/lab/box_light/full/17.jpg",
                     "full 4 light image close up 1,2,2.46,3 k freq",
                     0))
   error_list.append(Picture(run_test("/home/noah/lab/box_light/full/18.jpg",False,'box'),
                     "/home/noah/lab/box_light/full/18.jpg",
                     "full 4 light image close up 1,2,2.46,3 k freq",
                     0))
   error_list.append(Picture(run_test("/home/noah/lab/box_light/full/19.jpg",False,'box'),
                     "/home/noah/lab/box_light/full/19.jpg",
                     "full 4 light image close up 1,2,2.46,3 k freq",
                     0))
   """
   error_list.append(Picture(run_test("/home/noah/lab/box_light/full/20.jpg",False,'box'),
                     "/home/noah/lab/box_light/full/20.jpg",
                     "full 4 light image close up 1,2,2.46,3 k freq",
                     0))
   error_list.append(Picture(run_test("/home/noah/lab/box_light/full/21.jpg",False,'box'),
                     "/home/noah/lab/box_light/full/21.jpg",
                     "full 4 light image close up 1,2,2.46,3 k freq",
                     0))
   error_list.append(Picture(run_test("/home/noah/lab/box_light/full/22.jpg",False,'box'),
                     "/home/noah/lab/box_light/full/22.jpg",
                     "full 4 light image close up 1,2,2.46,3 k freq",
                     0))
   error_list.append(Picture(run_test("/home/noah/lab/box_light/full/23.jpg",False,'box'),
                     "/home/noah/lab/box_light/full/23.jpg",
                     "full 4 light image close up 1,2,2.46,3 k freq",
                     0))
   error_list.append(Picture(run_test("/home/noah/lab/box_light/full/24.jpg",False,'box'),
                     "/home/noah/lab/box_light/full/24.jpg",
                     "full 4 light image close up 1,2,2.46,3 k freq",
                     0))
   error_list.append(Picture(run_test("/home/noah/lab/box_light/full/25.jpg",False,'box'),
                     "/home/noah/lab/box_light/full/25.jpg",
                     "full 4 light image close up 1,2,2.46,3 k freq",
                     0))
   error_list.append(Picture(run_test("/home/noah/lab/box_light/full/26.jpg",False,'box'),
                     "/home/noah/lab/box_light/full/26.jpg",
                     "full 4 light image close up 1,2,2.46,3 k freq",
                     0))
   error_list.append(Picture(run_test("/home/noah/lab/box_light/full/27.jpg",False,'box'),
                     "/home/noah/lab/box_light/full/27.jpg",
                     "full 4 light image close up 1,2,2.46,3 k freq",
                     0))
   error_list.append(Picture(run_test("/home/noah/lab/box_light/full/28.jpg",False,'box'),
                     "/home/noah/lab/box_light/full/28.jpg",
                     "full 4 light image close up 1,2,2.46,3 k freq",
                     0))
   """
   return error_list
   
