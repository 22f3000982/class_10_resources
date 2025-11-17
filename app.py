from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash, send_from_directory
from werkzeug.utils import secure_filename
import os
import sqlite3
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max file size
app.config['UPLOAD_FOLDER'] = 'static/resources'
app.config['OWNER_PHOTO_FOLDER'] = 'static/owner'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'doc', 'docx', 'txt', 'jpg', 'jpeg', 'png', 'zip', 'rar'}

ADMIN_PASSWORD = '4129'

# Ensure upload folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OWNER_PHOTO_FOLDER'], exist_ok=True)

# Database initialization
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    # Resources table
    c.execute('''CREATE TABLE IF NOT EXISTS resources
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  link TEXT,
                  filename TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Owner info table
    c.execute('''CREATE TABLE IF NOT EXISTS owner_info
                 (id INTEGER PRIMARY KEY,
                  name TEXT,
                  description TEXT,
                  contact TEXT,
                  photo_filename TEXT,
                  telegram_link TEXT,
                  instagram_link TEXT,
                  mcq_link TEXT)''')
    
    # Insert default owner info if not exists
    c.execute('SELECT COUNT(*) FROM owner_info')
    if c.fetchone()[0] == 0:
        c.execute('''INSERT INTO owner_info (id, name, description, contact, photo_filename, telegram_link, instagram_link, mcq_link)
                     VALUES (1, 'Ashish Maurya', 
                             'Class 10 Resource Manager | Pursuing BS in Data Science at IIT Madras | Web Developer & Physics Teacher | Passionate about technology and education', 
                             'ashraj77777@gmail.com',
                             'mee.jpeg',
                             'https://t.me/chaipe_charcha', 'https://www.instagram.com/ashraj77777/', 
                             'https://www.perplexity.ai/apps/1d5d3a09-a3b4-4c9d-ae02-b5951bb98a80')''')
    
    conn.commit()
    conn.close()

init_db()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function
#
@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    search_query = request.args.get('search', '')
    
    if search_query:
        c.execute('SELECT * FROM resources WHERE name LIKE ? ORDER BY created_at ASC', 
                  ('%' + search_query + '%',))
    else:
        c.execute('SELECT * FROM resources ORDER BY created_at ASC')
    
    resources = c.fetchall()
    
    # Get owner info for social links
    c.execute('SELECT * FROM owner_info WHERE id = 1')
    owner_info = c.fetchone()
    
    conn.close()
    
    is_admin = 'admin' in session
    return render_template('index.html', resources=resources, is_admin=is_admin, 
                          search_query=search_query, owner_info=owner_info)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['admin'] = True
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid password!', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/download-database')
@login_required
def download_database():
    """Admin route to download the database file for backup"""
    try:
        return send_from_directory('.', 'database.db', as_attachment=True, download_name='database_backup.db')
    except Exception as e:
        flash(f'Error downloading database: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/add-resource', methods=['GET', 'POST'])
@login_required
def add_resource():
    if request.method == 'POST':
        name = request.form.get('name')
        link = request.form.get('link')
        file = request.files.get('file')
        
        filename = None
        if file and file.filename != '':
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Add timestamp to filename to avoid conflicts
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                filename = f"{timestamp}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                flash('Invalid file type!', 'error')
                return redirect(url_for('add_resource'))
        
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('INSERT INTO resources (name, link, filename) VALUES (?, ?, ?)',
                  (name, link, filename))
        conn.commit()
        conn.close()
        
        flash('Resource added successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('add_resource.html')

@app.route('/edit-resource/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_resource(id):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    if request.method == 'POST':
        name = request.form.get('name')
        link = request.form.get('link')
        
        c.execute('UPDATE resources SET name = ?, link = ? WHERE id = ?',
                  (name, link, id))
        conn.commit()
        conn.close()
        
        flash('Resource updated successfully!', 'success')
        return redirect(url_for('index'))
    
    c.execute('SELECT * FROM resources WHERE id = ?', (id,))
    resource = c.fetchone()
    conn.close()
    
    if not resource:
        flash('Resource not found!', 'error')
        return redirect(url_for('index'))
    
    return render_template('edit_resource.html', resource=resource)

@app.route('/delete-resource/<int:id>')
@login_required
def delete_resource(id):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    # Get resource info to delete file if exists
    c.execute('SELECT filename FROM resources WHERE id = ?', (id,))
    resource = c.fetchone()
    
    if resource and resource['filename']:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], resource['filename'])
        if os.path.exists(file_path):
            os.remove(file_path)
    
    c.execute('DELETE FROM resources WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    flash('Resource deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/view-resource/<int:id>')
def view_resource(id):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    # Get resource info
    c.execute('SELECT * FROM resources WHERE id = ?', (id,))
    resource = c.fetchone()
    conn.close()
    
    if not resource:
        flash('Resource not found!', 'error')
        return redirect(url_for('index'))
    
    # If there's a file, serve it
    if resource['filename']:
        return send_from_directory(app.config['UPLOAD_FOLDER'], resource['filename'])
    # If there's a link, redirect to it
    elif resource['link']:
        return redirect(resource['link'])
    else:
        flash('No file or link available for this resource!', 'error')
        return redirect(url_for('index'))

@app.route('/about-owner', methods=['GET', 'POST'])
def about_owner():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    if request.method == 'POST' and 'admin' in session:
        name = request.form.get('name')
        description = request.form.get('description')
        contact = request.form.get('contact')
        telegram_link = request.form.get('telegram_link')
        instagram_link = request.form.get('instagram_link')
        mcq_link = request.form.get('mcq_link')
        
        file = request.files.get('photo')
        photo_filename = None
        
        if file and file.filename != '':
            if file.filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png'}:
                photo_filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                photo_filename = f"owner_{timestamp}_{photo_filename}"
                file.save(os.path.join(app.config['OWNER_PHOTO_FOLDER'], photo_filename))
                
                # Delete old photo if exists
                c.execute('SELECT photo_filename FROM owner_info WHERE id = 1')
                old_photo = c.fetchone()
                if old_photo and old_photo['photo_filename']:
                    old_path = os.path.join(app.config['OWNER_PHOTO_FOLDER'], old_photo['photo_filename'])
                    if os.path.exists(old_path):
                        os.remove(old_path)
        
        if photo_filename:
            c.execute('''UPDATE owner_info SET name = ?, description = ?, contact = ?, 
                        photo_filename = ?, telegram_link = ?, instagram_link = ?, mcq_link = ?
                        WHERE id = 1''',
                     (name, description, contact, photo_filename, telegram_link, instagram_link, mcq_link))
        else:
            c.execute('''UPDATE owner_info SET name = ?, description = ?, contact = ?,
                        telegram_link = ?, instagram_link = ?, mcq_link = ?
                        WHERE id = 1''',
                     (name, description, contact, telegram_link, instagram_link, mcq_link))
        
        conn.commit()
        flash('Owner information updated successfully!', 'success')
    
    c.execute('SELECT * FROM owner_info WHERE id = 1')
    owner_info = c.fetchone()
    conn.close()
    
    is_admin = 'admin' in session
    return render_template('about_owner.html', owner_info=owner_info, is_admin=is_admin)

@app.route('/practice-mcq')
def practice_mcq():
    return render_template('practice_mcq.html')

if __name__ == '__main__':
    app.run(debug=True)
