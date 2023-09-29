#!/usr/bin/env python

from glob import glob
from pathlib import Path
import subprocess

classes = Path("target/classes")

for f in classes.glob("**/*.class"):
    result = f.relative_to(classes)
    decompiled = "decompiled" / result.with_suffix("").with_suffix(".json")
    decompiled.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.check_output(["jvm2json", "-s", f])
    with open(decompiled, "wb") as df:
        p = subprocess.Popen(["jq", "."], stdin=subprocess.PIPE, stdout=df)
        p.communicate(input=result)
