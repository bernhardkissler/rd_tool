import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

add_info_text = dcc.Markdown(
    """
These explanations can be reopened by clicking the "Show Explanations" button in the top right corner. In addition, many of the controls, charts and the table in the last section contain further documentation in pop-overs.

### **Basic Layout of the Tool**
#### **General**

The Tool is divided into four main segments and a control panel in the top right corner. There is the main input segment at the top, where you can decide which theory to use, and enter the lotteries to be analyzed. Below, the Tool displays some summary statistics of the entered lotteries. The third segment is dynamic and allows the user to change the specification of the theory he focuses on while the fourth displays the outcomes of the calculation in comparison to standard specifications of the other theories. Lastly, there is a small control panel in the top right corner of the window allowing the user to hide some of the sections if he wants a more focused experience. This is also, where these explanations can be opened and links to the  <a href="/static/Bachelor_Thesis.pdf" target="_blank"> companion essay </a> and the <a href="https://github.com/bernhardkissler/rd_tool" target="_blank"> GitHub repository </a> can be found. 

#### **Theory and Lottery**
On the top left of the first segment, you can choose the theory on which you want to focus. By default, this is Expected utility theory (EU).
Depending on which theory you choose, an input table of different dimensions will be displayed for you to enter the target lottery and any needed context information. For EU, the input segment shows a table on the left, where the target lottery can be entered. This table can be extended or shortened by deleting a row or clicking the “Add Row” button, respectively. If you choose theories like Optimal Anticipation with Savoring and Disappointment (OSAD) or Regret theory (RT) which expect more inputs than just the target lottery, additional columns will appear. Note that if you enter the context information for Salience theory (ST) or RT in the table on the left, the Tool automatically assumes correlated state spaces meaning that both outcomes do not only have the same probability but are intrinsically linked to the same state of the world. A more in depth discussion of this can be found in the companion essay in the section on RT. Alternatively, you may choose a sure amount in comparison to which your target lottery should be evaluated by clicking on the “Use single input” switch and entering that sure payoff in the additional input table appearing to the right of the initial input table. The same additional table will open when you choose the Reference Dependent Risk Attitudes theory (RDRA) in the dropdown. In this case, you will also be able to add and delete rows to the additional table similarly to the input table on the left. Additional inputs for parameters like the Savoring coefficient - $\delta$ of OSAD or the local thinking coefficient - k from ST will appear here as well.

#### **Summary of lotteries and statistics**
The second section offers a summary of statistical information about the target lottery you entered and possible context information. The chart labeled "Lotteries" displays the entered information in a decision tree consistent with the figures in the companion essay. The chart labeled "Probability Density Function" plots the lotteries with their payoffs on the x-axis and the associated probabilities on the y-axis. 

If more than the target lottery is entered in the first section, the chart displays the target and context lotteries as clustered bars. Finally, the chart labeled "Cumulative Density Function" displays similar information to the "Probability Density Function", but instead of displaying the individual probabilities on the y-axis, it takes the sum of the probabilities' of all outcomes with lower payoffs than the current outcome. Below these three charts, there is a table displaying some standard statistical moments of the entered lotteries. Like in the decision trees in the "Lotteries" chart and in this essay the first value in a cell refers to the target lottery and the one behind the vertical line refers to the context information, if target and context lotteries are entered.
#### **Utility function and auxiliary functions**
The third section is dynamic. Depending on which theory was chosen in the first section, it allows you to choose and adjust the utility function and other auxiliary functions such as the regret function or salience function for RT and ST. For each of these subsections, there is a dropdown field in the top left corner similar to the one in the first section to choose the functional form to be used.
If a preimplemented function is chosen, the tool will display the formula with all the necessary parameters beneath the dropdown field. Below the formula, there are input fields to adjust the function's parameters.

On the bottom of each dropdown, you will find a special option titled "Enter custom function".  
If you choose to use a custom function, only a text input and a button to run the function will appear. In this text field custom functions can be defined according to rules further described below in the Section "Rules for the input of custom functions". 
Currently, there is no good way to give the user feedback about whether the input function is interpreted correctly, but inspecting the chart to the right may be helpful. Note that invalid syntax in the input will cause the Tool to stop calculating accurate utilities. If you are unsure about whether the Tool is still responding correctly, try a simple function (for example simply enter x for univariate functions or x_1 for bivariate functions) for which the expected chart on the right is known.

For all the input sections, there is a chart on the right displaying the function entered on the left. Again, these charts are consistent with the figures in the first section of the companion essay and further information can be found there.


#### **Output**
The last section displays the utility, certainty equivalent and risk premium calculated for the entered lotteries in a table. The first, bold row displays the outcomes given the theory chosen in the first section and the adjustments  made to its specification afterwards. Below that, the tool displays the outcomes calculated by using standard parametrizations of all the theories presented in the companion essay and implemented in the tool as a comparison. To make the comparison easier, every row displays all the used auxiliary functions and parameters as well as the current target lottery and possible context-information in a consistent form.

### **Rules for entering custom functions**


The following rules apply:
* Only single-line inputs are accepted.
* Spaces are ignored.
* Floating point values have to be entered using a point and not a comma as a separator (i.e., $ \\frac{3}{4} $ can be entered as 0.75 but not 0,75)
* In the case of univariate functions (utility function and probability weighting function), the independent variable is always called "x". In the case of bivariate functions (Regret and Salience functions, etc.) the two independent variables are called "x\_1" and "x\_2". The entered formula must follow this convention.
* No other variables are allowed.
* Only the right-hand side of the equations is entered. $u(x)=3$<sup>\*</sup>$x$ becomes $3$<sup>\*</sup>$x$
* Every operation must be explicitly declared (i.e., $3x$ must be written as $3$<sup>\*</sup>$x$)
* Piecewise definitions of arbitrary complexity can be defined by using a shortened if statement of the form "do something if condition else do something else". The Utility function proposed by Tversky and Kahneman with parameters of $\lambda=2.25$, $\\alpha = 0.88$ and a reference point of $r=0$ can be entered as "$(x-0)$<sup>\*\*</sup>$0.88$ if $x >= 0$ else $-2.25$<sup>\*</sup>$(-(x-0))$<sup>\*\*</sup>$0.88$". Nesting if statements is possible.
* Simpleeval (the parser defining the set of allowed inputs) imposes some (generous) restrictions on the computational complexity of evaluated expressions to keep the server from crashing. This includes restrictions on the size of power-operations (exponents may not exceed a certain size) and similar measures which are not likely to impact normal usage of the Tool.

In addition, the following signs are allowed:

<table class="table-hover table-bordered table-sm mx-auto">
<thead>
  <tr>
    <th colspan="2">Allowed operators</th>
    <th colspan="2">Allowed mathematical functions</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>+</td>
    <td>"plus"</td>
    <td>abs()</td>
    <td>"the absolute vale of"</td>
  </tr>
  <tr>
    <td>-</td>
    <td>"minus"</td>
    <td>exp()</td>
    <td>"e to the power of"</td>
  </tr>
  <tr>
    <td>/</td>
    <td>"divided by"</td>
    <td>log()</td>
    <td>"the natural logarithm of"</td>
  </tr>
  <tr>
    <td><sup>*</sup></td>
    <td>"multiplied by"</td>
    <td>log10()</td>
    <td>"the base 10 logarithm of"</td>
  </tr>
  <tr>
    <td><sup>**</sup></td>
    <td>"to the power of"</td>
    <td>u()</td>
    <td>"the univariate utility function"<sup>1)</sup></td>
  </tr>
  <tr>
    <td>&lt;</td>
    <td>"smaller than"</td>
    <td>sqrt()</td>
    <td>"the square root of"</td>
  </tr>
  <tr>
    <td>&gt;</td>
    <td>"greater than"</td>
    <td>pi</td>
    <td>"$\pi$ - Pi"</td>
  </tr>
  <tr>
    <td>&lt;=</td>
    <td>"smaller equal"</td>
    <td>e</td>
    <td>"e - Euler's Number"</td>
  </tr>
  <tr>
    <td>&gt;=</td>
    <td>"greater equal"</td>
    <td>sin()</td>
    <td>"the sine of"</td>
  </tr>
  <tr>
    <td>==</td>
    <td>"equal to"</td>
    <td>cos()</td>
    <td>"the cosine of"</td>
  </tr>
</tbody>
</table>

<br>
<sup>1)</sup> This function is only provided when appropriate such as in the case of the bivariate utility function of OSAD and the regret function of RT.
<br>
From a security standpoint evaluating user input code is risky, which is why the Simpleeval Python-library is used to prevent most malevolent inputs. Unfortunately, this means that user input utility functions cannot be evaluated in a way that allows the construction of an appropriate certainty equivalent function. In this case only the utility resulting from the lottery is shown in the output section.

### **Miscellaneous**

The option to hide and show different sections using the control panels in the top right corner extends to the print layout of the page. This means that only section that are not hidden will be printed. Additionally, most controls will be hidden when printing for a nicer look.


""",
    dangerously_allow_html=True,
)


# ||Allowed operators     | |Allowed mathematical functions
# |---|---|---|---|
# | +  | "plus"            | abs()   | "the absolute vale of"                         |
# | -  | "minus"           | exp()   | "e to the power of"                            |
# | /  | "divided by"      | log()   | "the natural logarithm of"                     |
# | *  | "multiplied by"   | log10() | "the base 10 logarithm of"                     |
# | ** | "to the power of" | u()     | "the univariate utility function"              |
# | <  | "smaller than"    | sqrt()  | "the square root of"                           |
# | >  | "greater than"    | pi      | "$\pi$ - Pi"                                   |
# | <= | "smaller equal"   | e       | "e - Euler's Number"                           |
# | >= | "greater equal"   | sin()   | "the sine of"                                  |
# | == | "equal to"        | cos()   | "the cosine of"                                |
