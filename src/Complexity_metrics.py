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
    cc_result = cc_visit(code)
    halstead_result = h_visit(code)
    mi_results = mi_visit(code, None)
    return cc_result, halstead_result, mi_results

def remove_comments(code):
    code_no_single_line_comments = re.sub(r'#.*', '', code)
    code_no_multiline_comments = re.sub(r'\'\'\'(.*?)\'\'\'|\"\"\"(.*?)\"\"\"', '', code_no_single_line_comments, flags=re.DOTALL)
    return code_no_multiline_comments

def count_keywords(code):
    keywords = keyword.kwlist
    new_code =remove_comments(code)
    words = new_code.split()
    keyword_counts = Counter(word for word in words if word in keywords)
    for keyw in keywords:
      if keyword_counts[keyw]==0:
        keyword_counts[keyw]=0
    return keyword_counts

def count_lines(code):
    new_code =remove_comments(code)
    analysis = analyze(new_code)
    cl=analysis.loc - analysis.blank
    return cl

def count_loops(code):
    new_code =remove_comments(code)
    return len(re.findall(r'(for|while)', new_code))

def count_comparisons(code):
    new_code =remove_comments(code)
    return len(re.findall(r'(==|!=)', new_code))

def count_variables_in_code(code):
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
    new_code=remove_comments(code)
    single_quoted_strings = re.findall(r"'(.*?)'", new_code)
    double_quoted_strings = re.findall(r'"(.*?)"', new_code)
    count = len(single_quoted_strings) + len(double_quoted_strings)

    return count

def count_numeric_literals(code: str) -> int:
    new_code = remove_comments(code)
    numeric_literals = re.findall(r'\b\d+\.\d+|\b\d+', new_code)
    count = len(numeric_literals)

    return count

def count_math_operations(code: str) -> int:
    new_code = remove_comments(code)
    math_operations = re.findall(r'(?<!\w)[\+\-\*/%](?!\w)|<<|>>', new_code)
    count = len(math_operations)

    return count

def max_nested_blocks(code):

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
    new_code = remove_comments(source_code)
    word_pattern = re.compile(r'[A-Z]_*\d*[a-z]*_*\d*[a-z]*_*\d*[a-z]*_*\d*[a-z]*_*\d*|[a-z]+_*\d*[a-z]*_*\d*[a-z]*_*\d*')
    lines = new_code.splitlines()
    unique_words = set()

    def is_keyword(word):
        return keyword.iskeyword(word)

    for line in lines:
        line = re.sub(r'#.*|".*?"', '', line)
        words = word_pattern.findall(line)
        for word in words:
            if not is_keyword(word):
                unique_words.add(word)

    num_unique_words = len(unique_words)

    return num_unique_words
