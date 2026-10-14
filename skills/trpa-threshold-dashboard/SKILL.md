---
name: trpa-threshold-dashboard
description: "TRPA Threshold Dashboard (thresholds.laketahoeinfo.org) reference. Use this skill when building charts or maps for a threshold indicator page, drafting indicator page copy, reading evaluation status, trend, and confidence for an indicator, or working with the ThresholdEvaluation GitHub Pages repo that hosts the embeds. Covers the 10 threshold categories and their theme colors, reporting categories, the 192 indicators, the four-year evaluation cycle (2011, 2015, 2019, 2023), the 13-section indicator page and the API fields behind each section, status and trend vocabulary, the anonymous internalapi routes, file conventions in trpa-agency/ThresholdEvaluation, and the cumulative accounting and compliance measures pages. Trigger on: threshold dashboard, threshold evaluation, threshold indicator, threshold standard, status and trend, thresholds.laketahoeinfo.org, ThresholdEvaluation repo, cumulative accounting dashboard, compliance measures, 2023 Threshold Evaluation, indicator page copy, Theil-Sen trend."
---

# TRPA Threshold Dashboard

Reference for [thresholds.laketahoeinfo.org](https://thresholds.laketahoeinfo.org/), the public record of TRPA's environmental threshold standards and the four-year evaluations against them. The CMS holds the narrative and the evaluation calls; TRPA supplies one chart or map per indicator as standalone HTML on GitHub Pages.

**Always pair with** `ltinfo-platform` for the shell, tokens, embed contract, and stack facts, and `trpa-dashboard-stack` for libraries. Run `trpa-dashboard-qa` before handing a URL to the LT Info admin. Sampled Oct. 13, 2026.

---

## The framework

Thresholds are the environmental goals adopted in 1982 under the Bi-State Compact. The evaluation runs every four years; 2023 is the eighth report (evaluation periods 2011, 2015, 2019, 2023, each with its own `ThresholdEvaluationPeriodID`; 2023 is period 4). The 2023 report assesses 140 current standards; the Tahoe Science Advisory Council led the peer review.

### Ten categories, each with a theme color

| ID | Category | Theme color | Goal statement (short) |
|---|---|---|---|
| 1 | Air Quality | `#9CC3EA` | strictest federal, state, or regional standards; visibility; less traffic |
| 2 | Fisheries | `#B94F41` | stream habitat, stream flows, 6,000 acres of excellent lake habitat |
| 3 | Recreation | `#F78814` | high-quality recreation experience, undeveloped shorezone, fair-share capacity |
| 4 | Scenic Resources | `#B0A843` | scenic travel route ratings and views |
| 5 | Soil Conservation | `#9A5710` | preserve natural SEZ, restore 25 percent of disturbed urban SEZ, coverage limits |
| 6 | Vegetation Preservation | `#415414` | forest diversity, uncommon plant communities, old growth, fuels, sensitive plants |
| 7 | Water Quality | `#0F3F6F` | 1960s clarity and algal levels |
| 8 | Wildlife | `#9E2220` | habitat for special interest species |
| 9 | Noise | `#675EA1` | single event and background noise by land use |
| 10 | Transportation and Sustainable Communities | `#DB5B00` | reduce auto dependence, cut GHG, increase mobility |

The theme color is the category's identity on the site: category page headers, breadcrumb accents, and the legend on the evaluation overview. Use it for the category's series in cross-category charts. Each category has a white icon at `/assets/img/threshold-icons/{CategoryName}-white-icon.png`.

### Hierarchy

Category, then reporting category, then indicator. The API lists 192 indicators, 132 active. By category: Water Quality 67, Vegetation Preservation 34, Noise 25, Air Quality 19, Wildlife 16, Soil Conservation 14, Fisheries 8, Scenic Resources 6, Recreation 2, Transportation and Sustainable Communities 1. Standard types: Numeric 97, Management with Numeric 51, Management 26, Non-Degradation 11, Policy Statement 7. Standards reported as "Implemented" were adopted as policy guidance and live in the Regional Plan and Code rather than as measurements.

### Evaluation vocabulary

Status (the background color of the reporting icon): Considerably Better Than Target, Somewhat Better Than Target, At or Somewhat Better Than Target, Somewhat Worse Than Target, Considerably Worse Than Target, Insufficient Data. For numeric standards the class comes from the percent divergence of the current value from the standard or interim target, usually the most recent year, sometimes the period average, which the page then says.

Trend: Rapid Improvement, Moderate Improvement, Little or No Change, Moderate Decline, Rapid Decline, Insufficient Data to Determine Trend. Trends use Theil-Sen robust linear regression; confidence of trend rests on the coefficient of determination and t-test significance.

Confidence: High, Moderate (shown as Medium in rationale text), Low. The combination rule stated on indicator 1: if one of status and trend confidence is high and the other low, overall is medium.

Icons combine status and trend: `/assets/img/threshold-icons/evaluationIcons/StatusTrendConfidence/{StatusKey}/{TrendKey}.png`, for example `ConsiderablyBetter/ModerateDecline.png`. The keys are the vocabulary without spaces (`ConsiderablyBetter`, `SomewhatWorse`, `LittleOrNoChange`, `RapidDecline`).

---

## Site map

| Route | Page | Notes |
|---|---|---|
| `/` | Evaluation Overview | ten category tiles, then the category, reporting category, indicator tree with 2011 to 2023 icons |
| `/threshold/categories/{CategoryName}` | Category | narrative, reporting category list; `CategoryName` is the API name without spaces (`AirQuality`, `ScenicResources`) |
| `/threshold/indicators/{ThresholdIndicatorID}` | Indicator | the 13-section page below |
| `/threshold/evaluations/2023` | Evaluation Executive Summary | director's letter, executive summary, status and trend summary by category, peer review |
| `/threshold/evaluations` | Past Evaluations | |
| `/threshold/compliance-measures/2023` | Compliance Measures | one embedded HTML table |
| `/threshold/cumulative-accounting/2023` | Cumulative Accounting Dashboard | Code 16.8.2 accounting: units of use, resource utilization, threshold attainment; 25 embedded tables and maps |
| `/threshold/about-the-indicators`, `/threshold/adaptive-management`, `/threshold/how-thresholds-are-evaluated` | About pages | rich text |

---

## The indicator page, section by section

The populated model is indicator 1, Highest 8-Hour Average Concentration of Carbon Monoxide. Sections render in this order, each as a card with the steel blue `#6c91a4` header. The right column shows which API field feeds it, for drafting copy and for reading the data.

| # | Section | API field |
|---|---|---|
| 1 | Breadcrumb: Evaluation Overview, Category, Reporting Category | `ThresholdCategoryDisplayName`, `ThresholdReportingCategoryDisplayName` |
| 2 | Indicator title | `IndicatorDisplayName` (short form `IndicatorShortName`) |
| 3 | Overview paragraph and image | `ThresholdIndicatorPublicDescription`, `OverviewImageFileResourceGUID`, `OverviewImageCaption` |
| 4 | STATUS panel, Summary and Sources tabs, chart, caption | `/indicators/{IndicatorID}/chart-data`: `ChartSourceUrl` (the embed), `ChartTitle`, `ChartSummary`, `ChartSources`, `ChartDescription` |
| 5 | {year} EVALUATION: Status, Trend, Confidence | evaluation detail: `ThresholdEvaluationStatusTypeName`, `...TrendTypeName`, `...ConfidenceTypeName` |
| 6 | APPLICABLE STANDARD: code and verbatim language | `ApplicableStandard`, `StandardNarrative`, `ThresholdStandardTypeName` |
| 7 | KEY POINTS | `KeyMessages` (HTML list) |
| 8 | EVALUATION MAP with caption | evaluation detail: `MapUrl` (the embed), `MapCaption`, `MapTypeID`, `HasMapDashboard` |
| 9 | ABOUT THE THRESHOLD: Relevance; Human and Environmental Drivers | `Relevance`, `HumanAndEnvironmentalDrivers` |
| 10 | DELIVERING AND MEASURING SUCCESS: EIP Action Priorities, EIP Indicators, Local and Regional Plans, Example EIP Projects, Monitoring Programs | `/threshold-indicators/{id}/related-entities` (typed list with `RelatedEntityUrl`) |
| 11 | RATIONALE DETAILS: Status Rationale; Trend Rationale | `StatusRationale`, `TrendRationale` |
| 12 | CONFIDENCE DETAILS: Confidence of Status, of Trend, Overall | `ConfidenceStatus`, `ConfidenceTrend`, `ConfidenceOverall` |
| 13 | ADDITIONAL FIGURES AND RESOURCES | `/threshold-evaluations/{evalId}/images`, `/documents`; `LearnMore`, `ReferencesContent` |

The evaluation detail also carries `Methods`, `AnalyticApproach`, `InterimTarget`, `TargetAttainmentDate`, management status fields, and `HistoricEvaluationPdfFileResourceInfoGuid` for the pre-platform PDF.

Draft copy for new pages in markdown, one file per indicator, with `> **TODO:**` markers on anything unresolved. The ForestHealth repo's `thresholds/` folder (indicators 189 to 193, with `_TEMPLATE.md` and `_INDEX.md`) is the model. Nothing with an open TODO gets pasted into the CMS.

---

## API routes

Base `https://internalapi.laketahoeinfo.org`, anonymous GET. Type and admin routes return 401.

| Route | Returns |
|---|---|
| `/threshold-categories` | 10 categories: `ThresholdCategoryID`, `ThresholdCategoryName`, `DisplayName`, `ThemeColor`, `GoalStatement`, descriptions |
| `/threshold-categories/{id}` | one category with `Narrative` and `AdditionalInfo` HTML (images inlined as base64, so 270 KB) |
| `/threshold-reporting-categories/by-threshold-category/{id}` | reporting categories with narrative (7 MB for Air Quality because of inlined images) |
| `/threshold-indicators` | 192 indicators: IDs, names, reporting category, category and theme color, standard type, `IsActive` |
| `/threshold-indicators/{id}` | the indicator record (fields in the table above) |
| `/threshold-indicators/{id}/related-entities` | EIP action priorities, EIP indicators, plans, example projects, monitoring programs |
| `/threshold-evaluations/by-indicator/{id}/latest/detail` | the latest evaluation (`ThresholdEvaluationID`, year, status, trend, confidence, rationales, map fields) |
| `/threshold-evaluations/{evalId}/images`, `/documents` | additional figures and attachments |
| `/indicators/{IndicatorID}/chart-data` | the Status chart registration: `ChartSourceUrl`, `ChartTypeID`, `ChartTitle`, `ChartSummary`, `ChartSources`, `CanBeChartedCumulatively`, `SwapChartAxes` |
| `/threshold-evaluation-summary/dashboard/by-year/{year}` | the executive summary sections tree (4.6 MB with embedded content) |
| `/threshold-compliance-measures/by-year/{year}` | compliance measures page content |
| `/cumulative-accounting/dashboard/by-year/{year}` | cumulative accounting sections tree with `ContentSourceURL` and `ContentHeight` per embed |

Note the two ID spaces: `ThresholdIndicatorID` (the page URL, 1 to 193) and `IndicatorID` (the platform-wide indicator the chart data hangs on, for example 64 for threshold indicator 1).

---

## What TRPA builds: the ThresholdEvaluation repo

[trpa-agency/ThresholdEvaluation](https://github.com/trpa-agency/ThresholdEvaluation), published at `https://trpa-agency.github.io/ThresholdEvaluation/`, default branch `master`. One file per chart or map, 600 HTML files as of 2026.

```
{year}/{Category}/Chart/{Draft|Final}/{Name}.html      the Status chart (chart-data ChartSourceUrl)
{year}/{Category}/Map/{Draft|Final}/{Name}.html        the Evaluation Map (evaluation MapUrl)
{year}/CumulativeAccounting/Table{N}_{Name}/           one folder or file per accounting table
{year}/CumulativeAccounting/ComplianceMeasures{year}_files/{year}_TVAL_Compliance_Measures.html
{year}/ExecutiveSummary/{Name}.html                     figures in the executive summary
```

Category folder names: `AirQuality`, `Fisheries`, `Noise`, `Recreation`, `Scenic`, `SoilConservation`, `Vegetation`, `WaterQuality`, `Wildlife`. Example registrations on indicator 1:

- Chart: `2023/AirQuality/Chart/Final/AirQuality_8hrCO.html`, rendered in an iframe about 400 by 400 px in the Status panel's left column.
- Map: `2023/AirQuality/Map/Final/AirQualityStation_CO.html`, about 435 by 300 px, `frameborder="0" allowfullscreen`.

Draft files are working copies; the CMS points only at Final. Move a file from Draft to Final when the evaluation call is approved, and never rename a Final file the CMS already references.

### Chart conventions

The threshold element answers one question: is the Region meeting the standard? So the chart shows the measured series and the standard.

- **Series** in `--primary #3e72b0` (or the category theme color when several categories share a page). Second series `#e49937`.
- **Standard or target** as a dashed `#4e4e4e` horizontal line labeled with the standard's value and code (for example "AQ1 standard, 6 ppm"). An interim target gets a second dashed line in `#989898`.
- **Evaluation period** shaded lightly (`#f4f3ef`) when the chart spans decades, so the reader sees which years the status call used.
- **Attainment coloring**, if used, follows the status scale: better `#188c16`, at or near `#efd13d`, worse `#be4c4c`, insufficient data `#8a8a8a`. These mirror the icon set's intent and were not sampled from the icon PNGs; keep them consistent across categories.
- **Hover** `x unified`. **Font** Lexend Deca. **Background** white. No title inside the plot; the CMS shows `ChartTitle`.
- **Table and CSV** behind a toggle, per the platform contract.
- Load Plotly from a CDN. The 2019 and 2023 charts are Python `write_html` exports with the library inlined (3.6 MB each, Open Sans, default Plotly template). New files follow the `ltinfo-platform` layout instead; do not copy the old ones.

### Map conventions

One map per evaluation, the extent of what was measured: monitoring stations, treated acres, habitat polygons. Gray or terrain basemap, the host overlay names (Watersheds, Jurisdictions, TRPA Boundary), category theme color for the subject layer, a plain legend, wheel zoom stopped. Existing public web maps for Vegetation Preservation are listed in `trpa-monitoring-dashboard`.

---

## Data flow

1. Partners and TRPA collect the data under the monitoring programs listed on the indicator page (section 10 links to `monitoring.laketahoeinfo.org`).
2. TRPA computes status and trend for the evaluation (`Monitoring/TrendStatusThreshold.ipynb` holds the Theil-Sen pattern) and enters the calls and rationales in the CMS.
3. TRPA renders the chart and map files into the ThresholdEvaluation repo and pushes.
4. The LT Info admin sets `ChartSourceUrl` on the indicator's chart data and `MapUrl` on the evaluation.

The old `GetThresholdEvaluations` WebServices route is dead; read evaluations from the routes above.

---

## Cumulative Accounting and Compliance Measures

Both pages are CMS section trees whose content is embedded HTML from the repo. Cumulative accounting (Code of Ordinances 16.8.2) covers units of use (residential units, commercial floor area, tourist accommodation units, recreation), resource utilization (VMT, trip ends, impervious coverage, water demand, sewage capacity, SEZ disturbance), and threshold attainment investments. The 2023 page embeds 25 items, `Table1_Summary` through `Table24_RentalCarMitigationFeeRevenueExpenses`, plus a water provider map and utility districts map. Each section carries `ContentHeight`, which sets the iframe height, so a table that grows needs the admin to raise it. The numbers come from the annual cumulative accounting cycle in `trpa-agency/Reporting`.

---

## Relationship to the other dashboards

- The **Monitoring Dashboard** describes how data is collected; this dashboard says whether the standard is met. A threshold element never grows tiles, narrative, or a status badge of its own, and a monitoring dashboard never repeats a status call.
- The **Climate Resilience Dashboard** links to threshold indicators for lake level, clarity, old growth, and VMT (its 1.3.a, 1.3.c, 2.1.b, 3.3.b) rather than duplicating them.
- The **Transportation Tracker** is the home for the data behind category 10.
