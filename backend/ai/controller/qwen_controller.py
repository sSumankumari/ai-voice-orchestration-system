from ai.controller.qwen_client import qwen_infer

class QwenController:
    """
    Qwen-based orchestration controller.
    Handles intent classification and routing.
    """

    def classify_intent(self, user_text: str, agent_category: str = None) -> dict:
        """
        Classify user intent dynamically.
        
        Args:
            user_text: The user's message
            agent_category: Optional agent category for context-aware classification
            
        Returns:
            dict with 'category', 'subcategory', and 'confidence'
        """
        context = f"in the context of {agent_category}" if agent_category else ""
        
        prompt = f"""
Analyze the following user query and classify its intent {context}.

User query: {user_text}

Provide a JSON response with:
1. "category": The broad domain (e.g., medical, finance, education, technology, etc.)
2. "subcategory": Specific topic within that domain
3. "confidence": Your confidence level (high/medium/low)

Be flexible and creative with categories. Don't limit yourself to predefined options.

Return ONLY valid JSON.
"""
        raw = qwen_infer(prompt, extract_json=True)
        
        # Parse response
        try:
            result = eval(raw) if isinstance(raw, str) else raw
            return {
                "category": result.get("category", "general").lower().strip(),
                "subcategory": result.get("subcategory", "").lower().strip(),
                "confidence": result.get("confidence", "medium").lower()
            }
        except:
            # Fallback to simple text classification
            category = raw.lower().strip().replace(".", "").replace(",", "")
            return {
                "category": category if category else "general",
                "subcategory": "",
                "confidence": "low"
            }