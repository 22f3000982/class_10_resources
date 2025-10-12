# Class -10 Resources Web Application

A modern Flask-based web application for managing and sharing educational resources for Class 10 students.

## Features

### 🔐 Admin Features
- Admin login with fixed password: `4129`
- Add new resources (with name, link, and optional file upload ≤5MB)
- Edit resource name and link
- Delete resources
- View total view count for each resource
- Manage owner profile information

### 👥 User Features
- Browse all resources without login
- Search resources by name
- View/download resources
- Auto-increment view count on each view
- Quick access buttons to Telegram, Instagram, and MCQ practice
- Share website functionality

### 🎨 Design
- Dark mode by default
- Fully responsive (mobile and desktop)
- Clean, modern UI with Bootstrap 5
- Smooth animations and transitions
- Beautiful gradient action buttons

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Local Installation

1. **Clone or download this project**

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
flask run
```

Or alternatively:
```bash
python app.py
```

4. **Access the application**
Open your browser and go to: `http://127.0.0.1:5000`

5. **Admin Login**
- Click on "Admin Login" in the navigation
- Enter password: `4129`

## Project Structure

```
New note site/
│
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── database.db                 # SQLite database (auto-generated)
│
├── templates/                  # HTML templates
│   ├── base.html              # Base template with navbar
│   ├── index.html             # Homepage with resources
│   ├── login.html             # Admin login page
│   ├── add_resource.html      # Add new resource form
│   ├── edit_resource.html     # Edit resource form
│   ├── about_owner.html       # Owner information page
│   └── practice_mcq.html      # MCQ practice page
│
└── static/                     # Static files
    ├── resources/             # Uploaded resource files
    └── owner/                 # Owner profile photos
```

## Database Schema

### Resources Table
- `id`: Primary key
- `name`: Resource name
- `link`: External URL (optional)
- `filename`: Uploaded file name (optional)
- `view_count`: Number of views
- `created_at`: Creation timestamp

### Owner Info Table
- `id`: Primary key
- `name`: Owner name
- `description`: Short description
- `contact`: Contact information
- `photo_filename`: Profile photo filename
- `telegram_link`: Telegram channel link
- `instagram_link`: Instagram profile link
- `mcq_link`: MCQ practice page link

## Deployment

### Deploy to Render

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `gunicorn app:app`
5. Add `gunicorn` to requirements.txt:
```
Flask==3.0.0
Werkzeug==3.0.1
gunicorn==21.2.0
```

### Deploy to Vercel

1. Install Vercel CLI: `npm i -g vercel`
2. Create `vercel.json`:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```
3. Deploy: `vercel`

**Note**: For production deployment on Vercel, file uploads may need to be stored in cloud storage (AWS S3, Cloudinary, etc.) instead of local storage.

## Configuration

### Change Admin Password
Edit `app.py` and modify:
```python
ADMIN_PASSWORD = '4129'  # Change this to your preferred password
```

### Update Social Links
Admin can update social links from the "About Owner" page after logging in.

### Customize Upload Settings
Edit in `app.py`:
```python
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'doc', 'docx', 'txt', 'jpg', 'jpeg', 'png', 'zip', 'rar'}
```

## Usage

### For Students (Users)
1. Visit the homepage
2. Browse available resources
3. Use the search bar to find specific resources
4. Click "View" to access/download resources
5. Use quick action buttons to join Telegram, Instagram, or practice MCQs

### For Admin
1. Login with password `4129`
2. Click "Upload New" to add resources
3. Fill in resource name and either provide a link or upload a file (or both)
4. Edit or delete existing resources from the homepage
5. Update owner information from "About Owner" page
6. View total views for each resource

## Security Notes

- Change the `SECRET_KEY` in `app.py` before deployment
- Change the default admin password
- File upload size is limited to 5MB
- Only specific file types are allowed for upload
- Session-based authentication for admin

## Browser Compatibility

- Chrome (recommended)
- Firefox
- Safari
- Edge
- Mobile browsers (iOS Safari, Chrome Mobile)

## Support

For issues or questions, contact the owner through the information provided in the "About Owner" section.

## License

This project is open source and available for educational purposes.

---

**Made with ❤️ for Class 10 Students**
