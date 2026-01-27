import streamlit as st
import database as db
from PIL import Image
import os

def show_consumer_interface(user):
    """Consumer interface for browsing and purchasing products"""
    
    st.markdown(f"## 🛒 Welcome, {user['full_name']}!")
    st.markdown("---")
    
    # Tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs([
        "🏪 Browse Products", 
        "🛒 My Cart", 
        "📦 My Orders",
        "👤 Profile"
    ])
    
    # ==================== BROWSE PRODUCTS TAB ====================
    with tab1:
        st.subheader("🏪 Available Products")
        
        # Search and filter
        col1, col2 = st.columns([3, 1])
        with col1:
            search_query = st.text_input("🔍 Search products", placeholder="Search by name...")
        with col2:
            category_filter = st.selectbox("Category", 
                ["All", "Vegetables", "Fruits", "Grains", "Pulses", "Spices", "Others"])
        
        # Get products
        if search_query:
            products = db.search_products(search_query, None if category_filter == "All" else category_filter)
        else:
            products = db.get_all_products()
            if category_filter != "All":
                products = [p for p in products if p['category'] == category_filter]
        
        if products:
            # Display products in grid
            cols_per_row = 3
            for i in range(0, len(products), cols_per_row):
                cols = st.columns(cols_per_row)
                for j, col in enumerate(cols):
                    if i + j < len(products):
                        product = products[i + j]
                        with col:
                            # Product card
                            with st.container():
                                # Image
                                if product['image_path'] and os.path.exists(product['image_path']):
                                    try:
                                        img = Image.open(product['image_path'])
                                        st.image(img, use_container_width=True)
                                    except:
                                        st.image("https://via.placeholder.com/200", use_container_width=True)
                                else:
                                    st.image("https://via.placeholder.com/200", use_container_width=True)
                                
                                # Product info
                                st.markdown(f"### {product['name']}")
                                st.write(f"**₹{product['price']}/{product['unit']}**")
                                st.write(f"📦 {product['quantity_available']} {product['unit']} available")
                                st.write(f"👨‍🌾 {product['farmer_name']}")
                                
                                # Rating
                                rating_info = db.get_product_rating(product['id'])
                                if rating_info['review_count'] > 0:
                                    st.write(f"⭐ {rating_info['avg_rating']} ({rating_info['review_count']} reviews)")
                                
                                # Add to cart
                                quantity = st.number_input(
                                    "Quantity", 
                                    min_value=0.0, 
                                    max_value=float(product['quantity_available']),
                                    value=1.0,
                                    step=1.0,
                                    key=f"qty_{product['id']}"
                                )
                                
                                col_a, col_b = st.columns(2)
                                with col_a:
                                    if st.button("🛒 Add", key=f"add_{product['id']}", use_container_width=True):
                                        if quantity > 0:
                                            if db.add_to_cart(user['id'], product['id'], quantity):
                                                st.success("Added to cart!")
                                                st.rerun()
                                            else:
                                                st.error("Failed to add to cart")
                                        else:
                                            st.warning("Please enter quantity")
                                
                                with col_b:
                                    if st.button("👁️ View", key=f"view_{product['id']}", use_container_width=True):
                                        st.session_state['viewing_product'] = product['id']
                                        st.rerun()
                                
                                st.markdown("---")
        else:
            st.info("No products found")
        
        # Product detail view
        if 'viewing_product' in st.session_state:
            product = db.get_product_by_id(st.session_state['viewing_product'])
            if product:
                with st.expander("📋 Product Details", expanded=True):
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        if product['image_path'] and os.path.exists(product['image_path']):
                            try:
                                img = Image.open(product['image_path'])
                                st.image(img, use_container_width=True)
                            except:
                                st.image("https://via.placeholder.com/300", use_container_width=True)
                        else:
                            st.image("https://via.placeholder.com/300", use_container_width=True)
                    
                    with col2:
                        st.markdown(f"## {product['name']}")
                        st.write(f"**Category:** {product['category']}")
                        st.write(f"**Price:** ₹{product['price']}/{product['unit']}")
                        st.write(f"**Available:** {product['quantity_available']} {product['unit']}")
                        st.write(f"**Farmer:** {product['farmer_name']}")
                        st.write(f"**Contact:** {product['farmer_phone']}")
                        
                        if product['description']:
                            st.markdown("**Description:**")
                            st.write(product['description'])
                    
                    # Reviews
                    st.markdown("---")
                    st.markdown("### ⭐ Reviews")
                    
                    reviews = db.get_product_reviews(product['id'])
                    rating_info = db.get_product_rating(product['id'])
                    
                    if rating_info['review_count'] > 0:
                        st.write(f"**Average Rating:** {rating_info['avg_rating']} ⭐ ({rating_info['review_count']} reviews)")
                        
                        for review in reviews:
                            st.markdown(f"**{review['consumer_name']}** - {'⭐' * review['rating']}")
                            st.write(review['comment'])
                            st.caption(review['created_at'])
                            st.markdown("---")
                    else:
                        st.info("No reviews yet")
                    
                    # Add review form
                    with st.form("review_form"):
                        st.markdown("#### Leave a Review")
                        rating = st.slider("Rating", 1, 5, 5)
                        comment = st.text_area("Comment")
                        submit = st.form_submit_button("Submit Review")
                        
                        if submit:
                            if db.add_review(product['id'], user['id'], rating, comment):
                                st.success("Review added!")
                                st.rerun()
                            else:
                                st.error("Failed to add review")
                    
                    if st.button("Close Details"):
                        del st.session_state['viewing_product']
                        st.rerun()
    
    # ==================== MY CART TAB ====================
    with tab2:
        st.subheader("🛒 My Shopping Cart")
        
        cart_items = db.get_cart_items(user['id'])
        
        if cart_items:
            total = 0
            
            for item in cart_items:
                col1, col2, col3, col4 = st.columns([1, 3, 2, 1])
                
                with col1:
                    if item['image_path'] and os.path.exists(item['image_path']):
                        try:
                            img = Image.open(item['image_path'])
                            st.image(img, use_container_width=True)
                        except:
                            st.image("https://via.placeholder.com/100", use_container_width=True)
                    else:
                        st.image("https://via.placeholder.com/100", use_container_width=True)
                
                with col2:
                    st.markdown(f"### {item['name']}")
                    st.write(f"**₹{item['price']}/{item['unit']}**")
                    st.write(f"Farmer: {item['farmer_name']}")
                
                with col3:
                    new_qty = st.number_input(
                        "Quantity",
                        min_value=0.0,
                        max_value=float(item['quantity_available']),
                        value=float(item['quantity']),
                        step=1.0,
                        key=f"cart_qty_{item['id']}"
                    )
                    
                    if new_qty != item['quantity']:
                        db.update_cart_quantity(user['id'], item['product_id'], new_qty)
                        st.rerun()
                    
                    subtotal = item['price'] * item['quantity']
                    st.write(f"**Subtotal: ₹{subtotal:.2f}**")
                    total += subtotal
                
                with col4:
                    if st.button("🗑️", key=f"remove_{item['id']}"):
                        db.update_cart_quantity(user['id'], item['product_id'], 0)
                        st.rerun()
                
                st.markdown("---")
            
            # Checkout section
            st.markdown("### 💰 Order Summary")
            st.markdown(f"**Total Amount: ₹{total:.2f}**")
            
            with st.form("checkout_form"):
                st.markdown("#### Delivery Details")
                delivery_address = st.text_area("Delivery Address *", value=user.get('address', ''))
                phone = st.text_input("Contact Phone *", value=user.get('phone', ''))
                
                col1, col2 = st.columns(2)
                with col1:
                    checkout = st.form_submit_button("✅ Place Order", use_container_width=True)
                with col2:
                    clear = st.form_submit_button("🗑️ Clear Cart", use_container_width=True)
                
                if checkout:
                    if not delivery_address or not phone:
                        st.error("Please provide delivery address and phone number")
                    else:
                        # Prepare order items with farmer_id
                        order_items = []
                        for item in cart_items:
                            # Get product to fetch farmer_id
                            product = db.get_product_by_id(item['product_id'])
                            order_items.append({
                                'product_id': item['product_id'],
                                'farmer_id': product['farmer_id'],
                                'quantity': item['quantity'],
                                'price': item['price']
                            })
                        
                        order_id = db.create_order(user['id'], order_items, delivery_address, phone)
                        
                        if order_id:
                            db.clear_cart(user['id'])
                            st.success(f"✅ Order #{order_id} placed successfully!")
                            st.balloons()
                            st.rerun()
                        else:
                            st.error("Failed to place order. Please try again.")
                
                if clear:
                    db.clear_cart(user['id'])
                    st.success("Cart cleared!")
                    st.rerun()
        else:
            st.info("Your cart is empty. Browse products to add items!")
    
    # ==================== MY ORDERS TAB ====================
    with tab3:
        st.subheader("📦 My Orders")
        
        orders = db.get_orders_by_consumer(user['id'])
        
        if orders:
            for order in orders:
                status_color = {
                    'pending': '🟡',
                    'confirmed': '🔵',
                    'shipped': '🟣',
                    'delivered': '🟢',
                    'cancelled': '🔴'
                }
                
                with st.expander(f"{status_color.get(order['status'], '⚪')} Order #{order['id']} - {order['status'].upper()} - ₹{order['total_amount']} - {order['created_at'][:10]}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**Order Details:**")
                        st.write(f"Order ID: #{order['id']}")
                        st.write(f"Date: {order['created_at']}")
                        st.write(f"Status: {order['status'].upper()}")
                        st.write(f"Total: ₹{order['total_amount']}")
                    
                    with col2:
                        st.markdown("**Delivery Details:**")
                        st.write(f"Address: {order['delivery_address']}")
                        st.write(f"Phone: {order['phone']}")
                    
                    st.markdown("---")
                    st.markdown("**Items:**")
                    
                    items = db.get_order_items(order['id'])
                    for item in items:
                        st.write(f"- **{item['product_name']}**: {item['quantity']} {item['unit']} @ ₹{item['price_per_unit']}/{item['unit']} = ₹{item['subtotal']}")
                        st.caption(f"Farmer: {item['farmer_name']}")
        else:
            st.info("No orders yet. Start shopping!")
    
    # ==================== PROFILE TAB ====================
    with tab4:
        st.subheader("👤 My Profile")
        
        with st.form("profile_form"):
            full_name = st.text_input("Full Name", value=user['full_name'])
            email = st.text_input("Email", value=user['email'], disabled=True)
            phone = st.text_input("Phone", value=user.get('phone', ''))
            address = st.text_area("Address", value=user.get('address', ''))
            
            submit = st.form_submit_button("💾 Update Profile", use_container_width=True)
            
            if submit:
                db.update_user_profile(user['id'], full_name, phone, address)
                st.success("Profile updated successfully!")
                # Update session state
                st.session_state['user']['full_name'] = full_name
                st.session_state['user']['phone'] = phone
                st.session_state['user']['address'] = address
                st.rerun()
