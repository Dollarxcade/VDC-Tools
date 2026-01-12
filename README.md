# VDC-Tools
Community made tools for VDC community members, players, teams etc. can also be adapted to be used outside VDC.

## VDC League Simulation Script
> [!NOTE]
> This was made for a specific Valorant league that I participated in. Although the code is fairly simple and the tiebreaker logic is very similar to other Valorant leagues and VCT so if you have coding knowledge it's fairly simple to fix.

The **VDC Simulation Script** is a Python-based league simulator created specifically for a Valorant league called **VDC**. It simulates the outcome of an entire season by combining real past match results with simulated future matches.

The league uses a round-robin Best-of-2 format, meaning matches can end in ties on each matchday. For unplayed matches, the script applies a 50/50 match outcome logic to simulate future results based on existing match structure rather than team strength modeling.

Comments are included throughout the code to show where values can be edited to support Best-of-3 formats. While the script was designed for a specific league, its overall structure is similar to many other Valorant leagues and can be adapted by adjusting the relevant values and inputs.

### Limitations
- Designed **only for Valorant**
- Assumes the **MR13 format** (first to 13 rounds)
- Does **not** simulate overtime for future matches
- May require adjustments to fully support other leagues or formats

---

## How to Use

### 1. Install Required Software
- Download **Visual Studio Code**:  
  [VS Code Download](https://code.visualstudio.com/download)
- Install the **Python extension for VS Code**:  
  [Python Extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- Install required Python libraries by running the following in a terminal:
  `pip install pandas numpy`

---

### 2. Prepare the Match Data
Create a spreadsheet with the following columns:

1. Home Team  
2. Away Team  
3. Home Team Total Rounds Won  
4. Away Team Total Rounds Won  

- Leave both “Rounds Won” columns empty for **unplayed future matches**

Example format:  

![Spreadsheet Example](https://i.imgur.com/hxjtEDJ.png)

Export the spreadsheet as a **CSV file**.

---

### 3. Run the Simulation
1. Download the `VDC Simulation.py` file
2. Place it in the **same folder** as your CSV file
3. Open the `.py` file in **VS Code**
4. Edit the input filename near the top of the script  
   (default: `simulation.csv`)
5. Click the **▶ Run** button in the top-right corner of VS Code

---

### 4. View Results
- Simulation results will appear in the **VS Code console**
- A new **CSV file** containing the simulated standings/results will be created in the same folder as the script

## VDC MMR Scraper
> [!WARNING]
> This was made to only work for the VDC website as of **2026-01-10**

The primary goal of this tool is to allow users to **extract MMR values, Tiers, and Usernames** of players independently. It provides a way to gather league data without needing to be on the staff team or gaining access to sensitive administrative data. This tool bridges the gap created by current technical limitations in providing direct data exports.

### How It Works
The script uses **Playwright**, a professional-grade browser automation library, to interact with the website just like a human would.

* **Bypasses Security:** It launches a real instance of the Chromium browser, allowing you to manually complete Cloudflare "Verify you are human" checks.
* **Automated Loading:** Once you are past the security gate, the script handles the "Load More" logic, clicking the button automatically until the entire roster is rendered.
* **Targeted Extraction:** It scans the page specifically for Usernames, Tiers, and MMR values.
* **Data Cleaning:** It filters out banned or retired players who lack active stats and saves the final result to a `league_roster.csv` file.

### Installation & Setup

To keep things simple, we recommend using **Visual Studio Code (VS Code)**.

1. Install VS Code
  Download and install the code editor from the official site:
  **Download Link:** [VS Code Download](https://code.visualstudio.com/download)
2. Install the Python Extension
Open VS Code, click on the **Extensions** icon on the left sidebar (looks like four squares), and install:
  **Extension Link:** [Python for VS Code](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
3. Install Required Libraries
  Open your terminal inside VS Code (**Terminal > New Terminal**) and run these commands:

```bash
# Install the automation library
pip install playwright

# Install the browser engine required for the script
python -m playwright install chromium
```

### How To Use

1. Prepare the File: Create a new folder, download `VDC MMR.py` and put it into that new folder.
2. Prepare the Script: Right click on the file in file explorer and select **Open in Visual Studio Code**.
3. Run the Script: Click the "Run" triangle button in the top right corner of VS Code.
4. Human Verification: A browser window will open. Complete the Cloudflare prompt manually.
5. Optimize the List: To make the script go faster and avoid unnecessary data:
  - Go to the "League Status" dropdown on the webpage.
  - Select filters for GM/AGM, FA, RFA, and Signed.
  - This limits the list to active players only.
6. Trigger the Scrape: Once the filtered player list is visible, go back to the VS Code terminal at the bottom and press the Enter key.
7. Wait for Completion: The script will automatically click "Load more" until the end of the list is reached.
8. Find your Data: Once finished, a file named `league_roster.csv` will be created in the same folder as your script.

*Last updated 2026-1-12*
