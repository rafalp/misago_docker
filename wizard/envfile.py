from datetime import datetime
from pathlib import Path
from utils import safe_open


class EnvFile:
    def __init__(self, header, path):
        self.header = header
        self.path = Path(path)
        self.variables = {}

        if self.is_file():
            self.variables = self.read()

    def is_file(self):
        return self.path.is_file()

    def read(self):
        with safe_open(self.path, "r") as f:
            return parse_env_file(f.read())

    def save(self):
        lines = []
        lines.append("# %s" % self.header)
        lines.append("# %s\n" % datetime.now())

        for key in sorted(self.variables.keys()):
            value = self.variables[key]
            lines.append("%s=%s" % (key, value))

        with safe_open(self.path, "w") as f:
            f.write("\n".join(lines))

    def __setitem__(self, key, item):
        self.variables[key] = item

    def __getitem__(self, key):
        return self.variables[key]

    def get(self, name, default=None):
        return self.variables.get(name, default)


def parse_env_file(file_contents):
    variables = {}
    for line in file_contents.splitlines():
        stripped_line = line.strip()
        if not stripped_line:
            continue
        if stripped_line.startswith("#"):
            continue
        if "=" not in stripped_line:
            continue

        assignment_position = stripped_line.find("=")
        key = stripped_line[:assignment_position]
        value = stripped_line[assignment_position + 1 :].strip('"')
        variables[key] = value

    return variables
