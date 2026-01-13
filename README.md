# VDC-Tools
Community made tools for VDC community members, players, teams etc. can also be adapted to be used outside VDC. 

VDC is an NA based, community run VALORANT league for all skill levels. They offer a casually competitive season based environment without the need to make a team of your own.
More info [here](vdc.gg)

> [!NOTE]
> This project is a community-built, unofficial tool and is **not affiliated with, endorsed by, or partnered with VDC** in any way.  
It was created independently by the community for convenience and informational purposes only.

Content:
- League Simulation Script
- MMR Scraper
- Google Sheets Automated Standings & Tiebreaker System
- Google Sheets Automated ELO Rating & Standings System
- Team Manager – All-in-One Google Sheet


# League Simulation Script
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

# MMR Scraper
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

# Google Sheets Automated Standings & Tiebreaker System
> [!NOTE]
> This was built for VDC tiebreaker rules so it may not apply to different leagues.

This project is a Google Sheets–based automated standings, ranking, and tiebreaker calculation system designed specifically for VDC.  
It automatically calculates group standings, overall standings, and applies official VDC tiebreaker rules.

[Spreadsheet link](https://docs.google.com/spreadsheets/d/1iVqiCy_-m65NpP89y5CUFUeXKAkDZaXLG5w-slLKe_8/edit?usp=sharing)

[VDC tiebreaker ruleset](https://blog.vdc.gg/rulebook/)

---

### Setup Instructions

### 1. Make a Copy of the Spreadsheet

Before making any changes, create your own copy of the spreadsheet:

- File → Make a copy

---

### 2. Add Teams

1. Go to the `input` sheet  
2. Fill in the team names for Group A and Group B inside the yellow highlighted region

<img width="711" height="699" alt="image" src="https://github.com/user-attachments/assets/235b7c79-6655-415d-9877-61f924d6095a" />

#### Adding More Teams Than the Highlighted Area

If you have more teams than the provided yellow region:

- Do not type on a new row below the highlighted area
- Right-click anywhere inside the yellow highlighted region
- Select **Insert new row**
  
<img width="522" height="546" alt="image" src="https://github.com/user-attachments/assets/e83d7f85-3df0-4d44-8343-1cbd05cc22b5" />


This ensures all formulas remain aligned and functional.

After inserting a new row:

- Drag down all formulas from the row directly above into the new row
- Continue dragging until the very end of the sheet

<img width="1891" height="772" alt="image" src="https://github.com/user-attachments/assets/6f3b3211-482a-4c0d-b756-60a8c8a4acaf" />

---

### 3. Dashboard Sheet Row Setup

For every extra team added:

1. Go to the `Dashboard` sheet  
2. Right-click inside the standings table itself  
3. Select **Insert new row**

<img width="573" height="475" alt="image" src="https://github.com/user-attachments/assets/a4f6e141-b265-4926-8a68-0d770540f899" />

4. Drag down the formula into the new row

Do this for:
- Group standings
- Overall standings

Errors that appear at the bottom of the tables can be ignored.  
They will automatically disappear once the initial yellow highlighted region in the `input` sheet is fully populated.

---

### 4. Enter Match Results

In the `input` sheet:

- Fill in the blue highlighted region with:
  - Team names
  - Match scores
  - Matchday information
  - Any additional match data

Once entered, all standings and tiebreakers will update automatically.

---

### Simulation Results Sheet

A `Simulation Results` sheet is included.

You can copy and paste simulation outputs from the earlier simulation project into this sheet to preview projected standings and playoff chances

# Google Sheets Automated ELO Rating & Standings System

This project is a Google Sheets–based ELO rating system that automatically calculates team ratings from match results and converts them into live standings.  
It also tracks historical ELO data and visualizes rating changes over time using built-in graphs and statistics.

[Spreadsheet here](https://docs.google.com/spreadsheets/d/12b_lDNUbYqxHpNHtPxpJ_OTiewDC5RRBlatlvbtVSlw/edit?usp=sharing)

---

### Setup Instructions

### 1. Make a Copy of the Spreadsheet

Before editing, create your own copy:

- File → Make a copy

---

### 2. Initial Configuration (Setup Sheet)

1. Go to the `setup` sheet  
2. Fill in all **yellow highlighted cells** with the required configuration information

Only edit highlighted cells. All other cells may contain formulas.

<img width="464" height="163" alt="image" src="https://github.com/user-attachments/assets/a6eaaab3-4afb-4141-ac1c-3006cb6faad1" />


---

### 3. Enter Match Results

1. Go to the `match results` sheet  
2. Fill in match data inside the **yellow highlighted region**
   - Teams
   - Scores
   - MMR Values

<img width="1851" height="551" alt="image" src="https://github.com/user-attachments/assets/8f767390-7ce6-4ec0-85ad-0b0a3e8c983b" />

Once entered, ELO ratings, standings, and graphs will update automatically.

---

### Importing Match Results from the Automated Standings Tracker (Optional)

If you already use the [**Automated Standings & Tiebreaker System**](https://docs.google.com/spreadsheets/d/1iVqiCy_-m65NpP89y5CUFUeXKAkDZaXLG5w-slLKe_8/edit?usp=sharing), you can import match data directly using Google Sheets’ `IMPORTRANGE` feature to cover everything except MMR values.

### Example Usage

In the `match results` sheet, select the first yellow input cell and use: 

`=IMPORTRANGE(
"https://docs.google.com/spreadsheets/d/1iVqiCy_-m65NpP89y5CUFUeXKAkDZaXLG5w-slLKe_8/edit
",
"input!A2:B"
)`


- Replace the range (`A2:B`) with the exact columns used for match results and the link with your actual public google sheets link (Share -> General Access -> Anyone with the link -> Copy Link)
- The first time you use `IMPORTRANGE`, Google Sheets will prompt you to **Allow access**

After linking, match results will sync automatically.

---

### Formula Expansion (Important)

### Match Results Sheet

After initial setup, at the bottom of the `match results` sheet:

- Drag down all formula cells
- Continue dragging until **Column A shows the error**: `Out of Range`

This ensures all future matches are supported correctly.

<img width="567" height="711" alt="image" src="https://github.com/user-attachments/assets/1b6c9b3e-9a3f-40fe-882c-b6ee5ea5a4b0" />

---

### Current Stats + Historical Rating Sheet

For additional teams or matchdays:

- Always **right-click and use Insert new row or Insert new column**
- Then drag existing formulas into the new cells

This applies to:
- Elo rating standings
- Historical ELO calculations

Failure to insert rows/columns correctly may break formulas.

---

### Historical Rating Graph

The `Historical Rating Graph` sheet is fully customizable.

You may:
- Change line colors to match team branding
- Adjust axis scale
- Hide or show specific teams
- Modify labels and legends

These edits do not affect calculations.

# Team Manager – All-in-One Google Sheet

This project is an all-in-one Google Sheets tool designed to help manage a VDC team.  
It centralizes map pool analysis, match history, roster MMR checks, and agent composition planning into a single spreadsheet.

[Spreadsheet link here](https://docs.google.com/spreadsheets/d/1SWhro6UYdIzxZ5x-PP6vxIt23eZ_uJ9_1a1J2lPUx9E/edit?usp=sharing)

---

## Features

- Map pool strength analysis and recommendations
- Match history tracking (officials and scrims)
- Roster MMR limit checking
- Agent composition planning per map

---

## Setup Instructions

### 1. Make a Copy of the Spreadsheet

Before editing, create your own copy:

- File → Make a copy

---

## Sheet Overview & Usage

### 1. Map Pool Sheet

The `Map Pool` sheet helps identify your team’s strongest maps.

#### Setup Steps

1. First, go to the `Agent Comps` sheet  
2. Checkmark every map that is currently in the active VDC map pool  
3. Go back to the `Map Pool` sheet  
4. Fill in cells **B3 through L8** with:
   - Player names
   - Player roles
   - A rating for each map from **1–10**
     - 1 = worst map
     - 10 = best map

Once filled, the table underneath will automatically recommend your best maps based on team strength.

<img width="1821" height="774" alt="image" src="https://github.com/user-attachments/assets/5bab949b-62ff-4d50-b1fe-14a4e7703c2d" />

---

### 2. Input Sheet (Optional)

The `Input` sheet is optional but recommended.

- Enter all matches your team has played together
- Includes:
  - Official matches
  - Scrims

This data is used by the `Map Pool` system to improve map recommendations and better reflect real performance.

---

### 3. MMR Sheet

The `MMR` sheet is used to quickly compare different roster combinations and check if they fit within the allowed MMR limit.

<img width="783" height="699" alt="image" src="https://github.com/user-attachments/assets/d9709811-a5cb-4e9c-92d2-3ef04590bcd6" />


#### Important Setup Step

- Change the value in cell **D16** (grey cell) to match your league’s actual MMR limit

<img width="236" height="167" alt="image" src="https://github.com/user-attachments/assets/eb620970-a567-447d-908e-be3d06447126" />

- Make sure all main players are entered in the `Map Pool` sheet first

After updating the limit, you can freely test roster combinations to see whether they are eligible.

---

### 4. Agent Comps Sheet

The `Agent Comps` sheet is used to plan agent assignments per map.

<img width="1462" height="633" alt="image" src="https://github.com/user-attachments/assets/1458038a-c54c-4abf-a3b7-da608d10cf98" />

- All maps are listed automatically
- Player names are pulled directly from the `Map Pool` sheet

Important notes:
- Make sure all players are entered in the `Map Pool` sheet first
- Select which agent each player should play on each map
- This sheet depends on correct setup in `Map Pool`

---

## Final Notes

- Only edit input cells intended for user data
- Do not overwrite formula cells

*Last updated 2026-1-12*
