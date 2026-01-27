# 🌾 FarmDirect - Farmer to Consumer Marketplace

## Overview
FarmDirect is a comprehensive web-based marketplace platform that connects farmers directly with consumers, eliminating middlemen and ensuring fair prices for both parties. Built with Python and Streamlit, it provides an intuitive interface for farmers to sell their crops and for consumers to purchase fresh produce directly from the source.

## 🚀 Features

### For Farmers 👨‍🌾
- **Product Management**: Add, edit, and delete crop listings with images
- **Inventory Control**: Real-time inventory tracking and updates
- **Order Management**: View and manage incoming orders
- **Sales Analytics**: Track total products, orders, and revenue
- **Fertilizer Recommendation**: AI-powered fertilizer suggestions based on soil and crop data
- **Direct Communication**: Contact information shared with buyers

### For Consumers 🛒
- **Product Browsing**: Browse all available products with search and filter
- **Shopping Cart**: Add multiple items and manage quantities
- **Order Placement**: Easy checkout with delivery details
- **Order Tracking**: Track order status from pending to delivered
- **Product Reviews**: Rate and review purchased products
- **Profile Management**: Update personal information and delivery addresses

### Platform Features 🌟
- **Multi-Role Authentication**: Separate interfaces for farmers and consumers
- **Secure Login System**: Password hashing with SHA256
- **SQLite Database**: Lightweight, efficient data storage
- **Image Upload**: Support for product images
- **Responsive Design**: Modern, user-friendly interface
- **Real-time Updates**: Instant inventory and order status updates

## 📁 Project Structure

```
/vercel/sandbox/
├── marketplace_app.py              # Main application entry point
├── database.py                     # Database operations and schema
├── farmer_dashboard.py             # Farmer interface and features
├── consumer_interface.py           # Consumer interface and features
├── fertilizer_recommendation.py    # ML-based fertilizer tool
├── marketplace.db                  # SQLite database (auto-created)
├── static/
│   └── uploads/                    # Product images directory
├── fertilizer_model.joblib         # ML model files
├── fertilizer_scaler.joblib
├── fertilizer_label_encoder.joblib
├── fertilizer_feature_columns.joblib
├── requirements.txt                # Python dependencies
└── README_MARKETPLACE.md           # This file
```

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Steps

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Run the Application**
```bash
streamlit run marketplace_app.py
```

3. **Access the Platform**
- Open your browser and navigate to `http://localhost:8501`
- The database will be automatically initialized on first run

## 📊 Database Schema

### Users Table
- Stores farmer, consumer, and admin accounts
- Fields: id, username, email, password (hashed), role, full_name, phone, address

### Products Table
- Stores crop listings from farmers
- Fields: id, farmer_id, name, category, description, price, unit, quantity_available, image_path

### Orders Table
- Stores customer orders
- Fields: id, consumer_id, total_amount, status, delivery_address, phone

### Order Items Table
- Stores individual items in each order
- Fields: id, order_id, product_id, farmer_id, quantity, price_per_unit, subtotal

### Cart Table
- Stores shopping cart items for consumers
- Fields: id, consumer_id, product_id, quantity

### Reviews Table
- Stores product reviews and ratings
- Fields: id, product_id, consumer_id, rating, comment

## 🎯 User Workflows

### Farmer Workflow
1. Register as a farmer
2. Login to access farmer dashboard
3. Add products with details and images
4. Manage inventory and pricing
5. View and process incoming orders
6. Use fertilizer recommendation tool
7. Track sales analytics

### Consumer Workflow
1. Register as a consumer
2. Login to access marketplace
3. Browse and search for products
4. Add items to shopping cart
5. Proceed to checkout
6. Place order with delivery details
7. Track order status
8. Leave reviews for products

## 🔐 Security Features

- **Password Hashing**: SHA256 encryption for all passwords
- **Session Management**: Secure session handling with Streamlit
- **Role-Based Access**: Separate interfaces for different user types
- **Input Validation**: Server-side validation for all forms
- **SQL Injection Prevention**: Parameterized queries throughout

## 🌱 Fertilizer Recommendation Tool

The platform includes an integrated ML-based fertilizer recommendation system that helps farmers:
- Analyze soil conditions (pH, moisture, nutrients)
- Get crop-specific recommendations
- Receive top 3 fertilizer suggestions with confidence scores
- Understand nutrient status (N, P, K levels)

## 📈 Future Enhancements

- Payment gateway integration
- Real-time chat between farmers and consumers
- Mobile app version
- Advanced analytics dashboard
- Multi-language support
- Delivery tracking with GPS
- Bulk order discounts
- Seasonal crop predictions
- Weather integration
- Community forum

## 🤝 Contributing

This is an open-source project. Contributions are welcome!

## 📝 License

This project is open-source and available for educational and commercial use.

## 👥 Support

For issues, questions, or suggestions, please create an issue in the repository.

## 🎉 Getting Started

### Quick Start Guide

1. **First Time Setup**
   - Run the application
   - Click "Register Now"
   - Choose your role (Farmer or Consumer)
   - Fill in your details
   - Login with your credentials

2. **As a Farmer**
   - Navigate to "Add Product" tab
   - Fill in crop details
   - Upload an image (optional)
   - Set price and quantity
   - Click "Add Product"

3. **As a Consumer**
   - Browse available products
   - Click "Add to Cart"
   - Go to "My Cart" tab
   - Enter delivery details
   - Click "Place Order"

## 🌟 Key Benefits

### For Farmers
- **Higher Profits**: No middlemen means better margins
- **Direct Market Access**: Reach consumers directly
- **Inventory Control**: Manage stock efficiently
- **Fair Pricing**: Set your own prices
- **Value-Added Tools**: Free fertilizer recommendations

### For Consumers
- **Fresh Produce**: Direct from farm
- **Fair Prices**: No middlemen markup
- **Transparency**: Know your farmer
- **Quality Assurance**: Direct communication
- **Support Local**: Help local farmers

## 📞 Contact

For more information or support, please reach out through the platform's contact features.

---

**Built with ❤️ for farmers and consumers**
