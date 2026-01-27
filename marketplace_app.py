import streamlit as st
import database as db
from farmer_dashboard import show_farmer_dashboard
from consumer_interface import show_consumer_interface

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="FarmDirect - Farmer to Consumer Marketplace",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS ====================
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        color: white;
    }
    .stButton>button {
        width: 100%;
        background-color: #00E676;
        color: black;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        padding: 10px;
    }
    .stButton>button:hover {
        background-color: #00C853;
        color: white;
    }
    .big-title {
        text-align: center;
        color: #00E676;
        font-size: 48px;
        font-weight: 900;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        color: #cccccc;
        font-size: 20px;
        margin-bottom: 30px;
    }
    .success-box {
        padding: 20px;
        border-radius: 10px;
        background-color: #1b5e20;
        border-left: 5px solid #00E676;
        margin: 10px 0;
    }
    .info-box {
        padding: 20px;
        border-radius: 10px;
        background-color: #01579b;
        border-left: 5px solid #2196F3;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== SESSION STATE INITIALIZATION ====================
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user' not in st.session_state:
    st.session_state['user'] = None
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'

# ==================== AUTHENTICATION FUNCTIONS ====================
def login_page():
    """Login page"""
    st.markdown("<h1 class='big-title'>🌾 FarmDirect</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Direct from Farm to Your Table - No Middlemen!</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 Login")
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submit = st.form_submit_button("🚀 Login", use_container_width=True)
            
            if submit:
                if username and password:
                    user = db.authenticate_user(username, password)
                    if user:
                        st.session_state['logged_in'] = True
                        st.session_state['user'] = user
                        st.success(f"Welcome back, {user['full_name']}!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
                else:
                    st.warning("Please enter both username and password")
        
        st.markdown("---")
        st.markdown("### Don't have an account?")
        if st.button("📝 Register Now", use_container_width=True):
            st.session_state['page'] = 'register'
            st.rerun()

def register_page():
    """Registration page"""
    st.markdown("<h1 class='big-title'>🌾 FarmDirect</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Join Our Community</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 📝 Create Account")
        
        with st.form("register_form"):
            full_name = st.text_input("Full Name *", placeholder="Enter your full name")
            username = st.text_input("Username *", placeholder="Choose a username")
            email = st.text_input("Email *", placeholder="your.email@example.com")
            password = st.text_input("Password *", type="password", placeholder="Create a strong password")
            confirm_password = st.text_input("Confirm Password *", type="password", placeholder="Re-enter password")
            
            role = st.radio("I am a:", ["farmer", "consumer"], horizontal=True)
            
            phone = st.text_input("Phone Number", placeholder="Your contact number")
            address = st.text_area("Address", placeholder="Your address")
            
            submit = st.form_submit_button("✅ Register", use_container_width=True)
            
            if submit:
                if not all([full_name, username, email, password, confirm_password]):
                    st.error("Please fill all required fields marked with *")
                elif password != confirm_password:
                    st.error("Passwords do not match!")
                elif len(password) < 6:
                    st.error("Password must be at least 6 characters long")
                else:
                    success, message = db.create_user(
                        username, email, password, role, full_name, phone, address
                    )
                    if success:
                        st.success("✅ Account created successfully! Please login.")
                        st.balloons()
                        if st.button("Go to Login"):
                            st.session_state['page'] = 'home'
                            st.rerun()
                    else:
                        st.error(message)
        
        st.markdown("---")
        if st.button("← Back to Login", use_container_width=True):
            st.session_state['page'] = 'home'
            st.rerun()

def home_page():
    """Landing page for non-logged-in users"""
    st.markdown("<h1 class='big-title'>🌾 FarmDirect Marketplace</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Connecting Farmers Directly with Consumers</p>", unsafe_allow_html=True)
    
    # Hero section
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='info-box'>
            <h2>👨‍🌾 For Farmers</h2>
            <ul>
                <li>Sell your crops directly to consumers</li>
                <li>Set your own prices</li>
                <li>No middlemen, maximum profit</li>
                <li>Manage inventory easily</li>
                <li>Get fertilizer recommendations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='info-box'>
            <h2>🛒 For Consumers</h2>
            <ul>
                <li>Buy fresh produce directly from farmers</li>
                <li>Fair prices, no middlemen markup</li>
                <li>Know your farmer</li>
                <li>Support local agriculture</li>
                <li>Quality guaranteed</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Featured products
    st.markdown("### 🌟 Featured Products")
    products = db.get_all_products()[:6]
    
    if products:
        cols = st.columns(3)
        for idx, product in enumerate(products):
            with cols[idx % 3]:
                st.markdown(f"#### {product['name']}")
                st.write(f"**₹{product['price']}/{product['unit']}**")
                st.write(f"By: {product['farmer_name']}")
                st.markdown("---")
    
    # Call to action
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### Ready to get started?")
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🔐 Login", use_container_width=True):
                st.session_state['page'] = 'login'
                st.rerun()
        with col_b:
            if st.button("📝 Register", use_container_width=True):
                st.session_state['page'] = 'register'
                st.rerun()

# ==================== MAIN APP ====================
def main():
    """Main application logic"""
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 🌾 FarmDirect")
        st.markdown("---")
        
        if st.session_state['logged_in']:
            user = st.session_state['user']
            st.markdown(f"### Welcome, {user['full_name']}!")
            st.markdown(f"**Role:** {user['role'].title()}")
            st.markdown(f"**Email:** {user['email']}")
            st.markdown("---")
            
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state['logged_in'] = False
                st.session_state['user'] = None
                st.session_state['page'] = 'home'
                st.success("Logged out successfully!")
                st.rerun()
        else:
            st.info("Please login to access the marketplace")
            st.markdown("---")
            st.markdown("### 📊 Platform Stats")
            
            # Get some stats
            all_products = db.get_all_products()
            st.metric("Active Products", len(all_products))
            
            st.markdown("---")
            st.markdown("### 🌟 Features")
            st.markdown("""
            - Direct farmer-consumer connection
            - No middlemen
            - Fair pricing
            - Quality products
            - Easy ordering
            - Secure transactions
            """)
    
    # Main content
    if not st.session_state['logged_in']:
        if st.session_state['page'] == 'login':
            login_page()
        elif st.session_state['page'] == 'register':
            register_page()
        else:
            home_page()
    else:
        user = st.session_state['user']
        
        if user['role'] == 'farmer':
            show_farmer_dashboard(user)
        elif user['role'] == 'consumer':
            show_consumer_interface(user)
        elif user['role'] == 'admin':
            st.markdown("## 👑 Admin Panel")
            st.info("Admin panel coming soon!")

if __name__ == "__main__":
    main()
