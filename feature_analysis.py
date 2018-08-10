from autobpa import AutoBPA
from packetstatistics import PacketStatistics
from select_metrics import SelectMetrics


# def metric_analysis():
# def feature_statistics(dbm_antsignal, datarate, duration, seq, ttl):

def metric_analysis(dbm_antsignal, datarate, duration, seq, ttl, sw_size):
    # Extract the first 'sw_size' amount of packets and store in new arrays
    # sw -> sliding window + '_feature_name'
    sw_dbm_antsignal = dbm_antsignal[0:sw_size]
    sw_datarate = datarate[0:sw_size]
    sw_duration = duration[0:sw_size]
    sw_seq = seq[0:sw_size]
    sw_ttl = ttl[0:sw_size]

    array_dict = {'dbm_antsignal': dbm_antsignal, 'datarate': datarate,
                  'duration': duration, 'seq': seq, 'ttl': ttl}

    sw_dict = {'RSSI': sw_dbm_antsignal, 'Rate': sw_datarate,
               'NAV': sw_duration, 'Seq': sw_seq, 'TTL': sw_ttl}

    # ave_dict = {}
    #
    # stats_1 = PacketStatistics
    # # loop over each array and calculate the mean/frequency for each array storing it in new dictionary
    # for k, v in sw_dict.items():
    #     if k == 'sw_ttl':
    #         ave_dict[k] = stats_1.frequency(v)
    #         print(ave_dict[k])
    #     else:
    #         ave_dict[k] = stats_1.mean(v)
    #         print(ave_dict[k])
    #
    # stats_2 = PacketStatistics

    # Loop through the arrays, extract the next packets one at a time
    # compare features with average values and then add or disregard packet
    # and then update averages


    # counter = 0

    # for x in range(start, stop, step):
    #     for k_1, arrays in array_dict.items():
    #        for k_2, ave in ave_dict.items():
    #             counter += 1
    #             returns the absolute distance between the average for the feature and the new packet feature
    #            stats_2.distance(ave, arrays[x])
    # print(counter)

    # rssi_bpa = AutoBPA(data=sw_dbm_antsignal, sw=sw_size)
    # rate_bpa = AutoBPA(data=sw_datarate, sw=sw_size)
    # nav_bpa = AutoBPA(data=sw_duration, sw=sw_size)
    # seq_bpa = AutoBPA(data=sw_seq, sw=sw_size)
    # ttl_bpa = AutoBPA(data=sw_ttl, sw=sw_size)

    metric = SelectMetrics(metric_val=sw_size)
    features_to_analyse = metric.metric_combination()

    instance_dict = {}
    # create an instance of each feature that is going to be analysed
    # and store the instances in a dictionary 'instance_dict'
    for feature in features_to_analyse:
        for key, arrays in sw_dict.items():
            if feature == key:
                name = feature + '_bpa'
                print('Creating instance of AutoBPA class called {}.'
                      'The Feature is : {}'.format(name, feature))
                print(arrays)
                # creates an instance of AutoBPA class
                x = globals()[name] = AutoBPA(data=arrays, sw=sw_size)
                instance_dict[key] = x

    print(instance_dict)

    print('lenght of dbm_antsignal is {}'.format(len(dbm_antsignal)))
    start, stop, step = sw_size + 1, len(dbm_antsignal), 1

    for incr in range(start, stop, step):
        for k_1, arrays in array_dict.items():
            for k_2, inst in instance_dict.items():

                instance_dict[k_2].mean()
                instance_dict[k_2].distance(arrays[incr])
                instance_dict[k_2].box_plot()

                n = instance_dict[k_2].normal(arrays[incr])
                a = instance_dict[k_2].attack()
                u = instance_dict[k_2].uncertainty()
                phi = instance_dict[k_2].adjustment_factor()

                



