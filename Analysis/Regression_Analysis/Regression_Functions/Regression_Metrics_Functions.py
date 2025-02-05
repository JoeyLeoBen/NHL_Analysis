import math as ma

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
from sklearn import metrics
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import KFold, ShuffleSplit, cross_val_score


class Metrics:
    @staticmethod
    def regression_test_metrics(y: np.ndarray, y_pred: np.ndarray) -> None:
        """
        Calculates and prints regression test metrics: r-squared, MAE, MSE, and RMSE.

        Args:
            y (np.ndarray): Actual target values.
            y_pred (np.ndarray): Predicted target values.

        Returns:
            None
        """
        r2 = round(r2_score(y, y_pred), 2)
        mae = round(mean_absolute_error(y, y_pred), 2)
        mse = round(mean_squared_error(y, y_pred), 2)
        rmse = round(ma.sqrt(mse), 2)

        results = [
            ("r-squared:", r2),
            ("mean absolute error:", mae),
            ("mean squared error:", mse),
            ("root Mean squared error:", rmse),
        ]

        print("\nmodel metrics:\n")
        for label, value in results:
            print(f"{label:{35}} {value:.>{20}}")

        return None

    @staticmethod
    def regression_cross_val_shuffle(
        regressor: any, X_train: pd.DataFrame, y_train: pd.Series, cv: any, font: int
    ) -> None:
        """
        Performs k-fold cross-validation (with shuffling) for a regressor using various scoring metrics,
        plots the metrics for each fold, and prints the mean and standard deviation of the scores.

        Args:
            regressor (any): The regression model to evaluate.
            X_train (pd.DataFrame): Training feature data.
            y_train (pd.Series): Training target values.
            cv (any): Cross-validation splitting strategy (e.g., KFold or ShuffleSplit).
            font (int): Font scale for plots (suggested range: 1-3).

        Returns:
            None
        """
        # r2 scores
        accuracies_r2 = cross_val_score(
            estimator=regressor, X=X_train, y=y_train, cv=cv, n_jobs=-1, scoring="r2"
        )
        accuracies_r2_mean = round(accuracies_r2.mean(), 2)
        accuracies_r2_std = round(accuracies_r2.std(), 2)

        # MAE scores
        accuracies_mae = cross_val_score(
            estimator=regressor,
            X=X_train,
            y=y_train,
            cv=cv,
            n_jobs=-1,
            scoring="neg_mean_absolute_error",
        )
        score_mae = [score * -1 for score in accuracies_mae]
        score_mae_df = pd.DataFrame(score_mae, columns=["col"])
        accuracies_mae_mean = round(score_mae_df["col"].mean(), 2)
        accuracies_mae_std = round(score_mae_df["col"].std(), 2)

        # MSE scores
        accuracies_mse = cross_val_score(
            estimator=regressor,
            X=X_train,
            y=y_train,
            cv=cv,
            n_jobs=-1,
            scoring="neg_mean_squared_error",
        )
        score_mse = [score * -1 for score in accuracies_mse]
        score_mse_df = pd.DataFrame(score_mse, columns=["col"])
        accuracies_mse_mean = round(score_mse_df["col"].mean(), 2)
        accuracies_mse_std = round(score_mse_df["col"].std(), 2)

        # RMSE scores
        accuracies_rmse = cross_val_score(
            estimator=regressor,
            X=X_train,
            y=y_train,
            cv=10,
            n_jobs=-1,
            scoring="neg_root_mean_squared_error",
        )
        score_rmse = [score * -1 for score in accuracies_rmse]
        score_rmse_df = pd.DataFrame(score_rmse, columns=["col"])
        accuracies_rmse_mean = round(score_rmse_df["col"].mean(), 2)
        accuracies_rmse_std = round(score_rmse_df["col"].std(), 2)

        print("\ntest model f-fold metrics:\n")

        sns.set(font_scale=font, style="white")
        plt.figure(figsize=(10, 3))
        plt.plot(
            range(1, cv.get_n_splits(X_train) + 1, 1), accuracies_r2, ls="-", marker="o"
        )
        plt.title("r2 for kfold")
        plt.xlabel("kfold index")
        plt.ylabel("r2")
        plt.ylim(0, 1.1)
        plt.show()

        results1 = [
            ("r-squared k-fold cross validation: ", accuracies_r2_mean),
            ("r-squared std: ", accuracies_r2_std),
        ]
        for label, value in results1:
            print(f"{label:{50}} {value:.>{20}}")

        sns.set(font_scale=font, style="white")
        plt.figure(figsize=(10, 3))
        plt.plot(
            range(1, cv.get_n_splits(X_train) + 1, 1), score_mae, ls="-", marker="o"
        )
        plt.title("mae for kfold")
        plt.xlabel("kfold index")
        plt.ylabel("mae")
        plt.ylim(0, max(score_mae) * 1.25)
        plt.show()

        results2 = [
            ("mean absolute error k-fold cross validation: ", accuracies_mae_mean),
            ("mean absolute error std: ", accuracies_mae_std),
        ]
        print("\n")
        for label, value in results2:
            print(f"{label:{50}} {value:.>{20}}")

        sns.set(font_scale=font, style="white")
        plt.figure(figsize=(10, 3))
        plt.plot(
            range(1, cv.get_n_splits(X_train) + 1, 1), score_mse, ls="-", marker="o"
        )
        plt.title("mse for kfold")
        plt.xlabel("kfold index")
        plt.ylabel("mse")
        plt.ylim(0, max(score_mse) * 1.25)
        plt.show()

        results3 = [
            ("mean squared error k-fold cross validation: ", accuracies_mse_mean),
            ("mean squared error std: ", accuracies_mse_std),
        ]
        print("\n")
        for label, value in results3:
            print(f"{label:{50}} {value:.>{20}}")

        sns.set(font_scale=font, style="white")
        plt.figure(figsize=(10, 3))
        plt.plot(
            range(1, cv.get_n_splits(X_train) + 1, 1), score_rmse, ls="-", marker="o"
        )
        plt.title("rmse for kfold")
        plt.xlabel("kfold index")
        plt.ylabel("rmse")
        plt.ylim(0, max(score_rmse) * 1.25)
        plt.show()

        results4 = [
            ("root mean squared error k-fold cross validation: ", accuracies_rmse_mean),
            ("root mean squared error std: ", accuracies_rmse_std),
        ]
        print("\n")
        for label, value in results4:
            print(f"{label:{50}} {value:.>{20}}")
        print("\n")

        return None

    @staticmethod
    def regression_cross_val_splits(
        regressor: any, X_train: pd.DataFrame, y_train: pd.Series, cv: int, font: int
    ) -> None:
        """
        Performs k-fold cross-validation (using a specified number of splits) for a regressor using various scoring metrics,
        plots the metrics for each fold, and prints the mean and standard deviation of the scores.

        Args:
            regressor (any): The regression model to evaluate.
            X_train (pd.DataFrame): Training feature data.
            y_train (pd.Series): Training target values.
            cv (int): The number of folds for cross-validation.
            font (int): Font scale for plots (suggested range: 1-3).

        Returns:
            None
        """
        # r2 scores
        accuracies_r2 = cross_val_score(
            estimator=regressor, X=X_train, y=y_train, cv=cv, n_jobs=-1, scoring="r2"
        )
        accuracies_r2_mean = round(accuracies_r2.mean(), 2)
        accuracies_r2_std = round(accuracies_r2.std(), 2)

        # MAE scores
        accuracies_mae = cross_val_score(
            estimator=regressor,
            X=X_train,
            y=y_train,
            cv=cv,
            n_jobs=-1,
            scoring="neg_mean_absolute_error",
        )
        score_mae = [score * -1 for score in accuracies_mae]
        score_mae_df = pd.DataFrame(score_mae, columns=["col"])
        accuracies_mae_mean = round(score_mae_df["col"].mean(), 2)
        accuracies_mae_std = round(score_mae_df["col"].std(), 2)

        # MSE scores
        accuracies_mse = cross_val_score(
            estimator=regressor,
            X=X_train,
            y=y_train,
            cv=cv,
            n_jobs=-1,
            scoring="neg_mean_squared_error",
        )
        score_mse = [score * -1 for score in accuracies_mse]
        score_mse_df = pd.DataFrame(score_mse, columns=["col"])
        accuracies_mse_mean = round(score_mse_df["col"].mean(), 2)
        accuracies_mse_std = round(score_mse_df["col"].std(), 2)

        # RMSE scores
        accuracies_rmse = cross_val_score(
            estimator=regressor,
            X=X_train,
            y=y_train,
            cv=cv,
            n_jobs=-1,
            scoring="neg_root_mean_squared_error",
        )
        score_rmse = [score * -1 for score in accuracies_rmse]
        score_rmse_df = pd.DataFrame(score_rmse, columns=["col"])
        accuracies_rmse_mean = round(score_rmse_df["col"].mean(), 2)
        accuracies_rmse_std = round(score_rmse_df["col"].std(), 2)

        print("\ntest model f-fold metrics:\n")

        sns.set(font_scale=font, style="white")
        plt.figure(figsize=(10, 3))
        plt.plot(range(1, cv + 1, 1), accuracies_r2, ls="-", marker="o")
        plt.title("r2 for kfold")
        plt.xlabel("kfold index")
        plt.ylabel("r2")
        plt.ylim(0, 1.1)
        plt.show()

        results1 = [
            ("r-squared k-fold cross validation: ", accuracies_r2_mean),
            ("r-squared std: ", accuracies_r2_std),
        ]
        for label, value in results1:
            print(f"{label:{50}} {value:.>{20}}")

        sns.set(font_scale=font, style="white")
        plt.figure(figsize=(10, 3))
        plt.plot(range(1, cv + 1, 1), score_mae, ls="-", marker="o")
        plt.title("mae for kfold")
        plt.xlabel("kfold index")
        plt.ylabel("mae")
        plt.ylim(0, max(score_mae) * 1.25)
        plt.show()

        results2 = [
            ("mean absolute error k-fold cross validation: ", accuracies_mae_mean),
            ("mean absolute error std: ", accuracies_mae_std),
        ]
        print("\n")
        for label, value in results2:
            print(f"{label:{50}} {value:.>{20}}")

        sns.set(font_scale=font, style="white")
        plt.figure(figsize=(10, 3))
        plt.plot(range(1, cv + 1, 1), score_mse, ls="-", marker="o")
        plt.title("mse for kfold")
        plt.xlabel("kfold index")
        plt.ylabel("mse")
        plt.ylim(0, max(score_mse) * 1.25)
        plt.show()

        results3 = [
            ("mean squared error k-fold cross validation: ", accuracies_mse_mean),
            ("mean squared error std: ", accuracies_mse_std),
        ]
        print("\n")
        for label, value in results3:
            print(f"{label:{50}} {value:.>{20}}")

        sns.set(font_scale=font, style="white")
        plt.figure(figsize=(10, 3))
        plt.plot(range(1, cv + 1, 1), score_rmse, ls="-", marker="o")
        plt.title("rmse for kfold")
        plt.xlabel("kfold index")
        plt.ylabel("rmse")
        plt.ylim(0, max(score_rmse) * 1.25)
        plt.show()

        results4 = [
            ("root mean squared error k-fold cross validation: ", accuracies_rmse_mean),
            ("root mean squared error std: ", accuracies_rmse_std),
        ]
        print("\n")
        for label, value in results4:
            print(f"{label:{50}} {value:.>{20}}")
        print("\n")

        return None

    @staticmethod
    def regression_feature_importance(
        model: any,
        X_cols: pd.DataFrame,
        font: int,
        length: int,
        width: int,
        pos: str,
        neg: str,
    ) -> None:
        """
        Plots a horizontal bar chart of feature importances (model coefficients) and displays the coefficient values.

        Args:
            model (any): The regression model with a coef_ attribute.
            X_cols (pd.DataFrame): DataFrame of the predictor variables.
            font (int): Font scale for plots (suggested range: 1-3).
            length (int): Height of the plot (in inches).
            width (int): Width of the plot (in inches).
            pos (str): Color for positive coefficients.
            neg (str): Color for negative coefficients.

        Returns:
            None
        """
        coefficients = list(model.coef_)
        intercept = [model.intercept_]
        coefficients = coefficients + intercept
        X_col = list(X_cols.columns) + ["intercept"]
        coefficients_df = pd.DataFrame({"features": X_col, "coef": coefficients})
        coefficients_df["positive"] = coefficients_df["coef"] > 0
        coefficients_df["coef2"] = coefficients_df["coef"].abs()
        coefficients_df = coefficients_df.sort_values(
            by=["coef2"], ascending=True
        ).reset_index(drop=True)

        blue_patch = mpatches.Patch(color="#1f77b4", label="positive")
        red_patch = mpatches.Patch(color="r", label="negative")

        sns.set(font_scale=font, style="white")
        coefficients_df.plot(
            x="features",
            y="coef",
            kind="barh",
            figsize=(width, length),
            color=coefficients_df.positive.map({True: pos, False: neg}),
        )
        plt.title("feature importance (features scaled)")
        plt.xlabel("coefficient units")
        plt.ylabel("features")
        plt.legend(
            handles=[blue_patch, red_patch],
            bbox_to_anchor=(1.05, 1.0),
            loc="upper left",
        )
        plt.show()

        coefficients_df = coefficients_df.sort_values(by=["coef2"], ascending=False)
        coefficients_df = coefficients_df.drop(
            columns=["coef2", "index"], errors="ignore"
        )
        display(coefficients_df)

        return None

    @staticmethod
    def residual_means_counts_plot(
        df: pd.DataFrame,
        X: str,
        res: str,
        ymin1: float,
        ymax1: float,
        ymin2: float,
        ymax2: float,
        font: int,
        length: int,
        width: int,
    ) -> None:
        """
        Plots the average residuals and counts per binned intervals of a specified predictor variable.

        Args:
            df (pd.DataFrame): The input DataFrame containing the predictor and residual values.
            X (str): The column name of the predictor variable.
            res (str): The column name of the residual values.
            ymin1 (float): Adjustment to add to the minimum average residual (left axis).
            ymax1 (float): Adjustment to add to the maximum average residual (left axis).
            ymin2 (float): Adjustment to add to the minimum count (right axis).
            ymax2 (float): Adjustment to add to the maximum count (right axis).
            font (int): Font scale for plots (suggested range: 1-3).
            length (int): Height of the plot (in inches).
            width (int): Width of the plot (in inches).

        Returns:
            None
        """
        col_range = round(df[X].max() - df[X].min(), 0) + 1
        bins = pd.cut(df[X], int(col_range))
        mean_res = (
            df.groupby(bins)
            .agg({res: "mean"})
            .rename(columns={res: "mean"})
            .reset_index()
        )
        count_res = (
            df.groupby(bins)
            .agg({res: "count"})
            .rename(columns={res: "count"})
            .reset_index()
        )
        mean_count_res = pd.merge(mean_res, count_res, on=mean_res.columns[0])
        mean_count_res[mean_count_res.columns[0]] = mean_count_res[
            mean_count_res.columns[0]
        ].astype(str)

        sns.set(font_scale=font, style="white")
        plt.figure(figsize=(width, length))
        blue_patch = mpatches.Patch(color="#1f77b4", label="avg residuals per bin")
        darkgreen_patch = mpatches.Patch(
            color="darkgreen", label="count of residuals per bin"
        )
        red_patch = mpatches.Patch(color="r", label="avg residuals")
        plt.legend(
            handles=[blue_patch, darkgreen_patch, red_patch],
            bbox_to_anchor=(1.05, 1.0),
            loc="upper left",
        )

        ax1 = plt.gca()
        ax2 = ax1.twinx()

        ax1.plot(
            mean_count_res.iloc[:, 0],
            mean_count_res["mean"],
            ls="-",
            marker="o",
            color="#1f77b4",
        )
        ax1.set_xticklabels(mean_count_res.iloc[:, 0], rotation="vertical")
        ax1.axhline(y=0, color="r", linestyle="--")
        ax1.set(
            xlabel=f"{X} bins",
            ylabel="average residuals per bin",
            title=f"average residuals per binned {X}",
        )
        ax1.set_ylim(
            mean_count_res["mean"].min() + ymin1, mean_count_res["mean"].max() + ymax1
        )
        ax2.bar(mean_count_res.iloc[:, 0], mean_count_res["count"], color="darkgreen")
        ax2.set(ylabel="count per bin")
        ax2.set_ylim(
            mean_count_res["count"].min() + ymin2, mean_count_res["count"].max() + ymax2
        )
        plt.show()

        return None

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
        Computes the sum and count of a binary target variable for each category in selected categorical columns,
        calculates the percentage, and plots the results as a horizontal bar chart. Also displays the computed statistics.

        Args:
            df (pd.DataFrame): The input data frame.
            flag (str): The binary target variable.
            length (int): Height of the plot (in inches).
            width (int): Width of the plot (in inches).
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

        return None

    @staticmethod
    def calculate_vif(
        X: pd.DataFrame,
        target: str,
        threshold: float,
        feature_elim: int,
        print_markdown: str,
    ) -> tuple[list[str], list[float]]:
        """
        Iteratively calculates the Variance Inflation Factor (VIF) for features in the dataset by dropping one feature at a time
        until the VIF for all features is below a specified threshold or until a maximum number of features have been eliminated.
        Optionally prints the dropped features in markdown format.

        Args:
            X (pd.DataFrame): Data frame containing predictor variables.
            target (str): The target variable as a string (used in constructing the formula).
            threshold (float): Maximum acceptable VIF value.
            feature_elim (int): Maximum number of features to eliminate.
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
            vif["vif2"] = vif["vif"]
            vif.loc[vif.features == "Intercept", "vif2"] = 0
            max_feature = vif.loc[vif["vif2"].idxmax()]
            max_feature_name = max_feature["features"]
            max_feature_vif = max_feature["vif"]
            if max_feature_vif > threshold and max_feature_name != "Intercept":
                feature_list.append(max_feature_name)
                feature_vif_list.append(max_feature_vif)
            counter += 1

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
        normalizes rows to percentages, adds row totals and counts, and applies aesthetic formatting.

        Args:
            col_left (str): Column name for the left variable.
            col_top (str): Column name for the top variable.
            df (pd.DataFrame): The input data frame.

        Returns:
            pd.DataFrame: A formatted crosstab report.
        """
        crosstab = pd.crosstab(df[col_left], df[col_top])
        try:
            chi2, p, dof, ex = chi2_contingency(crosstab, correction=True)
            p = round(p, 2)
        except Exception:
            p = 'no data; "observed" has size 0'
        crosstab = crosstab.apply(lambda r: r / r.sum(), axis=1)
        crosstab["Total"] = crosstab.sum(axis=1, numeric_only=True)
        crosstab = crosstab.multiply(100).astype(int)
        crosstab_totals = pd.crosstab(df[col_left], df[col_top], margins=True)
        crosstab_totals = crosstab_totals[:-1][["All"]]
        crosstab_totals.columns = ["n Count"]
        crosstab = pd.concat([crosstab, crosstab_totals], axis=1)
        crosstab["Total"] = np.where(
            (crosstab["Total"] < 100) & (crosstab["Total"] > 98), 100, crosstab["Total"]
        )
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
            drop_cols (list[str]): List of columns to drop before generating crosstabs.

        Returns:
            pd.DataFrame: The concatenated crosstab report.
        """
        freq_book_df = df.drop(columns=drop_cols, errors="ignore")
        final_crosstab_list = []
        for col_top in freq_book_df.columns:
            crosstab_list = []
            for col_left in freq_book_df.columns:
                ct = Metrics.crosstabs(
                    col_left=col_left, col_top=col_top, df=freq_book_df
                )
                crosstab_list.append(ct)
            final_crosstab = pd.concat(crosstab_list, axis=0)
            final_crosstab_list.append(final_crosstab)
        final_df = pd.concat(final_crosstab_list, axis=1).reset_index(drop=True)

        return final_df
