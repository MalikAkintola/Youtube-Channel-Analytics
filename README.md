# YouTube Channel Analytics

This project was designed to test and showcase my skills in web scraping, data mining, and reporting. Using the YouTube Data API v3, I scraped data from various YouTube channels and stored the information in a MySQL database. The project involved cleaning and structuring the data, then building a Power BI dashboard to visualize key metrics such as video views, likes, and comments.

The goal was to demonstrate my ability to automate data collection, model the data effectively, and create meaningful reports. The process was automated with Python scripts and scheduled to run at intervals using Windows Task Scheduler and an on-premises data gateway.

The main components of the script include collecting video data (like views, likes, comments, etc.), storing it in a relational database, and generating basic statistics like the number of subscribers for each channel.

<details>
  <summary><h2>Features</h2></summary>



- **Scrapes video data** from specified YouTube channels including:
  - Video ID
  - Publish date
  - Title
  - Category ID
  - Duration
  - View count
  - Like count
  - Comment count
  - URL
  - Thumbnail URL
- **Stores data** in a MySQL database.
- **Generates summary statistics** for the channels, such as:
  - Channel name
  - Subscriber count
  - Channel image link
- Allows for easy retrieval and storage of data for further analysis.
</details>

<details>
  <summary><h2>Requirements and Setup</h2></summary>
<h3>Requirements</h3>
  
- Python 3.x
- Required Python libraries:
  - `google-api-python-client`: To interact with the YouTube API.
  - `pymysql`: For interacting with the MySQL database.
  - `pandas`: For data manipulation and storing the scraped data in tabular form.

You can install the required libraries using `pip`:

```bash
pip install google-api-python-client pymysql pandas
```
- MySQL Database (for storing the scraped data)
  - A local MySQL instance must be set up. Create a database named `youtube` (or any other name of your choice, and modify the connection string in the code accordingly).


<h3>Setup</h3>

#### Obtain a YouTube Data API Key:

1. Go to the [Google Developers Console](https://console.developers.google.com/).
2. Create a new project.
3. Enable the YouTube Data API v3.
4. Generate an API Key and replace `'API CODE HERE'` in the script with your key.

#### Set Up MySQL Database:

1. Make sure your MySQL server is running.
2. Create a database (for example `youtube`).
   
   ```sql
   CREATE DATABASE youtube;
  
3. Make sure you have the correct username and password for connecting to MySQL.
4. Update the connection details in the script accordingly.

</details>

<details>
  <summary><h2>Running the Script</h2></summary>

1. Replace the `api_key` variable with your actual **YouTube Data API key**:

   ```python
   api_key = 'YOUR_API_KEY'
   
2. Add the YouTube channel IDs that you want to track. The script includes sample channels (e.g., mrbeastid, dudeperfectid, etc.).
  - You can add or remove channel IDs as needed.

Run the script by executing:

```bash
python youtube_channel_analytics.py
```
The script will:
  - Fetch video details for the specified channels.
  - Insert the data into the MySQL database.
  - Generate a CSV file (Channels.csv) with summary statistics for each channel.
</details>

<details>
  <summary><h2>Functions & Output</h2></summary>
<h3>Functions</h3>

### 🔹 `get_video_ids(channel_id)`
This function retrieves the **video IDs** of all videos from a given YouTube channel.

- **Input:**  
  - `channel_id` (*str*): The ID of the YouTube channel.

- **Output:**  
  - A **list** of video IDs.

---

### 🔹 `databaseinsertion(data)`
This function inserts the **scraped video data** into a MySQL database.

- **Input:**  
  - `data` (*Pandas DataFrame*): The video data to be inserted into the database.

- **Output:**  
  - `None` (Directly inserts data into the database).

---

### 🔹 `get_videos(channelids)`
This function collects **video data** for multiple channels.

- **Input:**  
  - `channelids` (*list of str*): A list of YouTube channel IDs.

- **Output:**  
  - Inserts the collected **video data** into the **MySQL database**.

---

### 🔹 `get_summary_statistics(channelids, channelnames, images)`
This function generates **summary statistics** for the specified channels and stores them in a CSV file.

- **Input:**  
  - `channelids` (*list of str*): List of YouTube channel IDs.  
  - `channelnames` (*list of str*): List of channel names corresponding to `channelids`.  
  - `images` (*list of str*): List of **image URLs** for the channels.

- **Output:**  
  - A **CSV file (`Channels.csv`)** containing the summary statistics.

---

## 📊 Output

### 🔹 **MySQL Database**
- A **table** named `videos` will be created with columns for video data (e.g., **video ID, publish date, view count, etc.**).

### 🔹 **CSV File (`Channels.csv`)**
- Contains **summary statistics** about the channels, including:
  - The **number of subscribers**.
  - The **channel's image link**.

### ✅ **Expected Output (`videos` table in MySQL)**

| videoid  | publisheddate | title           | categoryId | duration | viewCount | likeCount | commentCount | url                                      | thumbnailUrl                           | channelId                      |
|----------|--------------|----------------|------------|----------|-----------|-----------|--------------|------------------------------------------|----------------------------------------|--------------------------------|
| abc123   | 2025-01-01   | Sample Video 1 | 20         | PT15M    | 100000    | 2000      | 100          | [Watch Video](https://youtube.com/watch?v=abc123) | ![Thumbnail](https://youtube.com/thumb.jpg) | UCX6OQ3DkcsbYNE6H8uQQuVA |

</details>

<details>
  <summary><h2>Power BI</h2></summary>
  
- **Data Model**:
  -  Power BI was connected to the SQL database to extract the data.
  -  The data was modeled using Power BI's data model, which integrates the video data fetched from the YouTube API(in the database), and the csv file of subscribers count and channel details.
  - Key metrics, such as total views, total likes, and total comments, were included in the model to allow for comprehensive reporting.
- **DAX Measures**
  - A key dax procedure implemented allowed users to easily get a ranking of videos by either total likes, total views or total comments.

![Data Model Screenshot](files/model.jpg)  <!-- Replace with the correct path -->


## Publishing to Power BI Service

- After finalizing the report in Power BI Desktop, the report was published to the Power BI Service to enable sharing and collaboration.

## Setting Up an On-Premises Data Gateway

- To enable automatic refresh of the data in Power BI Service, an On-Premises Data Gateway was set up.
  - This gateway facilitates the refresh of data from the MySQL database to Power BI.
  - The gateway ensures the data model stays up-to-date by periodically syncing the data from the local database to the cloud-based Power BI Service.

## Automating the Python Script Execution

- The Python script used to scrape data from the YouTube API is scheduled to run at regular intervals using **Windows Task Scheduler**.
  - The script fetches fresh data from YouTube, which is then inserted into the MySQL database.
  - By using Windows Scheduler, the script is automatically executed at predefined intervals without manual intervention, ensuring the data remains current.

- **Steps to Automate the Python Script**:
  - Set up a task in Windows Task Scheduler to run the script on a schedule (e.g., daily).
  - Ensure the script is executed with the correct environment and dependencies.

By combining these elements, the entire system remains automated and ensures that Power BI is always working with the most up-to-date data, providing real-time insights into YouTube channel performance.

For Live dashboard [Click here](https://app.powerbi.com/view?r=eyJrIjoiYWNhMDAwMWItNzBkYy00MWE4LThiMDEtY2FhZTNlYjE1Nzk3IiwidCI6ImRlMTM3ZmFmLTVmMDQtNDI1OC04ZjRmLTdhNDg0NDNiM2JiZCIsImMiOjZ9)
</details>


