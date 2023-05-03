"""
https://pypi.org/project/rule-engine/

https://zerosteiner.github.io/rule-engine/

"""


import rule_engine

# RULE MAKING
rule = rule_engine.Rule('first_name == "Luke" and email =~ ".*@rebels.org$"')


# TEST SCENARIO 1
result1 = rule.matches(
    {"first_name": "Luke", "last_name": "Skywalker", "email": "luke@rebels.org"}
)


# TEST SCENARIO 2
result2 = rule.matches(
    {"first_name": "Darth", "last_name": "Vader", "email": "dvader@empire.net"}
)


print(f"result1 - {result1}")
print(f"result2 - {result2}")


##### comic validation rules  ######

import datetime

comics = [
    {
        "title": "Batman",
        "publisher": "DC",
        "issue": 89,
        "released": datetime.date(2020, 4, 28),
    },
    {
        "title": "Flash",
        "publisher": "DC",
        "issue": 753,
        "released": datetime.date(2020, 5, 5),
    },
    {
        "title": "Captain Marvel",
        "publisher": "Marvel",
        "issue": 18,
        "released": datetime.date(2020, 6, 6),
    },
]

# RULE 1 - To match records that have publisher as `DC`
rule1 = rule_engine.Rule(
    # match books published by DC
    'publisher == "DC"'
)

# RULE 2 -
rule2 = rule_engine.Rule(
    # match DC books released in May 2020
    'released >= d"2020-05-01" and released < d"2020-06-01" and publisher == "DC"'
)


output1 = rule1.matches(comics[0])


# filter the iterable "comics" and return matching objects
output2 = rule2.filter(comics)

for comic in output2:
    print(comic)

breakpoint()


"""
Example trader mandate rule  `experience > 10 and trader_rating > 5 and client == "platinum"`

Trade 

```

    {
        "security": "",
        "jurisdiction": "IN",
        "trader_category": "",
        "volume": "",
        "min_price": "",
        "closure_timestamp": ""
    }
```




CJMRules

{"rule_id": 1111, rule_text="experience > 10 and trader_rating > 5 and client == "platinum""}



TMRules

{"rule_id": 1111, rule_text="experience > 10 and trader_rating > 5 and client == "platinum""}


"""
