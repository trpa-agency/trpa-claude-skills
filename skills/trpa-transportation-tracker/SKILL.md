---
name: trpa-transportation-tracker
description: "Lake Tahoe Info Transportation Tracker (transportation.laketahoeinfo.org) reference. Use when building a Data Trends embed, a funding or performance chart, or a project map for the tracker, reading transportation project, strategy, or funding data from the LT Info API, or connecting transportation monitoring data (bike and pedestrian counts, congestion, crashes, transit, traffic volumes, travel behavior) to it. Covers the site sections, the six strategies and their colors, project stages, the anonymous internalapi routes and JSON shapes, the embed content type, and the TRPA repos that produce the data. Trigger on: transportation tracker, transportation.laketahoeinfo.org, RTP performance measures, transportation funding dashboard, transportation data trends, TEPM, bike ped counts, congestion travel time, transportation projects map, transportation strategies, FTIP."
---

# Transportation Tracker

Reference for [transportation.laketahoeinfo.org](https://transportation.laketahoeinfo.org/), the performance side of the Regional Transportation Plan (RTP): vision, funding, projects by strategy, and data trends. Transportation projects are EIP projects; the tracker adds the strategy, objective, and performance layer on top of the EIP Project Tracker's records.

**Always pair with** `ltinfo-platform` for the shell, tokens, embed contract, and stack facts, and `trpa-dashboard-stack` for libraries. Sampled Oct. 13, 2026.

---

## Site map

| Route | Page | What is on it |
|---|---|---|
| `/` | Home | intro, three section tiles (Vision, Funding, Data Trends), Propose and Update a Project buttons, a Leaflet map of 226 located projects colored by strategy, four featured projects |
| `/transportation/regional-vision` | Vision | RTP vision statement rich text |
| `/transportation/funding-dashboard` | Funding Dashboard | annual expenditures and progress charts rendered by the host from chart data, FTIP note |
| `/transportation/data-trends` | Data Trends | Overview rich text with the performance measures framework, then the Data Trend tiles; today one trend, the Tahoe Effective Population Model, which embeds a Shiny app |
| `/transportation-projects` | Transportation Projects | grid of 369 projects, Total Records under it |
| `/transportation-strategies/{id}` | Strategy | basics, description, objectives, expenditure chart by objective, projects map, project grid with Basics, Timing, Capital Costs, Operating Costs, and performance measure tabs |
| `/transportation-taxonomy` | Taxonomy | strategies and objectives |

Card headers on this site are navy `#2c5282`. Section labels (DATA & MONITORING, REGIONAL VISION) are uppercase in that navy.

---

## Strategies and objectives

Six strategies, each with a color the host uses on the map legend, project tiles, and the expenditure chart. Use the same colors for any by-strategy series.

| ID | Strategy | Color | Sort |
|---|---|---|---|
| 1 | Bike and Pedestrian | `#6696B0` | 3 |
| 2 | Corridor Revitalization/Complete Streets | `#A1C432` | |
| 3 | Water Quality | `#3F5F33` | |
| 4 | Operations & Maintenance (Non-Transit) | `#4773BE` | |
| 5 | Transit | `#C7D610` | |
| 6 | TSM/ITS (Transportation System Management / Intelligent Transportation Solutions) | `#C58935` | |

Objectives sit under strategies. Bike and Pedestrian has Sidewalk, C-I/Shared Use, C-II/Bike Lane, C-III/Bike Route, and Rehabilitation, which are the Caltrans bikeway classes.

Project stages, with 2026 counts across all 369 projects: Proposal 2, Planning/Design 93, Implementation 48, Post-Implementation 2, Completed 126, Deferred 48, Terminated 50. The home map legend shows the five active stages.

---

## API routes and shapes

Base `https://internalapi.laketahoeinfo.org`, anonymous GET.

| Route | Returns |
|---|---|
| `/transportation-strategies` | 6 strategies: `TransportationStrategyID`, name, description HTML, `TransportationStrategyColor`, `SortOrder` |
| `/transportation-strategies/{id}` | one strategy with its objectives |
| `/transportation-strategies/{id}/projects` | the strategy's projects, full project record (below) |
| `/transportation-strategies/{id}/expenditure-chart` | rows of `{Group, XValue, YValue, SortOrder}` where Group is the objective and XValue the year, 2007 onward |
| `/transportation-strategies/{id}/map-markers`, `/regional/map-markers` | located and regional project markers |
| `/transportation-projects` | all 369 project records |
| `/transportation-projects/featured` | the four home page features with `KeyPhotoFileResourceGuid`, `KeyPhotoCaption`, `Duration`, implementers |
| `/transportation/home/map-data` | `Projects[]` of `{TransportationProjectID, ProjectID, ProjectNumber, ProjectName, Latitude, Longitude, TransportationStrategyID, ...StrategyName, ...StrategyColor, ProjectStageID, ProjectStageDisplayName}` |
| `/transportation/funding-dashboard/chart-data` | `AnnualExpendituresChartData` (groups Expended, Secured Funding), `ProgressChartData` (Expended, Secured Funding, Projected Expenditures, Unfunded Need), `Summary` with `TotalExpended`, `TotalBudget`, `StartYear` 2007, `EndYear` 2031, `ProjectsByStage` |
| `/transportation-data-trends` | the Data Trend tiles: `TransportationDataTrendID`, name, `TransportationDataTrendContentTypeName`, thumbnail GUID |
| `/transportation-data-trends/{id}` | one trend: content type and `ContentSourceUrl` (for `EmbedUrl`) or a `ContentFileResourceInfo` |
| `/custom-rich-texts/81`, `/82`, `/83`, `/84` | the Home, Funding, Data Trends, and Vision rich text blocks |

A project record: `TransportationProjectID`, `ProjectID`, `ProjectNumber` (EIP number such as 3.02.02.0054), `ProjectName`, `ProjectDescription`, lead implementer, strategy and objective, stage, `PlanningDesignStartYear`, `ImplementationStartYear`, `CompletionYear`, `FundingTypeShortName` (Capital or Operating), `EstimatedTotalCost`, `SecuredFunding`, `UnfundedNeed`, operating cost fields, `ExpectedPM23` and `ReportedPM23` (the performance measure the strategy tracks, miles for Bike and Pedestrian), `OnFTIPList`, `LocalAndRegionalPlans[]`.

The EIP snapshot at `https://trpa-agency.github.io/EIP/data/` carries the same projects with the legacy field names and open CORS, which is the safer source for a browser-side embed.

---

## What TRPA builds

### Data Trend embeds

A Data Trend is a tile on the Data Trends page whose content type is `EmbedUrl`, `File`, or rich text. The embed opens in a full-width frame like a monitoring dashboard. Today's only trend, the Tahoe Effective Population Model, embeds `https://trpa.shinyapps.io/effective_population/`, an R Shiny app from `Transportation/EffectivePopulationModel`.

New trends follow the platform contract: one complete, self-contained page per measure or measure family, no chrome, Lexend Deca, white background, table and CSV behind every chart, published from a TRPA repo on GitHub Pages. Candidate trends, each with a data home:

| Trend | Data home | Monitoring program |
|---|---|---|
| Bicycle and pedestrian counts | `Monitoring/TransportationMonitoringDataUpdate.ipynb` (Trafx and EcoVision counters, 56 sites) and `Monitoring/BikePedUpdate.py` | 33 Bicycle and Pedestrian |
| Congestion and travel time | RITIS probe data, 13 segments, median travel time both directions | 77 Congestion-Travel Time |
| Crashes and the High Injury Network | `Transportation/CrashData` (SWITRS and NDOT, HIN by mode, hot spots) | 34 Safety |
| Traffic volumes | `Transportation/TrafficCounts` | 64 Traffic Volumes |
| Transit ridership | TTD and TART, which the Climate Dashboard already charts (3.3.a) | 36 Transit |
| Travel behavior and mode share | `Transportation/Replica`, `TravelDemandModel` | 69 Travel Behavior (type Program With Dashboard, no dashboard set yet) |
| Effective population | `Transportation/EffectivePopulationModel` | 80 Effective Population |
| Socio-economic | Tahoe Open Data demographics page | 68 Socio-Economic (dashboard set to the open data page) |

The performance measure list is RTP Appendix G, linked from the Data Trends overview. Measures with threshold standing (VMT, VMT per capita) are evaluated on the Threshold Dashboard under category 10.

### Funding and strategy charts

The host renders the funding and expenditure charts itself from the chart-data routes, so TRPA does not build those. When a report or another dashboard needs the same picture, read the routes and use these colors so the two agree: Expended `#3e72b0`, Secured Funding `#89bf40`, Projected Expenditures `#89cad7`, Unfunded Need `#e49937`. Stack bars by year from `StartYear` to `EndYear`, dollars on the y axis with a comma format, hover `x unified`.

### Project maps

Points from `/transportation/home/map-data` or the EIP snapshot, colored by strategy with the strategy colors, filtered by stage. Regional projects without a location are listed, not mapped, with the host's wording: "Some projects operate over larger areas and are not represented on the map, but are listed in the project grid below."

---

## Relationship to the other dashboards

- The **Monitoring Dashboard** holds the Transportation category's seven programs and their sites; a Data Trend is the chart over that program's record.
- The **Threshold Dashboard** category 10 evaluates VMT against the standard.
- The **Climate Resilience Dashboard** indicators 3.3.a through 3.3.f (transit ridership, VMT, EV infrastructure, mode share, equity access, low-stress bicycle miles) draw on this tracker and should match its chart styles.
- The **EIP Project Tracker** owns the project records; the tracker's project grid is a strategy-tagged view of them.

---

## Data hygiene

The Transportation and Monitoring repos still contain notebooks that call the dead `www.laketahoeinfo.org/WebServices/...` routes with a personal token in the URL. Those routes return the Angular shell now. Replace them with the internalapi routes above or the EIP snapshot, and keep any future token in `.env` per `trpa-data-services`.
