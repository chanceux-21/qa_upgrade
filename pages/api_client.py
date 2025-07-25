import requests
import os
from dotenv import load_dotenv

load_dotenv()

class ATIAPIClient:
    def __init__(self):
        self.base_url = "https://api.ati.su/v1"
        self.token = os.getenv("ATI_API_TOKEN")
        
    def _get_headers(self):
        return {"Authorization": f"Bearer {self.token}"}
    
    def search_cargo(self, params: dict):
        response = requests.post(
            f"{self.base_url}/cargo/search",
            json=params,
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def get_cargo_details(self, cargo_id: str):
        response = requests.get(
            f"{self.base_url}/cargo/{cargo_id}",
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def create_test_cargo(self, cargo_data: dict):
        """Создание тестового груза (только для тестовой среды)"""
        response = requests.post(
            f"{self.base_url}/sandbox/cargos",
            json=cargo_data,
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()