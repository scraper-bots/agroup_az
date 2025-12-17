# -*- coding: utf-8 -*-
"""
Pharmacy Data Analysis and Visualization
Generates analytical charts for the Azerbaijan pharmacy sector
"""

import sys
import io

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from collections import Counter
import os
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

# Create charts directory
CHARTS_DIR = 'charts'
os.makedirs(CHARTS_DIR, exist_ok=True)

# Load data
df = pd.read_csv('aptekonline.csv', encoding='utf-8-sig')

print(f"Loaded {len(df)} pharmacies")
print(f"Columns: {list(df.columns)}")

# ============================================================
# Data Preprocessing
# ============================================================

# Extract pharmacy chain/brand from name
def extract_chain(name):
    if pd.isna(name):
        return 'Other'
    name_upper = str(name).upper()
    if 'ZƏFƏRAN' in name_upper or 'ZEFARAN' in name_upper:
        return 'ZƏFƏRAN'
    elif 'KANON' in name_upper:
        return 'KANON'
    elif 'AZERİMED' in name_upper or 'AZERIMED' in name_upper or 'AZƏRİMED' in name_upper:
        return 'AZERİMED'
    elif 'GÜNƏBAXAN' in name_upper or 'GUNEBAXAN' in name_upper:
        return 'GÜNƏBAXAN'
    elif 'BİO' in name_upper or 'BIO' in name_upper:
        return 'BİO-KANON'
    elif 'APTEKONLINE' in name_upper:
        return 'APTEKONLINE'
    else:
        return 'Other'

df['chain'] = df['name'].apply(extract_chain)

# Extract city from region
def extract_city(region):
    if pd.isna(region):
        return 'Unknown'
    region_str = str(region)
    if 'Bakı' in region_str or 'Baki' in region_str:
        return 'Bakı'
    elif 'Gəncə' in region_str:
        return 'Gəncə'
    elif 'Sumqayıt' in region_str:
        return 'Sumqayıt'
    elif 'Mingəçevir' in region_str:
        return 'Mingəçevir'
    elif 'Lənkəran' in region_str:
        return 'Lənkəran'
    elif 'Şirvan' in region_str:
        return 'Şirvan'
    else:
        return region_str.split()[0] if region_str else 'Other'

df['city'] = df['region'].apply(extract_city)

# Extract district from region (for Baku)
def extract_district(region):
    if pd.isna(region):
        return 'Unknown'
    region_str = str(region)
    if 'rayonu' in region_str.lower():
        parts = region_str.split()
        for i, part in enumerate(parts):
            if 'rayonu' in part.lower() and i > 0:
                return parts[i-1]
    return 'Other'

df['district'] = df['region'].apply(extract_district)

# Parse insurance partners
def count_insurances(partners):
    if pd.isna(partners) or partners == '':
        return 0
    return len(str(partners).split(';'))

df['insurance_count'] = df['insurance_partners'].apply(count_insurances)

# Convert boolean columns
df['is_duty_24h'] = df['is_duty_24h'].fillna(0).astype(int)
df['has_optika'] = df['has_optika'].fillna(0).astype(int)

print("\nData preprocessing complete")
print(f"Chains found: {df['chain'].value_counts().to_dict()}")

# ============================================================
# CHART 1: Pharmacy Chains Market Share
# ============================================================
print("\nGenerating Chart 1: Market Share by Chain...")

fig, ax = plt.subplots(figsize=(12, 7))
chain_counts = df['chain'].value_counts()

# Combine small categories (less than 2%) into "Other"
threshold = len(df) * 0.02
main_chains = chain_counts[chain_counts >= threshold]
other_count = chain_counts[chain_counts < threshold].sum()
if other_count > 0:
    main_chains['Other'] = other_count

colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#95a5a6']

# Horizontal bar chart - cleaner than pie for this data
bars = ax.barh(main_chains.index[::-1], main_chains.values[::-1],
               color=colors[:len(main_chains)][::-1], height=0.6, edgecolor='white', linewidth=2)

ax.set_xlabel('Number of Pharmacies', fontsize=12, fontweight='bold')
ax.set_ylabel('')
ax.set_title('Pharmacy Market Share by Chain\n(Total: 276 pharmacies)', fontsize=14, fontweight='bold', pad=20)

# Add value labels on bars
for bar, count in zip(bars, main_chains.values[::-1]):
    pct = count / len(df) * 100
    # Label inside bar if big enough, outside if small
    if count > 20:
        ax.text(count - 2, bar.get_y() + bar.get_height()/2, f'{count}',
                va='center', ha='right', fontsize=12, fontweight='bold', color='white')
        ax.text(count + 2, bar.get_y() + bar.get_height()/2, f'({pct:.1f}%)',
                va='center', ha='left', fontsize=11, fontweight='bold', color='#333')
    else:
        ax.text(count + 2, bar.get_y() + bar.get_height()/2, f'{count} ({pct:.1f}%)',
                va='center', ha='left', fontsize=11, fontweight='bold', color='#333')

ax.set_xlim(0, max(main_chains.values) * 1.2)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Add grid for readability
ax.xaxis.grid(True, linestyle='--', alpha=0.7)
ax.set_axisbelow(True)

plt.tight_layout()
plt.savefig(f'{CHARTS_DIR}/01_market_share_by_chain.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

# ============================================================
# CHART 2: Geographic Distribution by City
# ============================================================
print("Generating Chart 2: Geographic Distribution...")

fig, ax = plt.subplots(figsize=(12, 6))
city_counts = df['city'].value_counts().head(15)

bars = ax.barh(city_counts.index[::-1], city_counts.values[::-1], color=sns.color_palette("viridis", len(city_counts)))

for i, (count, bar) in enumerate(zip(city_counts.values[::-1], bars)):
    ax.text(count + 0.5, bar.get_y() + bar.get_height()/2, str(count),
            va='center', fontsize=10, fontweight='bold')

ax.set_xlabel('Number of Pharmacies', fontsize=12)
ax.set_ylabel('City/Region', fontsize=12)
ax.set_title('Pharmacy Distribution by City/Region\n(Top 15 locations)', fontsize=14, fontweight='bold')
ax.set_xlim(0, max(city_counts.values) * 1.15)
plt.tight_layout()
plt.savefig(f'{CHARTS_DIR}/02_distribution_by_city.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

# ============================================================
# CHART 3: Baku Districts Analysis
# ============================================================
print("Generating Chart 3: Baku Districts Analysis...")

baku_df = df[df['city'] == 'Bakı']
district_counts = baku_df['district'].value_counts().head(12)

fig, ax = plt.subplots(figsize=(12, 6))
colors = sns.color_palette("coolwarm", len(district_counts))
bars = ax.bar(range(len(district_counts)), district_counts.values, color=colors)

ax.set_xticks(range(len(district_counts)))
ax.set_xticklabels(district_counts.index, rotation=45, ha='right', fontsize=10)

for bar, count in zip(bars, district_counts.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, str(count),
            ha='center', va='bottom', fontsize=10, fontweight='bold')

ax.set_xlabel('District', fontsize=12)
ax.set_ylabel('Number of Pharmacies', fontsize=12)
ax.set_title(f'Pharmacy Distribution in Baku by District\n(Total in Baku: {len(baku_df)} pharmacies)',
             fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(f'{CHARTS_DIR}/03_baku_districts.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

# ============================================================
# CHART 4: Chain Distribution by City
# ============================================================
print("Generating Chart 4: Chain Distribution by City...")

top_cities = df['city'].value_counts().head(6).index.tolist()
chain_city = df[df['city'].isin(top_cities)].groupby(['city', 'chain']).size().unstack(fill_value=0)

fig, ax = plt.subplots(figsize=(12, 7))
chain_city.plot(kind='bar', ax=ax, width=0.8, colormap='Set2')

ax.set_xlabel('City', fontsize=12)
ax.set_ylabel('Number of Pharmacies', fontsize=12)
ax.set_title('Pharmacy Chain Distribution Across Major Cities', fontsize=14, fontweight='bold')
ax.legend(title='Chain', bbox_to_anchor=(1.02, 1), loc='upper left')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(f'{CHARTS_DIR}/04_chain_by_city.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

# ============================================================
# CHART 5: 24h Duty Pharmacies Analysis
# ============================================================
print("Generating Chart 5: 24h Duty Pharmacies...")

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Pie chart of duty vs non-duty
duty_counts = df['is_duty_24h'].value_counts()
labels = ['Regular Hours', '24h Duty']
colors = ['#95a5a6', '#e74c3c']
axes[0].pie(duty_counts.values, labels=labels, autopct='%1.1f%%', colors=colors,
            explode=[0, 0.1], shadow=True, startangle=90)
axes[0].set_title(f'24-Hour Duty Pharmacies\n({duty_counts.get(1, 0)} out of {len(df)})',
                  fontsize=12, fontweight='bold')

# Duty pharmacies by chain
duty_by_chain = df[df['is_duty_24h'] == 1]['chain'].value_counts()
axes[1].barh(duty_by_chain.index[::-1], duty_by_chain.values[::-1], color='#e74c3c')
axes[1].set_xlabel('Number of 24h Pharmacies', fontsize=11)
axes[1].set_title('24-Hour Duty Pharmacies by Chain', fontsize=12, fontweight='bold')

for i, v in enumerate(duty_by_chain.values[::-1]):
    axes[1].text(v + 0.1, i, str(v), va='center', fontweight='bold')

plt.tight_layout()
plt.savefig(f'{CHARTS_DIR}/05_24h_duty_analysis.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

# ============================================================
# CHART 6: Optical Services (Optika) Analysis
# ============================================================
print("Generating Chart 6: Optical Services Analysis...")

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Overall optika availability
optika_counts = df['has_optika'].value_counts()
labels = ['No Optika', 'Has Optika']
colors = ['#bdc3c7', '#3498db']
axes[0].pie(optika_counts.values, labels=labels, autopct='%1.1f%%', colors=colors,
            explode=[0, 0.05], shadow=True, startangle=90)
axes[0].set_title(f'Pharmacies with Optical Services\n({optika_counts.get(1, 0)} out of {len(df)})',
                  fontsize=12, fontweight='bold')

# Optika by chain
optika_by_chain = df.groupby('chain')['has_optika'].agg(['sum', 'count'])
optika_by_chain['percentage'] = (optika_by_chain['sum'] / optika_by_chain['count'] * 100).round(1)
optika_by_chain = optika_by_chain.sort_values('percentage', ascending=True)

bars = axes[1].barh(optika_by_chain.index, optika_by_chain['percentage'], color='#3498db')
axes[1].set_xlabel('% with Optical Services', fontsize=11)
axes[1].set_title('Optical Services Availability by Chain', fontsize=12, fontweight='bold')
axes[1].set_xlim(0, 100)

for bar, pct in zip(bars, optika_by_chain['percentage']):
    axes[1].text(pct + 1, bar.get_y() + bar.get_height()/2, f'{pct:.0f}%',
                 va='center', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig(f'{CHARTS_DIR}/06_optical_services.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

# ============================================================
# CHART 7: Insurance Partnerships Analysis
# ============================================================
print("Generating Chart 7: Insurance Partnerships...")

# Count insurance companies
all_insurances = []
for partners in df['insurance_partners'].dropna():
    if partners:
        all_insurances.extend([p.strip() for p in str(partners).split(';') if p.strip()])

insurance_counts = Counter(all_insurances)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Insurance company frequency
ins_df = pd.DataFrame(insurance_counts.items(), columns=['Insurance', 'Count']).sort_values('Count', ascending=True)
bars = axes[0].barh(ins_df['Insurance'], ins_df['Count'], color=sns.color_palette("Greens_r", len(ins_df)))
axes[0].set_xlabel('Number of Partner Pharmacies', fontsize=11)
axes[0].set_title('Insurance Company Partnerships', fontsize=12, fontweight='bold')

for bar, count in zip(bars, ins_df['Count']):
    axes[0].text(count + 0.5, bar.get_y() + bar.get_height()/2, str(count),
                 va='center', fontsize=10, fontweight='bold')

# Distribution of insurance partnerships per pharmacy
ins_dist = df['insurance_count'].value_counts().sort_index()
axes[1].bar(ins_dist.index, ins_dist.values, color='#27ae60', edgecolor='white')
axes[1].set_xlabel('Number of Insurance Partners', fontsize=11)
axes[1].set_ylabel('Number of Pharmacies', fontsize=11)
axes[1].set_title('Insurance Partnership Distribution per Pharmacy', fontsize=12, fontweight='bold')

for i, v in enumerate(ins_dist.values):
    axes[1].text(ins_dist.index[i], v + 1, str(v), ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig(f'{CHARTS_DIR}/07_insurance_partnerships.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

# ============================================================
# CHART 8: Services Heatmap by Chain
# ============================================================
print("Generating Chart 8: Services Heatmap...")

# Create services summary by chain
services_summary = df.groupby('chain').agg({
    'has_optika': 'mean',
    'is_duty_24h': 'mean',
    'insurance_count': 'mean',
    'id': 'count'
}).rename(columns={
    'has_optika': 'Optika Rate',
    'is_duty_24h': '24h Duty Rate',
    'insurance_count': 'Avg Insurance Partners',
    'id': 'Total Pharmacies'
})

# Normalize for heatmap (except Total Pharmacies)
services_norm = services_summary.copy()
services_norm['Optika Rate'] = services_norm['Optika Rate'] * 100
services_norm['24h Duty Rate'] = services_norm['24h Duty Rate'] * 100

fig, ax = plt.subplots(figsize=(10, 6))
heatmap_data = services_norm[['Optika Rate', '24h Duty Rate', 'Avg Insurance Partners']].T

sns.heatmap(heatmap_data, annot=True, fmt='.1f', cmap='YlOrRd', ax=ax,
            linewidths=0.5, cbar_kws={'label': 'Value'})
ax.set_title('Services Comparison Across Pharmacy Chains\n(Optika & Duty rates in %, Insurance as avg count)',
             fontsize=12, fontweight='bold')
ax.set_ylabel('')
plt.tight_layout()
plt.savefig(f'{CHARTS_DIR}/08_services_heatmap.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

# ============================================================
# CHART 9: Geographic Coverage Map (Scatter)
# ============================================================
print("Generating Chart 9: Geographic Coverage Map...")

fig, ax = plt.subplots(figsize=(12, 10))

# Filter valid coordinates
valid_coords = df[(df['latitude'].notna()) & (df['longitude'].notna()) &
                  (df['latitude'] != '') & (df['longitude'] != '')]
valid_coords = valid_coords.copy()
valid_coords['latitude'] = pd.to_numeric(valid_coords['latitude'], errors='coerce')
valid_coords['longitude'] = pd.to_numeric(valid_coords['longitude'], errors='coerce')
valid_coords = valid_coords.dropna(subset=['latitude', 'longitude'])

# Color by chain
chain_colors = {'ZƏFƏRAN': '#FF6B6B', 'KANON': '#4ECDC4', 'AZERİMED': '#45B7D1',
                'GÜNƏBAXAN': '#96CEB4', 'BİO-KANON': '#DDA0DD', 'Other': '#95a5a6', 'APTEKONLINE': '#FFEAA7'}

for chain in valid_coords['chain'].unique():
    chain_data = valid_coords[valid_coords['chain'] == chain]
    color = chain_colors.get(chain, '#95a5a6')
    ax.scatter(chain_data['longitude'], chain_data['latitude'],
               c=color, label=f'{chain} ({len(chain_data)})',
               alpha=0.7, s=50, edgecolors='white', linewidth=0.5)

ax.set_xlabel('Longitude', fontsize=12)
ax.set_ylabel('Latitude', fontsize=12)
ax.set_title('Geographic Distribution of Pharmacies in Azerbaijan\n(Colored by Chain)',
             fontsize=14, fontweight='bold')
ax.legend(title='Chain', loc='upper left', bbox_to_anchor=(1, 1))
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f'{CHARTS_DIR}/09_geographic_map.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

# ============================================================
# CHART 10: Chain Growth Potential (Coverage Gaps)
# ============================================================
print("Generating Chart 10: Regional Coverage Analysis...")

# Calculate chain presence in each city
city_chain_presence = df.groupby(['city', 'chain']).size().unstack(fill_value=0)
total_by_city = city_chain_presence.sum(axis=1)

# Focus on cities with more than 2 pharmacies
significant_cities = total_by_city[total_by_city >= 3].index.tolist()
coverage_df = city_chain_presence.loc[significant_cities]

# Calculate market share per city
coverage_pct = coverage_df.div(coverage_df.sum(axis=1), axis=0) * 100

fig, ax = plt.subplots(figsize=(14, 8))
coverage_pct.plot(kind='bar', stacked=True, ax=ax, colormap='Set2', width=0.8)

ax.set_xlabel('City/Region', fontsize=12)
ax.set_ylabel('Market Share (%)', fontsize=12)
ax.set_title('Market Share by Chain Across Regions\n(Cities with 3+ pharmacies)', fontsize=14, fontweight='bold')
ax.legend(title='Chain', bbox_to_anchor=(1.02, 1), loc='upper left')
ax.set_ylim(0, 100)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(f'{CHARTS_DIR}/10_market_share_by_region.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

# ============================================================
# CHART 11: Baku Concentration Analysis
# ============================================================
print("Generating Chart 11: Urban vs Regional Analysis...")

# Calculate Baku vs Rest of Azerbaijan
baku_count = len(df[df['city'] == 'Bakı'])
other_count = len(df) - baku_count

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Pie chart
labels = ['Bakı (Capital)', 'Other Regions']
sizes = [baku_count, other_count]
colors = ['#e74c3c', '#3498db']
explode = [0.05, 0]

axes[0].pie(sizes, labels=labels, autopct=lambda pct: f'{pct:.1f}%\n({int(pct/100*sum(sizes))})',
            colors=colors, explode=explode, shadow=True, startangle=90)
axes[0].set_title('Capital vs Regional Distribution', fontsize=12, fontweight='bold')

# Chain comparison Baku vs Others
baku_chains = df[df['city'] == 'Bakı']['chain'].value_counts()
other_chains = df[df['city'] != 'Bakı']['chain'].value_counts()

comparison = pd.DataFrame({
    'Bakı': baku_chains,
    'Other Regions': other_chains
}).fillna(0)

x = np.arange(len(comparison))
width = 0.35

bars1 = axes[1].bar(x - width/2, comparison['Bakı'], width, label='Bakı', color='#e74c3c')
bars2 = axes[1].bar(x + width/2, comparison['Other Regions'], width, label='Other Regions', color='#3498db')

axes[1].set_xlabel('Chain', fontsize=11)
axes[1].set_ylabel('Number of Pharmacies', fontsize=11)
axes[1].set_title('Chain Presence: Capital vs Regions', fontsize=12, fontweight='bold')
axes[1].set_xticks(x)
axes[1].set_xticklabels(comparison.index, rotation=45, ha='right')
axes[1].legend()

plt.tight_layout()
plt.savefig(f'{CHARTS_DIR}/11_urban_vs_regional.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

# ============================================================
# Print Summary Statistics
# ============================================================
print("\n" + "="*60)
print("ANALYSIS SUMMARY")
print("="*60)

print(f"\nTotal Pharmacies: {len(df)}")
print(f"Unique Chains: {df['chain'].nunique()}")
print(f"Cities/Regions Covered: {df['city'].nunique()}")

print(f"\n24-Hour Duty Pharmacies: {df['is_duty_24h'].sum()} ({df['is_duty_24h'].mean()*100:.1f}%)")
print(f"Pharmacies with Optika: {df['has_optika'].sum()} ({df['has_optika'].mean()*100:.1f}%)")
print(f"Pharmacies with Insurance Partners: {(df['insurance_count'] > 0).sum()} ({(df['insurance_count'] > 0).mean()*100:.1f}%)")

print(f"\nBakı Concentration: {baku_count} pharmacies ({baku_count/len(df)*100:.1f}%)")

print(f"\nChain Distribution:")
for chain, count in df['chain'].value_counts().items():
    print(f"  {chain}: {count} ({count/len(df)*100:.1f}%)")

print(f"\nAll 11 charts saved to '{CHARTS_DIR}/' folder")
print("="*60)
