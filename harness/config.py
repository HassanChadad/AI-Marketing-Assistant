MODEL_NAME = "llama3.2"
MAX_REVISIONS = 5 

SEO_THRESHOLDS = {
    "blog": {
        "min_density": 1.0,
        "max_density": 2.0,
        "min_readability": 60,
    },
    "linkedin": {
        "min_density": 0.5,
        "max_density": 3.0,
        "min_readability": 50,
    },
    "instagram": {
        "min_density": 0.3,   # very short captions, keyword may appear once or not at all naturally
        "max_density": 4.0,   # hashtags can inflate density, more tolerance needed
        "min_readability": 40, # casual, fragment-heavy, emoji-laden text scores low but is intentional
    },
}