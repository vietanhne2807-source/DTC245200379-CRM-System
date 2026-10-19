import os
import logging
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, render_template, request, redirect, url_for
from prometheus_flask_exporter import PrometheusMetrics

# Cấu hình logging đẩy ra stdout để Promtail + Loki thu thập
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] [CRM-APP] %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
metrics = PrometheusMetrics(app)

def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get('DB_HOST', 'postgres_db'),
        database=os.environ.get('DB_NAME', 'crm_db'),
        user=os.environ.get('DB_USER', 'crm_user'),
        password=os.environ.get('DB_PASSWORD', 'CrmApp@2026!Secure379'),
        cursor_factory=RealDictCursor
    )

@app.route('/')
def index():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM customers ORDER BY id DESC;")
        customers = cur.fetchall()

        cur.execute("""
            SELECT c.*, cu.full_name AS customer_name 
            FROM contacts c 
            LEFT JOIN customers cu ON c.customer_id = cu.id 
            ORDER BY c.id DESC;
        """)
        contacts = cur.fetchall()

        cur.execute("""
            SELECT i.*, cu.full_name AS customer_name 
            FROM interactions i 
            LEFT JOIN customers cu ON i.customer_id = cu.id 
            ORDER BY i.interaction_date DESC;
        """)
        interactions = cur.fetchall()

        cur.close()
        conn.close()
        logger.info("ACTION=VIEW_DASHBOARD status=success student=DTC245200379")
        return render_template('index.html', customers=customers, contacts=contacts, interactions=interactions)
    except Exception as e:
        logger.error(f"ACTION=VIEW_DASHBOARD status=error detail={str(e)}")
        return f"Lỗi kết nối CSDL: {str(e)}", 500

@app.route('/add_customer', methods=['POST'])
def add_customer():
    full_name = request.form.get('full_name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    company = request.form.get('company')
    status = request.form.get('status', 'Tiềm năng')
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO customers (full_name, email, phone, company, status) VALUES (%s, %s, %s, %s, %s)",
            (full_name, email, phone, company, status)
        )
        conn.commit()
        cur.close()
        conn.close()
        logger.info(f"ACTION=ADD_CUSTOMER status=success customer='{full_name}' email='{email}'")
    except Exception as e:
        logger.error(f"ACTION=ADD_CUSTOMER status=error detail={str(e)}")
    return redirect(url_for('index'))

@app.route('/add_contact', methods=['POST'])
def add_contact():
    customer_id = request.form.get('customer_id')
    contact_name = request.form.get('contact_name')
    position = request.form.get('position')
    phone = request.form.get('phone')
    email = request.form.get('email')
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO contacts (customer_id, contact_name, position, phone, email) VALUES (%s, %s, %s, %s, %s)",
            (customer_id, contact_name, position, phone, email)
        )
        conn.commit()
        cur.close()
        conn.close()
        logger.info(f"ACTION=ADD_CONTACT status=success contact='{contact_name}' customer_id={customer_id}")
    except Exception as e:
        logger.error(f"ACTION=ADD_CONTACT status=error detail={str(e)}")
    return redirect(url_for('index'))

@app.route('/add_interaction', methods=['POST'])
def add_interaction():
    customer_id = request.form.get('customer_id')
    channel = request.form.get('channel')
    summary = request.form.get('summary')
    staff_name = request.form.get('staff_name', 'Nguyễn Trần Việt Anh (DTC245200379)')
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO interactions (customer_id, channel, summary, staff_name) VALUES (%s, %s, %s, %s)",
            (customer_id, channel, summary, staff_name)
        )
        conn.commit()
        cur.close()
        conn.close()
        logger.info(f"ACTION=ADD_INTERACTION status=success channel='{channel}' customer_id={customer_id}")
    except Exception as e:
        logger.error(f"ACTION=ADD_INTERACTION status=error detail={str(e)}")
    return redirect(url_for('index'))

@app.route('/health')
def health():
    return {"status": "healthy", "service": "crm-web-app", "student": "DTC245200379"}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
