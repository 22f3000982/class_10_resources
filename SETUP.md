# Quick Setup Guide

## 🚀 Getting Started

### Method 1: Using the Run Script (Windows)
1. Double-click `run.bat`
2. Wait for dependencies to install
3. The application will start automatically
4. Open your browser to `http://127.0.0.1:5000`

### Method 2: Manual Setup

#### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 2: Run the Application
```bash
python app.py
```
Or:
```bash
flask run
```

#### Step 3: Access the Application
Open your browser and navigate to: `http://127.0.0.1:5000`

## 🔐 Admin Access

**Password:** `4129`

To login as admin:
1. Click "Admin Login" in the navigation bar
2. Enter password: `4129`
3. You can now add, edit, and delete resources

## 📝 First Steps

### As Admin:
1. **Update Owner Information**
   - Go to "About Owner" page
   - Click "Edit Information"
   - Update your name, description, contact info
   - Upload your profile photo
   - Add your social media links

2. **Add Your First Resource**
   - Click "Upload New" button
   - Enter resource name
   - Add either a link, upload a file, or both
   - Click "Upload Resource"

### As User:
1. **Browse Resources**
   - View all available resources on the homepage
   - Click "View" to access/download resources

2. **Search Resources**
   - Use the search bar to find specific resources
   - Search works on resource names

3. **Quick Actions**
   - Join Telegram channel
   - Follow on Instagram
   - Share the website
   - Practice MCQ questions

## 🎨 Customization

### Change Admin Password
Edit `app.py` line 16:
```python
ADMIN_PASSWORD = '4129'  # Change to your password
```

### Update Site Title
Edit `templates/base.html` line 7 and navbar brand section

### Modify Upload Limits
Edit `app.py` lines 9-11:
```python
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # Change file size limit
app.config['ALLOWED_EXTENSIONS'] = {...}  # Add/remove file types
```

## 📱 Features Overview

✅ Dark mode interface
✅ Responsive design (mobile-friendly)
✅ Admin authentication system
✅ Resource management (CRUD operations)
✅ File upload system (up to 5MB)
✅ Search functionality
✅ View counter for resources
✅ Social media integration
✅ Owner profile management
✅ MCQ practice page (template provided)

## 🌐 Deployment Options

### Render (Recommended for file uploads)
1. Push code to GitHub
2. Create new Web Service on Render
3. Connect repository
4. Build command: `pip install -r requirements.txt`
5. Start command: `gunicorn app:app`
6. Add gunicorn to requirements.txt

### Vercel (Fast deployment)
1. Install Vercel CLI: `npm i -g vercel`
2. Run: `vercel`
3. Follow prompts

**Note:** Vercel has limitations with file storage. Use cloud storage (AWS S3, Cloudinary) for production.

### PythonAnywhere
1. Upload files to PythonAnywhere
2. Set up web app with Flask
3. Configure WSGI file
4. Reload web app

## 🔧 Troubleshooting

### Database Issues
If you encounter database errors, delete `database.db` and restart the app. It will create a new database automatically.

### File Upload Issues
- Check file size (must be ≤5MB)
- Verify file type is in allowed extensions
- Ensure `static/resources` folder has write permissions

### Port Already in Use
If port 5000 is already in use:
```bash
flask run --port 5001
```

## 📞 Support

If you encounter any issues:
1. Check the README.md for detailed documentation
2. Verify all dependencies are installed
3. Ensure Python 3.8+ is installed
4. Check console for error messages

## 🎓 Usage Tips

1. **Organize Resources**: Use clear, descriptive names for resources
2. **Regular Backups**: Backup `database.db` regularly
3. **File Management**: Keep uploaded files organized
4. **Update Info**: Keep owner information and social links up to date
5. **Monitor Views**: Check view counts to see popular resources

---

**Happy Teaching & Learning! 📚**
