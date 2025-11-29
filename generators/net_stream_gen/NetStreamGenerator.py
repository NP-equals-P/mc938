from . import AbstractGenerator, MAX_DIGIT_COUNTER

from psutil import net_io_counters

class NetStreamGenerator(AbstractGenerator):

    def __init__(self, max_digit_counter = MAX_DIGIT_COUNTER):
        super().__init__()
        self.update_switch = 0
        self.digit_counter = 0
        self.max_digit_counter = max_digit_counter
        self.index_counter = 0
        self._setup_seed()
        self._setup_indexes()

    def _setup_seed(self):
        net_readings = net_io_counters()
        self.seed = str(net_readings.bytes_sent)[-4:] + str(net_readings.bytes_recv)[-4:]

    def _setup_indexes(self):
        self.seed_indexes = [-8, -4, -2, -1]

    def _append_new_reading(self):
        net_readings = net_io_counters()
        net_rd_list = [net_readings.bytes_sent, net_readings.bytes_recv]
        new_number = str(net_rd_list[self.update_switch])[-4:]
        self.update_switch = (self.update_switch + 1)%2
        new_seed = self.seed[-4:] + new_number
        self.seed = new_seed

    def _sum_to_char_digit(self, d:str, n:int):
        sum = (int(d)+n)%10
        return str(sum)

    def _swap_seed_digits(self, pos1, pos2):
        pos1, pos2 = pos1%8, pos2%8
        pos1, pos2 = min(pos1, pos2), max(pos1, pos2)
        print(pos1, pos2)
        if pos1 < pos2:
            digit1 = self.seed[pos1]
            digit1 = self._sum_to_char_digit(digit1, 1)
            digit2 = self.seed[pos2]
            digit2 = self._sum_to_char_digit(digit2, -1)
            swapSeed = self.seed[:pos1] + digit2 + \
                self.seed[pos1+1:pos2] + digit1
            if pos2 < len(self.seed) - 1:
                swapSeed += self.seed[pos2+1:]
            self.seed = swapSeed

    def _sort_seed(self):
        indexes = [
            i for i in self.seed_indexes if i%8 != (-i)%8
        ]
        idx_set = set(indexes)
        for i in idx_set:
            self._swap_seed_digits(i, -i)

    def _update_indexes(self):
        new_indexes = []
        for i in range(len(self.seed_indexes)):
            idx1 = self.seed_indexes[i]
            idx2 = self.seed_indexes[(i+1)%len(self.seed_indexes)]
            idx = (self._get_seed_digit(idx1, False) - \
                idx2 + (idx2 == 0))%8
            new_indexes.append(idx)
        self.seed_indexes = new_indexes

    def _update_counters(self):
        self.digit_counter = (self.digit_counter + 1)%self.max_digit_counter
        self.index_counter = (self.index_counter + 1)%len(self.seed_indexes)
        if self.index_counter == 0:
            self._sort_seed()
            self._update_indexes()
        if self.digit_counter == 0:
            self._append_new_reading()

    def _get_seed_digit(self, index=None, update=True):
        if index is None:
            index = self.seed_indexes[self.index_counter]
        digit = self.seed[index%8]
        if update:
            self._update_counters()
        return int(digit)

    def get_random_float(self, min, max):
        assert min <= max, f"Warning: min ({min}) is greater than max ({max})"
        num_digits = len(str(max))
        upper = int('9'*num_digits)
        lower = 0
        # Get a random number with 'num_digits' digits
        n = 0
        for i in range(num_digits):
            n *= 10
            n += self._get_seed_digit()
        # Scale 'n' between 0 and 1
        scale1 = (n - lower)/(upper - lower)
        # Scale 'n' between 'min' and 'max'
        scale2 = scale1 * (max - min) + min
        return scale2

    def get_random_int(self, min, max):
        return round(self.get_random_float(min, max))

    

    
