ioerr = " 2>[env]/error.txt"
version = 1
langarr = {
    "c": {
        "extension": "c",
        "compile": "gcc [sourcePath] -O2 -std=c17 -fomit-frame-pointer -Wunused-result -o [binPath]"
        + ioerr,
        "execute": "[binPath] [ioRedirect]",
        "timeFactor": 1,
    },
    "cpp": {
        "extension": "cpp",
        "compile": "g++ [sourcePath] -O2 -std=c++17 -fomit-frame-pointer -Wunused-result -o [binPath]"
        + ioerr,
        "execute": "[binPath] [ioRedirect]",
        "timeFactor": 1,
    },
    "python": {
        "extension": "py",
        "compile": "python3 -m py_compile [sourcePath]" + ioerr,
        "execute": "[uBin]python3 [sourcePath] [ioRedirect]",
        "timeFactor": 5,
    },
}
