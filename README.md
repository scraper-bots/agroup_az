# Azerbaijan Pharmacy Sector Analysis

An in-depth analysis of the pharmacy sector in Azerbaijan based on data scraped from [aptekonline.az](https://aptekonline.az/pharmacies) - the country's leading online pharmacy platform.

## Dataset Overview

| Metric | Value |
|--------|-------|
| **Total Pharmacies** | 276 |
| **Pharmacy Chains** | 6 |
| **Cities/Regions Covered** | 38 |
| **Data Points per Pharmacy** | 22 |

### Data Columns
- **Identity**: id, name, description
- **Location**: region, address, latitude, longitude
- **Contact**: phone numbers (multiple formats)
- **Services**: 24h duty status, optical services
- **Partnerships**: insurance companies
- **Media**: images, gallery

---

## Key Insights & Analysis

### 1. Market Share by Chain

![Market Share by Chain](charts/01_market_share_by_chain.png)

**Key Findings:**
- **ZƏFƏRAN** dominates the market with **37.7%** share (104 pharmacies)
- **KANON** follows closely with **35.5%** (98 pharmacies)
- **AZERİMED** holds third position with **20.3%** (56 pharmacies)
- Together, the top 3 chains control **93.5%** of the market
- **GÜNƏBAXAN** is a smaller regional player with 5.4% share

**Insight**: The pharmacy market is highly consolidated with just 3 major chains controlling nearly all locations. This oligopolistic structure suggests high barriers to entry for new competitors.

---

### 2. Geographic Distribution

![Distribution by City](charts/02_distribution_by_city.png)

**Key Findings:**
- **Bakı (Baku)** has the highest concentration with **154 pharmacies** (55.8%)
- **Gəncə** (Ganja) ranks second with significantly fewer locations
- Regional cities have limited pharmacy coverage
- 38 unique cities/regions are served

**Insight**: There's a significant urban-rural gap in pharmacy accessibility. The capital hosts over half of all pharmacies, indicating potential underservice in regional areas.

---

### 3. Baku Districts Analysis

![Baku Districts](charts/03_baku_districts.png)

**Key Findings:**
- **Binəqədi**, **Xətai**, and **Sabunçu** districts have the highest pharmacy density
- **Nərimanov** and **Nizami** districts are well-served
- Some districts like **Yasamal** have moderate coverage
- Peripheral districts show lower pharmacy presence

**Insight**: Within Baku, pharmacy distribution follows population density and commercial activity patterns. Central and residential districts have better coverage.

---

### 4. Chain Distribution Across Cities

![Chain by City](charts/04_chain_by_city.png)

**Key Findings:**
- **ZƏFƏRAN** has the widest geographic reach, present in most cities
- **KANON** focuses heavily on Baku but has regional presence
- **AZERİMED** is predominantly Baku-centric
- **GÜNƏBAXAN** has limited presence outside the capital

**Insight**: ZƏFƏRAN's expansion strategy appears to prioritize geographic coverage, while competitors focus on urban density. This creates regional market monopolies in some areas.

---

### 5. 24-Hour Duty Pharmacies

![24h Duty Analysis](charts/05_24h_duty_analysis.png)

**Key Findings:**
- Only **9 pharmacies (3.3%)** operate 24 hours
- **ZƏFƏRAN** operates the most 24h locations
- **KANON** and **AZERİMED** have minimal 24h presence
- 24h service is predominantly available in Baku

**Insight**: The extremely low rate of 24-hour pharmacies (3.3%) represents a significant service gap. Emergency medication access outside regular hours remains a challenge for citizens, particularly in regional areas.

---

### 6. Optical Services (Optika)

![Optical Services](charts/06_optical_services.png)

**Key Findings:**
- **50 pharmacies (18.1%)** offer optical services
- **KANON** leads with the highest optika rate (~25%)
- **ZƏFƏRAN** and **AZERİMED** both offer optical services at ~15% rate
- **GÜNƏBAXAN** has the lowest optical service availability

**Insight**: Optical services represent a diversification strategy for pharmacies. The 18% market penetration suggests room for growth in this complementary service line.

---

### 7. Insurance Partnerships

![Insurance Partnerships](charts/07_insurance_partnerships.png)

**Key Findings:**
- **70 pharmacies (25.4%)** have insurance partnerships
- **Xalq sığorta** (People's Insurance) is the most common partner
- **Ata sığorta** and **Mega sığorta** follow in popularity
- Average of **3-6 insurance partners** per affiliated pharmacy
- **74% of pharmacies** have no insurance partnerships

**Insight**: Insurance integration is still developing in the pharmacy sector. The low adoption rate (25%) suggests significant growth potential for both insurers and pharmacy chains seeking to attract insured customers.

---

### 8. Services Comparison Heatmap

![Services Heatmap](charts/08_services_heatmap.png)

**Key Findings:**
- **ZƏFƏRAN** leads in 24h duty availability
- **KANON** has the highest optical service rate and insurance partnerships
- **GÜNƏBAXAN** has the highest insurance partnership density (4+ avg partners)
- **AZERİMED** maintains moderate service levels across categories

**Insight**: Each chain has developed distinct service positioning. KANON appears to pursue a "premium services" strategy, while ZƏFƏRAN focuses on accessibility (24h, geographic reach).

---

### 9. Geographic Coverage Map

![Geographic Map](charts/09_geographic_map.png)

**Key Findings:**
- Pharmacies cluster heavily around **Baku and Absheron peninsula** (40.3-40.5°N, 49.8-50.2°E)
- **Gəncə** (western Azerbaijan) forms a secondary cluster
- **Lənkəran** region in the south has sparse coverage
- Northern and western border regions have limited pharmacy presence

**Insight**: The geographic distribution reveals clear coverage gaps in rural and border regions. Citizens in these areas face longer travel distances for pharmacy access.

---

### 10. Regional Market Share

![Market Share by Region](charts/10_market_share_by_region.png)

**Key Findings:**
- **ZƏFƏRAN** achieves 100% market share in several regional cities
- **Bakı** is the only truly competitive market with all chains present
- **Gəncə** has multi-chain competition
- Many regional markets are effective monopolies

**Insight**: Outside major cities, single-chain dominance is common. This reduces competitive pressure and may affect pricing and service quality in regional markets.

---

### 11. Capital vs Regional Distribution

![Urban vs Regional](charts/11_urban_vs_regional.png)

**Key Findings:**
- **55.8%** of all pharmacies are in Baku
- **44.2%** serve the rest of the country
- **AZERİMED** is most Baku-concentrated (75%+ of locations in capital)
- **ZƏFƏRAN** has the most balanced urban-regional split

**Insight**: The Baku-centric distribution reflects both population concentration and economic factors. However, with 60% of Azerbaijan's population living outside Baku, regional pharmacy access remains inadequate relative to population needs.

---

## Summary Statistics

| Category | Value | Percentage |
|----------|-------|------------|
| Total Pharmacies | 276 | 100% |
| In Baku | 154 | 55.8% |
| 24-Hour Service | 9 | 3.3% |
| Optical Services | 50 | 18.1% |
| Insurance Partners | 70 | 25.4% |

### Chain Breakdown

| Chain | Count | Market Share |
|-------|-------|--------------|
| ZƏFƏRAN | 104 | 37.7% |
| KANON | 98 | 35.5% |
| AZERİMED | 56 | 20.3% |
| GÜNƏBAXAN | 15 | 5.4% |
| Other | 3 | 1.1% |

---

## Strategic Recommendations

Based on the analysis, several opportunities emerge:

1. **24-Hour Service Expansion**: With only 3.3% of pharmacies offering round-the-clock service, significant unmet demand exists for emergency medication access.

2. **Regional Expansion**: The 55.8% Baku concentration leaves regional markets underserved. Chains expanding into secondary cities could capture growing markets with limited competition.

3. **Insurance Integration**: 74.6% of pharmacies lack insurance partnerships. Developing these relationships could attract health-insured customers and provide competitive differentiation.

4. **Service Diversification**: Optical services show only 18.1% penetration. Adding diagnostic services, health consultations, or wellness products could increase revenue per location.

5. **Digital Integration**: As this data comes from an online platform, further integration of e-commerce, delivery services, and mobile apps represents growth opportunities.

---

## Data Source & Methodology

- **Source**: [aptekonline.az/pharmacies](https://aptekonline.az/pharmacies)
- **Scraping Date**: December 2024
- **Method**: Python web scraping (requests + BeautifulSoup)
- **Data Points**: 22 attributes per pharmacy including coordinates, services, and partnerships

### Files in Repository

| File | Description |
|------|-------------|
| `aptekonline.py` | Web scraper script |
| `analyze_pharmacies.py` | Data analysis and visualization script |
| `aptekonline.csv` | Raw scraped data (276 pharmacies) |
| `charts/` | Generated visualization charts |

---

## Usage

### Run the scraper:
```bash
python aptekonline.py
```

### Generate analysis charts:
```bash
python analyze_pharmacies.py
```

---

## License

This analysis is for educational and research purposes. Data sourced from publicly available information on aptekonline.az.
