import fileutil
import subprocess
import json
from config import *
import functools


@functools.lru_cache()
def get_config(tool):
    jsn = json.load(
        open("{tools_dir}/{tool}.json".format(tools_dir=TOOLS_DIR, tool=tool))
    )
    return jsn


def process(file):
    methodjson = get_config(file.method)
    if file.name.split(".")[-1].lower() in methodjson["support"]:
        args = (
            methodjson["args"]
            .replace("{input}", file.location)
            .replace("{output}", file.destination)
        )
        subprocess.run(
            "{}/{} {}".format(TOOLS_DIR, methodjson["filename"], args),
            shell=False,
            capture_output=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        if fileutil.check_file_exists(file.destination):
            print(
                "{inname} is converted to {outext}".format(
                    inname=fileutil.get_filename(file.location), outext=file.method
                )
            )
            file.processed = True
    return file
