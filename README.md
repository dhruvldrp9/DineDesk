# DineDesk

DineDesk is an intelligent restaurant booking and delivery chatbot interface that provides a seamless experience for users to interact with restaurant services.

## Features

- Clean, modern UI inspired by ChatGPT
- Streaming response functionality
- Voice input ready (UI placeholder)
- Responsive design using TailwindCSS

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/DineDesk.git
cd DineDesk
```

2. Create and activate a virtual environment:
```bash
python -m venv env
source env/bin/activate  # On Windows, use: env\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running Locally

1. Start the Flask server:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

3. Click the microphone icon to see the streaming response in action.

## Project Structure

```
DineDesk/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── static/            # Static files
│   ├── css/
│   │   └── style.css  # Custom styles
│   └── js/
│       └── main.js    # Frontend JavaScript
└── templates/
    └── index.html     # Main HTML template
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.