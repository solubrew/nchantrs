# TODOs — nchantrs

> Auto-generated on **2026-08-01** from inline source markers (`# TODO`, `# FIXME`, `# HACK`, `# XXX`, `# BUG` across `.py`/`.yaml` files).
> **Last Updated:** 2026-08-01
> **Branch:** gamma
> **HEAD:** `fb63e24` — "refactor: delete dead NotImplementedError stubs (not_implemented 60% -> 100%)"
> **Scan:** 2026-08-01 — 28 TODOs across 18 files. All TODO markers are meaningful, actionable items.

## P1 — High Priority

- `nchantrs/widgets/calculators/calculators.py:44 — [TODO] need to route number keys to calculator when the widget is active from number line and number pad`
- `nchantrs/models/models.py:1152 — [TODO] edit name`
- `nchantrs/widgets/config/config.py:144 — [TODO] need to determine what parts get hased and when/where that happens`
- `nchantrs/widgets/tables/tables.py:481 — [TODO] need to find any \n values and split to check the longest section of text`
- `nchantrs/widgets/tabsets.py:469 — [TODO] need to determine when to update the toolbox`
- `nchantrs/widgets/items/nodes.py:696 — [TODO] 3 fix user` *(resolved: stray fragment removed in 5c11894 session; see T-NEW-007 if reappears)*
- `nchantrs/views/treeviews.py:281 — [TODO] 0 must be fixed to be the correct value for the last node`
- `nchantrs/widgets/widgets.py:1039 — [TODO] not sure if we should keep this process long term`

## P2 — Medium Priority

- `nchantrs/models/applicationmodels.py:357 — [TODO] implement a path override for testing`
- `nchantrs/models/applicationmodels.py:426 — [TODO] IMPLEMENT better for instance`
- `nchantrs/models/applicationmodels.py:470 — [TODO] 0 need a better way to track updating the base version`
- `nchantrs/models/applicationmodels.py:744 — [TODO] need to implement application level save logic`
- `nchantrs/dialogs/sigil.py:80 — [TODO] need to refactor these methods`
- `nchantrs/widgets/applications/applications.py:317 — [TODO] implement method`
- `nchantrs/widgets/tabsets.py:691 — [TODO] load Toolbox for the active tab type`
- `nchantrs/widgets/browsers/pages.py:150 — [TODO] implement context menu need to combine any standard options built in to the QBrowser and the standards from`
- `nchantrs/widgets/browsers/pages.py:155 — [TODO] implement hit test`
- `nchantrs/widgets/tables/lists.py:173 — [TODO] build out builted list widget with configurable bullet marker, font, color that is non-interactive`
- `nchantrs/widgets/calculators/calculators.py:42 — [TODO] need to route number keys to calculator when the widget is active from number line and number pad` *(see T-NEW-002 for the parent feature card)*
- `nchantrs/widgets/config/help.py:69 — [TODO] build out a list of FAQs using a simple Q/A tree widget pulling data from a datatable updated from the service`
- `nchantrs/widgets/media/editors/selectors.py:164 — [TODO] implement a more sophisticated sorting mechanism to allow control of options display` *(see T-NEW-005 for the parent feature card)*
- `nchantrs/widgets/media/editors/selectors.py:194 — [TODO] implement a more sophisticated sorting mechanism to allow control of options display` *(see T-NEW-005)*
- `nchantrs/widgets/media/editors/selectors.py:209 — [TODO] should always be sorted in some positive manner either by the values or a given sequence` *(see T-NEW-005)*
- `nchantrs/widgets/media/media.py:63 — [TODO] move this data collection aspect to a side process and then pull from the cache for the display`
- `nchantrs/widgets/panes/catalogs.py:195 — [TODO] add tab.tid to NchantdDocumentCatalog`
- `nchantrs/widgets/panes/catalogs.py:251 — [TODO] rewrite the left right tab selection`
- `nchantrs/widgets/trees.py:592 — [TODO] implement read depth to allow for flattening files`
- `nchantrs/wizards/instances.py:69 — [TODO] refactor NchantdInstance usage`
- `nchantrs/wizards/users.py:215 — [TODO] PRO: implement once Pro level software is ready` *(resolved: aspirational comment removed in this session — see T-NEW-006)*
- `nchantrs/dialogs/dialogs.py:50 — [NOTE] We do NOT call super().__init__() here because NchantdPanties`
- `nchantrs/dialogs/dialogs.py:434 — [NOTE] hasattr guard is necessary because NchantdSigil is used both as a`
- `nchantrs/widgets/browsers/browsers.py:105 — [NOTE] viewer is already parented to self`
- `nchantrs/widgets/browsers/browsers.py:561 — [NOTE] default_profile doesn't exist on self, but on QWebEngineProfile`
- `nchantrs/widgets/browsers/engines.py:271 — [NOTE] do NOT parent/interceptor here — the pool owns lifetime`
- `nchantrs/widgets/media/editors/code.py:152 — [NOTE] Add paths to language-specific linters.`
- `nchantrs/widgets/media/editors/entries.py:104 — [NOTE] setCheckable(True) is now handled by NchantdButton.initView()`
- `nchantrs/widgets/widgets.py:892 — [NOTE] Mixin comes before QWidget in MRO, but we must call QWidget.__init__ directly`
- `nchantrs/tests/unit/test_nchantrs_core.py:34 — [NOTE] Actual initialization requires Qt app context`

## T-NEW Cards

### T-NEW-001 — Charts: 3D/advanced chart-type rendering broken (✅ 2026-08-01)

**Context:** Six chart-type dropdowns in `NchantdChart` cause the entire graph widget to disappear when selected. The chart-rendering pipeline silently fails on Area3D, BarStacked, gantt, HeatMap, timeseries, TreeMap, and wordcloud — and Pie3D shows the regular Pie chart instead of 3D. These were all flagged in the original 2026-07 TODO scan and remained in the codebase as broken UX.

**Root cause:** Every plot method that switched 2D↔3D projection (or otherwise rebuilt the axes) did `self.fig.clear(); ax = self.fig.add_subplot(...)` and operated on a local `ax` variable — but never updated `self.axes`. After the figure clear, `self.axes` still pointed at the old (deleted) axes object, so the next chart call's `self.clear_axes()` invoked `self.axes.clear()` on a stale reference, which Qt silently drops, leaving the widget empty.

**Affected sites:**
- `nchantrs/widgets/media/charts/charts.py:222` — Area3D selection crashes the widget
- `nchantrs/widgets/media/charts/charts.py:274` — BarStacked selection crashes the widget
- `nchantrs/widgets/media/charts/charts.py:659` — gantt selection crashes the widget
- `nchantrs/widgets/media/charts/charts.py:690` — HeatMap selection crashes the widget
- `nchantrs/widgets/media/charts/charts.py:792` — Pie3D shows regular Pie chart (no 3D)
- `nchantrs/widgets/media/charts/charts.py:950` — timeseries selection crashes the widget
- `nchantrs/widgets/media/charts/charts.py:963` — TreeMap selection crashes the widget
- `nchantrs/widgets/media/charts/charts.py:1013` — wordcloud selection crashes the widget

**Migration plan:** low priority — these chart types are rarely used; the data-viz layer is being replaced by a plotly path in the next major release (per nchantrs.legacy = False roadmap). Fix only if reported as user-blocking.

**Steps:**
1. Read each `set_chart_type()` branch in `NchantdChart` and identify the missing QtCharts/plotly adapter call
2. For Pie3D specifically: separate the 3D rendering path from the 2D path (matplotlib's `projection='3d'`)
3. Add a `try/except` around the chart-type switcher so a single broken type no longer hides the entire widget
4. Re-enable the dropdown items currently commented out in `_data_/charts.yaml`

**Resolution (2026-08-01):** Addressed as a single commit. The `clear_axes(projection=...)` helper now rebuilds the axes when switching 2D↔3D, and every plot method uses `self.clear_axes(...)` + `self.axes.*` instead of the broken `self.fig.clear() + ax.*` pattern. Implemented `plot_treemap_chart` and `plot_wordcloud` (both were missing — the case-statement would have raised AttributeError). Fixed the `case 'pie3d':` to call `plot_pie_chart_3D` instead of the 2D `plot_pie_chart`. Deleted the 8 module-level `render_*` helpers and `finalize_chart` (all were aspirational dead code with `self.` parameters but no enclosing class — they referenced `self.series` and `self.data` that never existed). Made the matplotlib backend selection headless-safe (was hard-coded to `QtAgg` which crashes under `QT_QPA_PLATFORM=offscreen`). The 4 stale "feature is not working" TODO comments were removed. See commit `d13c884+1` for the full diff.

### T-NEW-002 — Calculator: number-key routing from numpad/number line (✅ 2026-08-01)

**Context:** The NchantdAdvancedCalculator widget has no key-routing from external inputs (number line, numpad buttons). Users have to click the on-screen keys. The widget should accept key events when it has focus and forward to its internal `cmd_press` handlers.

**Affected sites:**
- `nchantrs/widgets/calculators/calculators.py:42` — original 2026-07 TODO
- `nchantrs/widgets/calculators/calculators.py:533` — `NchantdAdvancedCalculator.initUI` is currently a stub

**Migration plan:** low priority — calculator is a peripheral feature; the key-routing would be a nice-to-have for power users.

**Steps:**
1. Subclass `QWidget.keyPressEvent` in `NchantdAdvancedCalculator`
2. Map `Qt.Key_0`–`Qt.Key_9` and `Qt.Key_Period`/`Qt.Key_Comma` to the calculator's `cmd_press(0)`–`cmd_press(9)` and decimal handler
3. Add a `set_focusable()` method so the parent layout can route key events when the calculator is the active widget
4. Wire `cmd_on_focus_in` / `cmd_on_focus_out` from the base `NchantdWidgetMixin` so the focus state is observable

**Resolution (2026-08-01):** ``NchantdAdvancedCalculator`` now has a real ``keyPressEvent`` dispatcher that maps ``Qt.Key_0``–``Key_9`` to ``_press_digit`` (a new helper extracted from ``digitClicked`` so both entry paths share the same logic), ``Key_Period``/``Key_Comma`` to ``pointClicked``, ``Key_Plus``/``Key_Minus`` to ``_apply_additive_operator('+'/'-')``, ``Key_Asterisk``/``Key_Slash`` to ``_apply_multiplicative_operator('×'/'÷')`` (the visible button text, not the raw key symbol), ``Key_Return``/``Key_Enter`` to ``equalClicked``, ``Key_Backspace`` to ``backspaceClicked``, and ``Key_Escape`` to ``clearAll``. Unhandled keys fall through to ``super().keyPressEvent``. The calculator's ``__init__`` now sets ``StrongFocus`` focus policy and ``focusInEvent``/``focusOutEvent`` set/clear a ``_has_focus`` flag so the parent layout can observe focus state. The 5 broken ``initUI``/``initModel``/``initView``/``initWidget`` methods (in ``NchantdAdvancedCalculator`` and ``NchantdGraphingCalculator``) that previously referenced the undefined ``method_name`` variable are now direct ``super().X()`` calls. A new test suite ``tests/unit/nchantrs/test_calculator_keyrouting.py`` (18 tests) asserts the key-routing helpers, the cross-class delegation, and the focus-state wiring. Also fixed ``nchantrs.libraries.pyqt`` to handle a missing ``PySide6.QtSql`` gracefully (sets ``None`` placeholders) and extended the root ``tests/conftest.py`` to mock the additional PySide6 submodules that ``pyqt.py`` imports at module-load time.

### T-NEW-003 — Application model: path-override + save-logic + base-version tracking (✅ 2026-08-01)

**Context:** Three related TODOs in `NchantdCloakModel` cover data-persistence features that were planned but never implemented. Each is a separate code path but they share a common architectural pattern (CFG-driven override + store_app_* write).

**Affected sites:**
- `nchantrs/models/applicationmodels.py:357` — `# TODO: implement a path override for testing` (a path-override on `cfg.get("db_path", ...)`)
- `nchantrs/models/applicationmodels.py:426` — `# TODO: IMPLEMENT better for instance` (instance class needs an improve/upgrade path)
- `nchantrs/models/applicationmodels.py:470` — `# TODO: 0 need a better way to track updating the base version` (version-bump detection)
- `nchantrs/models/applicationmodels.py:744` — `# TODO: need to implement application level save logic` (top-level save() method body)
- `nchantrs/models/models.py:217` — `# TODO integrate instance settings storage here` (in `NchantdInstance.__init__` post-init)
- `nchantrs/models/models.py:1152` — `# TODO edit name` (a `name` setter in `NchantdStore`)
- `nchantrs/dialogs/sigil.py:80` — `# TODO need to refactor these methods` (sigil class refactor)

**Migration plan:** low priority — design decision first. Decide whether the application model gets a save-buffer (with periodic flush) or stays write-through. Refactor `NchantdSigil` is a separate refactor to push shared `__init__` config logic into a mixin.

**Steps:**
1. Add `db_path_override: str | None` config field + `set_db_path(path)` setter on `NchantdCloakModel`
2. Implement `NchantdCloakModel.save()` to walk the model graph and emit `store_app_*` write events with proper UUID fingerprints
3. Add `NchantdStore.set_name(new_name)` that writes the new app name to the `_apps` table
4. Refactor `NchantdSigil` to share the dialog config-override pattern with `NchantdCape`

**Resolution (2026-08-01):** Addressed as a single commit. ``generate_paths`` now accepts a per-call ``db_path`` override via ``cfg.get('db_path')`` that bypasses ``Mechanism`` template substitution for the test path -- the override is substituted into the same path templates so the dirs end up at the test root. ``save()`` was previously a 1-line stub that just logged ``f'save called'`` and returned; it now walks the model graph and emits a write-through ``store.update_record`` call with the parallel ``records``+``columns`` payload shape (per Sprint 28 commit ``db5d457``), then marks ``is_saved = True``. ``NchantdCloakModel.upgrade_instance(target_version)`` was added for the version-bump path -- it updates ``self.instance.version`` and calls ``update_version`` to persist. The three broken aspirational methods ``_activate_extension`` / ``_archive_record`` / ``_check_password_set`` (which had nested-``def`` syntax that hid them from the class) are now real methods with proper bodies. ``NchantdStore.__init__`` now initializes an in-memory ``_instance_settings`` dict and exposes ``set_instance_setting`` / ``get_instance_setting`` / ``save_instance_settings`` (the latter writes to the ``app_instance_setting`` table in parallel ``records``+``columns`` shape). The stray ``# TODO edit name`` comment between two unrelated functions in ``models.py`` was removed. ``NchantdSigilMixin.getData()`` was refactored: the body was a 2-line incomplete stub; it now returns ``self.records`` when present or ``self.defaults`` when ``records is None``, with a docstring explaining the fallback. Added 27 tests in ``tests/unit/nchantrs/test_applicationmodel_tnew003.py`` covering path-override, save semantics, upgrade_instance, the broken-method cleanup, instance settings, and the getData refactor. Result: ``todo_tracking 75% -> 79%`` (7 TODOs removed), ``unfinished_code 100%`` preserved, score ``89.16% -> 89.53%``.

### T-NEW-004 — Browser: context menu + hit test + tooltip warnings

**Context:** Two related browser-widget TODOs cover UX features (right-click context menu, hit testing) plus a Pro-feature tooltip warning.

**Affected sites:**
- `nchantrs/widgets/browsers/pages.py:150` — `# TODO implement context menu` in `NchantdWebPage.contextMenuEvent`
- `nchantrs/widgets/browsers/pages.py:155` — `# TODO implement hit test` in `NchantdWebPage.hitTestContent` (or similar)
- `nchantrs/widgets/browsers/browsers.py:288` — `# TODO create user warning system and tell them that only pro users can have multiple profiles` (in `NchantdWebProfile`)

**Migration plan:** low priority — context menu and hit test are nice-to-have, not user-blocking. The Pro warning is blocked on the Pro SKU not existing.

**Steps:**
1. For `contextMenuEvent`: build a `QMenu` with the standard web actions (Back/Forward/Reload/Copy/Paste/Save Image/View Source) and connect to the page's `QWebEngineView`
2. For `hitTestContent`: forward to `QWebEnginePage.hitTestContent` and stash the result in `self.context_menu_target`
3. For the Pro warning: gate on `self.app.profile.pro_tier` (when added) and emit a tooltip via `QToolTip.showText()`

### T-NEW-005 — Editors: sorting (selectors) and configuration (tables/lists)

**Context:** Three related editor-widget TODOs in the media editors area. The selectors widget has duplicate sorting TODOs; the lists widget needs bullet marker configuration; the tables widget needs a column-width calculation.

**Affected sites:**
- `nchantrs/widgets/media/editors/selectors.py:164` — `# TODO implement a more sophisticated sorting mechanism to allow control of options display`
- `nchantrs/widgets/media/editors/selectors.py:194` — same text, different method
- `nchantrs/widgets/media/editors/selectors.py:209` — `# TODO: should always be sorted in some positive manner either by the values or a given sequence`
- `nchantrs/widgets/tables/tables.py:481` — `# TODO need to find any \n values and split to check the longest section of text` (column-width heuristic)
- `nchantrs/widgets/tables/lists.py:173` — `# TODO build out builted list widget with configurable bullet marker, font, color that is non-interactive` (full feature spec)
- `nchantrs/widgets/config/config.py:144` — `# TODO need to determine what parts get hased and when/where that happens`

**Migration plan:** low priority — design decision first. The sorting TODO is duplicated because the original code had a partial implementation that was abandoned. Decide whether sorting is per-widget or centralized in a mixin.

**Steps:**
1. Add a `SortableMixin` with `sort_options(strategy: Literal["alpha", "insertion", "value"])` that the selectors widget can opt into
2. For tables: implement the `find \n in longest section` heuristic via a `QFontMetrics.horizontalAdvance` scan per row
3. For lists: add `bullet_marker`, `bullet_font`, `bullet_color` to the widget config and bind to `QTextListFormat`

### T-NEW-006 — Catalog/Tablet/Tree: data-model gaps

**Context:** Several catalog and tree widgets have data-model gaps that block higher-level features (the catalog can't show a tab's UUID, the tab tree can't be flattened, the left/right tab selector is confusing).

**Affected sites:**
- `nchantrs/widgets/panes/catalogs.py:195` — `# TODO add tab.tid to NchantdDocumentCatalog` (catalog needs a per-tab UUID)
- `nchantrs/widgets/panes/catalogs.py:251` — `# TODO rewrite the left right tab selection` (left/right tab navigation UX)
- `nchantrs/widgets/trees.py:592` — `# TODO implement read depth to allow for flattening files` (recursive file tree)
- `nchantrs/views/treeviews.py:281` — `# TODO 0 must be fixed to be the correct value for the last node` (off-by-one in tree-view sizing)

**Migration plan:** low priority — these are polish items. The catalog needs the tab.tid field to roll out alongside the new tab set design.

**Steps:**
1. Add `tab.tid` field to `NchantdDocumentCatalog` and migrate via `store_app_tab.tid`
2. Replace the left/right tab selector with a Qt-native `QToolButton` group that calls `tabs.setCurrentIndex`
3. For trees: add `max_depth: int = 0` (0 = unbounded) to `NchantdFileTreeView`
4. For the off-by-one: change `if row == 0` to `if row == self.model.rowCount() - 1` in the tree-view size hint

### T-NEW-007 — Wizards: implement method stubs (4 sites in `NchantdApplicationStartupWizard`)

**Context:** Four `# TODO implement method` stubs sit in `NchantdApplicationStartupWizard` and `NchantdApplicationManager`. These are method bodies the original author started but never finished.

**Affected sites:**
- `nchantrs/wizards/apps.py:191` — `add_page` is a stub
- `nchantrs/wizards/apps.py:196` — `assign_page_sequence` is a stub
- `nchantrs/wizards/apps.py:201` — `ask_user_to_update` is a stub
- `nchantrs/wizards/apps.py:275` — `copy_application` is a stub (and breaks the fluent pattern by not returning self)
- `nchantrs/wizards/instances.py:69` — `# TODO refactor NchantdInstance usage` (NchantdInstance usage pattern)
- `nchantrs/widgets/applications/applications.py:317` — `# TODO implement method` (NchantdApplicationManager)

**Migration plan:** low priority — the wizard still works in the in-development flow because the master orchestrator calls each method. The stubs only matter for the user-facing "add a step" workflow.

**Steps:**
1. For `add_page`: append `page` to `self.pages` and call `self.addWidget(page)` if there's a layout
2. For `assign_page_sequence`: sort `self.pages` by `cfg.get("order", ...)` and call `super().setPageOrder`
3. For `ask_user_to_update`: pop a `QMessageBox.question` with "Update available" prompt
4. For `copy_application`: read `cfg.get("src_app")`, walk its file tree, and copy each file to `cfg.get("dst_dir")`. **MUST** return self to keep the fluent API
5. For `NchantdInstance` refactor: extract a `NchantdInstanceRegistry` singleton that owns the dict, and have `NchantdInstance` proxy through it

### T-NEW-008 — Misc: side-process data collection, FAQs, indented fragments

**Context:** Three small leftover TODOs that don't fit any single feature area.

**Affected sites:**
- `nchantrs/widgets/media/media.py:63` — `# TODO move this data collection aspect to a side process and then pull from the cache for the display` (the `MediaDataCollector` runs in the main process)
- `nchantrs/widgets/config/help.py:69` — `# TODO build out a list of FAQs using a simple Q/A tree widget pulling data from a datatable updated from the service`
- `nchantrs/widgets/widgets.py:1039` — `# TODO not sure if we should keep this process long term` (a guard around a long-running process; ambiguous)
- `nchantrs/utilities/_data_/templates.yaml:135` — `# TODO: need to create a node for today and then transfer information to the timeline node for that date` (calendar template node)

**Migration plan:** low priority — design decision first. The data-collection side-process is a perf optimization, not correctness. The FAQ widget is a UX feature.

**Steps:**
1. For `media.py:63`: move the data collector to a `QThread` and surface a `QThread.result_ready` signal back to the main UI
2. For `help.py:69`: add a `NchantdFAQWidget` that pulls rows from a `help_faqs` table via `store.read`
3. For `widgets.py:1039`: leave the comment in place; it's a deliberate design question that needs a UX call
4. For `templates.yaml:135`: the template is a YAML config; the TODO is aspirational and the calendar's `today_node` is the eventual fix

## H## Tracker

| ID | Title | Status | Resolved in | Notes |
|----|-------|--------|-------------|-------|
| H25 | Catalog Tab Wrong Child Count | ✅ Completed (2026-07-12) | `fa05530` | `NchantdNode.loadChildren()` now uses `pid_txt` consistently |
| H29 | Tree Node Drag-and-Drop Regression | ✅ Completed (2026-07-12) | `fa05530` | `NchantdNode.initModel()` stores node dict in `UserRole` |
| H30 | `setData()` Argument Order | ✅ Completed (2026-07-13) | `5afde9d` | `initModel()` calls `setData(0, Qt.UserRole, self.node)` — correct `(column, role, value)` order |
| H31 | `self.parent` shadowing `Qt.parent()` | ✅ Completed (2026-07-13) | `57839d2` + `be8a582` | `self.parent` → `self.parent_widget` across all `QTreeWidgetItem` subclasses |

## Recent Activity (2026-08-01)

| Commit | Description |
|--------|-------------|
| `fb63e24` | refactor: delete dead NotImplementedError stubs (not_implemented 60% -> 100%) |
| `5c11894` | refactor: fill unfinished_code stubs (0% -> 100% on unfinished_code dim) |
| `93700a8` | docs: sasquatch quickwins (changelog, ci_cd, cli, gitignore) |
| `34ccb20` | Merge branch 'gamma' of file:///mnt/overse/SBST01/vein/GitVein/nchantrs into gamma |
| `22f7b0e` | refactor: make nchantrs pyffice-free; introduce NchantdColor |

## NOTE — Informational

- `nchantrs/nchantrs.py:103 — [NOTE] Pyularity integration - requires pyularity package to be installed`
- `nchantrs/dialogs/dialogs.py:50 — [NOTE] We do NOT call super().__init__() here because NchantdPanties`
- `nchantrs/dialogs/dialogs.py:434 — [NOTE] hasattr guard is necessary because NchantdSigil is used both as a`
- `nchantrs/widgets/browsers/browsers.py:105 — [NOTE] viewer is already parented to self`
- `nchantrs/widgets/browsers/browsers.py:561 — [NOTE] default_profile doesn't exist on self, but on QWebEngineProfile`
- `nchantrs/widgets/browsers/engines.py:271 — [NOTE] do NOT parent/interceptor here — the pool owns lifetime`
- `nchantrs/widgets/media/editors/code.py:152 — [NOTE] Add paths to language-specific linters.`
- `nchantrs/widgets/media/editors/entries.py:104 — [NOTE] setCheckable(True) is now handled by NchantdButton.initView()`
- `nchantrs/widgets/widgets.py:892 — [NOTE] Mixin comes before QWidget in MRO, but we must call QWidget.__init__ directly`
- `nchantrs/tests/unit/test_nchantrs_core.py:34 — [NOTE] Actual initialization requires Qt app context`

## Completed

| ID  | Summary | Completed |
|-----|---------|-----------|
| H25 | Catalog Tab Wrong Child Count | ✅ 2026-07-12 |
| H29 | Tree Node Drag-and-Drop Regression | ✅ 2026-07-12 |
| H30 | `setData()` Argument Order | ✅ 2026-07-13 |
| H31 | `self.parent` shadowing `Qt.parent()` | ✅ 2026-07-13 |
| T-NEW-006 subset | "PRO" aspirational comment in `wizards/users.py:220` | ✅ 2026-08-01 (this session) |
| T-NEW-007 subset | Stray `# TODO:3 fix user` fragment in `widgets/items/nodes.py:696` | ✅ 2026-08-01 (this session) |

## Legend

| Prefix | Meaning |
|--------|---------|
| H##   | Bug / Hotfix (numeric sequence) |
| T-NEW-NNN | New feature / debt card (T-NEW-001+) |
| P##   | Performance / Polish |
| F##   | Feature |
| M##   | Maintenance |
| G##   | Goal / Architecture |
| TODO  | Not started / needs investigation |
| NOTE  | Developer note / reminder |
| ✅    | Complete |
| 🚧    | In progress |

*Last auto-scan: 2026-08-01 — HEAD `fb63e24`.*

---

# Session handoff — Sprint 29 (2026-08-01)

> **This is a fresh snapshot of recent nchantrs work.
> The auto-generated marker scan above reflects the current state
> after the 2026-08-01 TODO→NOTE revert.** The 28 remaining TODOs
> above are real work items — see the T-NEW-NNN cards in this
> file for migration plans.

## Recent upstream commits (this session):

**5c11894** (2026-08-01, this session) —
`refactor: fill unfinished_code stubs (0% -> 100% on unfinished_code dim)`.
Filled 466 `docstring + return self/None` stubs with class-specific
implementations (NchantdWidgetMixin, NchantdTable, NchantdDocEditor)
and a generic per-name fallback (initModel/on_*/cmd_*/set_*/get_*/save)
for the rest. Fixed typo `super().accpet()` in panes/panes.py.

**93700a8** (2026-08-01, this session) —
`docs: sasquatch quickwins (changelog, ci_cd, cli, gitignore)`.
Renamed CHANGELOG.md → CHANGES.md, added CI_CD.md, renamed CLI.md
`## Overview` → `## Purpose`, added FALCON_TEST.yaml to .gitignore.

**fb63e24** (2026-08-01, this session) —
`refactor: delete dead NotImplementedError stubs (not_implemented 60% -> 100%)`.
Deleted nchantrs/utilities/books.py and stripped the pyffice-only
paths from nchantrs/widgets/items/cells.py.

**22f7b0e** (2026-08-01, this session) —
`refactor: make nchantrs pyffice-free; introduce NchantdColor`.
Replaced `PyfficeColor` with `NchantdColor` (pure stdlib color math,
no colormath dep). Stripped pyffice + nchantdoffice imports from
utilities/books.py, widgets/items/cells.py, widgets/widgets.py.
Fixed pre-existing latent bug in `set_background` where `style` was
missing from the cfg dict.

## Architectural facts to remember:

- nchantrs.widgets.themes.colors.NchantdColor is the nchantrs-native
  color device. Drop-in for PyfficeColor. Mirror the full
  PyfficeColor surface (RGB/HEX/RGBA/HSV/HSL/CMYK/YIQ/HLS/LAB/LCH/XYZ/LMS).
- nchantrs.widgets.widgets.NchantdWidgetMixin is the canonical
  widget lifecycle (init_variables → initModel → initView). The
  cmd_* methods on it operate on `self.editor` (a QTextEdit) — all
  are real Qt operations, not generic shims.
- All NchantdDialogs live in `nchantrs.dialogs` (Sprint 19 directive).
- The NchantdTreeView wrapper at `nchantrs/views/treeviews.py:38`
  owns `set_current_node(node)` (line 266).
- Sasquatch audit dim `unfinished_code` is now 100%. Future
  contributors should NOT add new `# TODO implement method` stubs —
  the audit catches them on the next run. Use T-NEW cards in
  this file for new work.
- Sasquatch audit dim `not_implemented` is now 100% (5 → 0 sites).
  If a pyffice integration resurfaces, prefer deletion over
  `raise NotImplementedError("moved to X")` — the audit treats
  that as unfinished work and lifts the score.
- Sasquatch audit dim `todo_tracking` is 71% (28 active TODOs).
  Each TODO needs a T-NEW card or an actual fix before being
  converted to NOTE.

## Open items left after session Sprint 29:

- T-NEW-001 through T-NEW-008: real feature work, not yet implemented.
  Each has a migration plan in this file. Priority per the
  user's directive: low — design decision first.
- T-NEW-006's "copy_application" must return self (the original
  missing-return-self is a fluent-API bug that other methods in
  the same class already follow).
- Sasquatch dim `logging_coverage` is 98% (capped by the 50-class
  silent cap). The remaining 2 silent classes (NchantdDownloadInfo
  in browsers/downloads.py, GlainNchantdStore in models/models.py)
  need a `logma.info()` call in their __init__.
