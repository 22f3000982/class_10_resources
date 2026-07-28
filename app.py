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
app.config['NOTES_2026_FOLDER'] = 'static/notes_2026'
app.config['OWNER_PHOTO_FOLDER'] = 'static/owner'
app.config['MCQ_UPLOAD_FOLDER'] = 'static/mcq'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'doc', 'docx', 'txt', 'jpg', 'jpeg', 'png', 'zip', 'rar'}
app.config['MCQ_ALLOWED_EXTENSIONS'] = {'pdf', 'html', 'htm', 'doc', 'docx', 'md', 'txt'}

ADMIN_PASSWORD = '4129'

# Ensure upload folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['NOTES_2026_FOLDER'], exist_ok=True)
os.makedirs(app.config['OWNER_PHOTO_FOLDER'], exist_ok=True)
os.makedirs(app.config['MCQ_UPLOAD_FOLDER'], exist_ok=True)

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

    # 2026 notes table
    c.execute('''CREATE TABLE IF NOT EXISTS notes_2026
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

    # DPP table
    c.execute('''CREATE TABLE IF NOT EXISTS dpps
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT NOT NULL,
                  drive_link TEXT NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    # MCQ quizzes table
    c.execute('''CREATE TABLE IF NOT EXISTS mcq_quizzes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT NOT NULL,
                  details TEXT,
                  filename TEXT NOT NULL,
                  file_type TEXT NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
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

def allowed_note_file(filename):
    return allowed_file(filename)

def allowed_mcq_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['MCQ_ALLOWED_EXTENSIONS']

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

    # Get all DPPs
    c.execute('SELECT * FROM dpps ORDER BY created_at DESC')
    dpps = c.fetchall()
    
    conn.close()
    
    is_admin = 'admin' in session
    return render_template('index.html', resources=resources, is_admin=is_admin,
                          search_query=search_query, owner_info=owner_info, dpps=dpps)

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
        return_to = request.form.get('return_to', 'index')
        
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
        if return_to == 'notes_2026':
            return redirect('/notes-2026')
        return redirect(url_for('index'))
    
    return render_template('add_resource.html')

@app.route('/add-note-2026', methods=['POST'])
@login_required
def add_note_2026():
    name = request.form.get('name', '').strip()
    link = request.form.get('link', '').strip()
    file = request.files.get('file')

    if not name:
        flash('Note title is required!', 'error')
        return redirect(url_for('notes_2026'))

    filename = None
    if file and file.filename != '':
        if allowed_note_file(file.filename):
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            filename = f"note_{timestamp}_{filename}"
            file.save(os.path.join(app.config['NOTES_2026_FOLDER'], filename))
        else:
            flash('Invalid file type!', 'error')
            return redirect(url_for('notes_2026'))

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO notes_2026 (name, link, filename) VALUES (?, ?, ?)',
              (name, link, filename))
    conn.commit()
    conn.close()

    flash('2026 note added successfully!', 'success')
    return redirect(url_for('notes_2026'))

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

@app.route('/view-note-2026/<int:id>')
def view_note_2026(id):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM notes_2026 WHERE id = ?', (id,))
    note = c.fetchone()
    conn.close()

    if not note:
        flash('Note not found!', 'error')
        return redirect(url_for('notes_2026'))

    if note['filename']:
        return send_from_directory(app.config['NOTES_2026_FOLDER'], note['filename'])
    if note['link']:
        return redirect(note['link'])

    flash('No file or link available for this note!', 'error')
    return redirect(url_for('notes_2026'))

@app.route('/edit-note-2026/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_note_2026(id):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM notes_2026 WHERE id = ?', (id,))
    note = c.fetchone()

    if not note:
        conn.close()
        flash('Note not found!', 'error')
        return redirect(url_for('notes_2026'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        link = request.form.get('link', '').strip()
        file = request.files.get('file')

        if not name:
            flash('Note title is required!', 'error')
            return redirect(url_for('edit_note_2026', id=id))

        filename = note['filename']
        if file and file.filename != '':
            if not allowed_note_file(file.filename):
                flash('Invalid file type!', 'error')
                return redirect(url_for('edit_note_2026', id=id))

            new_filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            new_filename = f"note_{timestamp}_{new_filename}"
            file.save(os.path.join(app.config['NOTES_2026_FOLDER'], new_filename))

            if filename:
                old_path = os.path.join(app.config['NOTES_2026_FOLDER'], filename)
                if os.path.exists(old_path):
                    os.remove(old_path)

            filename = new_filename

        c.execute('UPDATE notes_2026 SET name = ?, link = ?, filename = ? WHERE id = ?',
                  (name, link, filename, id))
        conn.commit()
        conn.close()

        flash('2026 note updated successfully!', 'success')
        return redirect(url_for('notes_2026'))

    conn.close()
    return render_template('edit_resource.html', resource=note)

@app.route('/delete-note-2026/<int:id>')
@login_required
def delete_note_2026(id):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT filename FROM notes_2026 WHERE id = ?', (id,))
    note = c.fetchone()

    if note and note['filename']:
        file_path = os.path.join(app.config['NOTES_2026_FOLDER'], note['filename'])
        if os.path.exists(file_path):
            os.remove(file_path)

    c.execute('DELETE FROM notes_2026 WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    flash('2026 note deleted!', 'success')
    return redirect(url_for('notes_2026'))

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

@app.route('/notes-2025')
@app.route('/notes-2026')
def notes_2026():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    search_query = request.args.get('search', '')

    if search_query:
        c.execute('SELECT * FROM notes_2026 WHERE name LIKE ? ORDER BY created_at ASC',
                  ('%' + search_query + '%',))
    else:
        c.execute('SELECT * FROM notes_2026 ORDER BY created_at ASC')

    resources = c.fetchall()

    c.execute('SELECT * FROM owner_info WHERE id = 1')
    owner_info = c.fetchone()

    conn.close()

    is_admin = 'admin' in session
    return render_template('notes_2026.html', resources=resources, is_admin=is_admin,
                          search_query=search_query, owner_info=owner_info)

@app.route('/practice-mcq')
def practice_mcq():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM mcq_quizzes ORDER BY created_at DESC')
    quizzes = c.fetchall()
    conn.close()
    is_admin = 'admin' in session
    return render_template('practice_mcq.html', quizzes=quizzes, is_admin=is_admin)

@app.route('/add-mcq', methods=['POST'])
@login_required
def add_mcq():
    title = request.form.get('title', '').strip()
    details = request.form.get('details', '').strip()
    file = request.files.get('file')

    if not title:
        flash('Quiz name is required!', 'error')
        return redirect(url_for('practice_mcq'))

    if not file or file.filename == '':
        flash('Please upload a PDF or HTML file!', 'error')
        return redirect(url_for('practice_mcq'))

    if not allowed_mcq_file(file.filename):
        flash('Invalid file type! Only PDF or HTML files are allowed.', 'error')
        return redirect(url_for('practice_mcq'))

    filename = secure_filename(file.filename)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"mcq_{timestamp}_{filename}"
    file.save(os.path.join(app.config['MCQ_UPLOAD_FOLDER'], filename))

    file_type = filename.rsplit('.', 1)[1].lower()

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO mcq_quizzes (title, details, filename, file_type) VALUES (?, ?, ?, ?)',
              (title, details, filename, file_type))
    conn.commit()
    conn.close()

    flash('MCQ quiz uploaded successfully!', 'success')
    return redirect(url_for('practice_mcq'))

@app.route('/mcq/<int:id>')
def view_mcq(id):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM mcq_quizzes WHERE id = ?', (id,))
    quiz = c.fetchone()
    conn.close()

    if not quiz:
        flash('MCQ quiz not found!', 'error')
        return redirect(url_for('practice_mcq'))

    file_url = url_for('mcq_file', filename=quiz['filename'])
    return render_template('mcq_view.html', quiz=quiz, file_url=file_url)

@app.route('/mcq-file/<path:filename>')
def mcq_file(filename):
    return send_from_directory(app.config['MCQ_UPLOAD_FOLDER'], filename)

@app.route('/edit-mcq/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_mcq(id):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM mcq_quizzes WHERE id = ?', (id,))
    quiz = c.fetchone()

    if not quiz:
        conn.close()
        flash('MCQ quiz not found!', 'error')
        return redirect(url_for('practice_mcq'))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        details = request.form.get('details', '').strip()
        file = request.files.get('file')

        if not title:
            flash('Quiz name is required!', 'error')
            return redirect(url_for('edit_mcq', id=id))

        filename = quiz['filename']
        file_type = quiz['file_type']

        if file and file.filename != '':
            if not allowed_mcq_file(file.filename):
                flash('Invalid file type! Only PDF, DOC, DOCX, TXT, MD, or HTML files are allowed.', 'error')
                return redirect(url_for('edit_mcq', id=id))

            new_filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            new_filename = f"mcq_{timestamp}_{new_filename}"
            file.save(os.path.join(app.config['MCQ_UPLOAD_FOLDER'], new_filename))

            old_path = os.path.join(app.config['MCQ_UPLOAD_FOLDER'], filename)
            if os.path.exists(old_path):
                os.remove(old_path)

            filename = new_filename
            file_type = new_filename.rsplit('.', 1)[1].lower()

        c.execute('UPDATE mcq_quizzes SET title = ?, details = ?, filename = ?, file_type = ? WHERE id = ?',
                  (title, details, filename, file_type, id))
        conn.commit()
        conn.close()

        flash('MCQ quiz updated successfully!', 'success')
        return redirect(url_for('practice_mcq'))

    conn.close()
    return render_template('edit_mcq.html', quiz=quiz)

@app.route('/delete-mcq/<int:id>')
@login_required
def delete_mcq(id):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT filename FROM mcq_quizzes WHERE id = ?', (id,))
    quiz = c.fetchone()

    if quiz and quiz['filename']:
        file_path = os.path.join(app.config['MCQ_UPLOAD_FOLDER'], quiz['filename'])
        if os.path.exists(file_path):
            os.remove(file_path)

    c.execute('DELETE FROM mcq_quizzes WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    flash('MCQ quiz deleted!', 'success')
    return redirect(url_for('practice_mcq'))

# ── DPP routes ────────────────────────────────────────────────────────────────

@app.route('/dpp')
def dpp_page():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM dpps ORDER BY created_at DESC')
    dpps = c.fetchall()
    conn.close()
    is_admin = 'admin' in session
    return render_template('dpp.html', dpps=dpps, is_admin=is_admin)

@app.route('/add-dpp', methods=['POST'])
@login_required
def add_dpp():
    title = request.form.get('title', '').strip()
    drive_link = request.form.get('drive_link', '').strip()
    if not title or not drive_link:
        flash('Title and Drive link are required!', 'error')
        return redirect(url_for('dpp_page'))
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO dpps (title, drive_link) VALUES (?, ?)', (title, drive_link))
    conn.commit()
    conn.close()
    flash('DPP added successfully!', 'success')
    return redirect(url_for('dpp_page'))

@app.route('/edit-dpp/<int:id>', methods=['POST'])
@login_required
def edit_dpp(id):
    title = request.form.get('title', '').strip()
    drive_link = request.form.get('drive_link', '').strip()
    if not title or not drive_link:
        flash('Title and Drive link are required!', 'error')
        return redirect(url_for('dpp_page'))
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('UPDATE dpps SET title = ?, drive_link = ? WHERE id = ?', (title, drive_link, id))
    conn.commit()
    conn.close()
    flash('DPP updated successfully!', 'success')
    return redirect(url_for('dpp_page'))

@app.route('/delete-dpp/<int:id>')
@login_required
def delete_dpp(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('DELETE FROM dpps WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('DPP deleted!', 'success')
    return redirect(url_for('dpp_page'))

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)

