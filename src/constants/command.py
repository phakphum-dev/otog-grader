ioeredirect = " 2>env/error.txt"
langarr = {
    "c": {
        "extension": "c",
        "compile": "gcc [sourcePath] -O2 -std=c17 -fomit-frame-pointer -Wunused-result -o env/out"
        + ioeredirect,
        "execute": "./out [inputfile]",
    },
    "cpp": {
        "extension": "cpp",
        "compile": "g++ [sourcePath] -O2 -std=c++17 -fomit-frame-pointer -Wunused-result -o env/out"
        + ioeredirect,
        "execute": "./out [inputfile]",
    },
    "python": {
        "extension": "py",
        "execute": "python3 [sourcePath] [inputfile]",
        "compile": "python3 -m py_compile [sourcePath]" + ioeredirect,
    },
}
