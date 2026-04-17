# # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
# """
# ---
# <(META)>:
#     docid:
#     name:
#     description: >
#     version: 0.0.0.0.0.0
#     authority: filesystem
#     security: seclvl2
#     <(WT)>: -32
# """
# # -*- coding: utf-8 -*
# # ======================================Standard Library Modules======================================================||
# from os.path import abspath, dirname, join
# import datetime as dt
#
# # ======================================3rd Party Library Modules=====================================================||
#
# # ======================================Solutions Brewer Library Modules==============================================||
# from kahndor import kahndor
# from kahndor.logma import Logma
# from nchantrs.libraries import pyqt
# from nchantrs.nchantrs import nchantment
# from nchantrs.widgets.media.editors.editors import NchantdDocEditor
#
# # ====================================================================================================================||
# here = join(dirname(__file__), "")  # ||
# log = True
# logma = Logma(__name__)
#
# # ====================================================================================================================||
# pxcfg = join(here, "_data_", "code.yaml")
#
#
# class NchantdCodeEditor(NchantdDocEditor):
#     """"""
#
#     def __init__(self, parent=None, cfg=None):
#         """ """
#         self.parent = parent
#         self.config = kahndor.Instruct(pxcfg).select("NchantdCodeEditor")
#         if self.parent:
#             self.config.override(parent.config)
#         super().__init__(self)
#         self.config.override(cfg)
#
#     def initModel(self):
#         """"""
#         super().initModel()
#         return self
#
#     def initView(self):
#         """"""
#         super().initView()
#         return self
#
#     def initWidget(self):
#         """"""
#         self.initModel()
#         self.initView()
#         return self
#
#     def init_toolbar(self):
#         """
#         Create a toolbar with language selection and linting tools.
#         """
#         toolbar = QToolBar("Editor Toolbar", self)
#
#         # Language Selector
#         self.language_selector = QComboBox(toolbar)
#         self.language_selector.addItems(
#             [
#                 "Plain Text",
#                 "Python",
#                 "JavaScript",
#                 "HTML",
#                 "CSS",
#                 "C++",
#                 "JSON",
#                 "Markdown",
#             ]
#         )
#         self.language_selector.currentTextChanged.connect(self.language_changed)
#         toolbar.addWidget(self.language_selector)
#
#         # Linting Button
#         lint_action = QAction("Lint", self)
#         lint_action.triggered.connect(self.lint_code)
#         toolbar.addAction(lint_action)
#
#         return toolbar
#
#         ## --- Syntax Highlighter --- ##
#
#     def update_syntax_highlighter(self):
#         """
#         Update the syntax highlighter based on the selected language.
#         """
#         if self.syntax_highlighter:
#             self.syntax_highlighter.setDocument(None)  # Detach existing highlighter
#
#         selected_language = self.language_selector.currentText()
#         self.syntax_highlighter = LanguageSyntaxHighlighter(self.document_editor.document(), selected_language)
#
#     def language_changed(self, language):
#         """
#         Update the syntax highlighter when the language changes.
#         """
#         self.update_syntax_highlighter()
#
#         ## --- Linting --- ##
#
#     def lint_code(self):
#         """
#         Lint the currently written code based on the selected language.
#         Show lint results in the editor as annotations or in a popup.
#         """
#         language = self.language_selector.currentText()
#         code = self.document_editor.toPlainText()
#
#         result = ""
#         if language == "Python":
#             result = self.lint_python_code(code)
#         elif language in ["JavaScript", "HTML", "CSS", "C++", "JSON"]:
#             result = self.lint_external_tool(code, language)
#         else:
#             result = "Linting not available for this language."
#
#         # Show lint results in a dialog or annotation
#         self.show_lint_results(result)
#
#     def lint_python_code(self, code):
#         """
#         Lint Python code using pylint.
#         """
#         try:
#             # Save code to a temp file for analysis
#             with open("temp.py", "w") as file:
#                 file.write(code)
#
#             # Run pylint and capture output
#             process = subprocess.run(["pylint", "temp.py"], capture_output=True, text=True)
#             return process.stdout
#         except Exception as e:
#             return f"Error during linting: {str(e)}"
#
#     def lint_external_tool(self, code, language):
#         """
#         Call external linters for languages such as JavaScript, HTML, or C++.
#         """
#         # NOTE: Add paths to language-specific linters.
#         external_tool_mapping = {
#             "JavaScript": "eslint",
#             "HTML": "htmlhint",
#             "CSS": "stylelint",
#             "C++": "clang",
#             "JSON": "jsonlint",
#         }
#
#         if language not in external_tool_mapping:
#             return "No linter available for this language."
#
#         tool = external_tool_mapping[language]
#         try:
#             # Save code to a temp file for analysis
#             temp_file = f"temp.{language.lower()}"
#             with open(temp_file, "w") as file:
#                 file.write(code)
#
#             # Run the external linter and return output
#             process = subprocess.run([tool, temp_file], capture_output=True, text=True)
#             return process.stdout
#         except Exception as e:
#             return f"Error during linting: {str(e)}"
#
#     def show_lint_results(self, results):
#         """
#         Display lint results to the user.
#         """
#         # You can display this in a separate window, a popup, or as annotations in the editor.
#         self.document_editor.setPlainText(results)
#
#
# class LanguageSyntaxHighlighter(pyqt.QSyntaxHighlighter):
#     """
#     Custom syntax highlighter for various programming languages.
#     """
#
#     def __init__(self, document, language="Plain Text", cfg=None):
#         """"""
#         self.config = kahndor.Instruct(pxcfg).select("").override(cfg)
#         super().__init__(document)
#         self.language = language
#         self.highlighting_rules = []
#         self.initialize_rules()
#
#     def initialize_rules(self):
#         """
#         Create syntax highlighting rules based on the language.
#         """
#         self.highlighting_rules = []
#
#         if self.language == "Python":
#             # Keywords
#             keyword_format = QTextCharFormat()
#             keyword_format.setForeground(QColor("blue"))
#             keyword_format.setFontWeight(QFont.Bold)
#             keywords = [
#                 "def",
#                 "class",
#                 "import",
#                 "try",
#                 "except",
#                 "for",
#                 "while",
#                 "if",
#                 "else",
#                 "elif",
#                 "return",
#             ]
#             for word in keywords:
#                 pattern = QRegularExpression(rf"\b{word}\b")
#                 self.highlighting_rules.append((pattern, keyword_format))
#
#             # Strings
#             string_format = QTextCharFormat()
#             string_format.setForeground(QColor("green"))
#             pattern = QRegularExpression(r"\".*\"|'.*'")
#             self.highlighting_rules.append((pattern, string_format))
#
#         elif self.language == "JavaScript":
#             # Add JavaScript-specific rules here
#             keyword_format = QTextCharFormat()
#             keyword_format.setForeground(QColor("blue"))
#             keyword_format.setFontWeight(QFont.Bold)
#             keywords = [
#                 "function",
#                 "var",
#                 "let",
#                 "const",
#                 "return",
#                 "if",
#                 "else",
#                 "for",
#                 "while",
#             ]
#             for word in keywords:
#                 pattern = QRegularExpression(rf"\b{word}\b")
#                 self.highlighting_rules.append((pattern, keyword_format))
#
#         # Extend with more rules for other languages (HTML, CSS, etc.)
#
#     def highlightBlock(self, text):
#         """
#         Apply syntax highlighting to the given text block.
#         """
#         for pattern, fmt in self.highlighting_rules:
#             match_iterator = pattern.globalMatch(text)
#             while match_iterator.hasNext():
#                 match = match_iterator.next()
#                 self.setFormat(match.capturedStart(), match.capturedLength(), fmt)
#
#
# # ====================================================================================================================||
#
# # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
