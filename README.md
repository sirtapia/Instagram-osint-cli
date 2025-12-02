Installation
Prerequisites

Python 3.8 or higher
Instagram account (for API authentication)
Git (for cloning the repository)

Step 1: Clone the Repository
bashgit clone https://github.com/sirtapia/Instagram-osint-cli.git
cd Instagram-osint-cli
Step 2: Create Virtual Environment
bash# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
Step 3: Install Dependencies
bashpip install -r requirements.txt
Step 4: Configure Credentials
Create a .env file in the root directory:
envINSTAGRAM_USERNAME=your_instagram_username
INSTAGRAM_PASSWORD=your_instagram_password
Important: Never commit your .env file to version control. It's already included in .gitignore.

Usage
Basic Command Structure
bashpython run.py [COMMAND] [OPTIONS]
Available Commands
CommandDescriptionprofileGet detailed profile informationmediaRetrieve recent posts and engagement datapatternsAnalyze posting patterns and best timesfollowersGet list of account followersfollowingGet list of accounts the user followsmutualFind mutual followers between two accountshashtagGet top posts for a specific hashtagbatchAnalyze multiple profiles at once
