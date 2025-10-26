# AI Agent Platform UI

A modern, responsive web interface for interacting with the AI Agent API.

## Features

### 🏠 Welcome Page
- Clean, professional landing page with the HT brand identity
- Two main action buttons:
  - **Let's Chat**: Initialize a session and start chatting with the AI agent
  - **Add Documents**: Manage documents in ChromaDB

### 💬 Chat Interface
- Real-time chat with the AI agent
- Beautiful message bubbles with user/agent avatars
- Typing indicators for better UX
- Session management
- Auto-resizing text input
- Message timestamps
- Clear chat functionality

### 📁 Document Management
- Upload PDF documents to ChromaDB
- View all documents for a specific HR ID
- Delete documents
- Drag-and-drop file upload support
- Real-time document count and chunk statistics
- Visual feedback for all operations

## Design Features

### Color Scheme
- **Brand Color**: `#304870` - Professional blue used throughout the interface
- **Gradients**: Smooth gradients for buttons and headers
- **Clean Whites**: `#ffffff` and `#f5f7fa` for backgrounds
- **Semantic Colors**: Green for success, red for errors

### UI/UX Elements
- **Smooth Animations**: Fade-in, slide-in, and scale animations
- **Loading States**: Full-screen overlay with spinner for async operations
- **Toast Notifications**: Non-intrusive feedback for user actions
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Hover Effects**: Interactive feedback on all clickable elements
- **Icons**: Font Awesome icons for visual clarity
- **Shadows**: Layered shadows for depth perception

### Modern Components
- Gradient buttons with hover effects
- Card-based layouts
- Auto-resizing text areas
- File drag-and-drop zones
- Typing indicators in chat
- Session ID display
- Document cards with icons
- Error messages with contextual styling

## Usage

### 1. Start the Flask Application
```bash
python app.py
```

The server will start on `http://localhost:5000`

### 2. Open in Browser
Navigate to `http://localhost:5000` in your web browser

### 3. Using the Chat Feature
1. Click **"Let's Chat"** on the welcome page
2. Enter your User ID and Authentication Token
3. Click **"Initialize Session"**
4. Start chatting with the AI agent
5. Type messages and press Enter or click the send button

### 4. Managing Documents
1. Click **"Add Documents"** on the welcome page
2. Enter an HR ID (Healthcare Facility ID)
3. Click **"Load Documents"** to view existing documents
4. Upload new PDF files by clicking the upload zone or dragging files
5. Delete documents by clicking the delete button

## API Integration

The UI integrates with the following API endpoints:

- **POST** `/api/v1/pds/initialize` - Initialize a new session
- **POST** `/api/v1/pds/chat/<session_id>` - Send messages to the agent
- **POST** `/api/v1/pds/documents` - Upload documents
- **GET** `/api/v1/pds/documents/<hr_id>` - List documents
- **DELETE** `/api/v1/pds/documents` - Delete documents

## File Structure

```
static/
├── css/
│   └── styles.css          # All styling and animations
└── js/
    └── app.js              # Frontend logic and API integration

templates/
└── index.html              # Main HTML structure
```

## Browser Compatibility

- Chrome (recommended)
- Firefox
- Safari
- Edge
- Mobile browsers (iOS Safari, Chrome Mobile)

## Customization

### Changing the Logo
Replace the text "HT LOGO" in the `.logo-placeholder` section with your actual logo image:

```html
<div class="logo-placeholder">
    <img src="/static/images/logo.png" alt="HT Logo">
</div>
```

### Modifying Colors
All colors are defined as CSS variables in `:root` in `styles.css`:

```css
:root {
    --brand-color: #304870;
    --brand-light: #4a6b99;
    --brand-dark: #1f3452;
    /* ... */
}
```

### Changing API URL
Update the `API_BASE_URL` constant in `app.js`:

```javascript
const API_BASE_URL = 'http://your-api-url/api/v1/pds';
```

## Features Highlights

✨ **Single Page Application** - No page reloads, smooth transitions
🎨 **Modern Design** - Gradient buttons, smooth animations, professional look
📱 **Fully Responsive** - Adapts to all screen sizes
🔄 **Real-time Updates** - Live feedback for all operations
🎯 **User-Friendly** - Intuitive navigation and clear CTAs
🚀 **Fast Performance** - Optimized CSS and minimal JavaScript
♿ **Accessible** - Semantic HTML and proper ARIA labels
🎭 **Engaging UX** - Typing indicators, toast notifications, loading states

## Tips

- Use **Shift + Enter** to add new lines in the chat input
- The chat auto-scrolls to the latest message
- File uploads show real-time progress
- All errors are displayed with clear, actionable messages
- Sessions persist during the chat, but are lost on page navigation

Enjoy using the AI Agent Platform! 🚀
