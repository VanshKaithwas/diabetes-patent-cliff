# Diabetes Drug Patent Cliff Analyzer
by Vansh Kaithwas | Class 12 | Commerce + IT + IP

---

## What is this?

So in my IP class we were studying pharmaceutical patents and I got curious — when big diabetes drugs lose patent protection, how much money is actually at risk? Especially for German companies since I'm applying to universities there.

I used Python and SQL (which I study in Class 12 IT) to actually answer that question.

---

## The main thing I found

Boehringer Ingelheim — a German pharma company — has THREE diabetes drugs expiring in 2025. Jardiance, Synjardy, and Trajenta. Combined that's about $7 billion in revenue facing generic competition in one year.

I honestly didn't expect one company to have that much risk concentrated in a single year. That finding made the whole thing worth it.

---

## Files

```
diabetes_patents.csv   dataset I put together (15 drugs)
analysis.py            pandas analysis + charts
queries.sql            7 SQL queries on the data
```

---

## How to run

```bash
pip install pandas matplotlib
python analysis.py
```

For SQL — open diabetes_patents.csv in DB Browser for SQLite and run queries.sql

---

## Dataset

I compiled this from USPTO patent records, the FDA Orange Book, and company annual reports. Took me a while to cross check the expiry dates because some drugs have multiple patents.

15 drugs, 9 companies, 5 countries.

---

## What I used

- **Pandas** — cleaning the data, groupby analysis, filtering
- **Matplotlib** — 3 charts (bar, horizontal bar, pie)
- **SQL** — GROUP BY, HAVING, CASE WHEN queries
- All of this from my Class 12 IT syllabus + some googling

---

## Honest limitations

- Only 15 drugs, real market has hundreds
- Revenue numbers are approximate from public sources
- Haven't built a proper dashboard yet — that's next

---

## Why I focused on Germany

Boehringer Ingelheim is one of Germany's biggest pharma companies and they're privately owned which is unusual for a company this size. Since I'm applying to German universities I wanted to understand the German pharma industry specifically.

---

Vansh Kaithwas
Class 12 — Commerce + Information Technology + IP.
