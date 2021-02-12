import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

add_info_text = dcc.Markdown(
    """
##### Basic Layout of the Tool

The Tool is divided into four main segments. There is a main input segment on top, where the user can decide which theory to focus on, and enter the lotteries to be analyzed. Below, the Tool displays some statistic information on the entered lotteries. The third segment is dynamic and allows the user to change the parametrization of the theory he focuses on and the fourth displays the outcomes of the calculation in comparison to standard parametrizations of the other theories. Lastly, there is a small control panel on the top right corner of the window allowing the user to hide some of the sections if he wants a more focused experience. This is also, where additional explanations can be blended in and links to this thesis and the GitHub repository found. 

On the top left of the first segment, you can choose the theory on which you want to focus in your analysis. By default, this is EU.
Depending on which theory you choose, an input table of different dimensions will be displayed for you to enter the target lottery and any needed context information. For EU, the input segment shows a table on the left, where the target lottery can be entered. This table can be extended or shortened by deleting a row or clicking the “Add Row” button, respectively. If you choose theories like OSAD or RT which expect more inputs than just the target lottery, additional columns will be added. Additional inputs for parameters like the Savoring coefficient of OSAD or the local thinking coefficient from ST will appear here as well. Note that if you enter the context information for ST, RT in the table on the left, the Tool automatically assumes correlated state spaces meaning that both outcomes do not only have the same probability but are intrinsically linked to the same state of the world. Alternatively, you may choose a sure amount in comparison to which your target lottery should be evaluated by clicking on the “Use single input” button and entering that certain value in the additional input table appearing appearing to the right of the initial input table.

The second section offers a summary of statistical information about the target lottery you entered and possible context information. The chart labeled "Lotteries" displays the entered information in a decision tree consistent with the figures in this these. The chart labeled "Probability Density Function" plots the lotteries with their payoffs on the x-axis and the associated probabilities on the y-axis. If more than the target lottery is plotted, the chart displays them as clustered bars. Finally, the chart labeled "Cumulative Density Function" displays similar information to the "Probability Density Function", but instead of displaying the individual probabilities on the y-axis, it takes the sum of the probabilites of all outcomes with lower payoffs. There is a table displaying some standard statistical moments of the entered lotteries beneath the three charts.

The third section is dynamic. depending on which theory you chose to focus on in the first section, it allows you to choose and adjust the utility function and other auxiliary functions such as the regret function or salience function for RT and ST. For each of these subsections, there is an dropdown field to the left similar to the one in the first section to choose the functional form to be used and input fields below the dropdown to adjust the function's parameters. On the bottom of each dropdown, you will find a special option titled "Enter custom function". This will open a text input in which custom functions can be defined according to rules further described in Section. For all of the input sections, there is a chart on the right displaying the function entered on the left. Again, they are consistent with the figures in this essay and should therefore not be hard to understand.

The last section displays the utility, certainty equivalent and risk premium calculated for the entered lotteries in a table. The first, bold row displays the outcomes given the theory you chose in the first section and the adjustments you made to its parametrization afterwards. Below that, the tool displays the outcomes calculated by using standard parametrizations of all the theories presented in this thesis as a comparison. To make the comparison easier, every row displays all the used auxiliary functions and parameters as well as the current target lottery and possible context-information.

##### Rules for the input of custom functions

* Only single-line inputs are accepted.
* Spaces are ignored.
* In the case of univariate functions (utility function and probability weighting function), the independent variable is always called "x". In the case of bivariate functions (Regret and Salience functions, etc.) the two independent variables are called "x\_1" and "x\_2". The entered formula must follow this convention.
* No other variables are allowed.
* Floating point values have to be entered using a point and not a comma as a separator (i.e., 34 can be entered as 0.75 but not 0,75)
* Only the right-handside of the equations is entered. $u(x)=3$*$x$ becomes $3$*$x$"
* Every operation must be explicitly declared (i.e., $3x$ must be written as $3$*$x$)
* Piecewise definitions of arbitrary complexity can be defined by using a shortened if statement (do something if condition else do something else). The Utility function proposed by Tversky and Kahneman in Equation with parameters of $\lambda=2.25$, $\alpha=0.88$ and a reference point of $r=0$ can be entered as "$(x-0)$**$0.88$ if $ x >= 0 $ else $ -2.25$*$(-(x-0))$**$0.88$". Nesting if statements is possible.
* Simpleeval (the parser) imposes some (generous) restrictions on the computational complexity of evaluated expression to keep the server from crashing. This includes restrictions on the size of power-operations (exponents may not exceed a certain size) and similar measures which are not likely to impact normal usage of the Tool.

In addition, the following signs are allowed:

||Allowed operators      |Allowed mathematical functions
|----|-------------------|---------|------------------------------------------------|
| +  | "plus"            | abs()   | "the absolute vale of"                         |
| -  | "minus"           | exp()   | "e to the power of"                            |
| /  | "divided by"      | log()   | "the natural logarithm of"                     |
| *  | "multiplied by"   | log10() | "the base 10 logarithm of"                     |
| ** | "to the power of" | u()     | "the univariate utility function"              |
| <  | "smaller than"    | sqrt()  | "the square root of"                           |
| >  | "greater than"    | pi      | "$\pi$ - Pi"                                   |
| <= | "smaller equal"   | e       | "e - Euler's Number"                           |
| >= | "greater equal"   | sin()   | "the sine of"                                  |
| == | "equal to"        | cos()   | "the cosine of"                                |


"""
)

