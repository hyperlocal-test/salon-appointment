import boto3
import os
import requests
import json
from typing import Dict, Any, Optional

class ComprehendIntentClassifier:
    def __init__(self, endpoint_arn: str, region_name: str = "us-east-1"):
        self.endpoint_arn = endpoint_arn
        self.client = boto3.client(
            "comprehend", 
            region_name=region_name,
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )

    def classify_intent(self, text: str):
        resp = self.client.classify_document(
            Text=text,
            EndpointArn=self.endpoint_arn
        )
        # resp["Classes"] é lista de dicts com Name, Score
        classes = resp.get("Classes", [])
        if not classes:
            return None
        # escolha a classe de maior score
        best = max(classes, key=lambda c: c["Score"])
        return {"intent": best["Name"], "score": best["Score"], "all": classes}