# Static code-complexity metric extractors used by src/complexity_accuracy.py.
#
# Each function takes a raw Python source string (typically one of the
# generated .py files under Claude/, GPT/, Gemini/, Llama/, etc.) and returns
# a single scalar metric describing its structural complexity: cyclomatic
# complexity and maintainability index via the `radon` library, plus a set of
# hand-rolled counters (loops, comparisons, variables, literals, nesting
# depth, unique identifiers, per-keyword usage) implemented with regex/AST.
# These metrics are combined downstream to compare how "complex" the code
# produced by different LLMs/personas tends to be.
from radon.complexity import cc_visit
from radon.metrics import h_visit
from radon.metrics import mi_visit
from radon.raw import analyze
import re
import keyword
import keyword
from collections import Counter
import ast

def analyze_code_complexity(code):
    """Run radon's three headline analyses on `code` in one call.

    Returns a tuple of:
      - cc_result: list of per-function/class cyclomatic complexity blocks
      - halstead_result: Halstead volume/difficulty/effort metrics
      - mi_results: the maintainability index (0-100, higher = more maintainable)
    """
    cc_result = cc_visit(code)
    halstead_result = h_visit(code)
    mi_results = mi_visit(code, None)
    return cc_result, halstead_result, mi_results

def remove_comments(code):
    """Strip '#' comments and triple-quoted strings/docstrings from `code`.

    Used as a preprocessing step by nearly every counter below so that
    comment text (which may itself contain keywords, operators, or quotes)
    doesn't inflate the structural counts.
    """
    code_no_single_line_comments = re.sub(r'#.*', '', code)
    code_no_multiline_comments = re.sub(r'\'\'\'(.*?)\'\'\'|\"\"\"(.*?)\"\"\"', '', code_no_single_line_comments, flags=re.DOTALL)
    return code_no_multiline_comments

def count_keywords(code):
    """Count occurrences of every Python reserved keyword (if, for, def, ...)
    in `code` after comments are stripped.

    Returns a collections.Counter keyed by keyword string, with every keyword
    from keyword.kwlist explicitly present (defaulted to 0) even if unused,
    so downstream code can rely on every key existing (see
    complexity_accuracy.py's keyword_metrics dict).
    """
    keywords = keyword.kwlist
    new_code =remove_comments(code)
    words = new_code.split()
    keyword_counts = Counter(word for word in words if word in keywords)
    for keyw in keywords:
      if keyword_counts[keyw]==0:
        keyword_counts[keyw]=0
    return keyword_counts

def count_lines(code):
    """Return the number of non-blank lines of code (LOC), using radon's raw
    line analysis and subtracting blank lines, after comments are stripped.
    """
    new_code =remove_comments(code)
    analysis = analyze(new_code)
    cl=analysis.loc - analysis.blank
    return cl

def count_loops(code):
    """Count occurrences of the `for` and `while` keywords as a rough proxy
    for how many loop constructs the code contains."""
    new_code =remove_comments(code)
    return len(re.findall(r'(for|while)', new_code))

def count_comparisons(code):
    """Count `==` and `!=` occurrences as a rough proxy for equality-comparison
    density (does not count <, >, <=, >=)."""
    new_code =remove_comments(code)
    return len(re.findall(r'(==|!=)', new_code))

def count_variables_in_code(code):
    """Count the number of distinct variable names in `code` by parsing it
    into an AST and collecting:
      - every function parameter name (visit_FunctionDef)
      - every name that is ever assigned to, i.e. appears in a Store context
        (visit_Name) - covers `x = 1`, `for x in ...`, `x += 1`, etc.

    Raises SyntaxError if `code` isn't valid Python (callers in
    complexity_accuracy.py catch this and fall back to 0).
    """
    new_code = remove_comments(code)
    tree = ast.parse(new_code)

    variable_names = set()

    class VariableVisitor(ast.NodeVisitor):
        def visit_FunctionDef(self, node):
            # Collect parameter names
            for param in node.args.args:
                variable_names.add(param.arg)
            self.generic_visit(node)

        def visit_Name(self, node):
            if isinstance(node.ctx, ast.Store):
                variable_names.add(node.id)
            self.generic_visit(node)

    visitor = VariableVisitor()
    visitor.visit(tree)

    return len(variable_names)

def count_string_literals(code: str) -> int:
    """Count string literals via regex: every '...' and "..." span.

    Note this is a simple regex, not a tokenizer, so it can miscount strings
    that themselves contain escaped quotes or span multiple lines; treated as
    an acceptable approximation for aggregate complexity comparisons.
    """
    new_code=remove_comments(code)
    single_quoted_strings = re.findall(r"'(.*?)'", new_code)
    double_quoted_strings = re.findall(r'"(.*?)"', new_code)
    count = len(single_quoted_strings) + len(double_quoted_strings)

    return count

def count_numeric_literals(code: str) -> int:
    """Count numeric literals (integers and decimals) appearing in the code."""
    new_code = remove_comments(code)
    numeric_literals = re.findall(r'\b\d+\.\d+|\b\d+', new_code)
    count = len(numeric_literals)

    return count

def count_math_operations(code: str) -> int:
    """Count arithmetic/bitwise-shift operators: +, -, *, /, %, <<, >>.

    The lookaround assertions ((?<!\\w) / (?!\\w)) exclude a leading '-' or '+'
    that is part of an identifier-adjacent token rather than a standalone
    operator, though this is a heuristic rather than a full tokenizer.
    """
    new_code = remove_comments(code)
    math_operations = re.findall(r'(?<!\w)[\+\-\*/%](?!\w)|<<|>>', new_code)
    count = len(math_operations)

    return count

def max_nested_blocks(code):
    """Estimate the deepest indentation level in the code, assuming 4-space
    indents (leading_spaces // 4), as a proxy for maximum block nesting depth.

    The final `-1` offsets for the top-level (zero-indent) code always
    counting as depth 0 -> so a script with no nested blocks reports 0
    rather than the raw max_depth value. This is indentation-based, not
    AST-based, so it will be misled by inconsistent or tab-based indentation.
    """

    max_depth = 0
    current_depth = 0
    new_code = remove_comments(code)
    lines = new_code.splitlines()

    for line in lines:
        leading_spaces = len(line) - len(line.lstrip())
        current_depth = leading_spaces // 4

        if current_depth > max_depth:
            max_depth = current_depth

    return max_depth-1

def count_unique_words_in_code(source_code):
    """Count distinct identifier-like tokens (camelCase/snake_case words) in
    the code, excluding Python keywords and text inside string literals or
    comments, as a rough proxy for vocabulary/naming diversity.
    """
    new_code = remove_comments(source_code)
    word_pattern = re.compile(r'[A-Z]_*\d*[a-z]*_*\d*[a-z]*_*\d*[a-z]*_*\d*[a-z]*_*\d*|[a-z]+_*\d*[a-z]*_*\d*[a-z]*_*\d*')
    lines = new_code.splitlines()
    unique_words = set()

    def is_keyword(word):
        return keyword.iskeyword(word)

    for line in lines:
        # Best-effort strip of any remaining comment/string content on this
        # specific line before tokenizing (remove_comments already handled
        # block-level comments/docstrings above).
        line = re.sub(r'#.*|".*?"', '', line)
        words = word_pattern.findall(line)
        for word in words:
            if not is_keyword(word):
                unique_words.add(word)

    num_unique_words = len(unique_words)

    return num_unique_words
