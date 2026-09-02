from typing import List, Dict, Any, Optional

class CartTools:
    """Cart management and pricing calculation tools."""

    @staticmethod
    def add_to_cart(cart: List[Dict[str, Any]], product: Dict[str, Any], quantity: int = 1) -> List[Dict[str, Any]]:
        """Add a product or increment its quantity in the cart."""
        existing = next((item for item in cart if item["product_id"] == product["product_id"]), None)
        if existing:
            existing["quantity"] += quantity
            existing["subtotal"] = round(existing["quantity"] * float(existing["price"]), 2)
        else:
            price = float(product.get("price", 0.0))
            cart.append({
                "product_id": product["product_id"],
                "product_name": product.get("product_name", "Unknown Product"),
                "category": product.get("category", ""),
                "price": price,
                "quantity": quantity,
                "subtotal": round(price * quantity, 2),
                "image_url": product.get("image_url", "")
            })
        return cart

    @staticmethod
    def remove_from_cart(cart: List[Dict[str, Any]], product_id: str) -> List[Dict[str, Any]]:
        """Remove an item completely from the cart."""
        return [item for item in cart if item["product_id"] != product_id]

    @staticmethod
    def update_quantity(cart: List[Dict[str, Any]], product_id: str, quantity: int) -> List[Dict[str, Any]]:
        """Update item quantity or remove if quantity <= 0."""
        if quantity <= 0:
            return CartTools.remove_from_cart(cart, product_id)
        
        for item in cart:
            if item["product_id"] == product_id:
                item["quantity"] = quantity
                item["subtotal"] = round(quantity * float(item["price"]), 2)
                break
        return cart

    @staticmethod
    def calculate_cart_total(
        cart: List[Dict[str, Any]],
        tax_rate: float = 0.0, # Gross prices already include GST in standard Indian retail
        discount_amount: float = 0.0,
        shipping_fee: float = 0.0
    ) -> Dict[str, Any]:
        """
        Calculate total cart breakdown including items count, subtotal,
        taxes, discounts, and final payable total.
        """
        subtotal = sum(float(item.get("subtotal", 0.0)) for item in cart)
        item_count = sum(int(item.get("quantity", 1)) for item in cart)

        tax_amount = round(subtotal * tax_rate, 2)
        discount = min(subtotal, float(discount_amount))
        
        # Free delivery on orders > ₹1,000
        delivery = 0.0 if (subtotal > 1000 or subtotal == 0) else float(shipping_fee or 99.0)
        total = round(subtotal + tax_amount + delivery - discount, 2)

        return {
            "item_count": item_count,
            "subtotal": round(subtotal, 2),
            "tax_amount": tax_amount,
            "shipping_fee": delivery,
            "discount_amount": round(discount, 2),
            "total_payable": total,
            "currency": "INR",
            "currency_symbol": "₹",
            "items": cart
        }

    @staticmethod
    def clear_cart() -> List[Dict[str, Any]]:
        """Return an empty cart."""
        return []

cart_tools = CartTools()
