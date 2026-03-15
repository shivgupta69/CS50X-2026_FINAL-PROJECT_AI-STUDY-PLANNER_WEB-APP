AI Study Planner

Overview

AI Study Planner is a web-based productivity application designed to help students organize their study tasks and generate structured study schedules. The application allows users to register, log in, add study tasks, and automatically create a study plan based on the tasks they provide. In addition, the application provides study analytics that visualize how much time the user spends on different study categories.

The primary goal of this project is to help students manage their study time efficiently by providing a simple task management system combined with automated scheduling and data visualization. By organizing tasks and displaying study patterns, the application helps users stay productive and track their learning progress.

This project was developed as the final project for the Harvard CS50x Introduction to Computer Science course.

⸻

Features

User Authentication

The application includes a secure authentication system that allows users to create accounts and log in. Passwords are securely stored using hashing to ensure user data protection.

Task Management

Users can add study tasks by specifying the task name, category (such as DSA, AI/ML, or Revision), and the duration in hours. All tasks are stored in a SQLite database and are associated with the logged-in user.

Automated Study Scheduling

The system automatically generates a study schedule based on the tasks entered by the user. The scheduling logic organizes tasks into a structured timeline, helping users plan their study sessions more effectively.

Study Analytics

The dashboard includes a bar chart that visualizes study hours across different categories. This allows users to track their learning patterns and understand where most of their study time is being spent.

Task Deletion

Users can remove tasks from the dashboard, allowing them to update or modify their study plan whenever needed.

⸻

Technologies Used

The project was built using the following technologies:

Python for backend programming
Flask as the web framework
SQLite as the database
HTML and CSS for the frontend structure and styling
JavaScript for client-side interaction
Chart.js for visualizing study analytics

Flask handles routing and server logic, SQLite stores user and task data, and Chart.js displays study statistics on the dashboard.

⸻

Project Structure

The project is organized with a main application file, a database initialization script, HTML templates for different pages, and static files for styling.

The templates folder contains the dashboard, login, register, layout, and schedule pages. The static folder contains the stylesheet used for styling the interface.

⸻

How to Run the Project

First, download or clone the project repository to your computer. Then navigate to the project directory in your terminal. Install the required dependencies listed in the requirements file. After that, run the database initialization script to create the required tables. Finally, start the Flask application and open the project in a web browser using the local server address.

⸻

Future Improvements

Possible future improvements include integrating machine learning for smarter study scheduling, adding calendar integration, implementing study reminders, and providing more advanced analytics for tracking long-term learning progress.