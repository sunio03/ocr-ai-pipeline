import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

class IngredientClassifier:
    def __init__(self, model_path):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_path, local_files_only=True
        )
        self.model.to(self.device)
        self.model.eval()
        self.labels = ["vegan", "vegetarian", "halal", "kosher"]
    
    def classify_batch(self, texts):
        """Classify multiple ingredients at once."""
        if not texts:
            return []
        
        inputs = self.tokenizer(texts, return_tensors="pt", truncation=True, padding=True).to(self.device)
        with torch.no_grad():
            logits = self.model(**inputs).logits
            probs = torch.sigmoid(logits).tolist()
        
        results = []
        for prob_list in probs:
            results.append({label: bool(round(prob)) for label, prob in zip(self.labels, prob_list)})
        return results


class ProductClassifier:
    def __init__(self, model_path):
        self.classifier = IngredientClassifier(model_path)
    
    def process_ingredients(self, ingredients, allergens):
        """
        Classify ingredients and allergens, return enhanced data.
        
        Returns:
        {
            "ingredients": [{"name": "flour", "vegan": True, ...}, ...],
            "allergens": [...],
            "product_classification": {"vegan": False, ...},
            "friendly_summary": "This product is vegetarian, halal, kosher friendly"
        }
        """
        all_items = ingredients + allergens
        if not all_items:
            return {
                "ingredients": [],
                "allergens": [],
                "product_classification": {label: False for label in self.classifier.labels},
                "friendly_summary": "No ingredients detected"
            }
        
        classifications = self.classifier.classify_batch(all_items)
        
        # Split results
        ingredient_results = []
        for name, classification in zip(ingredients, classifications[:len(ingredients)]):
            ingredient_results.append({"name": name, **classification})
        
        allergen_results = []
        for name, classification in zip(allergens, classifications[len(ingredients):]):
            allergen_results.append({"name": name, **classification})
        
        # Product-level: ALL items must be compatible
        product_classification = {label: True for label in self.classifier.labels}
        for classification in classifications:
            for label in self.classifier.labels:
                if not classification[label]:
                    product_classification[label] = False
        
        # Generate summary
        friendly_labels = [label for label, is_friendly in product_classification.items() if is_friendly]
        if friendly_labels:
            friendly_summary = f"This product is {', '.join(friendly_labels)} friendly"
        else:
            friendly_summary = "This product does not meet any specific dietary requirements"
        
        return {
            "ingredients": ingredient_results,
            "allergens": allergen_results,
            "product_classification": product_classification,
            "friendly_summary": friendly_summary
        }
