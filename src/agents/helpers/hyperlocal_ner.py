from typing import Dict, Any
from src.agents.api.hyperlocal_ner import call_hyperlocal_ner_api

class HyperlocalNERClassifier:
    def __init__(self, base_url: str = None):
        # O base_url é configurado via variável de ambiente na função call_hyperlocal_ner_api
        pass

    def extract_entities(self, text: str) -> Dict[str, Any]:
        """
        Extrai entidades nomeadas do texto usando a API Hyperlocal NER.
        
        Args:
            text (str): Texto a ser processado para extração de entidades
            
        Returns:
            Dict[str, Any]: Resposta contendo as entidades extraídas no formato padrão
        """
        
        # Usar a função já desenvolvida
        result = call_hyperlocal_ner_api(text)
        
        # Verificar se houve erro na API
        if "error" in result:
            return {
                "entities": {},
                "all_entities": [],
                "success": False,
                "error": result["error"],
                "message": result["message"]
            }
        
        # Processar o novo formato de payload da API        
        if result:
            # Extrair informações principais
            original_text = result.get("text", "")
            intention = result.get("intention", "UNKNOWN")
            entities_list = result.get("entities", [])
            entity_count = result.get("entity_count", 0)
            
            # Processar entidades individuais
            best_entities = {}
            for entity in entities_list:
                entity_type = entity.get("label", "UNKNOWN")
                entity_text = entity.get("text", "")
                confidence = entity.get("confidence", 0.0)
                start = entity.get("start", 0)
                end = entity.get("end", 0)
                converted_date = entity.get("converted_date", {})
                converted_time = entity.get("converted_time", {})
                
                # Se não temos essa entidade ou a nova tem maior confiança
                if entity_type not in best_entities or confidence > best_entities[entity_type]["confidence"]:
                    best_entities[entity_type] = {
                        "text": entity_text,
                        "confidence": confidence,
                        "start": start,
                        "end": end,
                        "converted_date": converted_date,
                        "converted_time": converted_time
                    }
            
            return {
                "entities": best_entities,
                "all_entities": entities_list,
                "original_text": original_text,
                "intention": intention,
                "identifier_count": entity_count,
                "success": True
            }
        else:
            return {
                "entities": {},
                "all_entities": [],
                "original_text": "",
                "intention": "UNKNOWN",
                "identifier_count": 0,
                "success": True
            }
