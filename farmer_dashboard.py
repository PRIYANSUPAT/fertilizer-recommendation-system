import streamlit as st
import database as db
from PIL import Image
import os
from datetime import datetime

def show_farmer_dashboard(user):
    """Farmer dashboard for managing crops and viewing orders"""
    
    st.markdown(f"## 👨‍🌾 Welcome, {user['full_name']}!")
    st.markdown("---")
    
    # Tabs for different sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Dashboard", 
        "🌾 My Products", 
        "➕ Add Product", 
        "📦 Orders", 
        "🌱 Fertilizer Tool"
    ])
    
    # ==================== DASHBOARD TAB ====================
    with tab1:
        st.subheader("📊 Your Statistics")
        stats = db.get_farmer_stats(user['id'])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Products", stats['total_products'])
        with col2:
            st.metric("Total Orders", stats['total_orders'])
        with col3:
            st.metric("Total Revenue", f"₹{stats['total_revenue']}")
        
        st.markdown("---")
        st.subheader("📈 Recent Activity")
        
        # Recent orders
        orders = db.get_orders_by_farmer(user['id'])
        if orders:
            st.markdown("#### Recent Orders")
            for order in orders[:5]:
                with st.expander(f"Order #{order['id']} - {order['status'].upper()} - ₹{order['total_amount']}"):
                    st.write(f"**Customer:** {order['consumer_name']}")
                    st.write(f"**Phone:** {order['consumer_phone']}")
                    st.write(f"**Address:** {order['delivery_address']}")
                    st.write(f"**Date:** {order['created_at']}")
                    
                    items = db.get_order_items(order['id'])
                    farmer_items = [item for item in items if item['farmer_id'] == user['id']]
                    
                    if farmer_items:
                        st.markdown("**Your Items:**")
                        for item in farmer_items:
                            st.write(f"- {item['product_name']}: {item['quantity']} {item['unit']} @ ₹{item['price_per_unit']}/{item['unit']} = ₹{item['subtotal']}")
        else:
            st.info("No orders yet")
    
    # ==================== MY PRODUCTS TAB ====================
    with tab2:
        st.subheader("🌾 My Products")
        products = db.get_products_by_farmer(user['id'])
        
        if products:
            for product in products:
                col1, col2 = st.columns([1, 3])
                
                with col1:
                    if product['image_path'] and os.path.exists(product['image_path']):
                        try:
                            img = Image.open(product['image_path'])
                            st.image(img, use_container_width=True)
                        except:
                            st.image("https://via.placeholder.com/150", use_container_width=True)
                    else:
                        st.image("https://via.placeholder.com/150", use_container_width=True)
                
                with col2:
                    st.markdown(f"### {product['name']}")
                    st.write(f"**Category:** {product['category']}")
                    st.write(f"**Price:** ₹{product['price']}/{product['unit']}")
                    st.write(f"**Available:** {product['quantity_available']} {product['unit']}")
                    st.write(f"**Status:** {'🟢 Active' if product['is_active'] else '🔴 Inactive'}")
                    
                    col_a, col_b, col_c = st.columns(3)
                    
                    with col_a:
                        if st.button("✏️ Edit", key=f"edit_{product['id']}"):
                            st.session_state[f'editing_{product["id"]}'] = True
                    
                    with col_b:
                        if st.button("🗑️ Delete", key=f"del_{product['id']}"):
                            db.delete_product(product['id'])
                            st.success("Product deleted!")
                            st.rerun()
                    
                    with col_c:
                        # Get reviews
                        rating_info = db.get_product_rating(product['id'])
                        if rating_info['review_count'] > 0:
                            st.write(f"⭐ {rating_info['avg_rating']} ({rating_info['review_count']} reviews)")
                
                # Edit form
                if st.session_state.get(f'editing_{product["id"]}', False):
                    with st.form(key=f"edit_form_{product['id']}"):
                        st.markdown("#### Edit Product")
                        name = st.text_input("Product Name", value=product['name'])
                        category = st.selectbox("Category", 
                            ["Vegetables", "Fruits", "Grains", "Pulses", "Spices", "Others"],
                            index=["Vegetables", "Fruits", "Grains", "Pulses", "Spices", "Others"].index(product['category']) if product['category'] in ["Vegetables", "Fruits", "Grains", "Pulses", "Spices", "Others"] else 0
                        )
                        description = st.text_area("Description", value=product['description'] or "")
                        price = st.number_input("Price per unit (₹)", value=float(product['price']), min_value=0.0)
                        unit = st.selectbox("Unit", ["kg", "quintal", "ton", "piece", "dozen", "liter"],
                            index=["kg", "quintal", "ton", "piece", "dozen", "liter"].index(product['unit']) if product['unit'] in ["kg", "quintal", "ton", "piece", "dozen", "liter"] else 0
                        )
                        quantity = st.number_input("Quantity Available", value=float(product['quantity_available']), min_value=0.0)
                        
                        uploaded_file = st.file_uploader("Update Image (optional)", type=['png', 'jpg', 'jpeg'])
                        
                        col_save, col_cancel = st.columns(2)
                        with col_save:
                            submit = st.form_submit_button("💾 Save Changes", use_container_width=True)
                        with col_cancel:
                            cancel = st.form_submit_button("❌ Cancel", use_container_width=True)
                        
                        if submit:
                            image_path = product['image_path']
                            if uploaded_file:
                                # Save new image
                                os.makedirs("static/uploads", exist_ok=True)
                                image_path = f"static/uploads/{user['id']}_{datetime.now().timestamp()}_{uploaded_file.name}"
                                with open(image_path, "wb") as f:
                                    f.write(uploaded_file.getbuffer())
                            
                            db.update_product(product['id'], name, category, description, price, unit, quantity, image_path)
                            st.success("Product updated successfully!")
                            st.session_state[f'editing_{product["id"]}'] = False
                            st.rerun()
                        
                        if cancel:
                            st.session_state[f'editing_{product["id"]}'] = False
                            st.rerun()
                
                st.markdown("---")
        else:
            st.info("You haven't added any products yet. Go to 'Add Product' tab to get started!")
    
    # ==================== ADD PRODUCT TAB ====================
    with tab3:
        st.subheader("➕ Add New Product")
        
        with st.form("add_product_form"):
            name = st.text_input("Product Name *", placeholder="e.g., Fresh Tomatoes")
            category = st.selectbox("Category *", ["Vegetables", "Fruits", "Grains", "Pulses", "Spices", "Others"])
            description = st.text_area("Description", placeholder="Describe your product...")
            
            col1, col2 = st.columns(2)
            with col1:
                price = st.number_input("Price per unit (₹) *", min_value=0.0, value=0.0, step=1.0)
                unit = st.selectbox("Unit *", ["kg", "quintal", "ton", "piece", "dozen", "liter"])
            
            with col2:
                quantity = st.number_input("Quantity Available *", min_value=0.0, value=0.0, step=1.0)
            
            uploaded_file = st.file_uploader("Product Image", type=['png', 'jpg', 'jpeg'])
            
            submit = st.form_submit_button("🌾 Add Product", use_container_width=True)
            
            if submit:
                if not name or price <= 0 or quantity <= 0:
                    st.error("Please fill all required fields with valid values!")
                else:
                    # Save image if uploaded
                    image_path = ""
                    if uploaded_file:
                        os.makedirs("static/uploads", exist_ok=True)
                        image_path = f"static/uploads/{user['id']}_{datetime.now().timestamp()}_{uploaded_file.name}"
                        with open(image_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                    
                    # Create product
                    product_id = db.create_product(
                        user['id'], name, category, description, price, unit, quantity, image_path
                    )
                    
                    if product_id:
                        st.success(f"✅ Product '{name}' added successfully!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("Failed to add product. Please try again.")
    
    # ==================== ORDERS TAB ====================
    with tab4:
        st.subheader("📦 Orders Received")
        orders = db.get_orders_by_farmer(user['id'])
        
        if orders:
            # Filter options
            status_filter = st.selectbox("Filter by Status", 
                ["All", "pending", "confirmed", "shipped", "delivered", "cancelled"])
            
            filtered_orders = orders if status_filter == "All" else [o for o in orders if o['status'] == status_filter]
            
            for order in filtered_orders:
                with st.expander(f"Order #{order['id']} - {order['status'].upper()} - ₹{order['total_amount']} - {order['created_at'][:10]}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**Customer Details:**")
                        st.write(f"Name: {order['consumer_name']}")
                        st.write(f"Phone: {order['consumer_phone']}")
                        st.write(f"Address: {order['delivery_address']}")
                    
                    with col2:
                        st.markdown("**Order Details:**")
                        st.write(f"Order Date: {order['created_at']}")
                        st.write(f"Status: {order['status'].upper()}")
                        st.write(f"Total: ₹{order['total_amount']}")
                    
                    st.markdown("---")
                    st.markdown("**Your Items in this Order:**")
                    
                    items = db.get_order_items(order['id'])
                    farmer_items = [item for item in items if item['farmer_id'] == user['id']]
                    
                    for item in farmer_items:
                        st.write(f"- **{item['product_name']}**: {item['quantity']} {item['unit']} @ ₹{item['price_per_unit']}/{item['unit']} = ₹{item['subtotal']}")
                    
                    # Status update (only for pending/confirmed orders)
                    if order['status'] in ['pending', 'confirmed']:
                        st.markdown("---")
                        new_status = st.selectbox(
                            "Update Status",
                            ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled'],
                            index=['pending', 'confirmed', 'shipped', 'delivered', 'cancelled'].index(order['status']),
                            key=f"status_{order['id']}"
                        )
                        
                        if st.button("Update Status", key=f"update_{order['id']}"):
                            db.update_order_status(order['id'], new_status)
                            st.success(f"Order status updated to {new_status}!")
                            st.rerun()
        else:
            st.info("No orders received yet")
    
    # ==================== FERTILIZER TOOL TAB ====================
    with tab5:
        from fertilizer_recommendation import show_fertilizer_recommendation
        show_fertilizer_recommendation()
