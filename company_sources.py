# company_sources.py

# ----------------------------
# GREENHOUSE BOARDS
# ----------------------------
GREENHOUSE_BOARDS = [
    # Defense / Aerospace
    {"company_name": "Anduril",         "board_token": "andurilindustries"},
    {"company_name": "Sarcos Technology","board_token": "sarcos"},
    {"company_name": "Joby Aviation",   "board_token": "jobyaviation"},
    {"company_name": "Relativity Space","board_token": "relativityspace"},
    {"company_name": "Epirus",          "board_token": "epirus"},
    {"company_name": "Rebellion Defense","board_token": "rebelliondefense"},
    {"company_name": "Saildrone",       "board_token": "saildrone"},
    {"company_name": "Shield AI",       "board_token": "shieldai"},
    {"company_name": "Hermeus",         "board_token": "hermeus"},
    {"company_name": "Hadrian",         "board_token": "hadrian"},

    # Biomedical / Healthtech
    {"company_name": "Nuro",            "board_token": "nuro"},
    {"company_name": "Hinge Health",    "board_token": "hingehealth"},
    {"company_name": "Lyra Health",     "board_token": "lyrahealth"},
    {"company_name": "Omada Health",    "board_token": "omadahealth"},
    {"company_name": "Sword Health",    "board_token": "swordhealth"},

    # Robotics / Autonomy
    {"company_name": "Apptronik",       "board_token": "apptronik"},
    {"company_name": "Skydio",          "board_token": "skydio"},
    {"company_name": "Gecko Robotics", "board_token": "geckorobotics"},
    {"company_name": "Machina Labs",    "board_token": "machinalabs"},
    {"company_name": "Moog",            "board_token": "moog"},




# ----------------------------
# WORKDAY BOARDS
# ----------------------------
WORKDAY_SOURCES = [
    {
        "company_name": "L3Harris",
        "url": "https://l3harris.wd5.myworkdayjobs.com/wday/cxs/l3harris/External/jobs"
    },
    {
        "company_name": "BAE Systems",
        "url": "https://baesystems.wd3.myworkdayjobs.com/wday/cxs/baesystems/BAES_External/jobs"
    },
    {
        "company_name": "General Dynamics",
        "url": "https://generaldynamics.wd5.myworkdayjobs.com/wday/cxs/generaldynamics/External/jobs"
    },
    {
        "company_name": "Northrop Grumman",
        "url": "https://northropgrumman.wd1.myworkdayjobs.com/wday/cxs/northropgrumman/Northrop_Grumman_External_Site/jobs"
    },
    {
        "company_name": "Raytheon",
        "url": "https://raytheon.wd5.myworkdayjobs.com/wday/cxs/raytheon/RTX_Careers/jobs"
    },
    {
        "company_name": "Leidos",
        "url": "https://leidos.wd5.myworkdayjobs.com/wday/cxs/leidos/Leidos/jobs"
    },
    {
        "company_name": "SAIC",
        "url": "https://saic.wd5.myworkdayjobs.com/wday/cxs/saic/SAIC_External/jobs"
    },
    {
        "company_name": "Medtronic",
        "url": "https://medtronic.wd1.myworkdayjobs.com/wday/cxs/medtronic/MedtronicCareers/jobs"
    },
    {
        "company_name": "Johnson & Johnson",
        "url": "https://jnj.wd5.myworkdayjobs.com/wday/cxs/jnj/JnJJobs/jobs"
    },
    {
        "company_name": "Siemens Healthineers",
        "url": "https://siemens-healthineers.wd3.myworkdayjobs.com/wday/cxs/siemens-healthineers/Careers/jobs"
    },
]


# ----------------------------
# TARGET STATES (for filtering)
# Set to None to allow all states.
# ----------------------------
TARGET_STATES = ["NJ", "PA", "NY", "Remote"]
    # Tech / Software (high signal)
    {"company_name": "Palantir",            "board_token": "palantir"},
    {"company_name": "SpaceX",              "board_token": "spacex"},
    {"company_name": "OpenAI",              "board_token": "openai"},
    {"company_name": "Anyscale",            "board_token": "anyscale"},
    {"company_name": "Verkada",             "board_token": "verkada"},
    {"company_name": "Govini",              "board_token": "govini"},

    # Niche Defense / Dual-Use Startups
    {"company_name": "Vannevar Labs",       "board_token": "vannevarlabs"},
    {"company_name": "Kittyhawk",           "board_token": "kittyhawk"},
    {"company_name": "Sievert Larsen",      "board_token": "sievertlarsen"},
    {"company_name": "True Anomaly",        "board_token": "trueanomalyinc"},
    {"company_name": "Umbra",               "board_token": "umbra"},
    {"company_name": "Hawkeye 360",         "board_token": "hawkeye360"},
    {"company_name": "Slingshot Aerospace", "board_token": "slingshotaerospace"},
    {"company_name": "Cognitive Space",     "board_token": "cognitivespace"},
    {"company_name": "Apex Space",          "board_token": "apexspace"},
    {"company_name": "Ursa Major",          "board_token": "ursamajor"},
    {"company_name": "Firestorm Labs",      "board_token": "firestormlabs"},
    {"company_name": "Hyper Defense",       "board_token": "hyperdefense"},

    # Niche Biomedical / Neurotech
    {"company_name": "Kernel",              "board_token": "kernel"},
    {"company_name": "Neurosity",           "board_token": "neurosity"},
    {"company_name": "Synchron",            "board_token": "synchron"},
    {"company_name": "Motional",            "board_token": "motional"},
    {"company_name": "Proprio",             "board_token": "proprio"},
    {"company_name": "Avail Medsystems",    "board_token": "availmedsystems"},
    {"company_name": "Cadence",             "board_token": "cadencehealth"},
    {"company_name": "Hyperfine",           "board_token": "hyperfine"},

    # Niche Robotics / Embedded
    {"company_name": "Viam",                "board_token": "viam"},
    {"company_name": "Dusty Robotics",      "board_token": "dustyrobotics"},
    {"company_name": "Nuro",                "board_token": "nuro"},
    {"company_name": "Robust AI",           "board_token": "robustai"},
    {"company_name": "Covariant",           "board_token": "covariant"},
    {"company_name": "Dextrous Robotics",   "board_token": "dextrousrobotics"},
    {"company_name": "Symbotic",            "board_token": "symbotic"},
    {"company_name": "Mujoco / DeepMind",   "board_token": "deepmind"},
]