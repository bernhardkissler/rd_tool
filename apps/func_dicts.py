import rd_functions.main_functions as mf
import rd_functions.util_mod as um
import rd_functions.prob_weighting as pw


pw_func_dict = {
    "TKW": [
        pw.weigh_tversky_kahneman,
        "Tversky Kahnemann probability weighting function",
        "$W(p)=\\frac{p^{\delta}}{(p^{\delta}+(1-\ p)^{\delta})^{\\frac{1}{\delta}}}$",
    ],
    "GEW": [
        pw.weigh_goldstein_einhorn,
        "Goldstein Einhorn probability weighting function",
        "$W(p)=\\frac{(b\cdot{p})^{a}}{(b\cdot{p})^{a} + (1-p)^{a}}$",
    ],
    "PW": [
        pw.weigh_prelec,
        "Prelec probability weighting function",
        "$W(p)=e^{-b(-ln(p))^{a}}$",
    ],
    "YW": [pw.weig_user, "Custom probability weighting function", ""],
}

um_func_dict = {
    "TKU": [
        um.utility_tversky_kahneman,
        "Tversky Kahneman utility function",
        """$$U(x)=\\begin{cases}
                  (x-r)^{a}             & \\text{if }x \\geq r \\\\
                  -l \\cdot (-(x-r))^{a} & \\text{if }x < r
              \\end{cases}$$""",
    ],
    "RU": [um.root_utility, "Root utility function", "$U(x) = \\sqrt{x} $"],
    "LU": [um.lin_utility, "Linear utility function", "$U(x) = x$"],
    "YU": [um.user_utility, "Custom utilty function", ""],
    "BU": [um.bern_utility, "Bernoulli's utility funtion", "$U(x) = log(a + x)$"],
}

mf_func_dict = {
    "CPT": [mf.cumulative_prospect_theory, "Cumulative prospect theory"],
    "RDU": [mf.rank_dependent_utility, "Rank dependent utility"],
    "EU": [mf.expected_utility, "Expected utility"],
    "RT": [mf.regret_theory, "Regret theory"],
    "RT_i": [mf.regret_theory_interaction, "Regret theory interaction"],
}
