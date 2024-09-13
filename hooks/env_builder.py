import os
import os.path
import pathlib
import sys
import venv
from subprocess import PIPE, Popen
from threading import Thread
from urllib.parse import urlparse
from urllib.request import urlretrieve

# Based on example from https://docs.python.org/3/library/venv.html#venv.EnvBuilder.setup_scripts


class EnvBuilderWithRequirements(venv.EnvBuilder):
    """
    This builder installs setuptools and pip so that you can pip or
    easy_install other packages into the created virtual environment.

    :param nodist: If true, setuptools and pip are not installed into the
                   created virtual environment.
    :param nopip: If true, pip is not installed into the created
                  virtual environment.
    :param progress: If setuptools or pip are installed, the progress of the
                     installation can be monitored by passing a progress
                     callable. If specified, it is called with two
                     arguments: a string indicating some progress, and a
                     context indicating where the string is coming from.
                     The context argument can have one of three values:
                     'main', indicating that it is called from virtualize()
                     itself, and 'stdout' and 'stderr', which are obtained
                     by reading lines from the output streams of a subprocess
                     which is used to install the app.

                     If a callable is not specified, default progress
                     information is output to sys.stderr.
    """

    def __init__(self, *args, **kwargs):
        self.nodist = kwargs.pop("nodist", False)
        self.nopip = kwargs.pop("nopip", False)
        self.progress = kwargs.pop("progress", None)
        self.verbose = kwargs.pop("verbose", False)
        self.install_from_requirements = kwargs.pop("install_requirements", True)
        super().__init__(*args, **kwargs)

    def post_setup(self, context):
        """
        Set up any packages which need to be pre-installed into the
        virtual environment being created.

        :param context: The information for the virtual environment
                        creation request being processed.
        """
        os.environ["VIRTUAL_ENV"] = context.env_dir
        if not self.nodist:
            self.install_setuptools(context)
        # Can't install pip without setuptools
        if not self.nopip and not self.nodist:
            self.install_pip(context)
        if self.install_from_requirements:
            self.install_requirements(context)

    def install_requirements(self, context):
        binpath = context.bin_path
        if sys.platform.startswith("linux"):
            executable = "pip"
        else:
            executable = "pip.exe"
        pip_path = pathlib.Path(binpath, executable)
        requirement_fn = pathlib.Path(pathlib.Path.cwd(), "requirements.txt")
        p = Popen([pip_path, "install", "-r", requirement_fn])
        p.wait()

    def reader(self, stream, context):
        """
        Read lines from a subprocess' output stream and either pass to a progress
        callable (if specified) or write progress information to sys.stderr.
        """
        progress = self.progress
        while True:
            s = stream.readline()
            if not s:
                break
            if progress is not None:
                progress(s, context)
            else:
                if not self.verbose:
                    sys.stderr.write(".")
                else:
                    sys.stderr.write(s.decode("utf-8"))
                sys.stderr.flush()
        stream.close()

    def install_script(self, context, name, url):
        _, _, path, _, _, _ = urlparse(url)
        fn = os.path.split(path)[-1]
        binpath = context.bin_path
        distpath = os.path.join(binpath, fn)
        # Download script into the virtual environment's binaries folder
        urlretrieve(url, distpath)
        progress = self.progress
        if self.verbose:
            term = "\n"
        else:
            term = ""
        if progress is not None:
            progress("Installing %s ...%s" % (name, term), "main")
        else:
            sys.stderr.write("Installing %s ...%s" % (name, term))
            sys.stderr.flush()
        args = [context.env_exe, fn]
        p = Popen(args, stdout=PIPE, stderr=PIPE, cwd=binpath)
        t1 = Thread(target=self.reader, args=(p.stdout, "stdout"))
        t1.start()
        t2 = Thread(target=self.reader, args=(p.stderr, "stderr"))
        t2.start()
        p.wait()
        t1.join()
        t2.join()
        if progress is not None:
            progress("done.", "main")
        else:
            sys.stderr.write("done.\n")
        # Clean up - no longer needed
        os.unlink(distpath)

    def install_setuptools(self, context):
        """
        Install setuptools in the virtual environment.

        :param context: The information for the virtual environment
                        creation request being processed.
        """
        url = "https://bootstrap.pypa.io/ez_setup.py"
        self.install_script(context, "setuptools", url)
        # clear up the setuptools archive which gets downloaded
        pred = lambda o: o.startswith("setuptools-") and o.endswith(".tar.gz")
        files = filter(pred, os.listdir(context.bin_path))
        for f in files:
            f = os.path.join(context.bin_path, f)
            os.unlink(f)

    def install_pip(self, context):
        """
        Install pip in the virtual environment.

        :param context: The information for the virtual environment
                        creation request being processed.
        """
        url = "https://bootstrap.pypa.io/get-pip.py"
        self.install_script(context, "pip", url)
