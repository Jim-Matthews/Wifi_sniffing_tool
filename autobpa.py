from packetstatistics import PacketStatistics


class AutoBPA(PacketStatistics):
    """

    """
    # alf = 0

    # Putting new variables before kwargs seems to be allowed.
    # **kwargs is a dictionary of keyword arguments that can take on any
    # number of key, value pairs. No default values are set in Statistics class
    def __init__(self, sw, **kwargs):
        super().__init__(**kwargs)
        self._sw = sw
        if 'normal_bpa' in kwargs: self._normal_bpa = kwargs['normal_bpa']
        if 'attack_bpa' in kwargs: self._attack_bpa = kwargs['attack_bpa']
        if 'uncertainty_bpa' in kwargs: self._uncertainty_bpa = kwargs['uncertainty_bpa']
        if 'adjustment_factor' in kwargs: self._adjust_bpa = kwargs['adjustment_factor']

    def normal(self, value):
        """

        :param value:
        :return:
        """
        # This will use quartiles from a box and whisker plot in PacketStatistics
        # to assign a BPA for normal based on the metric value
        min_val = self._lower_quart - (1.5 * self._inter_quart_range)
        max_val = self._upper_quart + (1.5 * self._inter_quart_range)

        if self._lower_quart < value < self._upper_quart:
            self._normal_bpa = 0.4
        elif min_val < value < self._lower_quart or self._upper_quart < value < max_val:
                self._normal_bpa = 0.3
        else:
            self._normal_bpa = 0.15
        return self._normal_bpa

    def attack(self):
        """

        :return:
        """
        # Euclidean distance of current value from reference point and reference to max value
        self._attack_bpa = (self._dist_mean * 0.5) / self._dist_maxval
        # print(self._dist_mean, self._dist_maxval, self._attack_bpa)
        if self._attack_bpa > 0.5:
            self._attack_bpa = 0.5

        return self._attack_bpa

    def uncertainty(self):
        """

        :return:
        """
        # Min of N and A divided by Max of N and A
        if self._normal_bpa > self._attack_bpa:
            min_bpa = self._attack_bpa
            max_bpa = self._normal_bpa
        elif self._normal_bpa < self._attack_bpa:
            min_bpa = self._normal_bpa
            max_bpa = self._attack_bpa
        else:
            min_bpa, max_bpa = 0.5, 0.5

        self._uncertainty_bpa = min_bpa / max_bpa

        return self._uncertainty_bpa

    def adjustment_factor(self):
        """

        :return:
        """
        # Calculate the adjustment factor to be applied to each bpa
        self._adjust_bpa = ((self._normal_bpa + self._attack_bpa + self._uncertainty_bpa) - 1) / 3
        n_phi = self._normal_bpa /(self._normal_bpa + self._attack_bpa + self._uncertainty_bpa)
        a_phi = self._attack_bpa /(self._normal_bpa + self._attack_bpa + self._uncertainty_bpa)
        u_phi = self._uncertainty_bpa /(self._normal_bpa + self._attack_bpa + self._uncertainty_bpa)
        return self._adjust_bpa, n_phi, a_phi, u_phi

    def combined_value(self, value):
        """

        :param value:
        :return:
        """
        ds_dict = {}

        n = self.normal(value)
        a = self.attack()
        u = self.uncertainty()
        phi, n_phi, a_phi, u_phi = self.adjustment_factor()
        # print(n, a, u)

        ds_dict['n'] = n - phi
        ds_dict['a'] = a - phi
        ds_dict['u'] = u - phi

        # ds_dict['n'] = n_phi
        # ds_dict['a'] = a_phi
        # ds_dict['u'] = u_phi

        return ds_dict

    @classmethod
    def create_instance(cls, features_to_analyse, sw_dict, sw_size):
        """

        :param features_to_analyse:
        :param sw_dict:
        :param sw_size:
        :return:
        """
        instance_dict = {}

        # create an instance of each feature that is going to be analysed
        # and store the instances in a dictionary 'instance_dict'
        for feature, sw_dict_iter in zip(features_to_analyse, sw_dict.items()):
            # for feature in features_to_analyse:
            #     for key, arrays in sw_dict.items():
            #         if feature == key:
            name = feature + '_bpa'
            # print('Creating instance of AutoBPA class called {}. '
            #       'The Feature is : {}'.format(name, feature))
            # print(sw_dict_iter[1])
            # print(len(sw_dict_iter[1]))
            #if len(sw_dict_iter[1]) != 30:
                #print('sw_dict metric array data inside create_instance function: {}'.format(sw_dict_iter[1]))
            # creates an instance of AutoBPA class
            # instance = globals()[name] = AutoBPA(data=sw_dict_iter[1], sw=sw_size)
            # instance_dict[sw_dict_iter[0]] = instance
            # print('sw_dict metric array data inside create_instance function: {}'.format(sw_dict_iter[1]))
            instance_dict[sw_dict_iter[0]] = AutoBPA(data=sw_dict_iter[1], sw=sw_size)
        ttl_array = sw_dict['TTL']
        # print(instance_dict)
        return instance_dict, ttl_array
