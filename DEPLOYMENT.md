# Deployment Guide 🚀

## Prerequisites for All Platforms
- Git installed
- GitHub account (recommended)
- Code pushed to a Git repository

---

## Option 1: Deploy to Render (Recommended)

**Why Render?**
- Free tier available
- Supports file uploads
- Persistent disk storage
- Easy database management
- Great for Flask apps

### Steps:

1. **Prepare Your Code**
   - Update `requirements.txt` to include gunicorn:
   ```
   Flask==3.0.0
   Werkzeug==3.0.1
   gunicorn==21.2.0
   ```

2. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

3. **Create Render Account**
   - Go to https://render.com
   - Sign up with GitHub

4. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name**: class-10-resources (or your choice)
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn app:app`
     - **Instance Type**: Free

5. **Add Environment Variables** (Optional)
   - `SECRET_KEY`: your-secret-key-here
   - `ADMIN_PASSWORD`: 4129 (or your choice)

6. **Deploy**
   - Click "Create Web Service"
   - Wait 5-10 minutes for deployment
   - Your app will be live at: `https://your-app-name.onrender.com`

### Post-Deployment:
- Test all features
- Update owner information
- Add your resources

---

## Option 2: Deploy to PythonAnywhere

**Why PythonAnywhere?**
- Beginner-friendly
- Free tier with good limits
- Built for Python/Flask
- Persistent file storage

### Steps:

1. **Create Account**
   - Go to https://www.pythonanywhere.com
   - Sign up for free account

2. **Upload Files**
   - Method A: Use Git
     ```bash
     git clone YOUR_GITHUB_REPO_URL
     ```
   - Method B: Upload via Files tab

3. **Open Bash Console**
   - Go to "Consoles" → "Bash"
   
4. **Install Dependencies**
   ```bash
   cd ~/your-project-folder
   pip3 install --user -r requirements.txt
   ```

5. **Configure Web App**
   - Go to "Web" tab
   - Click "Add a new web app"
   - Choose: Manual configuration → Python 3.10
   - Set Source code directory: `/home/yourusername/your-project-folder`
   - Set Working directory: `/home/yourusername/your-project-folder`

6. **Edit WSGI File**
   - Click on WSGI configuration file link
   - Replace content with:
   ```python
   import sys
   path = '/home/yourusername/your-project-folder'
   if path not in sys.path:
       sys.path.append(path)
   
   from app import app as application
   ```

7. **Configure Static Files**
   - URL: `/static/`
   - Directory: `/home/yourusername/your-project-folder/static/`

8. **Reload Web App**
   - Click green "Reload" button
   - Visit your app at: `https://yourusername.pythonanywhere.com`

---

## Option 3: Deploy to Railway

**Why Railway?**
- Modern platform
- Simple deployment
- Good free tier
- Automatic deploys from Git

### Steps:

1. **Prepare Code**
   - Add gunicorn to requirements.txt
   - Create `Procfile`:
   ```
   web: gunicorn app:app
   ```

2. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push
   ```

3. **Deploy on Railway**
   - Go to https://railway.app
   - Sign up with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway auto-detects Python and deploys

4. **Configure**
   - Add environment variables if needed
   - Get your deployment URL

---

## Option 4: Deploy to Heroku

**Why Heroku?**
- Well-established platform
- Easy deployment
- Good documentation

### Steps:

1. **Prepare Files**
   
   Add to `requirements.txt`:
   ```
   Flask==3.0.0
   Werkzeug==3.0.1
   gunicorn==21.2.0
   ```
   
   Create `Procfile`:
   ```
   web: gunicorn app:app
   ```
   
   Create `runtime.txt`:
   ```
   python-3.11.0
   ```

2. **Install Heroku CLI**
   - Download from: https://devcenter.heroku.com/articles/heroku-cli

3. **Deploy**
   ```bash
   heroku login
   heroku create your-app-name
   git push heroku main
   heroku open
   ```

---

## Option 5: Deploy to Vercel

**Why Vercel?**
- Fast deployment
- Global CDN
- Free tier

**⚠️ Important Limitations:**
- Serverless environment
- File uploads won't persist
- Need external storage (AWS S3, Cloudinary) for production

### Steps:

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Deploy**
   ```bash
   cd "c:\MY_PROJECTS\New note site"
   vercel
   ```

3. **Follow Prompts**
   - Select project settings
   - Confirm deployment

4. **For Production with File Storage:**
   - Integrate Cloudinary or AWS S3
   - Modify file upload code to use cloud storage
   - Example with Cloudinary:
   ```bash
   pip install cloudinary
   ```

---

## Post-Deployment Checklist

### Security:
- [ ] Change `SECRET_KEY` in app.py
- [ ] Change admin password from default
- [ ] Review file upload permissions
- [ ] Enable HTTPS (most platforms do this automatically)

### Configuration:
- [ ] Update owner information
- [ ] Add social media links
- [ ] Upload owner profile photo
- [ ] Add initial resources

### Testing:
- [ ] Test admin login
- [ ] Test file upload
- [ ] Test resource viewing
- [ ] Test search functionality
- [ ] Test on mobile devices
- [ ] Test share functionality
- [ ] Verify view counter works
- [ ] Test all navigation links

### Monitoring:
- [ ] Set up error logging
- [ ] Configure backup strategy for database
- [ ] Monitor disk usage (for file uploads)
- [ ] Set up uptime monitoring

---

## Environment Variables for Production

Add these to your deployment platform:

```bash
SECRET_KEY=your-very-secret-key-change-this
ADMIN_PASSWORD=4129
FLASK_ENV=production
```

---

## Database Backup

### Manual Backup:
```bash
# Download database.db file from your server
# Store safely with date: database_backup_2024_01_15.db
```

### Automated Backup (Advanced):
- Set up cron job on server
- Use platform-specific backup tools
- Store in cloud storage (AWS S3, Google Cloud Storage)

---

## Custom Domain Setup

### For Render/Heroku/Railway:
1. Go to Settings → Custom Domain
2. Add your domain name
3. Update DNS records:
   - Type: CNAME
   - Name: www
   - Value: your-app.platform.com

### For PythonAnywhere:
1. Upgrade to paid plan
2. Go to Web tab
3. Add custom domain
4. Follow DNS instructions

---

## Troubleshooting Deployment Issues

### Issue: App crashes on startup
**Solution**: Check logs for errors, verify all dependencies in requirements.txt

### Issue: File uploads not working
**Solution**: 
- Check write permissions on static/resources folder
- For Vercel: Implement cloud storage solution

### Issue: Database not persisting
**Solution**: 
- Ensure database.db is in writable directory
- Some platforms need persistent storage configuration

### Issue: Static files not loading
**Solution**: 
- Verify static folder configuration
- Check URL routing for /static/ path

### Issue: Admin login not working
**Solution**: 
- Verify SECRET_KEY is set
- Check session configuration
- Clear browser cookies

---

## Recommended Platform Summary

| Platform | Best For | File Storage | Complexity | Free Tier |
|----------|----------|--------------|------------|-----------|
| **Render** | Production use | ✅ Persistent | Easy | ✅ Good |
| **PythonAnywhere** | Beginners | ✅ Persistent | Easy | ✅ Limited |
| **Railway** | Modern apps | ✅ Persistent | Easy | ✅ Good |
| **Heroku** | Enterprise | ✅ With addon | Medium | ⚠️ Limited |
| **Vercel** | Static/API | ❌ Serverless | Easy | ✅ Excellent |

**Recommendation**: Use **Render** or **PythonAnywhere** for this project due to file upload requirements.

---

## Support & Resources

- **Render Docs**: https://render.com/docs
- **PythonAnywhere Help**: https://help.pythonanywhere.com
- **Flask Deployment**: https://flask.palletsprojects.com/en/latest/deploying/
- **Railway Docs**: https://docs.railway.app

---

**Ready to deploy? Choose your platform and follow the steps above!** 🚀
