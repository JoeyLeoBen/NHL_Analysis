import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from IPython.display import display
from patsy import dmatrices
from scipy.stats import chi2_contingency
from statsmodels.stats.outliers_influence import variance_inflation_factor

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)


class Preprocessing:
    @staticmethod
    def num_univariate_histogram(
        df: pd.DataFrame, length: int, width: int, rows: int, col: int, font: int
    ) -> None:
        """
        Plots histograms for all numeric variables in the DataFrame (excluding target variable if desired)
        and displays descriptive statistics.

        Args:
            df (pd.DataFrame): The input data frame containing numeric data.
            length (int): The height of the overall plot (in inches).
            width (int): The width of the overall plot (in inches).
            rows (int): The number of subplot rows.
            col (int): The number of subplot columns.
            font (int): Font scale factor (suggested range: 1-3).

        Returns:
            None
        """
        X_num = df.copy()
        sns.set(font_scale=font, style="white")
        X_num.hist(bins=50, figsize=(width, length), layout=(rows, col), grid=False)
        plt.show()
        print("\nX continuous descriptive stats:")
        describe = X_num.describe().T
        display(describe)

    @staticmethod
    def cat_univariate_freq(
        df: pd.DataFrame,
        length: int,
        width: int,
        col_start: int,
        col_end: int,
        font: int,
    ) -> None:
        """
        Generates horizontal bar plots for the frequency distribution (in percent) of categorical columns
        within the specified column index range, and displays the supporting statistics.

        Args:
            df (pd.DataFrame): The input data frame.
            length (int): The height of the plot (in inches).
            width (int): The width of the plot (in inches).
            col_start (int): Starting index of categorical columns to plot.
            col_end (int): Ending index (exclusive) of categorical columns to plot.
            font (int): Font scale factor (suggested range: 1-3).

        Returns:
            None
        """
        X_cat = df.select_dtypes(include=["object"]).columns[col_start:col_end]
        for X in X_cat:
            series = round(df[X].value_counts(normalize=True) * 100, 0)
            series = series.sort_values(ascending=True)
            sns.set(font_scale=font, style="white")
            series.plot.barh(figsize=(width, length))
            plt.title(f"{X} frequencies")
            plt.xlabel("percent")
            plt.ylabel(X)
            plt.show()

    @staticmethod
    def target_univariate_scatter(
        df: pd.DataFrame, x: str, y: str, length: int, width: int, font: int
    ) -> None:
        """
        Creates a scatter plot between two specified variables and displays the plot with custom labels.

        Args:
            df (pd.DataFrame): The input data frame.
            x (str): The column name for the x-axis.
            y (str): The column name for the y-axis.
            length (int): The height of the plot (in inches).
            width (int): The width of the plot (in inches).
            font (int): Font scale factor (suggested range: 1-3).

        Returns:
            None
        """
        df = df.reset_index()
        sns.set(font_scale=font, style="white")
        plt.figure(figsize=(width, length))
        sns.scatterplot(data=df, x=x, y=y)
        plt.title(f"season {y} by {x}")
        plt.xlabel(x)
        plt.ylabel(y)
        plt.show()

    @staticmethod
    def num_bivariate_scatter(
        df: pd.DataFrame,
        y: str,
        x: str,
        font: int,
        length: int,
        width: int,
        dot_size: int,
    ) -> None:
        """
        Creates a scatter plot for a pair of numeric variables using a pairplot, with custom dot size.

        Args:
            df (pd.DataFrame): The input data frame containing numeric variables.
            y (str): The name of the target variable to plot on the y-axis.
            x (str): The name of the variable to plot on the x-axis.
            font (int): Font scale factor (suggested range: 1-3).
            length (int): The height of the plot (in inches).
            width (int): The width of the plot (in inches).
            dot_size (int): The size of the scatter plot dots.

        Returns:
            None
        """
        sns.set(font_scale=font, style="white")
        plot = sns.pairplot(
            data=df, y_vars=y, x_vars=x, diag_kind=None, plot_kws={"s": dot_size}
        )
        plot.fig.set_size_inches(width, length)
        plt.show()

    @staticmethod
    def num_bivariate_corr_target(
        df: pd.DataFrame,
        target: str,
        threshold: float,
        font: int,
        length: int,
        width: int,
        print_markdown: str,
    ) -> list[str]:
        """
        Creates a correlation heat map for all variables against the target variable and displays features
        with correlation below a given threshold. Optionally prints the features in markdown format.

        Args:
            df (pd.DataFrame): The input data frame.
            target (str): The target variable name.
            threshold (float): The correlation threshold; features with absolute correlation below this value are returned.
            font (int): Font scale factor (suggested range: 1-3).
            length (int): The height of the plot (in inches).
            width (int): The width of the plot (in inches).
            print_markdown (str): 'yes' to print features in markdown format, 'no' otherwise.

        Returns:
            list[str]: A list of feature names (strings) with absolute correlation less than the threshold.
        """
        X_corr = df.corr(method="pearson")
        X_corr = X_corr[[target]].sort_values(by=[target], ascending=False)
        sns.set(font_scale=font, style="white")
        fig, ax = plt.subplots()
        fig.set_size_inches(width, length)
        sns.heatmap(X_corr, annot=True)
        plt.title("correlation matrix")
        plt.show()
        display(X_corr)

        X_corr = X_corr.reset_index()
        X_corr[target] = abs(X_corr[target])
        X_corr = X_corr.loc[X_corr[target] < threshold]
        feature_list = list(X_corr["index"])

        markdown = [f"* **`{mark}`**" for mark in feature_list]
        if print_markdown.lower() == "yes":
            for mark in markdown:
                print(mark)
        print("\nfeatures to remove:")
        return feature_list

    @staticmethod
    def cat_bivariate_avg_target(
        df: pd.DataFrame,
        col_start: int,
        col_end: int,
        target: str,
        length: int,
        width: int,
        font: int,
    ) -> None:
        """
        Plots bar charts showing the average of a numeric target variable for each category in selected categorical variables.
        Displays the resulting statistics as well.

        Args:
            df (pd.DataFrame): The input data frame.
            col_start (int): Starting index for selecting categorical columns.
            col_end (int): Ending index (exclusive) for selecting categorical columns.
            target (str): The numeric target variable whose average is computed.
            length (int): The height of the plot (in inches).
            width (int): The width of the plot (in inches).
            font (int): Font scale factor (suggested range: 1-3).

        Returns:
            None
        """
        X_cat = df.select_dtypes(include=["object"]).columns[col_start:col_end]
        for X in X_cat:
            label = df[[X, target]].sort_values(by=[target], ascending=False)
            label = round(label.groupby([X]).mean(), 0)
            label = label.sort_values(by=[target], ascending=True)
            label["positive"] = label[target] > 0
            sns.set(font_scale=font, style="white")
            label[target].plot(
                kind="barh",
                figsize=(width, length),
                color=label.positive.map({True: "b", False: "r"}),
            )
            plt.title(f"average {target} per {X}")
            plt.xlabel(f"average {target}")
            plt.ylabel(X)
            plt.show()
            label = label.sort_values(by=[target], ascending=False)
            display(label)

    @staticmethod
    def remove_outliers(df: pd.DataFrame, col: str) -> tuple[str, float, str, float]:
        """
        Calculates the lower and upper bounds for outliers in a numeric column using the 1.5*IQR rule,
        and returns these thresholds.

        Args:
            df (pd.DataFrame): The input data frame.
            col (str): The name of the column for which to calculate outlier thresholds.

        Returns:
            tuple[str, float, str, float]: A tuple containing labels and the calculated low and high outlier thresholds.
        """
        p_25 = df[col].quantile(0.25)
        p_75 = df[col].quantile(0.75)
        iqr = (p_75 - p_25) * 1.5
        low_outliers = p_25 - iqr
        high_outliers = p_75 + iqr
        return ("low end outliers:", low_outliers, "high end outliers", high_outliers)

    @staticmethod
    def class_cat_bivariate(
        df: pd.DataFrame,
        flag: str,
        length: int,
        width: int,
        col_start: int,
        col_end: int,
    ) -> None:
        """
        For each categorical variable (selected by column index range), computes the sum and count of a binary target,
        calculates the percentage rate, and plots the rate as a horizontal bar chart. Also displays the underlying statistics.

        Args:
            df (pd.DataFrame): The input data frame.
            flag (str): The binary target variable for classification.
            length (int): The height of the plot (in inches).
            width (int): The width of the plot (in inches).
            col_start (int): Starting index for selecting categorical columns.
            col_end (int): Ending index (exclusive) for selecting categorical columns.

        Returns:
            None
        """
        X_cat = df.select_dtypes(include=["object"]).columns[col_start:col_end]
        for X in X_cat:
            label1 = round(df[[X, flag]].groupby([X]).sum(), 0)
            label2 = round(df[[X, flag]].groupby([X]).count(), 0)
            label3 = pd.concat([label1, label2], axis=1)
            label3.columns = ["sum", "count"]
            label3["rate"] = round((label3["sum"] / label3["count"]) * 100, 0)
            label3 = label3.sort_values(by=["rate"], ascending=True)
            label3["rate"].plot.barh(figsize=(width, length))
            plt.title(f"percentage {flag} per {X}")
            plt.xlabel(f"rate of {flag}")
            plt.ylabel(X)
            plt.show()
            label3 = label3.sort_values(by=["rate"], ascending=False)
            display(label3)

    @staticmethod
    def calculate_vif(
        X: pd.DataFrame,
        target: str,
        threshold: float,
        feature_elim: int,
        print_markdown: str,
    ) -> tuple[list[str], list[float]]:
        """
        Iteratively calculates Variance Inflation Factor (VIF) for features in the data frame by dropping one feature at a time
        until the VIF for all features is below the threshold or until a specified number of features have been eliminated.
        Optionally prints the dropped features in markdown format.

        Args:
            X (pd.DataFrame): Data frame containing predictor variables.
            target (str): The target variable as a string (used in constructing the formula).
            threshold (float): The maximum acceptable VIF value.
            feature_elim (int): The maximum number of features to eliminate.
            print_markdown (str): 'yes' to print markdown of dropped features, 'no' otherwise.

        Returns:
            tuple[list[str], list[float]]: A tuple where the first element is a list of eliminated feature names and the
                                            second element is a list of their corresponding VIF scores.
        """
        feature_list: list[str] = []
        feature_vif_list: list[float] = []
        max_elim = feature_elim
        counter = 0

        while counter <= max_elim:
            # Drop previously eliminated features
            X_curr = X.drop(columns=feature_list, errors="ignore")
            features = "+".join(X_curr.columns[:-1])
            y, X1 = dmatrices(f"{target} ~ {features}", X_curr, return_type="dataframe")
            vif = pd.DataFrame(
                {
                    "vif": [
                        variance_inflation_factor(X1.values, i)
                        for i in range(X1.shape[1])
                    ],
                    "features": X1.columns,
                }
            )
            vif = vif.sort_values(by=["vif"], ascending=False).reset_index(drop=True)
            # Replace intercept VIF with 0 for elimination purposes
            vif["vif2"] = vif["vif"]
            vif.loc[vif.features == "Intercept", "vif2"] = 0
            max_feature = vif.loc[vif["vif2"].idxmax()]
            max_feature_name = max_feature["features"]
            max_feature_vif = max_feature["vif"]
            if max_feature_vif > threshold and max_feature_name != "Intercept":
                feature_list.append(max_feature_name)
                feature_vif_list.append(max_feature_vif)
            counter += 1

        # Drop helper column if exists
        vif = vif.drop(columns=["vif2"], errors="ignore")
        display(vif)
        print("\ndropped features:")
        markdown = [f"* **`{feat}`**" for feat in feature_list]
        if print_markdown.lower() == "yes":
            for mark in markdown:
                print(mark)
        return (feature_list, feature_vif_list)

    @staticmethod
    def crosstabs(col_left: str, col_top: str, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generates a crosstab report between two categorical variables, calculates the chi-square test p-value,
        converts frequencies to percentages, adds row totals and n counts, and applies aesthetic formatting.

        Args:
            col_left (str): The column name to be used as the left variable.
            col_top (str): The column name to be used as the top variable.
            df (pd.DataFrame): The input data frame.

        Returns:
            pd.DataFrame: A formatted crosstab report as a DataFrame.
        """
        # Create cross tab
        crosstab = pd.crosstab(df[col_left], df[col_top])
        # Get p-value
        try:
            chi2, p, dof, ex = chi2_contingency(crosstab, correction=True)
            p = round(p, 2)
        except Exception:
            p = 'no data; "observed" has size 0'
        # Normalize rows to percentages and add total
        crosstab = crosstab.apply(lambda r: r / r.sum(), axis=1)
        crosstab["Total"] = crosstab.sum(axis=1, numeric_only=True)
        crosstab = crosstab.multiply(100).astype(int)
        # Get n counts
        crosstab_totals = pd.crosstab(df[col_left], df[col_top], margins=True)
        crosstab_totals = crosstab_totals[:-1][["All"]]
        crosstab_totals.columns = ["n Count"]
        crosstab = pd.concat([crosstab, crosstab_totals], axis=1)
        # Adjust total to 100 if nearly complete
        crosstab["Total"] = np.where(
            (crosstab["Total"] < 100) & (crosstab["Total"] > 98), 100, crosstab["Total"]
        )
        # Aesthetic adjustments
        crosstab["Feature"] = col_left
        crosstab = crosstab.reset_index()
        first_column = crosstab.pop("Feature")
        crosstab.insert(0, "Feature", first_column)
        crosstab.columns.values[1] = "Feature_Value"
        crosstab["Feature"] = crosstab["Feature"] + " - p-value: " + str(p)
        crosstab = crosstab.astype(str)
        crosstab.columns.name = None
        crosstab = crosstab.append(pd.Series(), ignore_index=True)
        crosstab = crosstab.fillna("")
        # Create MultiIndex for column headers
        col_names = list(crosstab.columns[2:])
        col_names_list = [("", "Feature"), ("", "Feature_Value")]
        for i, col in enumerate(col_names):
            if i == 0:
                col_names_list.append((col_top, col))
            else:
                col_names_list.append(("", col))
        crosstab.columns = pd.MultiIndex.from_tuples(col_names_list)
        crosstab["."] = ""
        return crosstab

    @staticmethod
    def crosstab_report(df: pd.DataFrame, drop_cols: list[str]) -> pd.DataFrame:
        """
        Generates a complete crosstab report for all combinations of categorical variables in the DataFrame,
        excluding specified columns.

        Args:
            df (pd.DataFrame): The input data frame.
            drop_cols (list[str]): A list of column names to drop before generating crosstabs.

        Returns:
            pd.DataFrame: A concatenated crosstab report.
        """
        freq_book_df = df.drop(columns=drop_cols, errors="ignore")
        final_crosstab_list = []
        for col_top in freq_book_df.columns:
            crosstab_list = []
            for col_left in freq_book_df.columns:
                ct = Preprocessing.crosstabs(
                    col_left=col_left, col_top=col_top, df=freq_book_df
                )
                crosstab_list.append(ct)
            final_crosstab = pd.concat(crosstab_list, axis=0)
            final_crosstab_list.append(final_crosstab)
        final_df = pd.concat(final_crosstab_list, axis=1).reset_index(drop=True)
        return final_df
