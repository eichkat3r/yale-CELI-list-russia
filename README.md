# yalelist

Script that fetches data from the [Yale List of over 1000 companies that have curtailed or still continue operations in Russia](https://som.yale.edu/story/2022/over-1000-companies-have-curtailed-operations-russia-some-remain), parses the HTML and converts it to machine-friendly JSON.

The JSON will have the following format:

```json
{
    "CATEGORY_1": {
        "description": "...",
        "grade": "[A-F]",
        "records": [
            {
                "name": "NAME_A",
                "action": "ACTION_A",
                "industry": "INDUSTRY_A",
                "country": "COUNTRY_A"
            },
            ...
        ]
    },
    ...
}
```

Please note that some fields in the records might be empty.

## Usage

First, run

```bash
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

to create a virtual environment with all requirements you'll need.
This step is optional if you have all requirements installed or if you prefer something other than virtualenv.

Then, run

```bash
python3 yalelist.py --output yalelist.json
```

to generate the full list as json.