<h>**GTJ GO! The Ultimate Travel Safety Companion**</h>
---

## <h3>Table of Contents</h3>
- [About](#-about)
- [How Does GTJ GO! Work?](#-howdoesgtjgowork?)
- [Installation Guide](#-installationguide)
- [Contribution Guidelines](#-contributionguidelines)

## About
<p>GTJ Go is a travel guide made by women for women and solo travelers who value safety, convenience, and accessibility. GTJ Go is the convenient travel companion that offers live language translation, currency exchange figures, local public transportation routes and guides, packing planning guides, current weather guides, preparedness, and safety scores. GTJ Go calculates safety scores using the most current data about domestic violence, women's/solo walking safety, domestic violence laws, female homicide rates, crime rates, political freedom, and verified user ratings, and gives a percentage using a modern intelligent formula. Along with the overall score, GTJ GO! uses Artificial-Intelligence to curate safety information, cultural tips, and a variety of emergency numbers for that destination. </p>

![laptop](https://github.com/user-attachments/assets/9cb5c8b8-9cdf-46ef-834a-30b0bae8edb9)

## How Does GTJ GO! Work?
GTJGo works by utilizing database statistics and current API information together in a comprehensive formula to give an all-encompassing score. The score breakdown is as follows:
* Women's Safety accounts for 50% of the overall score, with factors being:
  -  Laws on domestic violence
  -  % of women who have experienced domestic violence
  -  Global gender gap index
  -  Socio and political attitudes toward violence against women (%)​
  -  Female homicide victims (per 100,000 women)​
* Crime Rates and Data account for 20% of the overall score
  -  Pulls from FBI crime statistics 
* Night safety accounts for 20% of the overall score
  -  Information gathered on the % of people who felt safe while walking alone during late hours
* User Reviews account for 10% of the overall score
  -  Reviews from trusted, verified users of GTJ GO! leaving star rating % and/or comments about a destination

---
## Installation Guide
<p>Install on your device:</p>

```pip install django djangorestframework amadeus python-dotenv```

```pip install psycopg2-binary```

<p>To run:</p>

```python manage.py runserver```

---
## Contribution Guidelines
**Pull Request Process**
- You may merge the Pull Request once you have the sign-off of at least two developers, or if you do not have permission to do that, you may request the second reviewer to merge it for you.
