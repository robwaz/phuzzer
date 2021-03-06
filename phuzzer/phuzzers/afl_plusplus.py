import subprocess
import logging
import os

from .afl import AFL

l = logging.getLogger(__name__)


class AFLPlusPlus(AFL):
    """ AFL++ port of AFL phuzzer.
        Paper found here:
        https://aflplus.plus//papers/aflpp-woot2020.pdf
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def choose_afl(self):
        self.afl_bin_dir = '/phuzzers/AFLplusplus/' if 'AFL_PATH' not in os.environ else os.environ['AFL_PATH']
        afl_bin_path = os.path.join(self.afl_bin_dir, "afl-fuzz")
        return afl_bin_path

    def _start_afl_instance(self, instance_cnt=0):

        args, fuzzer_id = self.build_args()
        my_env = os.environ.copy()

        if "AFL_SET_AFFINITY" in my_env:
            core_num = int(my_env["AFL_SET_AFFINITY"])
            core_num += instance_cnt
            print(args)
            args = [args[0]] + [f"-b {core_num}"] + args[1:]

        logpath = os.path.join(self.work_dir, fuzzer_id + ".log")
        l.debug("execing: %s > %s", ' '.join(args), logpath)

        with open(logpath, "w") as fp:
            return subprocess.Popen(args, stdout=fp, stderr=fp, close_fds=True, env=my_env)
