#! /usr/bin/python3
from settings import (
        REPO,
        BRANCHES,
        STARTING_REVISIONS,
        LLVM_VERSIONS,
        PROJECT_NAME,
        ENVIRONMENT,
        CODESPEED_URL,
        BENCHS
        )

import os
import subprocess
import time
from urllib import parse, request
import json


class RevDB:
    def __init__(self):
        self.done = []
        self.revisions = STARTING_REVISIONS
        with open("revisions.db") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                branch, rev = line.strip().split(":")
                self.revisions[branch] = rev

    def commit(self):
        commited = {}
        for branch in self.done:
            commited[branch] = self.revisions[branch]
        with open("revisions.db") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                branch, rev = line.strip().split(":")
                if branch not in self.done:
                    commited[branch] = rev
        with open("revisions.db", "w") as f:
            for branch, rev in commited.items():
                f.write("{}:{}\n".format(branch, rev))

    def __getitem__(self, branch):
        return self.revisions[branch]

    def __setitem__(self, branch, rev):
        self.done.append(branch)
        self.revisions[branch] = rev


DB = RevDB()


class Repo:
    def __init__(self, path):
        self.path = path

    def git(self, cmd):
        cmd = ["git", "-C", self.path] + cmd
        print(" ".join(cmd))
        return subprocess.check_output(cmd)

    def checkout(self, revision):
        return self.git(["checkout", revision])

    def fetch(self):
        return self.git(["fetch"])

    def rev_list(self, revs, merges=None):
        opts = []
        if merges is not None:
            opts.append("--merges" if merges else "--no-merges")
        return self.git(["rev-list"] + opts + list(revs))

    def pull(self):
        return self.git(["pull"])


class Executable:
    def __init__(self, llvm_version):
        self.llvm_version = llvm_version
        self.exe = os.path.abspath(os.sep.join([".", "build", "release", "ponyc"]))
        self.name = "ponyc-llvm" + self.llvm_version

    def make(self):
        print(subprocess.check_output(["pwd"]))
        subprocess.check_output(["make", "clean"])
        cmd = [
            "make",  "config=release",
            "LLVM_CONFIG=llvm-config-{0}".format(self.llvm_version),
            "LLVM_LINK=llvm-link-{0}".format(self.llvm_version),
            "LLVM_OPT=opt-{0}".format(self.llvm_version)]
        print(" ".join(cmd))
        subprocess.check_output(cmd)

    def compile(self, bench):
        os.chdir(bench)
        bench_exe = os.path.basename(bench)
        dest_dir = "build"
        target = os.sep.join([dest_dir, bench_exe])
        try:
            os.unlink(target)
        except OSError:
            pass
        os.makedirs(dest_dir, exist_ok=True)
        start = time.time()
        subprocess.check_output([self.exe, "-o", dest_dir])
        duration = time.time() - start
        return (os.path.abspath(target),
                "{}_compile".format(bench_exe),
                duration)


class BenchRunner:
    def __init__(self, llvm_version):
        self.llvm_version = llvm_version
        self.exe = Executable(llvm_version)
        self.exe.make()

    def run(self):
        results = []
        for b in BENCHS:
            compile_time = 10000
            for _ in range(3):
                target, name, _compile_time = self.exe.compile(b)
                compile_time = min(compile_time, _compile_time)
            results.append({
                'executable': self.exe.name,
                'benchmark': name,
                'result_value': compile_time,
            })
            results.append({
                'executable': self.exe.name,
                'benchmark': name[:-8],
                'result_value': self.run_bench(target),
            })
        return results

    def run_bench(self, bench):
        duration = 10000
        for _ in range(3):
            start = time.time()
            subprocess.call([bench])
            duration = min(duration, time.time() - start)
        return duration


class ProjectRunner:
    def __init__(self):
        self.last_ref = None
        self.git = Repo(os.path.abspath(REPO))
        self.orig = os.path.abspath(".")

    def run_branch(self, branch):
        os.chdir(self.orig)
        done = DB[branch]
        print("Starting at " + done)
        self.git.checkout(branch)
        self.git.pull()
        revisions = self.git.rev_list(["...{}".format(done)], merges=False
                                      ).split()
        revisions = [r.decode() for r in revisions]
        revisions.reverse()
        for rev in revisions:
            self.git.checkout(rev)
            os.chdir(REPO)
            results = []
            for llvm in LLVM_VERSIONS:
                os.chdir(self.git.path)
                benchs = BenchRunner(llvm).run()
                for b in benchs:
                    b["commitid"] = rev
                    b["branch"] = branch
                    b["project"] = PROJECT_NAME
                    b["environment"] = ENVIRONMENT
                results = results + benchs
            send(results)
            os.chdir(self.orig)
            DB[branch] = rev
            DB.commit()

    def run(self, branch="master"):
        self.git.fetch()
        for branch in BRANCHES:
            print("Running benchmarks on branch `{}`".format(branch))
            self.run_branch(branch)


def send(data):
    data = {'json': json.dumps(data)}
    print(data)
    response = "None"
    try:
        f = request.urlopen(
            CODESPEED_URL + 'result/add/json/', parse.urlencode(data).encode())
    except request.HTTPError as e:
        print(str(e))
        print(e.read())
        return
    response = f.read()
    f.close()
    print("Server ({}) response: {}\n".format(CODESPEED_URL, response))

if __name__ == "__main__":
    results = ProjectRunner().run()
    #results = [{'result_value': 1.5111408233642578, 'executable': 'ponyc-3.8', 'branch': 'default', 'environment': 'lisael-laptop', 'project': 'ponyc', 'benchmark': 'montecarlo_compile', 'commitid': 'e74800f893e23f39e733f56a8b5c9cf2f192806f'}, {'result_value': 0.6346533298492432, 'executable': 'ponyc-3.8', 'branch': 'default', 'environment': 'lisael-laptop', 'project': 'ponyc', 'benchmark': 'montecarlo', 'commitid': 'e74800f893e23f39e733f56a8b5c9cf2f192806f'}, {'result_value': 1.4899559020996094, 'executable': 'ponyc-3.8', 'branch': 'default', 'environment': 'lisael-laptop', 'project': 'ponyc', 'benchmark': 'montecarlo_compile', 'commitid': '91e690faeddf5be28af17e6fad13ae845442a778'}, {'result_value': 0.6266851425170898, 'executable': 'ponyc-3.8', 'branch': 'default', 'environment': 'lisael-laptop', 'project': 'ponyc', 'benchmark': 'montecarlo', 'commitid': '91e690faeddf5be28af17e6fad13ae845442a778'}, {'result_value': 1.4882090091705322, 'executable': 'ponyc-3.8', 'branch': 'default', 'environment': 'lisael-laptop', 'project': 'ponyc', 'benchmark': 'montecarlo_compile', 'commitid': '843910841fc1458e0fd4961c75b84191c8220c02'}, {'result_value': 0.5727229118347168, 'executable': 'ponyc-3.8', 'branch': 'default', 'environment': 'lisael-laptop', 'project': 'ponyc', 'benchmark': 'montecarlo', 'commitid': '843910841fc1458e0fd4961c75b84191c8220c02'}, {'result_value': 1.4979708194732666, 'executable': 'ponyc-3.8', 'branch': 'default', 'environment': 'lisael-laptop', 'project': 'ponyc', 'benchmark': 'montecarlo_compile', 'commitid': '8910b3cd9fc71a30a340c8159a83991be7aee5be'}, {'result_value': 0.5691986083984375, 'executable': 'ponyc-3.8', 'branch': 'default', 'environment': 'lisael-laptop', 'project': 'ponyc', 'benchmark': 'montecarlo', 'commitid': '8910b3cd9fc71a30a340c8159a83991be7aee5be'}, {'result_value': 1.4882702827453613, 'executable': 'ponyc-3.8', 'branch': 'default', 'environment': 'lisael-laptop', 'project': 'ponyc', 'benchmark': 'montecarlo_compile', 'commitid': '9ffba47501f9bba5870891b233af8a6a0cda66fb'}, {'result_value': 0.5743973255157471, 'executable': 'ponyc-3.8', 'branch': 'default', 'environment': 'lisael-laptop', 'project': 'ponyc', 'benchmark': 'montecarlo', 'commitid': '9ffba47501f9bba5870891b233af8a6a0cda66fb'}, {'result_value': 1.486685037612915, 'executable': 'ponyc-3.8', 'branch': 'default', 'environment': 'lisael-laptop', 'project': 'ponyc', 'benchmark': 'montecarlo_compile', 'commitid': 'd51cdfa9fecab8a83b812965aaf3e2ad57a76f94'}, {'result_value': 0.5681722164154053, 'executable': 'ponyc-3.8', 'branch': 'default', 'environment': 'lisael-laptop', 'project': 'ponyc', 'benchmark': 'montecarlo', 'commitid': 'd51cdfa9fecab8a83b812965aaf3e2ad57a76f94'}]
    #send(results)
