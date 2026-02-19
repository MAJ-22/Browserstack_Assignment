# El País Scraper - BrowserStack Assignment

A comprehensive web scraping solution demonstrating Selenium automation, API integration, and cross-browser testing on BrowserStack. This project scrapes Spanish opinion articles from El País, translates them, and performs text analysis.

## 📋 Assignment Overview

This project fulfills the BrowserStack Customer Engineering technical assignment requirements:
- Web scraping with Selenium
- API integration (translation)
- Text processing and analysis
- Cross-browser testing on BrowserStack (5 parallel sessions)

## 🚀 Features

- **Article Scraping**: Extracts first 5 opinion articles from [El País](https://elpais.com/opinion/)
- **Multi-language Support**: Translates Spanish article titles to English using RapidAPI
- **Text Analysis**: Identifies words repeated more than twice across translated headers
- **Image Download**: Saves article cover images locally
- **Cross-browser Testing**: Runs on 5 different browser/device combinations simultaneously on BrowserStack
- **Comprehensive Logging**: Real-time progress tracking and error handling

## 🛠️ Technology Stack

- **Python 3.8+**
- **Selenium WebDriver**: Browser automation
- **BrowserStack**: Cloud-based cross-browser testing
- **RapidAPI (Deep Translate)**: Spanish-to-English translation
- **Threading**: Parallel execution
- **dotenv**: Environment variable management

## 📁 Project Structure

```
.
├── BS_scrapper.py          # Main scraper script
├── requirements.txt     
├── README.md              
├── images/                # Downloaded article images
└── articles_text/         # Scraped article content
    └── all_articles.txt   # Combined articles file
```

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd <repo-name>
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
# RapidAPI Credentials
RAPID_API_KEY=your_rapidapi_key_here

# BrowserStack Credentials
BS_USERNAME=your_browserstack_username
BS_ACCESSKEY=your_browserstack_access_key
```

**Getting Credentials:**
- **RapidAPI**: Sign up at [RapidAPI](https://rapidapi.com/), subscribe to [Deep Translate API](https://rapidapi.com/gatzuma/api/deep-translate1)
- **BrowserStack**: Get credentials from [BrowserStack Account Settings](https://www.browserstack.com/accounts/settings)

### 4. Install Chrome WebDriver

Ensure ChromeDriver is installed and in your PATH, or Selenium Manager will handle it automatically (Selenium 4.6+).

## 🎯 Usage

### Run the Complete Pipeline

```bash
python BS_scrapper.py
```

This will:
1. **Local Execution**: Scrape 5 articles locally, save images & text
2. **Translation**: Translate titles to English via RapidAPI
3. **Analysis**: Identify repeated words across titles
4. **BrowserStack**: Run same scrape across 5 parallel browser sessions

### Expected Output

```
============================================================
RUNNING LOCALLY
============================================================
[local] Starting scrape...
[local] --- Article 1 ---
Title: Cerrar la brecha educativa
Content preview: Cada vez menos jóvenes españoles abandonan sus estudios...

============================================================
TRANSLATED ARTICLE HEADERS
============================================================
1. Original  : Cerrar la brecha educativa
   Translated: Closing the educational gap

============================================================
REPEATED WORDS (appearing more than twice across all titles)
============================================================
  'the' — 4 times

============================================================
RUNNING ON BROWSERSTACK (5 parallel threads)
============================================================
[ElPais_Chrome_Windows11] ✓ PASSED — 5 articles scraped
[ElPais_Safari_macOS] ✓ PASSED — 5 articles scraped
...
```

## 🌐 BrowserStack Configuration

The script tests across:

| Browser | OS | Device |
|---------|-------|---------|
| Chrome (latest) | Windows 11 | Desktop |
| Safari (latest) | macOS Ventura | Desktop |
| Firefox (latest) | Windows 10 | Desktop |
| Safari | iOS 16 | iPhone 14 (Real Device) |
| Chrome | Android 13 | Samsung Galaxy S23 (Real Device) |

View live session recordings at: [BrowserStack Dashboard](https://automate.browserstack.com/dashboard)

## 📊 Output Files

### `articles_text/all_articles.txt`
Combined text file containing all 5 scraped articles with:
- Article title (Spanish)
- Article URL
- Full article body text

### `images/`
Directory containing cover images named by article title:
```
images/
├── Cerrar_la_brecha_educativa.jpg
├── Las_amenazas_electorales_de_Trump.jpg
└── ...
```


## 📝 Assignment Checklist

- ✅ Scrape first 5 articles from El País Opinion section
- ✅ Print title and content in Spanish
- ✅ Download and save cover images
- ✅ Translate article headers to English (RapidAPI)
- ✅ Print translated headers
- ✅ Analyze and print repeated words (count > 2)
- ✅ Run locally to verify functionality
- ✅ Execute on BrowserStack across 5 parallel threads
- ✅ Test on desktop + mobile browsers
- ✅ Upload source code to GitHub

## 🎓 Technical Skills Demonstrated

- **Web Scraping**: DOM navigation, CSS selectors, JavaScript execution
- **API Integration**: REST API calls, authentication, response parsing
- **Asynchronous Programming**: Multi-threading, parallel execution
- **Cloud Testing**: BrowserStack integration, session management
- **Error Handling**: Try-catch blocks, graceful degradation
- **Text Processing**: Regular expressions, word frequency analysis
- **Environment Management**: Secure credential storage with dotenv

## 📄 License

This project is submitted as part of the BrowserStack technical assessment.
