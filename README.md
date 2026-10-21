# FUTURE_DS_03 – Marketing Campaign Conversion Analysis

## Project Overview
This project analyzes the Bank Marketing dataset using Python to understand campaign conversion performance and identify patterns associated with successful customer subscriptions.

## Objectives
- Calculate the overall campaign conversion rate.
- Compare conversion rates by contact method.
- Identify monthly campaign performance patterns.
- Analyze previous campaign outcomes.
- Compare conversion rates across customer age groups.

## Tools and Technologies
- Python
- Pandas
- Matplotlib
- Jupyter Notebook
- VS Code

## Dataset
The analysis uses the `bank-additional-full.csv` dataset, containing 41,188 records and 21 columns.

The target variable is `y`:
- `yes`: Customer subscribed.
- `no`: Customer did not subscribe.

## Key Findings
- **Overall conversion rate:** 11.27% (4,640 successful conversions out of 41,188 contacts).
- **Contact method:** Cellular contacts had a 14.74% conversion rate, compared with 5.23% for telephone contacts.
- **Campaign month:** March recorded the highest conversion rate at 50.55%, while May recorded the lowest at 6.43%.
- **Previous campaign outcome:** Customers with a previous successful outcome had a 65.11% conversion rate.
- **Age group:** Customers aged 65+ had a 46.85% conversion rate, based on 619 contacts.

## Recommendations
1. Evaluate cellular outreach as a potentially effective contact channel.
2. Investigate why conversion rates differ across campaign months.
3. Consider previous campaign outcomes when prioritizing customer outreach.
4. Validate age-related patterns before using them for campaign targeting.
5. Monitor both conversion rates and contact volumes when evaluating performance.

## Conclusion
The analysis highlights differences in conversion performance across contact methods, months, previous campaign outcomes, and age groups. These findings can help inform future campaign planning and further investigation.

The results show associations in the dataset and do not prove that any factor directly causes higher conversion rates.

## Project Files
- `task3_analysis.ipynb` – Data analysis, calculations, and visualizations.
- `bank-additional-full.csv` – Dataset used for the analysis.
- `README.md` – Project documentation.
