import re
from ai.agent_categories import AGENT_CATEGORIES


class IntentClassifier:
    def classify(self, message: str) -> dict:
        message = message.lower()

        # tokenize words safely
        words = re.findall(r"\b\w+\b", message)

        # greetings (whole-word match)
        if any(word in words for word in ["hi", "hello", "hey"]):
            return {"intent": "greeting", "category": None}

        # farewell
        if any(word in words for word in ["bye", "goodbye"]):
            return {"intent": "farewell", "category": None}

        # domain/category detection
        for category, cfg in AGENT_CATEGORIES.items():
            if any(keyword in words for keyword in cfg["keywords"]):
                return {"intent": "domain_query", "category": category}

        return {"intent": "general", "category": "general"}
