import re
from files import get_content

content = get_content("../definitions/", "acordo.sqlx")

def regex_validate():
    content = get_content("../definitions/", "acordo.sqlx")
    print(content)
    result = re.search('@@query_label', content)
    return result

def validate_query_label(content):
    result = re.search('@@query_label', content)
    if (result):
        print("Query label: OK")
    else:
        print("Query label: ERROR")
        return exit 

if __name__ == "__main__":
    print(regex_validate())

