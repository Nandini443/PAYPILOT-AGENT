import os
import random
import json
import sqlite3
import pandas as pd
from datetime import datetime, timedelta

# Deterministic seed for reproducibility
SEED = 42
random.seed(SEED)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "paypilot.db")

def generate_products():
    products_data = [
        # Audio & Headphones
        {
            "product_id": "PROD-AUD-001",
            "product_name": "SonicPulse Pro Wireless ANC Headphones",
            "category": "Headphones",
            "price": 4799.0,
            "rating": 4.6,
            "review_count": 1420,
            "stock": 45,
            "brand": "SonicPulse",
            "features": json.dumps(["Active Noise Cancellation", "60 Hours Battery Life", "Bluetooth 5.3", "Fast Charging 10min=5hr", "Multipoint Connect", "Ultra-comfortable Memory Foam"]),
            "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&q=80"
        },
        {
            "product_id": "PROD-AUD-002",
            "product_name": "SoundMax Over-Ear Wireless 50H",
            "category": "Headphones",
            "price": 3899.0,
            "rating": 4.4,
            "review_count": 980,
            "stock": 60,
            "brand": "SoundMax",
            "features": json.dumps(["50 Hours Battery Life", "Deep Bass Boost", "Bluetooth 5.2", "Foldable Design", "Built-in Mic", "Voice Assistant Support"]),
            "image_url": "https://images.unsplash.com/photo-1583394838336-acd977736f90?w=500&q=80"
        },
        {
            "product_id": "PROD-AUD-003",
            "product_name": "AeroBeats Elite ANC Wireless",
            "category": "Headphones",
            "price": 4999.0,
            "rating": 4.5,
            "review_count": 1150,
            "stock": 30,
            "brand": "AeroBeats",
            "features": json.dumps(["Hybrid Active Noise Cancellation", "45 Hours Battery Life", "Low Latency Gaming Mode", "Transparency Mode", "Custom EQ App"]),
            "image_url": "https://images.unsplash.com/photo-1484704849700-f032a568e944?w=500&q=80"
        },
        {
            "product_id": "PROD-AUD-004",
            "product_name": "boAt Rockerz 550 Over-Ear",
            "category": "Headphones",
            "price": 1999.0,
            "rating": 4.1,
            "review_count": 5200,
            "stock": 120,
            "brand": "boAt",
            "features": json.dumps(["20 Hours Battery", "50mm Dynamic Drivers", "Physical Noise Isolation", "Bluetooth 5.0", "Plush Earpads"]),
            "image_url": "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=500&q=80"
        },
        {
            "product_id": "PROD-AUD-005",
            "product_name": "Sony WH-1000XM4 Flagship ANC",
            "category": "Headphones",
            "price": 22990.0,
            "rating": 4.8,
            "review_count": 3400,
            "stock": 18,
            "brand": "Sony",
            "features": json.dumps(["Industry-leading ANC", "30 Hours Battery Life", "Touch Sensor Controls", "Speak-to-Chat", "LDAC Hi-Res Audio"]),
            "image_url": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=500&q=80"
        },
        {
            "product_id": "PROD-AUD-006",
            "product_name": "JBL Tune 760NC Lightweight ANC",
            "category": "Headphones",
            "price": 4999.0,
            "rating": 4.3,
            "review_count": 890,
            "stock": 25,
            "brand": "JBL",
            "features": json.dumps(["Active Noise Cancelling", "35 Hours Battery with ANC", "JBL Pure Bass Sound", "Lightweight & Foldable"]),
            "image_url": "https://images.unsplash.com/photo-1577174881658-0f30ed549adc?w=500&q=80"
        },
        {
            "product_id": "PROD-AUD-007",
            "product_name": "boAt Airdopes 141 ANC TWS",
            "category": "Headphones",
            "price": 1499.0,
            "rating": 4.0,
            "review_count": 8400,
            "stock": 150,
            "brand": "boAt",
            "features": json.dumps(["42 Hours Playback", "ENx Tech Mic", "Low Latency Beast Mode", "IPX5 Sweat Resistance", "Type-C Fast Charge"]),
            "image_url": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=500&q=80"
        },
        {
            "product_id": "PROD-AUD-008",
            "product_name": "Sennheiser HD 450BT Wireless ANC",
            "category": "Headphones",
            "price": 7990.0,
            "rating": 4.5,
            "review_count": 670,
            "stock": 20,
            "brand": "Sennheiser",
            "features": json.dumps(["Active Noise Cancellation", "30 Hours Battery", "AAC and AptX Low Latency", "USB-C Fast Charging", "Podcast Mode"]),
            "image_url": "https://images.unsplash.com/photo-1545127398-14699f92334b?w=500&q=80"
        },
        {
            "product_id": "PROD-AUD-009",
            "product_name": "OnePlus Bullets Wireless Z2 ANC",
            "category": "Headphones",
            "price": 2299.0,
            "rating": 4.3,
            "review_count": 4100,
            "stock": 85,
            "brand": "OnePlus",
            "features": json.dumps(["45dB Hybrid ANC", "28 Hours Battery Life", "10 Min Charge for 20 Hours", "12.4mm Drivers", "IP55 Rating"]),
            "image_url": "https://images.unsplash.com/photo-1606220588913-b3aacb4d2f46?w=500&q=80"
        },
        {
            "product_id": "PROD-AUD-010",
            "product_name": "Realme Buds Air 5 Pro ANC",
            "category": "Headphones",
            "price": 4699.0,
            "rating": 4.4,
            "review_count": 1320,
            "stock": 40,
            "brand": "Realme",
            "features": json.dumps(["50dB Active Noise Cancellation", "40 Hours Playback", "Hi-Res Audio LDAC", "Spatial Audio Effect", "40ms Super Low Latency"]),
            "image_url": "https://images.unsplash.com/photo-1598331668826-20cecc596b86?w=500&q=80"
        },

        # Laptops & Computing
        {
            "product_id": "PROD-LAP-001",
            "product_name": "Lenovo IdeaPad Slim 3 15.6 Core i5",
            "category": "Laptops",
            "price": 48990.0,
            "rating": 4.3,
            "review_count": 640,
            "stock": 22,
            "brand": "Lenovo",
            "features": json.dumps(["Intel Core i5 12th Gen", "16GB DDR4 RAM", "512GB NVMe SSD", "FHD IPS Antiglare", "Backlit Keyboard", "Windows 11 Home", "Fast Charging"]),
            "image_url": "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=500&q=80"
        },
        {
            "product_id": "PROD-LAP-002",
            "product_name": "ASUS Vivobook 15 Ryzen 7 Thin & Light",
            "category": "Laptops",
            "price": 56990.0,
            "rating": 4.5,
            "review_count": 510,
            "stock": 16,
            "brand": "ASUS",
            "features": json.dumps(["AMD Ryzen 7 7730U", "16GB RAM", "512GB SSD", "Fingerprint Sensor", "180-degree Hinge", "Fast Charging 60% in 49min", "Great for Coding"]),
            "image_url": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=500&q=80"
        },
        {
            "product_id": "PROD-LAP-003",
            "product_name": "HP Pavilion 14 13th Gen Intel i5",
            "category": "Laptops",
            "price": 59990.0,
            "rating": 4.4,
            "review_count": 420,
            "stock": 14,
            "brand": "HP",
            "features": json.dumps(["Intel Core i5-1335U", "16GB DDR4 RAM", "512GB SSD", "Audio by B&O", "FHD Micro-edge Display", "Fast Charge", "Backlit Keyboard"]),
            "image_url": "https://images.unsplash.com/photo-1531297484001-80022131f5a1?w=500&q=80"
        },
        {
            "product_id": "PROD-LAP-004",
            "product_name": "Acer Aspire Lite AMD Ryzen 5",
            "category": "Laptops",
            "price": 38990.0,
            "rating": 4.2,
            "review_count": 310,
            "stock": 28,
            "brand": "Acer",
            "features": json.dumps(["AMD Ryzen 5 5500U", "16GB RAM", "512GB SSD", "Full HD Display", "Metal Cover", "1.59kg Light", "Student Friendly"]),
            "image_url": "https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=500&q=80"
        },
        {
            "product_id": "PROD-LAP-005",
            "product_name": "Apple MacBook Air M2 13.6-inch",
            "category": "Laptops",
            "price": 94900.0,
            "rating": 4.9,
            "review_count": 1820,
            "stock": 10,
            "brand": "Apple",
            "features": json.dumps(["Apple M2 Chip 8-core CPU", "8GB Unified Memory", "256GB SSD", "Liquid Retina Display", "18 Hours Battery Life", "MagSafe 3"]),
            "image_url": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=500&q=80"
        },
        {
            "product_id": "PROD-LAP-006",
            "product_name": "Dell Inspiron 3520 Intel i5 12th Gen",
            "category": "Laptops",
            "price": 49990.0,
            "rating": 4.3,
            "review_count": 480,
            "stock": 19,
            "brand": "Dell",
            "features": json.dumps(["Intel Core i5-1235U", "16GB RAM", "512GB SSD", "120Hz FHD Display", "ExpressCharge 80% in 60min", "Spill-resistant Keyboard"]),
            "image_url": "https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=500&q=80"
        },

        # Smartphones & Mobile
        {
            "product_id": "PROD-PHN-001",
            "product_name": "OnePlus Nord CE 4 5G 8GB/128GB",
            "category": "Smartphones",
            "price": 24999.0,
            "rating": 4.5,
            "review_count": 2100,
            "stock": 35,
            "brand": "OnePlus",
            "features": json.dumps(["Snapdragon 7 Gen 3", "100W SUPERVOOC Fast Charge", "5500mAh Battery", "50MP Sony LYT-600 OIS", "120Hz AMOLED"]),
            "image_url": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=500&q=80"
        },
        {
            "product_id": "PROD-PHN-002",
            "product_name": "Redmi Note 13 Pro 5G 8GB/256GB",
            "category": "Smartphones",
            "price": 23999.0,
            "rating": 4.3,
            "review_count": 3400,
            "stock": 40,
            "brand": "Xiaomi",
            "features": json.dumps(["200MP OIS Camera", "1.5K 120Hz Curved AMOLED", "Snapdragon 7s Gen 2", "67W Turbo Charge", "Corning Gorilla Glass Victus"]),
            "image_url": "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=500&q=80"
        },
        {
            "product_id": "PROD-PHN-003",
            "product_name": "Samsung Galaxy M34 5G 8GB/128GB",
            "category": "Smartphones",
            "price": 17499.0,
            "rating": 4.2,
            "review_count": 4800,
            "stock": 50,
            "brand": "Samsung",
            "features": json.dumps(["6000mAh Monster Battery", "120Hz Super AMOLED Display", "50MP No Shake Cam (OIS)", "4 Gen OS Upgrades"]),
            "image_url": "https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=500&q=80"
        },
        {
            "product_id": "PROD-PHN-004",
            "product_name": "Apple iPhone 15 128GB Black",
            "category": "Smartphones",
            "price": 71990.0,
            "rating": 4.8,
            "review_count": 2890,
            "stock": 15,
            "brand": "Apple",
            "features": json.dumps(["Dynamic Island", "48MP Main Camera 2x Telephoto", "A16 Bionic Chip", "USB-C Connector", "All-day Battery Life"]),
            "image_url": "https://images.unsplash.com/photo-1510557880182-3d4d3cba35a5?w=500&q=80"
        },
        {
            "product_id": "PROD-PHN-005",
            "product_name": "Motorola Edge 50 Fusion 5G",
            "category": "Smartphones",
            "price": 22999.0,
            "rating": 4.6,
            "review_count": 1850,
            "stock": 25,
            "brand": "Motorola",
            "features": json.dumps(["Sony LYTIA 700C Camera OIS", "144Hz 3D Curved pOLED", "IP68 Underwater Protection", "68W TurboPower", "Vegan Leather Finish"]),
            "image_url": "https://images.unsplash.com/photo-1580910051074-3eb694886505?w=500&q=80"
        },

        # Wearables & Smartwatches
        {
            "product_id": "PROD-WAT-001",
            "product_name": "Noise ColorFit Pro 5 Max AMOLED",
            "category": "Wearables",
            "price": 3499.0,
            "rating": 4.3,
            "review_count": 1650,
            "stock": 70,
            "brand": "Noise",
            "features": json.dumps(["1.96-inch AMOLED Display", "BT Calling with Tru Sync", "Emergency SOS", "100+ Sports Modes", "7 Days Battery Life"]),
            "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&q=80"
        },
        {
            "product_id": "PROD-WAT-002",
            "product_name": "Fire-Boltt Invincible Plus AMOLED Smartwatch",
            "category": "Wearables",
            "price": 4299.0,
            "rating": 4.4,
            "review_count": 1200,
            "stock": 40,
            "brand": "Fire-Boltt",
            "features": json.dumps(["1.43-inch AMOLED 60Hz", "4GB Inbuilt Storage for Music", "TWS Connection", "Bluetooth Calling", "300+ Sports Modes"]),
            "image_url": "https://images.unsplash.com/photo-1579586337278-3befd40fd17a?w=500&q=80"
        },
        {
            "product_id": "PROD-WAT-003",
            "product_name": "Apple Watch SE (2nd Gen) GPS 40mm",
            "category": "Wearables",
            "price": 27900.0,
            "rating": 4.7,
            "review_count": 1400,
            "stock": 12,
            "brand": "Apple",
            "features": json.dumps(["Crash Detection", "Heart Rate Tracking & Sleep Stages", "Retina OLED Display", "Water Resistant 50m"]),
            "image_url": "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=500&q=80"
        },
        {
            "product_id": "PROD-WAT-004",
            "product_name": "Amazfit GTS 4 Mini Smart Watch",
            "category": "Wearables",
            "price": 7999.0,
            "rating": 4.5,
            "review_count": 920,
            "stock": 28,
            "brand": "Amazfit",
            "features": json.dumps(["Ultra-slim 9.1mm Design", "15 Days Battery Life", "5 Satellite Positioning Systems", "120+ Sports Modes", "5 ATM Water Resistance"]),
            "image_url": "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=500&q=80"
        },

        # Footwear & Running Shoes
        {
            "product_id": "PROD-SHO-001",
            "product_name": "Puma Velocity Nitro 2 Running Shoes",
            "category": "Footwear",
            "price": 3799.0,
            "rating": 4.5,
            "review_count": 820,
            "stock": 35,
            "brand": "Puma",
            "features": json.dumps(["NITRO Foam Cushioning", "PUMAGRIP High-traction Rubber", "Engineered Mesh Upper", "Reflective Accents for Night Running"]),
            "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500&q=80"
        },
        {
            "product_id": "PROD-SHO-002",
            "product_name": "Nike Revolution 6 Next Nature Running Shoes",
            "category": "Footwear",
            "price": 3695.0,
            "rating": 4.4,
            "review_count": 1900,
            "stock": 48,
            "brand": "Nike",
            "features": json.dumps(["Soft Foam Midsole", "Breathable Mesh Design", "Reinforced Heel", "Flexible Rubber Outsole"]),
            "image_url": "https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=500&q=80"
        },
        {
            "product_id": "PROD-SHO-003",
            "product_name": "Adidas Duramo SL 2.0 Lightweight Running Shoes",
            "category": "Footwear",
            "price": 3299.0,
            "rating": 4.3,
            "review_count": 1340,
            "stock": 55,
            "brand": "Adidas",
            "features": json.dumps(["LIGHTMOTION Cushioning", "Sandwich Mesh Upper", "Supportive No-sew Overlays", "Adiwear Durable Outsole"]),
            "image_url": "https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?w=500&q=80"
        },
        {
            "product_id": "PROD-SHO-004",
            "product_name": "Asics Gel-Contend 8 Running Shoes",
            "category": "Footwear",
            "price": 3999.0,
            "rating": 4.6,
            "review_count": 670,
            "stock": 25,
            "brand": "Asics",
            "features": json.dumps(["Rearfoot GEL Technology Cushioning", "AmpliFoam Midsole", "Ortholite Sockliner", "Durable Synthetic Stitching"]),
            "image_url": "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=500&q=80"
        },

        # Accessories & Computer Peripherals
        {
            "product_id": "PROD-ACC-001",
            "product_name": "Logitech MX Master 3S Wireless Mouse",
            "category": "Accessories",
            "price": 8995.0,
            "rating": 4.8,
            "review_count": 2400,
            "stock": 30,
            "brand": "Logitech",
            "features": json.dumps(["Quiet Clicks", "8K DPI Any-Surface Tracking", "MagSpeed Electromagnetic Scrolling", "Ergonomic Sculpted Design", "Type-C Quick Charge"]),
            "image_url": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=500&q=80"
        },
        {
            "product_id": "PROD-ACC-002",
            "product_name": "Keychron K2 Wireless Mechanical Keyboard",
            "category": "Accessories",
            "price": 7499.0,
            "rating": 4.7,
            "review_count": 1100,
            "stock": 22,
            "brand": "Keychron",
            "features": json.dumps(["75% Compact Layout", "Gateron G Pro Mechanical Switches", "Bluetooth 5.1 & Type-C Wired", "Mac & Windows Layout", "RGB Backlight"]),
            "image_url": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=500&q=80"
        },
        {
            "product_id": "PROD-ACC-003",
            "product_name": "Anker 737 Power Bank 24,000mAh 140W",
            "category": "Accessories",
            "price": 10999.0,
            "rating": 4.7,
            "review_count": 890,
            "stock": 18,
            "brand": "Anker",
            "features": json.dumps(["140W High-Speed Charging", "Smart Digital Display", "Charges Laptops and Phones", "ActiveShield 2.0 Protection", "24,000mAh Capacity"]),
            "image_url": "https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?w=500&q=80"
        }
    ]
    return pd.DataFrame(products_data)

def generate_customers(n=300):
    locations = ["Bengaluru", "Mumbai", "Delhi NCR", "Hyderabad", "Pune", "Chennai", "Kolkata", "Ahmedabad"]
    age_groups = ["18-24", "25-34", "35-44", "45-54", "55+"]
    segments = ["High Value", "Budget Conscious", "Tech Enthusiast", "Bargain Hunter", "Regular"]

    customers = []
    for i in range(1, n + 1):
        cid = f"CUST-{i:04d}"
        loc = random.choice(locations)
        age = random.choices(age_groups, weights=[0.25, 0.40, 0.20, 0.10, 0.05])[0]
        seg = random.choices(segments, weights=[0.15, 0.30, 0.25, 0.15, 0.15])[0]
        
        if seg == "High Value":
            prev_orders = random.randint(8, 30)
            aov = round(random.uniform(8000, 35000), 2)
        elif seg == "Tech Enthusiast":
            prev_orders = random.randint(4, 18)
            aov = round(random.uniform(4000, 20000), 2)
        elif seg == "Budget Conscious":
            prev_orders = random.randint(1, 6)
            aov = round(random.uniform(1200, 4500), 2)
        elif seg == "Bargain Hunter":
            prev_orders = random.randint(2, 10)
            aov = round(random.uniform(800, 3000), 2)
        else:
            prev_orders = random.randint(2, 12)
            aov = round(random.uniform(2000, 7000), 2)

        customers.append({
            "customer_id": cid,
            "age_group": age,
            "location": loc,
            "customer_segment": seg,
            "previous_orders": prev_orders,
            "average_order_value": aov
        })
    return pd.DataFrame(customers)

def generate_orders_and_transactions(products_df, customers_df, n_orders=1500):
    end_date = datetime(2026, 9, 2)
    start_date = end_date - timedelta(days=90)
    
    orders = []
    transactions = []
    tx_counter = 1

    payment_methods = ["UPI", "Card", "Net Banking", "Wallet"]
    method_weights = [0.55, 0.25, 0.12, 0.08]

    failure_reasons = {
        "UPI": ["TIMEOUT", "BANK_DECLINED", "NETWORK_ERROR"],
        "Card": ["BANK_DECLINED", "INSUFFICIENT_FUNDS", "TIMEOUT", "INVALID_REQUEST"],
        "Net Banking": ["TIMEOUT", "BANK_DECLINED", "NETWORK_ERROR"],
        "Wallet": ["INSUFFICIENT_FUNDS", "NETWORK_ERROR"]
    }

    for i in range(1, n_orders + 1):
        order_id = f"ORD-{i:05d}"
        cust = customers_df.sample(n=1, random_state=SEED + i).iloc[0]
        cust_id = cust["customer_id"]

        random_seconds = random.randint(0, int((end_date - start_date).total_seconds()))
        ts = start_date + timedelta(seconds=random_seconds)
        ts_str = ts.strftime("%Y-%m-%d %H:%M:%S")

        selected_prod = products_df.sample(n=1, random_state=SEED + i).iloc[0]
        amount = float(selected_prod["price"])
        item = {
            "product_id": selected_prod["product_id"],
            "product_name": selected_prod["product_name"],
            "price": float(selected_prod["price"]),
            "quantity": 1
        }

        # Intentional synthetic pattern:
        # Orders > ₹3,000 have ~24% checkout abandonment vs ~13% for <= ₹3,000
        if amount > 3000:
            is_abandoned = (random.random() < 0.24)
        else:
            is_abandoned = (random.random() < 0.13)

        if is_abandoned:
            order_status = "ABANDONED"
            checkout_status = "ABANDONED"
            payment_status = "PENDING"
            orders.append({
                "order_id": order_id,
                "customer_id": cust_id,
                "timestamp": ts_str,
                "amount": amount,
                "order_status": order_status,
                "checkout_status": checkout_status,
                "payment_status": payment_status,
                "items_json": json.dumps([item])
            })
            continue

        checkout_status = "COMPLETED"
        method = random.choices(payment_methods, weights=method_weights)[0]
        device = random.choices(["Mobile", "Desktop", "Tablet"], weights=[0.68, 0.24, 0.08])[0]

        # Success rates per method:
        # UPI ~ 92%, Wallet ~ 89%, Card ~ 83%, Net Banking ~ 74%
        if method == "UPI":
            success_prob = 0.92
            proc_time = round(random.uniform(1.2, 4.5), 2)
        elif method == "Wallet":
            success_prob = 0.89
            proc_time = round(random.uniform(1.0, 3.8), 2)
        elif method == "Card":
            success_prob = 0.83
            proc_time = round(random.uniform(2.5, 7.5), 2)
        else: # Net Banking
            success_prob = 0.74
            proc_time = round(random.uniform(4.0, 14.2), 2)

        is_success = (random.random() < success_prob)

        if is_success:
            tx_status = "SUCCESS"
            order_payment_status = "SUCCESS"
            order_status = "COMPLETED"
            f_reason = "NONE"
        else:
            tx_status = "FAILED"
            order_payment_status = "FAILED"
            order_status = "CANCELLED"
            f_reason = random.choice(failure_reasons[method])

        tx_id = f"TXN-{tx_counter:06d}"
        tx_counter += 1

        transactions.append({
            "transaction_id": tx_id,
            "order_id": order_id,
            "customer_id": cust_id,
            "product_id": selected_prod["product_id"],
            "timestamp": ts_str,
            "amount": amount,
            "payment_method": method,
            "payment_status": tx_status,
            "failure_reason": f_reason,
            "processing_time": proc_time,
            "device_type": device
        })

        orders.append({
            "order_id": order_id,
            "customer_id": cust_id,
            "timestamp": ts_str,
            "amount": amount,
            "order_status": order_status,
            "checkout_status": checkout_status,
            "payment_status": order_payment_status,
            "items_json": json.dumps([item])
        })

    return pd.DataFrame(orders), pd.DataFrame(transactions)

def seed_all():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    print("Generating synthetic dataset...")
    products_df = generate_products()
    customers_df = generate_customers(300)
    orders_df, transactions_df = generate_orders_and_transactions(products_df, customers_df, 1500)

    # Save CSVs
    products_df.to_csv(os.path.join(DATA_DIR, "products.csv"), index=False)
    customers_df.to_csv(os.path.join(DATA_DIR, "customers.csv"), index=False)
    orders_df.to_csv(os.path.join(DATA_DIR, "orders.csv"), index=False)
    transactions_df.to_csv(os.path.join(DATA_DIR, "transactions.csv"), index=False)
    print("Saved CSV files to data/ folder.")

    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
        except Exception:
            pass

    from database.database import db
    db.init_db()

    with db.get_connection() as conn:
        products_df.to_sql("products", conn, if_exists="append", index=False)
        customers_df.to_sql("customers", conn, if_exists="append", index=False)
        orders_df.to_sql("orders", conn, if_exists="append", index=False)
        transactions_df.to_sql("transactions", conn, if_exists="append", index=False)

    print(f"Seeded SQLite database successfully at {DB_PATH}")
    print(f"Total Products: {len(products_df)}")
    print(f"Total Customers: {len(customers_df)}")
    print(f"Total Orders: {len(orders_df)}")
    print(f"Total Transactions: {len(transactions_df)}")

if __name__ == "__main__":
    seed_all()
