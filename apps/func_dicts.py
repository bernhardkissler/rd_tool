import rd_functions.main_functions as mf
import rd_functions.util_mod as um
import rd_functions.prob_weighting as pw
import rd_functions.context_eval as ce
import rd_functions.bivu_functions as bu

plot_color_sec = "#03bb8a"
plot_color = "#360498"
# plot_color = "#f7e224"
prim_color = "#e3685f"
sub_bg_color = "rgba(255,255,255,1)"
# heatscale = [[0, plot_color_sec], [0.5, "#a2a6ae"], [1, plot_color]]

heat_scale = [[0, "rgb(255,255,255)"], [0.33, plot_color_sec], [1, plot_color]]


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
    "LW": [pw.weigh_lin, "Linear probability weighting function", "$W(p) = p $"],
    "POW": [pw.weigh_pow, "Power probability weighting function", "$W(p) = p^{r}$"],
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
        um.ce_tversky_kahneman,
    ],
    "BU": [
        um.bern_utility,
        "Bernoulli's utility funtion",
        "$U(x) = log(a + x)$",
        um.bern_ce,
    ],
    "RU": [
        um.root_utility,
        "Root utility function",
        """$$U(x)=\\begin{cases}
                  \\sqrt{x}             & \\text{if }x > 0 \\\\
                  -lm \\cdot \\sqrt{{-x}} & \\text{if }x \\leq 0
              \\end{cases}$$""",
        um.root_ce,
    ],
    "LU": [um.lin_utility, "Linear utility function", "$U(x) = x$", um.lin_ce],
    "PU": [um.pow_utility, "Power utility function", "$U(x) = x^{exp}$"],
    "QU": [um.quad_utility, "Quadratic utility function", "$U(x) = ax - x^{2}$"],
    "EXU": [
        um.exp_utility,
        "Exponential utiltiy function",
        "$U(x) = 1-e^{-ax}$",
        um.exp_ce,
    ],
    "BEU": [um.bell_utility, "Bell utility function", "$U(x) = b\\cdot{x}-e^{-ax}$"],
    "HU": [um.hara_utility, "Hara utility function", "$U(x) = -(b+x)^{a}$"],
    "YU": [
        um.user_utility,
        "Custom utility function",
        "",
        um.user_ce,
    ],  # MARK use lin_ce until later
}

mf_func_dict = {
    "CPT": [mf.cumulative_prospect_theory, "Cumulative prospect theory"],
    "RDU": [mf.rank_dependent_utility, "Rank dependent utility"],
    "EU": [mf.expected_utility, "Expected utility"],
    "RT": [mf.regret_theory, "Regret theory"],
    "ST": [mf.salience_theory, "Salience theory"],
    "SDT": [mf.sav_dis_theory, "Savoring and Disappointment theory"],
    "RDRA": [mf.RDRA_theory, "Reference dependent risk attitudes"],
}

rg_func_dict = {
    "LS": [
        ce.ls_regret,
        "Loomes and Sugden regret function",
        "$ Q(x,y) = u(x) + weight\\cdot(u(x) - u(y)) $",
    ],
    "YR": [ce.user_regret, "Custom regret function", ""],
}

sl_func_dict = {
    "OG": [
        ce.og_salience,
        "Original Salience function",
        "$ \\sigma(x_1, x_2) = \\frac{|x_1 - x_2|}{|x_1| + |x_2| + \\theta} $",
    ],
    "YS": [ce.user_salience, "Custom salience function", ""],
}

sdt_func_dict = {
    "AH": [bu.additive_habits, "Additive Habits Utility", "$ U(c,y) = u(c-\\eta y) $",],
    "YB": [bu.user_bivu, "Custom Bivariate Utility", ""],
}
