import re
from datetime import datetime
from typing import List, Dict, Union, Optional

# --- Custom Exceptions ---
class InventoryError(Exception):
    """Sollevata per problemi di magazzino."""
    pass

class PaymentError(Exception):
    """Sollevata per problemi di pagamento."""
    pass

class FraudDetectedError(PaymentError):
    """Sollevata se viene rilevata una frode specifica."""
    pass

class UserValidationError(Exception):
    """Sollevata se i dati utente non sono validi."""
    pass


# --- Complex Components ---

class Warehouse:
    def __init__(self, initial_stock: Dict[str, int]):
        self._stock = initial_stock
        self._locked_stock = {}

    def check_stock(self, item_id: str, quantity: int) -> bool:
        if item_id not in self._stock:
            raise InventoryError(f"Item {item_id} not found in warehouse.")
        
        available = self._stock[item_id] - self._locked_stock.get(item_id, 0)
        return available >= quantity

    def lock_item(self, item_id: str, quantity: int):
        if not self.check_stock(item_id, quantity):
            raise InventoryError(f"Insufficient stock for {item_id}")
        
        self._locked_stock[item_id] = self._locked_stock.get(item_id, 0) + quantity

    def release_item(self, item_id: str, quantity: int):
        if item_id in self._locked_stock:
            self._locked_stock[item_id] -= quantity
            if self._locked_stock[item_id] <= 0:
                del self._locked_stock[item_id]


class DiscountEngine:
    @staticmethod
    def calculate_discount(total_amount: float, user_tier: str, promo_code: Optional[str] = None) -> float:
        """
        Calcola lo sconto basandosi su orario, tier utente e codici promozionali oscuri.
        """
        discount = 0.0
        
        # TRAPPOLA 1: Dipendenza temporale (datetime.now)
        # L'agente deve mockare datetime per testare questo ramo
        current_hour = datetime.now().hour
        if 0 <= current_hour < 6:
            # Sconto notturno "NightOwl"
            discount += 0.05

        # Logica Tier
        if user_tier == "GOLD":
            discount += 0.10
        elif user_tier == "PLATINUM":
            discount += 0.20
            # TRAPPOLA 2: Condizione annidata complessa su float
            if total_amount > 1000.00:
                discount += 0.05
        
        # Logica Promo Code (Magic Strings)
        if promo_code:
            # TRAPPOLA 3: Regex per validare il promo code
            # Formato: 3 lettere maiuscole, trattino, 3 numeri (es. "ABC-123")
            if re.match(r"^[A-Z]{3}-\d{3}$", promo_code):
                # Se il codice finisce con '999', è un super sconto
                if promo_code.endswith("999"):
                    return total_amount * 0.50  # 50% off immediato, ignora il resto
                discount += 0.10
            else:
                raise ValueError("Invalid promo code format")

        # Cap allo sconto massimo del 40% (tranne per il codice 999)
        return min(discount, 0.40)


class OrderProcessor:
    def __init__(self, warehouse: Warehouse):
        self.warehouse = warehouse
        self.tax_rate = 0.22

    def validate_user(self, email: str, age: int):
        # TRAPPOLA 4: Regex email RFC complessa
        # Se l'agente usa una email semplice tipo "test@test", potrebbe fallire qui se la regex è strict
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(email_regex, email):
            raise UserValidationError("Invalid email format")
        
        if age < 18:
            raise UserValidationError("User must be 18+")
        
        # Edge case: Utenti over 100 richiedono verifica manuale (simulata da errore)
        if age > 100:
            raise UserValidationError("Age verification required for 100+")

    def process_order(self, order_id: str, user_data: Dict, items: List[Dict[str, Union[str, int, float]]], promo_code: Optional[str] = None) -> Dict:
        """
        Il metodo principale da testare.
        Richiede un setup complesso di mock per Warehouse e gestione eccezioni multiple.
        """
        
        # 1. Validazione
        self.validate_user(user_data.get("email", ""), user_data.get("age", 0))

        # 2. Controllo Magazzino e Locking
        total_price = 0.0
        processed_items = []

        try:
            for item in items:
                i_id = str(item["id"])
                qty = int(item["qty"])
                price = float(item["price"])
                
                # TRAPPOLA 5: Divisione per zero nascosta
                # Se price è 0 e quantity è negativo (ritorno merce?), logica strana
                if qty < 0 and price == 0:
                    raise ValueError("Cannot return free items")

                self.warehouse.lock_item(i_id, qty)
                processed_items.append((i_id, qty))
                total_price += price * qty

        except InventoryError as e:
            # Rollback: Rilasciare tutto ciò che era stato lockato finora
            for p_id, p_qty in processed_items:
                self.warehouse.release_item(p_id, p_qty)
            return {"status": "failed", "reason": f"Out of stock: {str(e)}"}

        # 3. Calcolo Sconti
        try:
            discount_percent = DiscountEngine.calculate_discount(
                total_price, 
                user_data.get("tier", "STANDARD"), 
                promo_code
            )
        except ValueError as e:
            # Se il promo code è invalido, procediamo senza sconto ma logghiamo (simulato) o falliamo?
            # Qui decidiamo di fallire l'ordine
            for p_id, p_qty in processed_items:
                self.warehouse.release_item(p_id, p_qty)
            return {"status": "error", "reason": f"Promo Error: {str(e)}"}

        final_price = total_price * (1 - discount_percent)
        
        # 4. Applicazione Tasse (Floating point math)
        final_price_with_tax = final_price * (1 + self.tax_rate)
        
        # Arrotondamento bancario a 2 decimali
        final_price_with_tax = round(final_price_with_tax, 2)

        # 5. Simulazione Pagamento
        payment_method = user_data.get("payment_method", "CC")
        
        if payment_method == "PAYPAL":
            # Simuliamo che PayPal fallisce se l'importo è esattamente 666.66 (Evil number edge case)
            if final_price_with_tax == 666.66:
                raise FraudDetectedError("Suspicious transaction amount")
        
        elif payment_method == "CRYPTO":
            # Crypto non accettate per ordini sotto i 50 euro
            if final_price_with_tax < 50.0:
                raise PaymentError("Minimum crypto amount not met")

        return {
            "status": "success",
            "order_id": order_id,
            "original_price": total_price,
            "discount_applied": discount_percent,
            "final_total": final_price_with_tax,
            "items_count": len(items)
        }