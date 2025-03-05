# Django Project with Tailwind CSS

This is a Django project that integrates Tailwind CSS for styling. It comes with a pre-configured theme folder, and all the necessary dependencies are already set up.

## Prerequisites

Before running the project, ensure that you have the following installed on your machine:

- Python 3.x
- Virtualenv
- Git

## Installation

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone <your-repo-url>
```

### 2. Create and Activate a Virtual Environment
It's recommended to work within a virtual environment to isolate project dependencies. Run the following commands:
```
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate
```

### 3. Install Dependencies
Install the required Python dependencies using pip:
```
pip install -r requirements.txt
```
### 4. Run Tailwind CSS
Since Tailwind CSS is already configured in the project, you don't need to install or initialize it. Simply run the following command to start the Tailwind CSS build process:
```
python manage.py tailwind start
```
### 5. Run the Django Server
Now, you can start the Django development server to run the application:
```
python manage.py runserver
```
You should now be able to access the application at http://127.0.0.1:8000/.
