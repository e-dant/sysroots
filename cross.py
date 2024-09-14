import os
import subprocess
from dataclasses import dataclass


@dataclass
class Container:
    arch: str
    image: str

    def copy_sysroot_to(self, triple: str, dst: str):
        os.makedirs(f"sysroots/{triple}")
        c = subprocess.run(
            [
                "docker",
                "run",
                "--rm",
                "-it",
                "-d",
                f"--platform={self.arch}",
                f"{self.image}:latest",
            ],
            stdout=subprocess.PIPE,
        ).stdout.decode().strip()
        if self.image == "alpine":
            subprocess.run(
                [
                    "docker",
                    "exec",
                    c,
                    "apk",
                    "add",
                    "libstdc++",
                    "libatomic",
                ],
                stdout=subprocess.DEVNULL,
            )
        else:
            subprocess.run(
                [
                    "docker",
                    "exec",
                    c,
                    "apt-get",
                    "update",
                ],
            )
            subprocess.run(
                [
                    "docker",
                    "exec",
                    c,
                    "apt-get",
                    "install",
                    "-y",
                    "libstdc++6",
                    "libatomic1",
                    "build-essential",
                ],
            )
        subprocess.run(
            [
                "docker",
                "cp",
                f"{c}:/usr",
                f"{dst}/{triple}/usr",
            ],
            stdout=subprocess.DEVNULL,
        )
        subprocess.run(
            [
                "docker",
                "cp",
                f"{c}:/lib",
                f"{dst}/{triple}/lib",
            ],
            stdout=subprocess.DEVNULL,
        )
        subprocess.run(["docker", "stop", c], stdout=subprocess.DEVNULL)


@dataclass
class Toolchain:
    triple: str
    sysroot_path: str
    include_paths: list[str]
    sysroot_via_container: Container

    def copy_sysroot_to_host(self):
        self.sysroot_via_container.copy_sysroot_to(self.triple, self.sysroot_path)



TOOLCHAINS = [
    Toolchain(
        "aarch64-unknown-linux-gnu",
        "sysroots",
        [
            "usr/include",
            "usr/include/c++/12",
            "usr/include/arm-linux-gnueabihf/c++/12",
            "usr/include/arm-linux-gnueabihf",
        ],
        Container("linux/arm64", "debian"),
    ),
    Toolchain(
        "armv7-unknown-linux-gnueabihf",
        "sysroots",
        [
            "usr/include",
            "usr/include/c++/12",
            "usr/include/arm-linux-gnueabihf/c++/12",
            "usr/include/arm-linux-gnueabihf",
        ],
        Container("linux/arm/v7", "debian"),
    ),
    Toolchain(
        "arm-unknown-linux-gnueabihf",
        "sysroots",
        [
            "usr/include",
            "usr/include/c++/12",
            "usr/include/arm-linux-gnueabihf/c++/12",
            "usr/include/arm-linux-gnueabihf",
        ],
        Container("linux/arm/v6", "debian"),
    ),
    Toolchain(
        "x86_64-unknown-linux-gnu",
        "sysroots",
        [
            "usr/include",
            "usr/include/c++/12",
            "usr/include/x86_64-linux-gnu/c++/12",
            "usr/include/x86_64-linux-gnu",
        ],
        Container("linux/amd64", "debian"),
    ),
    Toolchain(
        "i686-unknown-linux-gnu",
        "sysroots",
        [
            "usr/include",
            "usr/include/c++/12",
            "usr/include/i686-linux-gnu/c++/12",
            "usr/include/i686-linux-gnu",
        ],
        Container("linux/i386", "debian"),
    ),
    Toolchain(
        "aarch64-unknown-linux-musl",
        "sysroots",
        [
            "usr/include",
            "usr/include/c++/12",
            "usr/include/arm-linux-gnueabihf/c++/12",
            "usr/include/arm-linux-gnueabihf",
        ],
        Container("linux/arm64", "alpine"),
    ),
    Toolchain(
        "armv7-unknown-linux-musleabihf",
        "sysroots",
        [
            "usr/include",
            "usr/include/c++/12",
            "usr/include/arm-linux-gnueabihf/c++/12",
            "usr/include/arm-linux-gnueabihf",
        ],
        Container("linux/arm/v7", "alpine"),
    ),
    Toolchain(
        "arm-unknown-linux-musleabihf",
        "sysroots",
        [
            "usr/include",
            "usr/include/c++/12",
            "usr/include/arm-linux-gnueabihf/c++/12",
            "usr/include/arm-linux-gnueabihf",
        ],
        Container("linux/arm/v6", "alpine"),
    ),
    Toolchain(
        "x86_64-unknown-linux-musl",
        "sysroots",
        [
            "usr/include",
            "usr/include/c++/12",
            "usr/include/x86_64-linux-gnu/c++/12",
            "usr/include/x86_64-linux-gnu",
        ],
        Container("linux/amd64", "alpine"),
    ),
    Toolchain(
        "i686-unknown-linux-musl",
        "sysroots",
        [
            "usr/include",
            "usr/include/c++/12",
            "usr/include/i686-linux-gnu/c++/12",
            "usr/include/i686-linux-gnu",
        ],
        Container("linux/i386", "alpine"),
    ),
]


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--triples",
        nargs="*",
        default=[s.triple for s in TOOLCHAINS],
        help="List of triples to generate sysroots for",
    )
    parser.add_argument(
        "--list-triples",
        action="store_true",
        help="List available triples",
    )
    args = parser.parse_args()
    triples = args.triples
    if args.list_triples:
        for t in TOOLCHAINS:
            print(t.triple)
    else:
        for t in TOOLCHAINS:
            if t.triple not in triples:
                print(f"[{t.triple}] Skipped")
            elif os.path.exists(f"{t.sysroot_path}/{t.triple}"):
                print(f"[{t.triple}] Exists")
            else:
                t.copy_sysroot_to_host()
                print(f"[{t.triple}] Created")
