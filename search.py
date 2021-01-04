import os
import requests
from functools import lru_cache


def get_search_query(query, academics):
    exact_matches = [f'"{a}"' for a in academics]
    return f"{query} AND ({' OR '.join(exact_matches)})"


def get_top_level_topics(count=100):
    """
    e.g. get_top_level_topics()
    """

    params = {
        "expr": "FL=0",
        "attributes": "DFN,CC",
        "count": count,
        "orderby": "CC:desc",
    }

    payload = query_knowledge_graph(params, "evaluate")

    topics = [topic["DFN"] for topic in payload["entities"]]

    return sorted(topics)


@lru_cache(maxsize=30)
def get_child_topics(topic, count=500):
    """
    e.g. get_child_topics('biochemistry')
    """

    topic_normalised = topic.lower()

    params = {
        "expr": f"FN=='{topic_normalised}'",
        "attributes": "FC.FN",
        "count": count,
    }

    payload = query_knowledge_graph(params, "evaluate")

    topics = [topic["FN"] for topic in payload["entities"][0]["FC"]]

    return sorted(topics)


def get_academics(topic):
    """
    e.g. get_academics('restricted boltzmann machine')

    TODO: figure out how ranking works for calchistogram.
        Can we sort by number of citations?
    """

    topic_normalised = topic.lower()

    params = {
        "expr": f"Composite(F.FN='{topic_normalised}')",
        "attributes": "AA.AuN",
        "count": 10,
    }

    payload = query_knowledge_graph(params, "calchistogram")
    authors = [author["value"] for author in payload["histograms"][0]["histogram"]]

    return [remove_middle_name(author) for author in authors]


def remove_middle_name(name):
    split_names = name.split(" ")

    if len(split_names) == 3:
        return " ".join([split_names[0], split_names[2]])

    return name


def query_knowledge_graph(params, service):
    url = f"https://api.labs.cognitive.microsoft.com/academic/v1.0/{service}?"
    headers = {"Ocp-Apim-Subscription-Key": os.environ["MICROSOFT_ACADEMIC_API_KEY"]}
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()
