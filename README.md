# Instagram OSINT CLI

A command-line tool for gathering OSINT (Open-Source Intelligence) from Instagram using automation and pattern analysis.

---

## 📦 Installation

### **Prerequisites**

- Python 3.8 or higher  
- Instagram account (for API authentication)  
- Git (for cloning the repository)

---

### **Step 1: Clone the Repository**

```bash
git clone https://github.com/sirtapia/Instagram-osint-cli.git
cd Instagram-osint-cli
```
### **Step 2: Create Virtual Environment**
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate

### **Step 3: Install Dependencies**
```bash
pip install -r requirements.txt
```
### **Step 4: Configure Credentials**
```env
INSTAGRAM_USERNAME=your_instagram_username
INSTAGRAM_PASSWORD=your_instagram_password
```
#Important: Never commit your .env file to version control.It is already included in .gitignore

### **Basic Command Structure**
```bash
python run.py [COMMAND] [OPTIONS]
```

### **Available Commands**
| Command     | Description                                        |
| ----------- | -------------------------------------------------- |
| `profile`   | Get detailed profile information                   |
| `media`     | Retrieve recent posts and engagement data          |
| `patterns`  | Analyze posting patterns and best engagement times |
| `followers` | Get list of account followers                      |
| `following` | Get list of accounts the user follows              |
| `mutual`    | Find mutual followers between two accounts         |
| `hashtag`   | Get top posts for a specific hashtag               |
| `batch`     | Analyze multiple profiles at once                  |

### **Troubleshooting**
| Issue                     | Solution                                                |
| ------------------------- | ------------------------------------------------------- |
| **Login Failed**          | Verify credentials in `.env` are correct                |
| **Rate Limiting**         | Wait a few minutes — Instagram limits request frequency |
| **"Status 201" Warnings** | Safe to ignore — API still handled successfully         |
| **Session Errors**        | Delete `session.json` and log in again                  |

### Built with: 
- [instagrapi](https://github.com/adw0rd/instagrapi)

## Author:
- GitHub: [@sirtapia](https://github.com/sirtapia)
- Email: cristian.tapiavalenz@gmail.com
- LinkedIn: [Cristian Tapia](https://www.linkedin.com/in/cristian-tapia-076a84326/)

  




