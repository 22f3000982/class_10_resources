# 🧪 Testing Guide

## Pre-Testing Checklist

- [x] Application is running on http://127.0.0.1:5000
- [ ] Browser is ready (Chrome/Firefox recommended)
- [ ] Admin password known: `4129`
- [ ] Test files ready (PDF, image, etc.)

---

## 🔍 Test Plan

### Phase 1: Initial Setup & Admin Login

#### Test 1.1: Homepage Access
**Steps:**
1. Open browser
2. Navigate to http://127.0.0.1:5000
3. Observe the homepage

**Expected:**
- ✅ Dark mode interface loads
- ✅ Navigation bar visible
- ✅ Action buttons displayed (Telegram, Instagram, Share, Practice MCQ)
- ✅ "No resources found" message (if first time)
- ✅ No errors in console

#### Test 1.2: Admin Login - Success
**Steps:**
1. Click "Admin Login" in navigation
2. Enter password: `4129`
3. Click "Login" button

**Expected:**
- ✅ Redirected to homepage
- ✅ Success message: "Login successful!"
- ✅ "Upload New" button appears
- ✅ "Logout" replaces "Admin Login"
- ✅ "Add Resource" appears in navbar

#### Test 1.3: Admin Login - Failure
**Steps:**
1. Navigate to login page
2. Enter wrong password: `0000`
3. Click "Login"

**Expected:**
- ✅ Stay on login page
- ✅ Error message: "Invalid password!"
- ✅ No access granted

---

### Phase 2: Owner Profile Management

#### Test 2.1: View Owner Profile
**Steps:**
1. Click "About Owner" in navigation
2. Observe the page

**Expected:**
- ✅ Default owner info displayed
- ✅ Placeholder photo or default avatar
- ✅ Social media links visible
- ✅ "Edit Information" button (admin only)

#### Test 2.2: Update Owner Profile
**Steps:**
1. As admin, go to "About Owner"
2. Click "Edit Information"
3. Update all fields:
   - Name: "Your Name"
   - Description: "Class 10 Teacher"
   - Contact: "teacher@school.com"
   - Telegram: "https://t.me/yourclass"
   - Instagram: "https://instagram.com/yourclass"
4. Click "Save Changes"

**Expected:**
- ✅ Success message appears
- ✅ Modal closes
- ✅ New information displayed
- ✅ Social links updated

#### Test 2.3: Upload Owner Photo
**Steps:**
1. Edit owner information
2. Choose a profile photo (JPG/PNG, <5MB)
3. Save changes

**Expected:**
- ✅ Photo uploads successfully
- ✅ Photo displays in circular frame
- ✅ File saved in static/owner/

---

### Phase 3: Resource Management

#### Test 3.1: Add Resource with File Upload
**Steps:**
1. As admin, click "Upload New"
2. Fill form:
   - Name: "Test Resource 1"
   - Link: (leave empty)
   - File: Upload a PDF (< 5MB)
3. Click "Upload Resource"

**Expected:**
- ✅ Success message: "Resource added successfully!"
- ✅ Redirected to homepage
- ✅ New resource card appears
- ✅ Shows file icon and filename
- ✅ View count shows 0
- ✅ File saved in static/resources/

#### Test 3.2: Add Resource with Link Only
**Steps:**
1. Click "Upload New"
2. Fill form:
   - Name: "Test Resource 2"
   - Link: "https://www.example.com"
   - File: (leave empty)
3. Submit

**Expected:**
- ✅ Resource created successfully
- ✅ Shows link icon
- ✅ No filename displayed

#### Test 3.3: Add Resource with Both File and Link
**Steps:**
1. Click "Upload New"
2. Fill form with both file and link
3. Submit

**Expected:**
- ✅ Both saved successfully
- ✅ File takes priority when viewing

#### Test 3.4: File Upload Validation - Size Limit
**Steps:**
1. Try to upload file > 5MB
2. Submit form

**Expected:**
- ✅ Error message or upload fails
- ✅ User notified about size limit

#### Test 3.5: File Upload Validation - File Type
**Steps:**
1. Try to upload .exe or .bat file
2. Submit

**Expected:**
- ✅ Error: "Invalid file type!"
- ✅ Resource not created

#### Test 3.6: Edit Resource
**Steps:**
1. As admin, click "Edit" on a resource
2. Change name: "Updated Resource Name"
3. Change link: "https://newlink.com"
4. Save

**Expected:**
- ✅ Success message
- ✅ Name updated on card
- ✅ Link updated
- ✅ File remains unchanged
- ✅ View count unchanged

#### Test 3.7: Delete Resource
**Steps:**
1. As admin, click "Delete" on a resource
2. Confirm deletion

**Expected:**
- ✅ Confirmation dialog appears
- ✅ After confirm: resource removed
- ✅ Success message
- ✅ File deleted from static/resources/
- ✅ Database entry removed

---

### Phase 4: User Features (Non-Admin)

#### Test 4.1: Logout and User View
**Steps:**
1. As admin, click "Logout"
2. Observe homepage

**Expected:**
- ✅ "Upload New" button hidden
- ✅ Edit/Delete buttons hidden
- ✅ Only "View" buttons visible
- ✅ Search bar still accessible
- ✅ Action buttons visible

#### Test 4.2: View Resource with File
**Steps:**
1. As user, click "View" on resource with file
2. Observe

**Expected:**
- ✅ File opens in new tab OR downloads
- ✅ View count increases by 1
- ✅ Return to homepage shows updated count

#### Test 4.3: View Resource with Link
**Steps:**
1. Click "View" on resource with link only
2. Observe

**Expected:**
- ✅ Redirected to external link
- ✅ Opens in new tab
- ✅ View count increases

#### Test 4.4: Multiple Views
**Steps:**
1. Click "View" on same resource 3 times
2. Check view count

**Expected:**
- ✅ Count increases each time
- ✅ Shows: 0 → 1 → 2 → 3

---

### Phase 5: Search Functionality

#### Test 5.1: Search - Found
**Steps:**
1. Add resources: "Math Chapter 1", "Science Notes", "Math Quiz"
2. Search: "Math"
3. Observe results

**Expected:**
- ✅ Only "Math Chapter 1" and "Math Quiz" displayed
- ✅ "Science Notes" hidden
- ✅ Search term shown in input
- ✅ "Clear search" link appears

#### Test 5.2: Search - Not Found
**Steps:**
1. Search: "xyz123nonexistent"
2. Observe

**Expected:**
- ✅ "No resources found" message
- ✅ Suggestion: "Try a different search term"
- ✅ Clear search option available

#### Test 5.3: Clear Search
**Steps:**
1. Perform search
2. Click "Clear search"

**Expected:**
- ✅ All resources displayed again
- ✅ Search input cleared
- ✅ URL updated

#### Test 5.4: Search - Case Insensitive
**Steps:**
1. Search: "MATH", "math", "MaTh"
2. Compare results

**Expected:**
- ✅ All return same results
- ✅ Case doesn't matter

---

### Phase 6: Social Features

#### Test 6.1: Telegram Button
**Steps:**
1. Click "Telegram" button on homepage
2. Observe

**Expected:**
- ✅ Opens Telegram link in new tab
- ✅ Uses link from owner settings

#### Test 6.2: Instagram Button
**Steps:**
1. Click "Instagram" button
2. Observe

**Expected:**
- ✅ Opens Instagram link in new tab
- ✅ Uses link from owner settings

#### Test 6.3: Share Button - Native Share
**Steps:**
1. On mobile or modern browser
2. Click "Share" button
3. Observe

**Expected:**
- ✅ Native share dialog opens
- ✅ Can share via apps
- ✅ URL included

#### Test 6.4: Share Button - Fallback
**Steps:**
1. On older browser
2. Click "Share"

**Expected:**
- ✅ Fallback: Link copied to clipboard
- ✅ Alert: "Link copied to clipboard!"

#### Test 6.5: Practice MCQ Page
**Steps:**
1. Click "Practice MCQ" button
2. Observe page

**Expected:**
- ✅ MCQ page loads
- ✅ Template/placeholder shown
- ✅ "Coming Soon" message or sample questions
- ✅ Back to Home link works

---

### Phase 7: Responsive Design

#### Test 7.1: Desktop View (1920x1080)
**Steps:**
1. Set browser to full screen desktop
2. Navigate site

**Expected:**
- ✅ 3-column resource grid
- ✅ All buttons in one row
- ✅ Navigation bar expanded
- ✅ Proper spacing

#### Test 7.2: Tablet View (768x1024)
**Steps:**
1. Resize browser or use device
2. Navigate site

**Expected:**
- ✅ 2-column resource grid
- ✅ Responsive navigation
- ✅ Action buttons wrap properly
- ✅ Readable text

#### Test 7.3: Mobile View (375x667)
**Steps:**
1. Use mobile device or emulator
2. Navigate site

**Expected:**
- ✅ 1-column resource grid
- ✅ Hamburger menu
- ✅ Full-width buttons
- ✅ Touch-friendly targets
- ✅ Proper spacing

#### Test 7.4: Mobile - Add Resource
**Steps:**
1. On mobile, add resource as admin
2. Test form

**Expected:**
- ✅ Form is usable
- ✅ File upload works
- ✅ All inputs accessible
- ✅ Buttons easy to tap

---

### Phase 8: Performance & Browser Testing

#### Test 8.1: Chrome
**Steps:**
1. Test all features in Chrome
2. Check console for errors

**Expected:**
- ✅ All features work
- ✅ No console errors
- ✅ Fast loading

#### Test 8.2: Firefox
**Steps:**
1. Test all features in Firefox

**Expected:**
- ✅ All features work
- ✅ Styling consistent

#### Test 8.3: Safari (Mac/iOS)
**Steps:**
1. Test on Safari

**Expected:**
- ✅ All features work
- ✅ File upload works
- ✅ Animations smooth

#### Test 8.4: Edge
**Steps:**
1. Test on Microsoft Edge

**Expected:**
- ✅ All features work
- ✅ Compatible

#### Test 8.5: Load Time
**Steps:**
1. Clear cache
2. Reload homepage
3. Check load time

**Expected:**
- ✅ Loads in < 3 seconds
- ✅ Resources load progressively

#### Test 8.6: Many Resources
**Steps:**
1. Add 50+ resources
2. Test homepage

**Expected:**
- ✅ Page still loads fast
- ✅ Scrolling is smooth
- ✅ Search still works well

---

### Phase 9: Security Testing

#### Test 9.1: Session Management
**Steps:**
1. Login as admin
2. Close browser
3. Reopen and visit site

**Expected:**
- ✅ Session persists (cookie-based)
- ✅ Still logged in

#### Test 9.2: Unauthorized Access
**Steps:**
1. Without logging in
2. Try to access: /add-resource directly

**Expected:**
- ✅ Redirected to login page
- ✅ Access denied

#### Test 9.3: SQL Injection Test
**Steps:**
1. In search: `' OR '1'='1`
2. In resource name: `'; DROP TABLE resources; --`
3. Submit

**Expected:**
- ✅ Treated as regular text
- ✅ No database damage
- ✅ Parameterized queries protect

#### Test 9.4: XSS Test
**Steps:**
1. In resource name: `<script>alert('XSS')</script>`
2. Save and view

**Expected:**
- ✅ Script not executed
- ✅ Displayed as text
- ✅ Auto-escaped by Jinja2

#### Test 9.5: File Path Traversal
**Steps:**
1. Try uploading file with name: `../../etc/passwd`
2. Submit

**Expected:**
- ✅ Filename sanitized
- ✅ Saved safely in resources folder
- ✅ No path traversal possible

---

### Phase 10: Error Handling

#### Test 10.1: Database Error
**Steps:**
1. Corrupt database.db file
2. Try to access site

**Expected:**
- ✅ Graceful error handling
- ✅ Or auto-recreate database

#### Test 10.2: Missing File
**Steps:**
1. Delete a resource file from static/resources/
2. Try to view that resource

**Expected:**
- ✅ Error message or 404
- ✅ App doesn't crash

#### Test 10.3: Large File Upload
**Steps:**
1. Try to upload 10MB file
2. Submit

**Expected:**
- ✅ Upload rejected
- ✅ Error message about size limit
- ✅ User informed

#### Test 10.4: Network Offline
**Steps:**
1. Disconnect internet
2. Try to use app

**Expected:**
- ✅ Local features work (localhost)
- ✅ External links fail gracefully
- ✅ CDN resources cached

---

## 📊 Test Results Template

### Test Session: [Date]
**Tester:** [Name]
**Browser:** [Chrome/Firefox/etc.]
**Device:** [Desktop/Mobile/Tablet]

| Test ID | Test Name | Status | Notes |
|---------|-----------|--------|-------|
| 1.1 | Homepage Access | ✅ Pass | |
| 1.2 | Admin Login Success | ✅ Pass | |
| 1.3 | Admin Login Failure | ✅ Pass | |
| 2.1 | View Owner Profile | ✅ Pass | |
| ... | ... | ... | ... |

### Issues Found:
1. [Issue description]
2. [Issue description]

### Overall Status:
- [ ] Ready for deployment
- [ ] Needs fixes

---

## 🎯 Critical Tests (Must Pass)

Before deployment, these MUST work:
- ✅ Admin login/logout
- ✅ Add resource with file
- ✅ View resource + count increment
- ✅ Search functionality
- ✅ Mobile responsiveness
- ✅ Delete resource
- ✅ Owner profile update

---

## 🐛 Common Issues & Solutions

### Issue: Can't login
**Solution:** 
- Check password is exactly `4129`
- Clear browser cookies
- Check SECRET_KEY in app.py

### Issue: File upload fails
**Solution:**
- Check file size < 5MB
- Verify file type allowed
- Check folder permissions

### Issue: Views don't increment
**Solution:**
- Check database write permissions
- Verify SQL query works
- Check transaction commit

### Issue: Search returns nothing
**Solution:**
- Check SQL LIKE query syntax
- Verify case-insensitive search
- Check resource names in database

---

## 📝 Testing Notes

- Test as both admin and regular user
- Test on multiple devices
- Test with real files (PDFs, images, etc.)
- Test with many resources (50+)
- Test all buttons and links
- Check console for errors
- Monitor network requests
- Test form validations
- Test edge cases

---

## ✅ Final Checklist Before Deployment

- [ ] All critical tests passed
- [ ] Tested on 3+ browsers
- [ ] Tested on mobile device
- [ ] No console errors
- [ ] Admin password changed
- [ ] SECRET_KEY changed
- [ ] Owner info updated
- [ ] Social links work
- [ ] Sample resources added
- [ ] Documentation reviewed
- [ ] Database backed up

---

**Happy Testing!** 🧪✨
