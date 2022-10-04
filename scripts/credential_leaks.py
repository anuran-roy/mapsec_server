import requests
from typing import Optional, Any


def credential_leak_check(credential: str, check_type: Optional[str] = "auto") -> Any:
    """auto: Returns passwords, SHA-1 hashes, and sources given any username or email.
    sources: Returns sources given username or email.
    password: Returns how many times a given password has been leaked.
    domain: Returns passwords, SHA-1 hashes, and sources given any domain (Limited to 1000 results for security).
    dehash: Attempts to decrypt a given hash."""

    url = "https://breachdirectory.p.rapidapi.com/"

    check_types = ["auto", "sources", "password", "domain", "dehash"]
    if check_type not in check_types:
        check_type = "auto"

    query_string = {"func": check_type, "term": credential}

    headers = {
        "X-RapidAPI-Key": "08f9acebcamshe0023f4887789f9p1656fejsnada539d5937e",
        "X-RapidAPI-Host": "breachdirectory.p.rapidapi.com",
    }

    response = requests.request("GET", url, headers=headers, params=query_string)

    print(response.text)
    
    return eval(response.txt)
