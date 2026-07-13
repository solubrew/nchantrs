# TODOs — nchantrs

> Auto-generated on **2026-07-09** from inline source markers (`# TODO`, `# FIXME`, `# HACK`, `# XXX`, `# BUG`, `# NOTE` across `.py`/`.yaml` files).
> Total markers found: **97** — P0: 0, P1: 7, P2: 16, P3: 59, NOTE: 15
> Last updated: **2026-07-13** (H30/H31 resolved in commits `5afde9d` + `57839d2` + `be8a582`)

## P1 — High Priority

- `PROJECT_TRACKER.yaml:3045 — [TODO] 3 fix user'`
- `TODOs.md:249 — [TODO] fix this shouldn't reference NchantdOffice`
- ~~`TODOs.md:265 — [TODO] tree node failing`~~ ✅ **Resolved** in `fa05530` (H29 — drag-drop UserRole fix in `nchantrs/widgets/items/nodes.py`)
- `nchantrs/models/applicationmodels.py:222 — [TODO] fix this shouldn't reference NchantdOffice`
- `nchantrs/views/treeviews.py:281 — [TODO] 0 must be fixed to be the correct value for the last node`
- `nchantrs/widgets/items/nodes.py:684 — [TODO] 3 fix user`
- `nchantrs/widgets/tabsets.py:513 — [TODO] fix following error`

## H## Tracker (nchantdoffice nomenclature — applies here as upstream library)

| ID | Title | Status | Resolved in | Notes |
|----|-------|--------|-------------|-------|
| H25 | Catalog Tab Wrong Child Count | ✅ Completed (2026-07-12) | `fa05530` | `NchantdNode.loadChildren()` now uses `pid_txt` consistently |
| H29 | Tree Node Drag-and-Drop Regression | ✅ Completed (2026-07-12) | `fa05530` | `NchantdNode.initModel()` stores node dict in `UserRole` |
| H30 | `setData()` Argument Order | ✅ Completed (2026-07-13) | `5afde9d` | `initModel()` calls `setData(0, Qt.UserRole, self.node)` — correct `(column, role, value)` order |
| H31 | `self.parent` shadowing `QTreeWidgetItem.parent()` | ✅ Completed (2026-07-13) | `57839d2` + `be8a582` | `self.parent` → `self.parent_widget` across `NchantdItem`, `NchantdTreeItem`, `NchantdTreeNode`, `NchantdTree` |

## P2 — Medium Priority  

- `TODOs.md:250 — [TODO] IMPLEMENT better for instance`
- `TODOs.md:256 — [TODO] 20240723 create Sentinel dialog`
- `TODOs.md:260 — [TODO] track web addresses for login persistence`
- `nchantrs/models/_data_/applicationmodels.yaml:58 — [TODO] need to add some configuration to this`
- `nchantrs/models/applicationmodels.py:209 — [TODO] need to connect user'`
- `nchantrs/models/applicationmodels.py:422 — [TODO] implement a path override for testing`
- `nchantrs/models/applicationmodels.py:426 — [TODO] IMPLEMENT better for instance`
- `nchantrs/models/applicationmodels.py:744 — [TODO] need to implement application level save logic`
- `nchantrs/models/applicationmodels.py:770 — [TODO] implement method`
- `nchantrs/utilities/_data_/templates.yaml:135 — [TODO] need to create a node for today and then transfer information to the timeline node for that date`
- `nchantrs/widgets/browsers/browsers.py:281 — [TODO] create user warning system and tell them that only pro users can have multiple profiles`
- `nchantrs/widgets/media/editors/selectors.py:195 — [TODO] implement a more sophisticated sorting mechanism to allow control of options display`
- `nchantrs/widgets/media/media.py:144 — [TODO] build in the ability to make the button checkable`
- `nchantrs/widgets/panes/catalogs.py:195 — [TODO] add tab.tid to NchantdDocumentCatalog`
- `nchantrs/widgets/trees.py:592 — [TODO] implement read depth to allow for flattening files`
- `nchantrs/wizards/users.py:215 — [TODO] PRO: implement once Pro level software is ready`

## P3 — Low / Cleanup  

- `PROJECT_TRACKER.yaml:3063 — [TODO] need to check to see if server is running'`
- `PROJECT_TRACKER.yaml:3095 — [TODO] should always be sorted in some positive manner either`
- `TODOs.md:246 — [TODO] ensure that this will work`
- `TODOs.md:247 — [TODO] this is not built out for full control`
- `TODOs.md:248 — [TODO] this is not built out for full control`
- `TODOs.md:251 — [TODO] 0 need a better way to track version`
- `TODOs.md:252 — [TODO] streamline primary keys`
- `TODOs.md:253 — [TODO] move into tab`
- `TODOs.md:254 — [TODO] refactor source`
- `TODOs.md:255 — [TODO] move to a config file`
- `TODOs.md:257 — [TODO] eventually in a separate process`
- `TODOs.md:258 — [TODO] Proper engine reuse`
- `TODOs.md:259 — [TODO] web app Viewer subclass`
- `TODOs.md:261 — [TODO] get tab name`
- `TODOs.md:262 — [TODO] make checkable group?`
- `TODOs.md:263 — [TODO] need max columns grid`
- `TODOs.md:264 — [TODO] HACK: scroll calculations`
- `TODOs.md:266 — [TODO] calculate space`
- `TODOs.md:267 — [TODO] make button checkable`
- `TODOs.md:268 — [TODO] not sure if keep long term`
- `TODOs.md:269 — [TODO] paid version controls`
- `nchantrs/models/applicationmodels.py:470 — [TODO] 0 need a better way to track updating the base version`
- `nchantrs/models/models.py:1287 — [TODO] not valid for nchantrs but still haven't seperated the underlying table config files`
- `nchantrs/models/models.py:1476 — [TODO] edit name`
- `nchantrs/models/tabsetmodels.py:266 — [TODO] move into tab`
- `nchantrs/models/tabsetmodels.py:297 — [TODO] refactor source`
- `nchantrs/utilities/_data_/templates.yaml:133 — [TODO] move to a config file`
- `nchantrs/utilities/comms.py:111 — [TODO] need to check to see if server is running`
- `nchantrs/views/applicationviews.py:183 — [TODO] we need to make sure the config goes to load Widget`
- `nchantrs/widgets/applications/applications.py:266 — [TODO] eventually this will need to be put into a seperate process`
- `nchantrs/widgets/calculators/calculators.py:42 — [TODO] need to route number keys to calculator when the widget is active from number line and number pad`
- `nchantrs/widgets/calendars/days.py:123 — [TODO] get tab name`
- `nchantrs/widgets/calendars/timelines.py:109 — [TODO] check entries by time and rotate out ones older than 24 hours`
- `nchantrs/widgets/config/config.py:142 — [TODO] need to determine what parts get hased and when/where that happens`
- `nchantrs/widgets/config/settings.py:104 — [TODO] flip icon`
- `nchantrs/widgets/config/settings.py:113 — [TODO] flip icon`
- `nchantrs/widgets/groups.py:429 — [TODO] HACK:`
- `nchantrs/widgets/groups.py:430 — [TODO] HACK:`
- `nchantrs/widgets/groups.py:436 — [TODO] HACK:`
- `nchantrs/widgets/items/catalogs.py:106 — [TODO] need better heuristic`
- `nchantrs/widgets/media/charts/charts.py:1009 — [TODO] this feature is not working the entire graph widget disappears when wordcloud is selected in the chart type dropdown`
- `nchantrs/widgets/media/charts/charts.py:218 — [TODO] this feature is not working the entire graph widget disappears when Area3D is selected in the chart type dropdown`
- `nchantrs/widgets/media/charts/charts.py:270 — [TODO] this feature is not working the entire graph widget disappears when BarStacked is selected in the chart type dropdown`
- `nchantrs/widgets/media/charts/charts.py:655 — [TODO] this feature is not working the entire graph widget disappears when gantt is selected in the chart type dropdown`
- `nchantrs/widgets/media/charts/charts.py:686 — [TODO] this feature is not working the entire graph widget disappears when HeatMap is selected in the chart type dropdown`
- `nchantrs/widgets/media/charts/charts.py:788 — [TODO] Pie3D is showing the same graph as regular Pie chart`
- `nchantrs/widgets/media/charts/charts.py:946 — [TODO] this feature is not working the entire graph widget disappears when timeseries is selected in the chart type dropdown`
- `nchantrs/widgets/media/charts/charts.py:959 — [TODO] this feature is not working the entire graph widget disappears when TreeMap is selected in the chart type dropdown`
- `nchantrs/widgets/media/editors/editors.py:310 — [TODO] check previous text for number of newline characters`
- `nchantrs/widgets/media/editors/selectors.py:210 — [TODO] should always be sorted in some positive manner either by the values or a given sequence`
- `nchantrs/widgets/media/editors/selectors.py:77 — [TODO] replace with size methods from NchantdWidgetMixin`
- `nchantrs/widgets/media/images.py:224 — [TODO] need to calculate space`
- `nchantrs/widgets/media/images.py:226 — [TODO] need to calculate space`
- `nchantrs/widgets/media/media.py:63 — [TODO] move this data collection aspect to a side process and then pull from the cache for the display`
- `nchantrs/widgets/panes/catalogs.py:251 — [TODO] rewrite the left right tab selection`
- `nchantrs/widgets/tables/tables.py:488 — [TODO] need to find any \n values and split to check the longest section of text`
- `nchantrs/widgets/tabsets.py:465 — [TODO] need to determine when to update the toolbox`
- `nchantrs/widgets/tabsets.py:691 — [TODO] load Toolbox for the active tab type`
- `nchantrs/widgets/widgets.py:1039 — [TODO] not sure if we should keep this process long term`

## NOTE — Informational  

- `PROJECT_TRACKER.yaml:3056 — [NOTE] Pyularity integration - requires pyularity package to`
- `PROJECT_TRACKER.yaml:3069 — [NOTE] We do NOT call super().__init__() here because NchantdPanties'`
- `PROJECT_TRACKER.yaml:3075 — [NOTE] Mixin comes before QWidget in MRO, but we must call QWidget.__init__`
- `PROJECT_TRACKER.yaml:3082 — [NOTE] setCheckable(True) is now handled by NchantdButton.initView()`
- `PROJECT_TRACKER.yaml:3089 — [NOTE] Add paths to language-specific linters.'`
- `nchantrs/dialogs/dialogs.py:434 — [NOTE] hasattr guard is necessary because NchantdSigil is used both as a`
- `nchantrs/dialogs/dialogs.py:50 — [NOTE] We do NOT call super().__init__() here because NchantdPanties`
- `nchantrs/nchantrs.py:103 — [NOTE] Pyularity integration - requires pyularity package to be installed`
- `nchantrs/widgets/browsers/browsers.py:105 — [NOTE] viewer is already parented to self`
- `nchantrs/widgets/browsers/browsers.py:561 — [NOTE] default_profile doesn't exist on self, but on QWebEngineProfile`
- `nchantrs/widgets/browsers/engines.py:271 — [NOTE] do NOT parent/interceptor here — the pool owns lifetime`
- `nchantrs/widgets/media/editors/code.py:152 — [NOTE] Add paths to language-specific linters.`
- `nchantrs/widgets/media/editors/entries.py:104 — [NOTE] setCheckable(True) is now handled by NchantdButton.initView() via config`
- `nchantrs/widgets/widgets.py:892 — [NOTE] Mixin comes before QWidget in MRO, but we must call QWidget.__init__ directly`
- `tests/unit/test_nchantrs_core.py:34 — [NOTE] Actual initialization requires Qt app context`
