# ANtio - A Robust Social Media Backend


## Project Description
ANtio is a comprehensive social media platform built using Python and Django for the backend and PostgreSQL for the database. The platform supports essential social media functionalities, including user authentication, profile management, post creation with image uploads, dynamic feed updates, liking posts, user search, and follow/unfollow features. This project showcases my backend development skills and my ability to create scalable and efficient server-side applications.

## Features
- **User Authentication**: Secure user signup, login, and logout functionality.
- **Profile Management**: Customizable user profiles.
- **Post Creation**: Users can create posts with image uploads.
- **Dynamic Feed**: Real-time post feed updates with like functionality.
- **Search Functionality**: Search for users and get user suggestions.
- **Follow/Unfollow**: Follow and unfollow other users to stay connected.

## Technologies Used
- **Backend**: Python, Django
- **Database**: PostgreSQL
- **Containerization**: Docker
- **Frontend**: HTML, CSS, JavaScript

## Installation and Setup

### Docker Setup
1. **Clone the repository**
   ```bash
   git clone https://github.com/aneebp/SocialMedia.git
   ```
   
2. **Navigate to the project directory**
   ```bash
   cd SocialMedia
   ```

3. **Build and run the Docker container**
   ```bash
   docker-compose up --build
   ```

### Django Setup (if not using Docker)
1. **Clone the repository**
    ```bash
   git clone https://github.com/aneebp/SocialMedia.git
   ```
2. **Navigate to the project directory**
    ```bash
     cd SocialMedia
   ```
3. **Create and activate a virtual environment**
    ```bash
     python -m venv venv
     source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
4. **Install the required packages**
    ```bash
   pip install -r requirements.txt
   ```
5. **Run the Django development server**
    ```bash
   python manage.py runserver
   ```

## Docker Usage
**The project is containerized using Docker, allowing for easy deployment and management.**
**A Docker image is available for the application, streamlining the setup process.**


### Summary:
- The **Django Setup** section is formatted as you requested, and it flows well with the overall structure of the `README.md`.
- Each command is clearly indicated in code blocks for easy copying.

