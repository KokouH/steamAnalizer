
from typing import List, Dict

class Validator:
    def __init__(self, confidens: List) -> None:
        self.confidens = list(confidens)

    def validate(self, data: Dict) -> bool:
        '''
        data - {
            'history': [[datetime.datetime, float, int], ...],
            'histogram': {
                'buy_orders': [...],
                'sell_orders': [...]
            }
        }
        '''
        for conf in self.confidens:
            if not conf(data):
                print(f"Fail on {conf.__name__}")
                return False

        return True