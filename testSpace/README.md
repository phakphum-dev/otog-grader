# How to test

## Prepare the test environment

### test codes

In the test directory (./testSpace), you have to create `codes` directory first, after that create directory with the same problem id as the problem you want to test, and put your code in it.

for example, if you want to test problem 1000, the folder structure should be like this:

```
testSpace
├── codes
│   └── 1000
│       └── main.cpp
│       └── cool.cpp
│       └── bruh.c
│       └── another one.py
│       └── ...
│   └── ...
└── README.md
```

### config the problem

you can config by modifying the `testCodeDB.ini.template` file, and rename it to `testCodeDB.ini`.

```ini
# you can add the other problems here
[1000]
# #testcase  (required)
TestCase = 10
# memory in mb
Memory = 256
# time in seconds
Time = 1

[13]
TestCase = 14
Time = 2
...
```

## Run the test

just use docker compose to run the test

```bash
docker compose -f docker-compose.test.yml up --build
```

## Result

the result will be in the `testSpace/logs` folder, the result file name is the the time that start testing. (file are in markdown format)