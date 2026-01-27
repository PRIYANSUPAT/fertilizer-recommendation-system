# 🚀 FarmDirect Marketplace - Quick Start Guide

## What is FarmDirect?

FarmDirect is a web-based marketplace that connects farmers directly with consumers, eliminating middlemen and ensuring fair prices for both parties. Farmers can list their crops, manage inventory, and receive orders directly. Consumers can browse fresh produce, add items to cart, and purchase directly from farmers.

## ⚡ Quick Start (3 Steps)

### Step 1: Install Dependencies
```bash
pip install streamlit pandas numpy scikit-learn imbalanced-learn joblib pillow
```

Or use the requirements file:
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
streamlit run marketplace_app.py
```

Or use the startup script:
```bash
./run_marketplace.sh
```

### Step 3: Access the Platform
- Open your browser and go to: **http://localhost:8501**
- The application will automatically open in your default browser

## 🎯 Test Accounts

The test script creates sample accounts you can use:

**Farmer Account:**
- Username: `testfarmer`
- Password: `pass123`

**Consumer Account:**
- Username: `testconsumer`
- Password: `pass123`

## 📋 Features Overview

### For Farmers 👨‍🌾
1. **Dashboard**: View statistics (products, orders, revenue)
2. **My Products**: Manage your crop listings
3. **Add Product**: List new crops with images
4. **Orders**: View and manage customer orders
5. **Fertilizer Tool**: Get AI-powered fertilizer recommendations

### For Consumers 🛒
1. **Browse Products**: Search and filter available crops
2. **My Cart**: Manage shopping cart
3. **My Orders**: Track order status
4. **Profile**: Update delivery information

## 🔄 Complete User Journey

### As a Farmer:
1. Register → Choose "farmer" role
2. Login with credentials
3. Go to "Add Product" tab
4. Fill in crop details (name, category, price, quantity)
5. Upload product image (optional)
6. Click "Add Product"
7. View orders in "Orders" tab
8. Update order status as you process them

### As a Consumer:
1. Register → Choose "consumer" role
2. Login with credentials
3. Browse available products
4. Click "Add to Cart" for desired items
5. Go to "My Cart" tab
6. Enter delivery address and phone
7. Click "Place Order"
8. Track order in "My Orders" tab

## 🧪 Testing the Platform

Run the comprehensive test suite:
```bash
python3 test_marketplace.py
```

This will test:
- ✓ User registration and authentication
- ✓ Product creation and management
- ✓ Shopping cart operations
- ✓ Order placement and tracking
- ✓ Reviews and ratings
- ✓ Search and filtering
- ✓ Farmer statistics

## 📁 Project Structure

```
marketplace_app.py              # Main application (START HERE)
database.py                     # Database operations
farmer_dashboard.py             # Farmer interface
consumer_interface.py           # Consumer interface
fertilizer_recommendation.py    # ML fertilizer tool
test_marketplace.py             # Test suite
run_marketplace.sh              # Startup script
marketplace.db                  # SQLite database (auto-created)
static/uploads/                 # Product images
```

## 🛠️ Troubleshooting

### Issue: "Module not found" error
**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: "Database locked" error
**Solution:** Close any other instances of the app and restart

### Issue: Images not displaying
**Solution:** Ensure the `static/uploads/` directory exists and has write permissions

### Issue: Port 8501 already in use
**Solution:** Stop other Streamlit apps or use a different port:
```bash
streamlit run marketplace_app.py --server.port 8502
```

## 🎨 Customization

### Change Database Location
Edit `database.py`:
```python
DATABASE_PATH = "your_custom_path.db"
```

### Add More Product Categories
Edit the category lists in:
- `farmer_dashboard.py` (line ~95)
- `consumer_interface.py` (line ~25)

### Modify Styling
Edit CSS in `marketplace_app.py` (lines 15-50)

## 📊 Database Schema

The platform uses SQLite with these tables:
- **users**: Farmer and consumer accounts
- **products**: Crop listings
- **orders**: Customer orders
- **order_items**: Individual items in orders
- **cart**: Shopping cart items
- **reviews**: Product reviews and ratings

## 🔐 Security Features

- ✓ Password hashing (SHA256)
- ✓ Session management
- ✓ Role-based access control
- ✓ SQL injection prevention
- ✓ Input validation

## 📈 Next Steps

1. **Add Real Payment Integration**: Integrate Razorpay, Stripe, or PayPal
2. **Enable Notifications**: Email/SMS for order updates
3. **Add Delivery Tracking**: GPS-based delivery tracking
4. **Mobile App**: Create mobile version with React Native
5. **Analytics Dashboard**: Advanced reporting for farmers

## 💡 Tips

- **For Farmers**: Add detailed descriptions and high-quality images to attract more buyers
- **For Consumers**: Check farmer ratings and reviews before purchasing
- **Use Fertilizer Tool**: Farmers can get free AI-powered fertilizer recommendations
- **Update Inventory**: Keep product quantities updated to avoid overselling

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the full documentation in `README_MARKETPLACE.md`
3. Run the test suite to verify functionality

## 🎉 Success!

If you can see the login page at http://localhost:8501, you're all set! 

**Happy Farming! 🌾**
