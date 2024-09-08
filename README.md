# Facebook Scraping Project

This project allows users to log into Facebook and scrape posts from Facebook groups or individual posts. After scraping, the project uses **Ollama** with **Llama 3 8B** to infer whether the scraped posts can be classified as leads or not. The number of posts to scrape is customizable through hyperparameters.

## Features

- **Facebook Login:** Securely login to Facebook to scrape data.
- **Scrape Facebook Groups or Posts:** Extract posts from groups or specific posts based on user preferences.
- **Hyperparameter Tuning:** Set the number of posts to scrape with user-defined parameters.
- **Lead Inference:** Utilize Ollama with Llama 3 8B to determine if a post qualifies as a lead.

## Prerequisites

- Python 3.8 or higher
- Facebook account (for logging in and scraping)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ahmedumersiddiqui/facebook-scraping-project.git
   cd facebook-scraping-project
2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
