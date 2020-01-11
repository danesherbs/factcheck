import requests
from secrets import MICROSOFT_ACADEMIC_API_KEY


def get_search_query(query, academics):
    exact_matches = [f"\"{a}\"" for a in academics]
    academics_or = " OR ".join(exact_matches)
    return f"{query} AND ({academics_or})"


def get_academics(query, count=10):
    calchistogram_url = "https://api.labs.cognitive.microsoft.com/academic/v1.0/calchistogram?"

    params = {
        "expr": _interpret_query(query),
        "attributes": "AA.DAuN",
        "count": count,
    }

    headers = {
        "Ocp-Apim-Subscription-Key": MICROSOFT_ACADEMIC_API_KEY,
    }

    response = requests.get(
            calchistogram_url,
            params=params,
            headers=headers,
    )

    response.raise_for_status()
    payload = response.json()

    return [item["value"] for item in payload["histograms"][0]["histogram"]]


def _interpret_query(query):
    interpret_url = "https://api.labs.cognitive.microsoft.com/academic/v1.0/interpret?"

    params = {
        "query": query,
        "count": 1,
    }

    headers = {
        "Ocp-Apim-Subscription-Key": MICROSOFT_ACADEMIC_API_KEY,
    }

    response = requests.get(
            interpret_url,
            params=params,
            headers=headers,
        )

    response.raise_for_status()
    payload = response.json()

    return payload["interpretations"][0]["rules"][0]["output"]["value"]
