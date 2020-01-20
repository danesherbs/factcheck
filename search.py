import requests
from secrets import MICROSOFT_ACADEMIC_API_KEY


def get_search_query(query, academics):
    exact_matches = [f"\"{a}\"" for a in academics]
    return f"{query} AND ({' OR '.join(exact_matches)})"


def get_top_level_topics(count=100):
    """
    e.g. get_top_level_topics()
    """

    params = {
        "expr": "FL=0",
        "attributes": "DFN,CC",
        "count": count,
        "orderby": "CC:desc"
    }

    payload = query_knowledge_graph(params, 'evaluate')

    topics = [topic["DFN"] for topic in payload["entities"]]

    return sorted(topics)


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

    payload = query_knowledge_graph(params, 'evaluate')

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

    payload = query_knowledge_graph(params, 'calchistogram')

    return [author["value"] for author in payload["histograms"][0]["histogram"]]


def query_knowledge_graph(params, service):
    url = f"https://api.labs.cognitive.microsoft.com/academic/v1.0/{service}?"
    headers = {"Ocp-Apim-Subscription-Key": MICROSOFT_ACADEMIC_API_KEY}
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()
