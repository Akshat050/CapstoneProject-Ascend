
# ASCEND Project Deliverable

![Python version](https://img.shields.io/badge/python-3.8%2B-blue)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen)

## Overview

The ASCEND Project is a comprehensive data-driven initiative aimed at providing insightful business intelligence through the use of advanced analytics and software solutions. This project encompasses several key components, including data processing applications, interactive dashboards, and thorough documentation to guide users through the project's findings and methodologies.

## Background and Motivation

In today’s data-driven world, organizations often struggle to extract actionable insights from large volumes of data. The ASCEND Project was initiated to address this challenge by developing tools and processes that transform raw data into meaningful business intelligence. The project combines advanced data processing techniques with intuitive visualizations to help stakeholders make informed decisions.

## Project Components

### 1. Power BI Dashboard
The `capstone final BI.pbix` file contains an interactive Power BI dashboard that visualizes key metrics and trends uncovered during the project. This dashboard serves as the primary tool for business stakeholders to interact with and analyze the data.



### 2. Final Presentation
The `Capstone Final Presentation.pptx` is a comprehensive PowerPoint presentation that summarizes the project's objectives, methods, results, and conclusions. It is designed to be presented to stakeholders who need a high-level understanding of the project's outcomes.

### 3. Final Documentation
The `Final Documentation capstone.pdf` provides an in-depth written report of the project. It includes the project's background, objectives, methodologies, data analysis, and conclusions. This document is essential for anyone seeking to understand the project's technical and analytical details.

### 4. SAM Application
The `SAM application/` directory contains a Python-based Serverless Application Model (SAM) that processes data for the ASCEND Project. The application is structured with several key modules:

- **`data_processor/`**: Contains various scripts for data cleaning, processing, and translation.
- **`config.py`**: Configuration settings for the data processing tasks.
- **`template.yaml`**: SAM template defining the infrastructure and resources required by the application.
- **`requirements.txt`**: List of Python dependencies required to run the application.

### Key Files:
- `data_cleaner.py`: Script for cleaning and preprocessing data.
- `translations.py`: Handles the translation logic for multi-language support.
- `db.py`: Manages database interactions.

## Getting Started

### Prerequisites
- **Python 3.8+**
- **AWS CLI**: Required for deploying the SAM application.
- **Power BI Desktop**: To view and interact with the `.pbix` file.

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Akshat050/ascend-project.git
   cd ascend-project/SAM\ application/
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up AWS CLI**:
   Ensure that your AWS CLI is configured properly for deployment:
   ```bash
   aws configure
   ```

### Deploy the SAM Application

1. **Deploy**:
   ```bash
   sam deploy --guided
   ```

2. **Run the Data Processor**:
   ```bash
   python data_processor/data_cleaner.py
   ```

## Usage Example

After deploying the SAM application, you can trigger the data processing function by uploading a dataset to the specified S3 bucket. For example:

```bash
aws s3 cp sample_data.csv s3://your-s3-bucket-name/
```

The application will automatically process the file and store the cleaned data in the output bucket.

## How to Use

1. **Power BI Dashboard**: Open the `.pbix` file in Power BI Desktop to explore the interactive reports.
2. **Presentation**: Use the `.pptx` file to present project findings to stakeholders.
3. **Documentation**: Refer to the `.pdf` file for a detailed understanding of the project.
4. **SAM Application**: Follow the steps in the Getting Started section to deploy and use the data processing application.

## Contributors

This project was a collaborative effort made possible by the following team members:

- **Akshat Bhatt**
- **Dievya Shree**
- **Megha Bhagat**
- **Swathi Jakka**
- **Siddharth Alashi**

We worked together as a team, sharing responsibilities and contributing equally to the project's success.

