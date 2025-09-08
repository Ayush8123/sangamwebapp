# Ujjain Mahakumbh - Sacred Streams

A comprehensive web application for the Ujjain Mahakumbh experience, featuring an interactive scrolly-telling story and family safety features.

## Features

### 🏠 Home Page
- Beautiful landing page with Ujjain Mahakumbh introduction
- Navigation to all major sections
- Feature preview cards

### 📖 Sacred Streams (Interactive Story)
- **8 Animated Scenes** with GSAP-powered scroll animations
- **Golden yellow typography** for authentic spiritual feel
- **Scene descriptions** from the ancient Kumbh Mela legend
- **Smooth transitions** between scenes with scroll/touch controls
- **Responsive design** for all devices

### 👨‍👩‍👧‍👦 Family Safety Features
- **User Registration & Login** system
- **Family member management** - add and track family connections
- **Emergency SOS alerts** - notify family members in emergencies
- **SOS history tracking** - view past emergency alerts

### 🎨 Design Features
- **Sacred color scheme** - Gold, saffron, and indigo
- **Modern UI/UX** with Tailwind CSS
- **Smooth animations** and transitions
- **Mobile-responsive** design
- **Accessibility** considerations

## Story Scenes

1. **The Devas' Curse** - The beginning of the cosmic struggle
2. **The Quest for Amrita** - The search for immortality
3. **The Great Churning** - The cosmic ocean churning begins
4. **Lord Vishnu's Support** - The Kurma Avatar intervention
5. **The Poison and the Sacrifice** - Shiva's ultimate sacrifice
6. **The Arrival of Amrita** - The nectar emerges
7. **The Final Trick** - Mohini's divine deception
8. **The Legacy of the Drops** - The birth of Kumbh Mela

## Technical Stack

- **Backend**: Flask (Python)
- **Database**: Firebase Firestore
- **Frontend**: HTML5, CSS3, JavaScript
- **Animations**: GSAP (GreenSock)
- **Styling**: Tailwind CSS
- **Fonts**: Inter (Google Fonts)

## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd web_app
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Firebase**
   - Place your Firebase service account JSON file as `firebase_service_account.json`
   - Update the configuration in `config.py` if needed

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   - Open your browser and go to `http://localhost:5000`
   - The home page will load with navigation to all features

## Usage

### For Visitors
1. **Explore the Story**: Click "Begin Sacred Journey" to experience the interactive story
2. **Learn about Ujjain**: Read about the spiritual significance on the home page
3. **Register**: Create an account to access family safety features

### For Registered Users
1. **Login**: Use your User ID to access the app
2. **Add Family**: Manage your family connections for safety
3. **Emergency SOS**: Use the SOS feature to alert family members
4. **View History**: Check your SOS alert history

## API Endpoints

- `POST /api/register` - User registration
- `POST /api/login` - User login
- `GET /api/@<user_id>/family` - Get family members
- `POST /api/@<user_id>/add_family` - Add family member
- `POST /api/@<user_id>/sos` - Trigger SOS alert
- `GET /api/@<user_id>/sos/history` - Get SOS history

## File Structure

```
web_app/
├── api/                    # API blueprints
│   ├── auth.py            # Authentication endpoints
│   ├── family.py          # Family management
│   └── sos.py             # SOS functionality
├── assets/                # Story images and script
│   ├── scene 1.png        # Story scene images
│   ├── scene 2.png
│   ├── ...
│   ├── scene 8.png
│   └── script.txt         # Story descriptions
├── templates/             # HTML templates
│   ├── home.html          # Landing page
│   ├── story.html         # Interactive story
│   └── index.html         # Main app interface
├── app.py                 # Flask application
├── config.py              # Configuration
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is created for the Ujjain Mahakumbh hackathon and is intended for educational and spiritual purposes.

## Support

For support or questions, please contact the development team or create an issue in the repository.

---

**Sacred Streams** - Experience the divine journey of Ujjain Mahakumbh through interactive storytelling and modern technology.
