from ai.controller.qwen_client import qwen_infer

ALLOWED_CATEGORIES = {
    "medical", "nutrition", "finance",
    "legal", "research", "interview", "general"
}


class QwenController:
    """
    Qwen-based orchestration controller.
    Handles intent classification and routing.
    """

    def classify_intent(self, user_text: str) -> str:
        prompt = f"""
Classify the following user query into ONE category only:
medical, nutrition, finance, legal, research, interview, general

User query:
{user_text}

Return ONLY the category name.
"""
        raw = qwen_infer(prompt)
        category = raw.lower().strip().replace(".", "").replace(",", "")

        if category not in ALLOWED_CATEGORIES:
            category = "general"

        return category
