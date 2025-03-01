from sympy import sign, symbols

from report.model.report_prettifier import expr_latex, rational_latex
from tasks.task1_2_lp.model.lp_problem.enums.comp_operator import CompOperator
from tasks.task1_2_lp.model.lp_problem.enums.objective_type import ObjectiveType
from tasks.task1_2_lp.model.lp_problem.lp_problem import LPProblem
from tasks.task1_2_lp.model.lp_problem.objective.objective import Objective


def get_non_negative_vars_latex(vars_count: int, variable_symbol: str = "x"):
    result = [f"{variable_symbol}_{i + 1} \\ge 0" for i in range(vars_count)]
    return ",".join(result)


def problem_latex(lp_problem: LPProblem, add_non_negative: bool = True) -> list[str]:
    def comp_operator_sign(operator: CompOperator):
        match operator:
            case CompOperator.LE:
                return "\\le"
            case CompOperator.GE:
                return "\\ge"
            case CompOperator.EQ:
                return "="

    obj = lp_problem.objective
    constraints = lp_problem.constraints
    result = []
    func_name = 'max' if lp_problem.objective.type == ObjectiveType.MAX else 'min'
    obj_latex = f"{func_name}({expr_latex(obj.coeffs, obj.variables, obj.const)})"
    result.append(obj_latex)
    for constraint in constraints:
        constraint_expression_latex = expr_latex(constraint.coeffs, constraint.variables)
        constraint_latex = f"{constraint_expression_latex}{comp_operator_sign(constraint.comp_operator)}{rational_latex(constraint.const)}"
        result.append(constraint_latex)
    if add_non_negative:
        result.append(get_non_negative_vars_latex(lp_problem.var_count, variable_symbol=obj.variable_symbol))
    return result


class LPProblemViewModel:
    def __init__(self, lp_problem: LPProblem):
        self.lp_problem = lp_problem

    def problem_latex(self) -> list[str]:
        return problem_latex(self.lp_problem)

    def canonical_problem_latex(self) -> list[str]:
        return problem_latex(self.lp_problem.canonical_form)

    def dual_problem_latex(self, from_canonical: bool = False) -> list[str]:
        problem = self.lp_problem
        if from_canonical:
            problem = self.lp_problem.canonical_form
        return problem_latex(problem.get_dual_problem(variable_symbol="y"), add_non_negative=not from_canonical)

    def auxiliary_form_latex(self) -> list[str]:
        return problem_latex(self.lp_problem.auxiliary_form)

    def art_form_latex(self) -> list[str]:
        constraints = self.lp_problem.auxiliary_form.constraints
        m_sym = symbols('M')
        art_form_obj_coeffs = []
        obj_coeffs = self.lp_problem.canonical_form.objective.coeffs
        auxiliary_obj_coeffs = self.lp_problem.auxiliary_form.objective.coeffs
        for i in range(len(auxiliary_obj_coeffs)):
            if i < len(obj_coeffs):
                art_form_obj_coeffs.append(obj_coeffs[i])
            else:
                art_form_obj_coeffs.append(-m_sym)

        objective = Objective(
            obj_type=ObjectiveType.MAX,
            coeffs=art_form_obj_coeffs,
            const=self.lp_problem.objective.const)
        art_form_problem = LPProblem(constraints=constraints, objective=objective)
        return problem_latex(art_form_problem)
